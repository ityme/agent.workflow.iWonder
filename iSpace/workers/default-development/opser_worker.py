from worker_common import base_result, load_input, write_result


def main() -> int:
    payload, output = load_input()
    result = base_result(payload, "opser", "示例收口已完成。")
    result.update(
        {
            "closeout_action": "no_op",
            "closeout_result": "no_op",
            "noop_reason": "demo worker 不执行真实提交或发布。",
            "staged_files": [],
            "commit_message": "",
            "commit_sha": "",
        }
    )
    write_result(output, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
