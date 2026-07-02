# Adapter

本文说明 adapter 的职责、结构和安全边界。

## 职责

Adapter 负责把通用 harness 规则映射到具体执行环境：

- worker 命令。
- 输入文件。
- 输出文件。
- workspace。
- 超时。
- allowlist。
- 权限等级。

## 为什么需要 Adapter

不同平台的启动命令、日志格式、权限模型和输出格式不同。adapter 把这些差异隔离在配置层，避免核心 harness 绑定某个平台。

## 安全规则

- command 必须完整匹配 allowlist。
- 默认不使用 shell。
- 默认拒绝未声明命令。
- workspace 必须在配置中显式声明。
- 外部发布动作必须单独启用。

## 第一版 Adapter

第一版至少包含：

- `local-python-workers`
- `manual`
- `cli-worker`
- `template`
