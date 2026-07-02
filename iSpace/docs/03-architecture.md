# 架构

本文说明 harness 的分层架构。

## 四层结构

```text
规约层 -> 记录层 -> 执行层 -> 审计层
```

## 规约层

规约层定义角色、流程、状态机、事件字段、权限和错误处理策略。

相关文件：

- `iSpace/docs/`
- `iSpace/profiles/`
- `iSpace/schemas/`

## 记录层

记录层使用 `iSpace/track` 保存运行事实。它是校验、恢复、审计和汇总的主要依据。

相关文件：

- `iSpace/track/README.md`
- `iSpace/templates/track/`

## 执行层

执行层由 Python CLI 和 worker 组成。CLI 读取 profile 和 adapter，按 allowlist 调用 worker。

相关文件：

- `iSpace/tools/harness.py`
- `iSpace/tools/harness_lib/`
- `iSpace/workers/`

## 审计层

审计层检查状态、权限、路径、事件引用、敏感信息和任务闭环情况。

相关文件：

- `iSpace/tools/harness_lib/audit.py`
- `iSpace/tools/harness_lib/redact.py`
- `iSpace/reports/`

## 写入边界

核心工具默认只写：

- `iSpace/track`
- `iSpace/tmp`
- `iSpace/reports`

业务变更只能由 worker 在 adapter 声明的 workspace 内完成。
