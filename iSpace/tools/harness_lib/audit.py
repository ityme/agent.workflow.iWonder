from __future__ import annotations

import json
import re
from pathlib import Path

from .jsonio import read_json, read_jsonl
from .paths import HarnessPaths
from .redact import contains_secret


ABSOLUTE_PATH_PATTERN = re.compile(
    r"[A-Za-z]:\\" + r"|" + "/" + "Users" + "/" + r"|" + "/" + "home" + "/"
)


def audit_run(paths: HarnessPaths, run_id: str) -> list[str]:
    findings: list[str] = []
    track_root = paths.root / "track"
    run_path = track_root / "runs" / run_id / "run.json"
    if not run_path.exists():
        return [f"missing run file: {run_id}"]

    _scan_track_files(paths, findings)
    _check_event_links(paths, findings)
    _check_run_tasks(paths, run_id, findings)
    return findings


def _scan_track_files(paths: HarnessPaths, findings: list[str]) -> None:
    for path in sorted((paths.root / "track").rglob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = _rel(paths, path)
        if contains_secret(text):
            findings.append(f"sensitive content in {rel}")
        if ABSOLUTE_PATH_PATTERN.search(text):
            findings.append(f"absolute path in {rel}")
        if path.suffix == ".json":
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                findings.append(f"invalid json in {rel}: {exc}")


def _check_run_tasks(paths: HarnessPaths, run_id: str, findings: list[str]) -> None:
    run = read_json(paths.root / "track" / "runs" / run_id / "run.json")
    for task_id in run.get("task_ids", []):
        task_dir = paths.root / "track" / "task" / task_id
        if not (task_dir / "task.json").exists():
            findings.append(f"missing task file: {task_id}")
            continue
        result_files = sorted(task_dir.glob(f"tm/{run_id}/*/attempt-*/result.json"))
        if not result_files:
            findings.append(f"missing result files: {task_id}")
        for result_file in result_files:
            result = read_json(result_file)
            _check_evidence_refs(paths, result_file, result, findings)
            if result.get("role") == "opser":
                closeout = result_file.parent / "closeout.json"
                if not closeout.exists():
                    findings.append(f"missing closeout file: {_rel(paths, closeout)}")


def _check_event_links(paths: HarnessPaths, findings: list[str]) -> None:
    event_ids: dict[str, Path] = {}
    duplicate_ids: set[str] = set()
    reply_refs: list[tuple[str, Path]] = []
    for path in sorted((paths.root / "track").rglob("*.jsonl")):
        try:
            records = list(read_jsonl(path))
        except json.JSONDecodeError as exc:
            findings.append(f"invalid jsonl in {_rel(paths, path)}: {exc}")
            continue
        for record in records:
            if not isinstance(record, dict):
                continue
            event_id = record.get("event_id")
            if event_id:
                if event_id in event_ids:
                    duplicate_ids.add(event_id)
                else:
                    event_ids[event_id] = path
            reply_to = record.get("reply_to")
            if reply_to:
                reply_refs.append((reply_to, path))

    for event_id in sorted(duplicate_ids):
        findings.append(f"duplicate event_id: {event_id}")
    for reply_to, path in reply_refs:
        if reply_to not in event_ids:
            findings.append(f"invalid reply_to {reply_to} in {_rel(paths, path)}")


def _check_evidence_refs(
    paths: HarnessPaths,
    result_file: Path,
    result: dict[str, object],
    findings: list[str],
) -> None:
    refs = result.get("evidence_refs", [])
    if not isinstance(refs, list):
        return
    for ref in refs:
        if not isinstance(ref, str):
            continue
        ref_path = Path(ref)
        resolved = ref_path.resolve() if ref_path.is_absolute() else (paths.root / ref_path).resolve()
        try:
            resolved.relative_to(paths.root)
        except ValueError:
            findings.append(
                f"evidence path escapes harness root in {_rel(paths, result_file)}: {ref}"
            )


def _rel(paths: HarnessPaths, path: Path) -> str:
    try:
        return path.resolve().relative_to(paths.root).as_posix()
    except ValueError:
        return str(path)
