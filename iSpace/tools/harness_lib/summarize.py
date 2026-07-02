from __future__ import annotations

from pathlib import Path

from .audit import audit_run
from .atomic import atomic_write_text
from .jsonio import read_json
from .paths import HarnessPaths


def summarize_run(paths: HarnessPaths, run_id: str) -> Path:
    run = read_json(paths.root / "track" / "runs" / run_id / "run.json")
    findings = audit_run(paths, run_id)
    task_lines = []
    for task_id in run.get("task_ids", []):
        task_path = paths.root / "track" / "task" / task_id / "task.json"
        if task_path.exists():
            task = read_json(task_path)
            task_lines.append(f"- `{task_id}`: {task.get('title', '')} ({task.get('state', '')})")
        else:
            task_lines.append(f"- `{task_id}`: 缺少 task 文件")
    audit_lines = [f"- {item}" for item in findings] if findings else ["- 未发现阻塞级审计问题。"]

    lines = [
        f"# Run {run_id} 摘要",
        "",
        f"- 标题：{run.get('title', '')}",
        f"- profile：{run.get('profile', '')}",
        f"- 状态：{run.get('state', '')}",
        f"- 任务数：{len(run.get('task_ids', []))}",
        "",
        "## 任务",
        "",
        *(task_lines or ["- 暂无任务。"]),
        "",
        "## 审计",
        "",
        *audit_lines,
        "",
    ]
    report_path = paths.resolve_core_write_path(Path("reports") / f"run-{run_id}-summary.md")
    atomic_write_text(report_path, "\n".join(lines))
    return report_path
