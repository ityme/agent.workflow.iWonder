# Adapter

Adapter 用来声明 harness 如何调用具体 worker。它只描述命令、输入输出、workspace、超时、权限和 allowlist，不包含业务逻辑。

使用时机：

- 当调度器需要调用 worker 时，先读取当前 profile 对应的 adapter。
- 当接入新的 CLI、脚本、人工步骤或平台运行器时，新增 adapter 配置。
- 当命令参数发生变化时，必须同步更新 `allowlist`，否则调度器应拒绝执行。

安全约束：

- `command` 必须与 `allowlist` 中某个命令数组完整一致。
- 不使用 shell 字符串拼接。
- workspace 必须显式声明。
- `allow_publish`、`allow_merge`、`allow_remote_write` 默认保持 `false`。

内置目录：

- `local-python-workers/`: 本地 Python 示例 worker 配置。
- `template/`: 新 adapter 模板。
- `manual/`: 人工执行 adapter 说明。
- `cli-worker/`: 外部 CLI worker 接入说明。
