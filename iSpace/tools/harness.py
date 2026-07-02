#!/usr/bin/env python
"""AI Agent Harness command line entry point."""

from __future__ import annotations

import argparse
from pathlib import Path

from harness_lib.paths import HarnessPaths, find_harness_root
from harness_lib.profile import load_profile
from harness_lib.track import TrackStore
from harness_lib.adapter import load_adapter
from harness_lib.dispatcher import run_task


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI Agent Harness tools")
    parser.add_argument(
        "--root",
        help="显式指定 harness 根目录；默认从当前目录向上查找。",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="harness 0.1.0",
    )

    subparsers = parser.add_subparsers(dest="command")

    new_run = subparsers.add_parser("new-run", help="创建或复用一个 run。")
    new_run.add_argument("--title", required=True)
    new_run.add_argument("--profile", required=True)
    new_run.set_defaults(handler=handle_new_run)

    new_task = subparsers.add_parser("new-task", help="在 run 下创建或复用一个 task。")
    new_task.add_argument("--run", required=True)
    new_task.add_argument("--name", required=True)
    new_task.add_argument(
        "--acceptance",
        action="append",
        default=[],
        help="验收标准，可重复传入。",
    )
    new_task.add_argument(
        "--non-goal",
        action="append",
        default=[],
        help="非目标，可重复传入。",
    )
    new_task.set_defaults(handler=handle_new_task)

    validate = subparsers.add_parser("validate", help="校验 run、关联 task 或 profile。")
    validate.add_argument("--run")
    validate.add_argument("--profile")
    validate.set_defaults(handler=handle_validate)

    run_task_parser = subparsers.add_parser("run-task", help="按 adapter 执行单个 task。")
    run_task_parser.add_argument("--run", required=True)
    run_task_parser.add_argument("--task", required=True)
    run_task_parser.add_argument("--profile", default="default-development")
    run_task_parser.set_defaults(handler=handle_run_task)

    demo = subparsers.add_parser("demo", help="运行 default-development 本地 demo。")
    demo.set_defaults(handler=handle_demo)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "handler"):
        parser.print_help()
        return 0
    return args.handler(args)


def make_store(root: str | None) -> TrackStore:
    harness_root = Path(root).resolve() if root else find_harness_root(Path(__file__))
    return TrackStore(HarnessPaths(harness_root))


def handle_new_run(args: argparse.Namespace) -> int:
    run = make_store(args.root).create_run(args.title, args.profile)
    print(f"created run {run['run_id']}")
    return 0


def handle_new_task(args: argparse.Namespace) -> int:
    task = make_store(args.root).create_task(
        args.run,
        args.name,
        acceptance_criteria=args.acceptance,
        non_goals=args.non_goal,
    )
    print(f"created task {task['task_id']}")
    return 0


def handle_validate(args: argparse.Namespace) -> int:
    if args.profile:
        root = Path(args.root).resolve() if args.root else find_harness_root(Path(__file__))
        profile_root = root if (root / "profiles").exists() else builtin_harness_root()
        profile_path = profile_root / "profiles" / args.profile / "profile.json"
        load_profile(profile_path)
        print(f"valid profile {args.profile}")
        return 0
    if not args.run:
        print("invalid: validate requires --run or --profile")
        return 2
    errors = make_store(args.root).validate_run(args.run)
    if errors:
        for error in errors:
            print(f"invalid: {error}")
        return 1
    print(f"valid run {args.run}")
    return 0


def handle_run_task(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else find_harness_root(Path(__file__))
    store = TrackStore(HarnessPaths(root))
    adapter = load_adapter(adapter_root(root) / "local-python-workers" / f"{args.profile}.json")
    results = run_task(
        harness_root=root,
        store=store,
        adapter=adapter,
        run_id=args.run,
        task_id=args.task,
    )
    failed = [item for item in results if item["exit_code"] != 0 or item["result"].get("result") != "success"]
    print(f"ran task {args.task}: {len(results)} role(s)")
    return 1 if failed else 0


def handle_demo(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else find_harness_root(Path(__file__))
    store = TrackStore(HarnessPaths(root))
    run = store.create_run("demo", "default-development")
    task = store.create_task(
        run["run_id"],
        "demo task",
        acceptance_criteria=["demo 链路以 0 退出。"],
        non_goals=["不执行真实提交、发布或远端写入。"],
    )
    adapter = load_adapter(adapter_root(root) / "local-python-workers" / "default-development.json")
    results = run_task(
        harness_root=root,
        store=store,
        adapter=adapter,
        run_id=run["run_id"],
        task_id=task["task_id"],
    )
    failed = [item for item in results if item["exit_code"] != 0 or item["result"].get("result") != "success"]
    print(f"demo run {run['run_id']} task {task['task_id']} roles {len(results)}")
    return 1 if failed else 0


def builtin_harness_root() -> Path:
    return Path(__file__).resolve().parents[1]


def adapter_root(root: Path) -> Path:
    if (root / "adapters").exists():
        return root / "adapters"
    return builtin_harness_root() / "adapters"


if __name__ == "__main__":
    raise SystemExit(main())
