from worker_common import base_result, load_input, write_result


def main() -> int:
    payload, output = load_input()
    write_result(output, base_result(payload, "planner", "运维变更计划已生成。"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
