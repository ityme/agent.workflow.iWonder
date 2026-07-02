from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .jsonio import append_jsonl, read_json, write_json
from .paths import HarnessPaths
from .schema import validate_file


class TrackError(ValueError):
    """Raised when track data cannot be created or validated."""


class TrackStore:
    def __init__(self, paths: HarnessPaths) -> None:
        self.paths = paths
        self.track_dir = self.paths.resolve_core_write_path("track")
        self.schemas_dir = self._resolve_schemas_dir()

    def create_run(self, title: str, profile: str) -> dict[str, Any]:
        existing = self._find_run_by_title_and_profile(title, profile)
        if existing is not None:
            return existing

        run_id = self._next_run_id()
        now = utc_now()
        run = {
            "run_id": run_id,
            "title": title,
            "profile": profile,
            "state": "intake",
            "created_at": now,
            "updated_at": now,
            "summary": "",
            "task_ids": [],
        }
        write_json(self.run_path(run_id), run)
        self._append_timeline(
            {
                "event_type": "run_created",
                "run_id": run_id,
                "title": title,
                "profile": profile,
                "timestamp": now,
            }
        )
        return run

    def create_task(
        self,
        run_id: str,
        name: str,
        acceptance_criteria: list[str] | None = None,
        non_goals: list[str] | None = None,
    ) -> dict[str, Any]:
        run = self._read_run(run_id)
        existing = self._find_task_by_title(name)
        if existing is not None and existing["run_id"] == run_id:
            return existing

        task_id = self._next_task_id(name)
        now = utc_now()
        task = {
            "run_id": run_id,
            "task_id": task_id,
            "title": name,
            "profile": run["profile"],
            "state": "planned",
            "created_at": now,
            "updated_at": now,
            "depends_on": [],
            "acceptance_criteria": acceptance_criteria or ["任务结果可验证。"],
            "non_goals": non_goals or [],
        }
        write_json(self.task_path(task_id), task)
        if task_id not in run["task_ids"]:
            run["task_ids"].append(task_id)
            run["updated_at"] = now
            write_json(self.run_path(run_id), run)
        self._append_timeline(
            {
                "event_type": "task_created",
                "run_id": run_id,
                "task_id": task_id,
                "title": name,
                "timestamp": now,
            }
        )
        return task

    def validate_run(self, run_id: str) -> list[str]:
        errors: list[str] = []
        run_path = self.run_path(run_id)
        errors.extend(validate_file(run_path, self.schemas_dir / "run.schema.json"))
        if errors:
            return errors

        run = read_json(run_path)
        for task_id in run.get("task_ids", []):
            task_errors = validate_file(self.task_path(task_id), self.schemas_dir / "task.schema.json")
            errors.extend(f"{task_id}: {error}" for error in task_errors)
        return errors

    def run_path(self, run_id: str) -> Path:
        return self.paths.resolve_core_write_path(Path("track") / "runs" / run_id / "run.json")

    def task_path(self, task_id: str) -> Path:
        return self.paths.resolve_core_write_path(Path("track") / "task" / task_id / "task.json")

    def _read_run(self, run_id: str) -> dict[str, Any]:
        path = self.run_path(run_id)
        if not path.exists():
            raise TrackError(f"run not found: {run_id}")
        run = read_json(path)
        if not isinstance(run, dict):
            raise TrackError(f"run file is not an object: {run_id}")
        return run

    def _find_run_by_title_and_profile(self, title: str, profile: str) -> dict[str, Any] | None:
        runs_dir = self.track_dir / "runs"
        if not runs_dir.exists():
            return None
        for run_file in sorted(runs_dir.glob("*/run.json")):
            run = read_json(run_file)
            if run.get("title") == title and run.get("profile") == profile:
                return run
        return None

    def _find_task_by_title(self, title: str) -> dict[str, Any] | None:
        tasks_dir = self.track_dir / "task"
        if not tasks_dir.exists():
            return None
        for task_file in sorted(tasks_dir.glob("*/task.json")):
            task = read_json(task_file)
            if task.get("title") == title:
                return task
        return None

    def _next_run_id(self) -> str:
        runs_dir = self.track_dir / "runs"
        existing = [int(path.name) for path in runs_dir.glob("[0-9][0-9][0-9][0-9]") if path.is_dir()]
        return f"{(max(existing) if existing else 0) + 1:04d}"

    def _next_task_id(self, name: str) -> str:
        tasks_dir = self.track_dir / "task"
        existing = []
        if tasks_dir.exists():
            for path in tasks_dir.iterdir():
                if path.is_dir() and re.match(r"^[0-9]{3}_", path.name):
                    existing.append(int(path.name[:3]))
        return f"{(max(existing) if existing else 0) + 1:03d}_{slugify(name)}"

    def _append_timeline(self, event: dict[str, Any]) -> None:
        append_jsonl(self.paths.resolve_core_write_path("track/timeline.jsonl"), event)

    def _resolve_schemas_dir(self) -> Path:
        root_schemas = self.paths.root / "schemas"
        if root_schemas.exists():
            return root_schemas
        return Path(__file__).resolve().parents[2] / "schemas"


def slugify(value: str) -> str:
    lowered = value.lower()
    chars = [char if char.isascii() and (char.isalnum() or char in "-_") else "-" for char in lowered]
    slug = re.sub(r"-+", "-", "".join(chars)).strip("-_")
    return slug or "task"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
