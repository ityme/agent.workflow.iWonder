# 事件协议

本文说明事件字段和 schema 使用方式。

## 最小字段

每条关键事件至少包含：

- `event_id`
- `reply_to`
- `correlation_id`
- `run_id`
- `task_id`
- `role`
- `state`
- `summary`
- `result`
- `ack_result`
- `timestamp`

## 字段职责

- `event_id`: 当前事件唯一编号。
- `reply_to`: 当前事件确认的上游事件。
- `correlation_id`: 贯穿同一任务链的关联编号。
- `state`: 当前状态。
- `result`: 当前动作结果。
- `ack_result`: 接收方确认结果。
- `evidence_refs`: 证据引用。

## Schema

schema 放在 `iSpace/schemas/` 下。标准库校验器覆盖核心子集；安装 `jsonschema` 后启用完整校验。

## 模板

模板放在 `iSpace/templates/events/` 下。新事件应从模板复制，再填入实际字段。
