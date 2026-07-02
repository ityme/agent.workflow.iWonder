from worker_common import base_result, load_input, write_result


def main() -> int:
    payload, output = load_input()
    write_result(output, base_result(payload, "verifier", "示例分析校验已通过。"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
