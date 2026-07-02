# 失败并重试运行

本示例说明失败和重试的记录方式。第一版工具已经支持递增 `attempt_id`，后续调度策略会把失败后的重试规则和人工介入规则进一步自动化。

建议命令：

```powershell
python iSpace/tools/harness.py run-task --run 0001 --task 001_demo-task --profile default-development
python iSpace/tools/harness.py validate --run 0001
python iSpace/tools/harness.py audit --run 0001
```

预期 track 形态：

- 失败尝试保留在原始 `attempt-0001` 或对应编号下。
- 重试创建新的 `attempt-0002`，不得覆盖旧结果。
- 失败 result 应包含 `failure_reason`、`evidence_refs` 和 `next_step`。

失败语义：

- `result = fail` 表示动作执行了，但没有达到验收标准。
- 失败不等于阻塞；只有缺少依赖、权限不足或无法继续推进时才写 `blocked`。
- 连续失败达到 profile 策略上限后，应升级人工介入。
