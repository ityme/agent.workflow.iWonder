from worker_common import base_result, load_input, write_result


def main() -> int:
    payload, output = load_input()
    write_result(output, base_result(payload, "analyst", "示例分析结果已生成。"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
