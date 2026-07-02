# 最小成功运行

本示例对应当前仓库内置的 `default-development` demo。

运行：

```powershell
python iSpace/tools/harness.py demo
python iSpace/tools/harness.py validate --run 0001
python iSpace/tools/harness.py audit --run 0001
python iSpace/tools/harness.py summarize --run 0001
```

预期 track 文件：

- `iSpace/track/runs/0001/run.json`
- `iSpace/track/task/001_demo-task/task.json`
- `iSpace/track/task/001_demo-task/tm/0001/coder/attempt-0001/result.json`
- `iSpace/track/task/001_demo-task/tm/0001/tester/attempt-0001/result.json`
- `iSpace/track/task/001_demo-task/tm/0001/opser/attempt-0001/result.json`
- `iSpace/track/task/001_demo-task/tm/0001/opser/attempt-0001/closeout.json`
- `iSpace/reports/run-0001-summary.md`

成功语义：

- 所有 worker 结果为 `success`。
- `validate` 以 0 退出。
- `audit` 以 0 退出。
- 收口为 `no_op`，因为 demo 不执行真实提交、发布或远端写入。
