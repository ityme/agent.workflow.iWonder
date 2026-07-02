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

## 使用时机

- `local-python-workers`: 本地 demo、自检和无外部依赖验证。
- `manual`: 需要人工审批、人工执行或不能自动化的步骤。
- `cli-worker`: 接入已有外部 CLI worker。
- `template`: 新建 adapter 时复制使用。

## 命令匹配

调度器必须使用完整数组匹配：

```json
["python", "iSpace/workers/default-development/coder_worker.py"]
```

下面这种附加参数不在 allowlist 中时必须拒绝：

```json
["python", "iSpace/workers/default-development/coder_worker.py", "--extra"]
```
