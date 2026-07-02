# 权限

本文说明权限模型和默认禁用项。

## 默认允许

- 读取 harness 文档。
- 写入 `iSpace/track`。
- 写入 `iSpace/tmp`。
- 写入 `iSpace/reports`。
- 执行 adapter allowlist 中声明的本地 worker 命令。

## 默认禁止

- 未在 allowlist 声明的外部命令。
- shell 拼接命令。
- 远端写入。
- push。
- PR。
- merge。
- 部署。
- 修改 adapter 未授权的业务路径。

## 权限升级

需要更高权限时，必须记录：

- 请求原因。
- 请求角色。
- 操作范围。
- 风险。
- 用户确认依据。

## Worker Workspace

worker 只能在 adapter 声明的 workspace 内执行业务操作。核心工具不得直接修改业务项目文件。
