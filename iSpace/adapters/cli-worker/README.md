# CLI Worker Adapter

cli-worker adapter 用于接入外部 CLI 或内部命令行工具。

使用时机：

- 现有组织已有独立 CLI worker。
- worker 通过文件输入输出 JSON。
- 需要把平台差异隔离在配置层，而不是写进 harness 核心。

约束：

- 命令必须使用数组形式，例如 `["python", "worker.py"]`。
- 传参必须显式进入 allowlist。
- 不默认启用远端写入、发布、合并或部署。
