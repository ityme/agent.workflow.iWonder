from __future__ import annotations

import subprocess
import sys
import os
from pathlib import Path
from typing import Any

from .adapter import assert_command_allowed
from .jsonio import read_json, write_json
from .paths import HarnessPaths
from .retry import next_attempt_id
from .track import TrackStore, utc_now


class DispatchError(RuntimeError):
    """Raised when a worker cannot be dispatched."""


def dispatch_role(
    *,
    harness_root: str | Path,
    store: TrackStore,
    adapter: dict[str, Any],
    run_id: str,
    task_id: str,
    role: str,
) -> dict[str, Any]:
    root = Path(harness_root).resolve()
    command_root = _command_root(root)
    role_config = adapter["roles"].get(role)
    if role_config is None:
        raise DispatchError(f"role not configured in adapter: {role}")

    command = list(role_config["command"])
    assert_command_allowed(adapter, command)

    attempt_dir = _next_attempt_dir(store.paths, run_id, task_id, role)
    attempt_id = attempt_dir.name
    input_file = _render_path(role_config["input_file"], root, attempt_dir, run_id, task_id)
    output_file = _render_path(role_config["output_file"], root, attempt_dir, run_id, task_id)
    workspace = _render_path(role_config["workspace"], root, attempt_dir, run_id, task_id)
    workspace.mkdir(parents=True, exist_ok=True)

    input_payload = {
        "run_id": run_id,
        "task_id": task_id,
        "attempt_id": attempt_id,
        "role": role,
        "harness_root": str(root),
        "workspace": str(workspace),
        "timestamp": utc_now(),
    }
    write_json(input_file, input_payload)

    resolved_command = _resolve_command(command, command_root)
    env = os.environ.copy()
    worker_path = str(command_root / "iSpace" / "workers")
    env["PYTHONPATH"] = (
        worker_path if not env.get("PYTHONPATH") else f"{worker_path}{os.pathsep}{env['PYTHONPATH']}"
    )
    completed = subprocess.run(
        [*resolved_command, "--input", str(input_file), "--output", str(output_file)],
        cwd=command_root,
        check=False,
        capture_output=True,
        text=True,
        timeout=role_config.get("timeout_seconds", adapter.get("default_timeout_seconds", 60)),
        env=env,
    )

    if output_file.exists():
        result = read_json(output_file)
    else:
        result = {
            "run_id": run_id,
            "task_id": task_id,
            "attempt_id": attempt_id,
            "role": role,
            "result": "fail",
            "summary": "worker did not write result file",
            "failure_reason": completed.stderr.strip(),
            "blockers": [],
            "evidence_refs": [],
            "next_step": "检查 worker 输出。",
            "timestamp": utc_now(),
        }
        write_json(output_file, result)

    if completed.returncode != 0 and result.get("result") == "success":
        result["result"] = "fail"
        result["failure_reason"] = completed.stderr.strip() or f"exit code {completed.returncode}"
        write_json(output_file, result)

    result = _normalize_result_refs(result, root)

    append_result_path = store.paths.resolve_core_write_path(
        Path("track")
        / "task"
        / task_id
        / "tm"
        / run_id
        / role
        / attempt_id
        / "result.json"
    )
    write_json(append_result_path, result)
    if role == "opser":
        closeout = _closeout_from_result(result)
        write_json(append_result_path.parent / "closeout.json", closeout)

    return {
        "role": role,
        "attempt_id": attempt_id,
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "result": result,
        "result_path": str(append_result_path),
    }


def run_task(
    *,
    harness_root: str | Path,
    store: TrackStore,
    adapter: dict[str, Any],
    run_id: str,
    task_id: str,
    roles: list[str] | None = None,
) -> list[dict[str, Any]]:
    selected_roles = roles or [role for role in ("coder", "tester", "opser") if role in adapter["roles"]]
    results = []
    for role in selected_roles:
        result = dispatch_role(
            harness_root=harness_root,
            store=store,
            adapter=adapter,
            run_id=run_id,
            task_id=task_id,
            role=role,
        )
        results.append(result)
        if result["exit_code"] != 0 or result["result"].get("result") != "success":
            break
    return results


def _next_attempt_dir(paths: HarnessPaths, run_id: str, task_id: str, role: str) -> Path:
    role_dir = paths.resolve_core_write_path(Path("tmp") / "attempts" / run_id / task_id / role)
    role_dir.mkdir(parents=True, exist_ok=True)
    existing = [path for path in role_dir.glob("attempt-[0-9][0-9][0-9][0-9]") if path.is_dir()]
    attempt_id = next_attempt_id(len(existing))
    attempt_dir = role_dir / attempt_id
    attempt_dir.mkdir()
    return attempt_dir


def _render_path(template: str, root: Path, attempt_dir: Path, run_id: str, task_id: str) -> Path:
    rendered = template.format(
        harness_root=str(root),
        attempt_dir=str(attempt_dir),
        run_id=run_id,
        task_id=task_id,
    )
    return Path(rendered).resolve()


def _resolve_command(command: list[str], command_root: Path) -> list[str]:
    if not command:
        raise DispatchError("empty command")
    executable = sys.executable if command[0] == "python" else command[0]
    return [
        executable,
        *[
            str((command_root / part).resolve()) if part.startswith("iSpace/") else part
            for part in command[1:]
        ],
    ]


def _command_root(harness_root: Path) -> Path:
    repo_root = harness_root.parent if harness_root.name == "iSpace" else harness_root
    if (repo_root / "iSpace" / "workers").exists():
        return repo_root
    return Path(__file__).resolve().parents[3]


def _closeout_from_result(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": result["run_id"],
        "task_id": result["task_id"],
        "attempt_id": result["attempt_id"],
        "role": result["role"],
        "closeout_action": result.get("closeout_action", "no_op"),
        "closeout_result": result.get("closeout_result", "no_op"),
        "summary": result["summary"],
        "staged_files": result.get("staged_files", []),
        "commit_message": result.get("commit_message", ""),
        "commit_sha": result.get("commit_sha", ""),
        "noop_reason": result.get("noop_reason", ""),
        "closeout_failure_reason": result.get("closeout_failure_reason", ""),
        "timestamp": result["timestamp"],
    }


def _normalize_result_refs(result: dict[str, Any], root: Path) -> dict[str, Any]:
    normalized = dict(result)
    refs = []
    for ref in normalized.get("evidence_refs", []):
        path = Path(ref)
        if path.is_absolute():
            try:
                refs.append(path.resolve().relative_to(root).as_posix())
                continue
            except ValueError:
                pass
        refs.append(str(ref).replace("\\", "/"))
    normalized["evidence_refs"] = refs
    return normalized
