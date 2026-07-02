from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_input() -> tuple[dict[str, Any], Path]:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    with Path(args.input).open("r", encoding="utf-8") as handle:
        return json.load(handle), Path(args.output)


def write_result(output: Path, payload: dict[str, Any]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def base_result(payload: dict[str, Any], role: str, summary: str) -> dict[str, Any]:
    workspace = Path(payload["workspace"])
    evidence = workspace / f"{role}-summary.json"
    workspace.mkdir(parents=True, exist_ok=True)
    evidence.write_text(
        json.dumps({"role": role, "summary": summary}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    evidence_ref = evidence
    harness_root = payload.get("harness_root")
    if harness_root:
        try:
            evidence_ref = evidence.resolve().relative_to(Path(harness_root).resolve())
        except ValueError:
            evidence_ref = evidence
    return {
        "run_id": payload["run_id"],
        "task_id": payload["task_id"],
        "attempt_id": payload["attempt_id"],
        "role": role,
        "result": "success",
        "summary": summary,
        "failure_reason": "",
        "blockers": [],
        "evidence_refs": [evidence_ref.as_posix()],
        "next_step": "交回调度器处理下一步。",
        "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }
