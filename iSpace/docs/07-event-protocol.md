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

第一版 schema 覆盖：

- `run.schema.json`: run 元数据。
- `task.schema.json`: task 元数据、依赖和验收标准。
- `handoff.schema.json`: 跨角色交接事件。
- `progress-event.schema.json`: 进度事件。
- `result.schema.json`: worker 结果。
- `closeout.schema.json`: 收口结果。
- `profile.schema.json`: profile 定义。
- `adapter.schema.json`: adapter 定义和 allowlist。

标准库子集校验至少覆盖：

- 必填字段。
- 字段类型。
- 枚举值。
- 数组元素类型。
- 简单对象结构。

安装可选依赖 `jsonschema` 后，可以启用完整 JSON Schema 校验，包括更严格的格式、pattern 和嵌套结构检查。

## 模板

模板放在 `iSpace/templates/events/` 下。新事件应从模板复制，再填入实际字段。

模板目录包括：

- `iSpace/templates/track/`: run 和 task 模板。
- `iSpace/templates/events/`: handoff、progress event、result、closeout 模板。
- `iSpace/templates/profiles/`: profile 模板。
- `iSpace/templates/adapters/`: adapter 模板。

新增事件时，应先选择对应模板，再保证：

- `event_id` 唯一。
- `reply_to` 指向已存在上游事件。
- `correlation_id` 贯穿同一任务链。
- `run_id` 和 `task_id` 与当前运行记录一致。
- `evidence_refs` 只引用必要证据，不塞入大段原始日志。
