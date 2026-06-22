# track

这是一个追加式运行记录目录。
目标不是存源码，而是把 `pm / builder / tm / coder / tester / opser` 的任务流转、重试、结果和时间线分门别类地留痕。

## 目录原则

- 每个角色一个独立子树。
- 每次启动一个独立 `run_id`。
- 每个任务一个独立 `task_id`。
- 每次尝试一个独立 `attempt_id`。
- 文件只追加，不覆盖历史。
- 文件名必须使用 `序号-名称`、零填充序号和角色唯一后缀，方便按时间排序并避免覆盖。

## 推荐结构

```text
track/
├─ pm/
│  └─ 0001/
│     ├─ intake.json
│     ├─ questions.jsonl
│     ├─ decisions.jsonl
│     └─ handoff.json
├─ builder/
│  └─ 0001/
│     ├─ plan.json
│     ├─ summary.json
│     └─ tasks/
│        ├─ 001_login-api/
│        │  ├─ task.json
│        │  ├─ deps.json
│        │  └─ status.json
│        └─ 002_session-refresh/
│           ├─ task.json
│           ├─ deps.json
│           └─ status.json
├─ task/
│  ├─ 001_login-api/
│  │  └─ tm/
│  │     └─ 0001/
│  │        ├─ tm.json
│  │        ├─ events.jsonl
│  │        ├─ coder/
│  │        │  └─ attempt-0001/
│  │        │     ├─ coder.json
│  │        │     ├─ worktree.json
│  │        │     ├─ solution-summary.json
│  │        │     └─ result.json
│  │        ├─ tester/
│  │        │  └─ attempt-0001/
│  │        │     ├─ tester.json
│  │        │     ├─ test-summary.json
│  │        │     └─ result.json
│  │        └─ opser/
│  │           └─ attempt-0001/
│  │              ├─ opser.json
│  │              ├─ commit.json
│  │              ├─ opser-summary.json
│  │              ├─ result.json
│  │              ├─ push.disabled
│  │              └─ merge.disabled
│  └─ 002_session-refresh/
│     └─ tm/
│        └─ 0001/
│           └─ ...
└─ timeline.jsonl
```

## 字段建议

- `run_id`: 启动序号，如 `0001`。
- `task_id`: 带序号的任务名，如 `001_login-api`。
- `attempt_id`: 重试序号，如 `attempt-0002`。
- `role`: `pm` / `builder` / `tm` / `coder` / `tester` / `opser`。
- `summary`: 当前步骤的简短摘要。
- `result`: `success` / `fail` / `blocked`。
- `ack_result`: `received` / `processed` / `rejected`，表示下游对上游回执的确认。
- `event_id`: 当前事件的唯一编号。
- `reply_to`: 被当前回执确认的上游 `event_id`。
- `correlation_id`: 贯穿同一任务链的关联编号。
- `state`: `intake` / `planned` / `running` / `waiting_ack` / `passed` / `failed` / `blocked` / `exited`。
- `tester_result`: `passed` / `failed` / `blocked`，tester 必须先回报该结果再退出。
- `opser_result`: `success` / `fail` / `blocked`，opser 必须先回报该结果再退出。
- `tm_decision`: `start_opser` / `retry_coder` / `retry_task` / `retry_opser` / `escalate_human`。
- `retry_count`: 当前任务或角色的重试次数。
- `retry_reason`: 触发重试的简短原因。
- `next_actor`: 下一步接收方，如 `tm` / `coder` / `tester` / `opser` / `pm` / `human`。
- `recv_at`: 接收确认时间戳。
- `timestamp`: 时间戳。
- `worktree_path`: 对应 worktree 路径。

## 读取顺序

建议先看：

1. `pm/<run_id>/intake.json`
2. `builder/<run_id>/plan.json`
3. `task/<task_id>/tm/<run_id>/tm.json`
4. 对应 `coder`、`tester`、`opser` 的 `result.json`
5. `timeline.jsonl`

## 时序约束

- `tester` 无论通过与否都先回报 `tm`，然后退出。
- `tm` 只在 `tester_result = passed` 时启动 `opser`。
- `opser` 无论通过与否都先回报 `tm`，然后退出。
- `tm` 只在 `opser_result = success` 时退出。
- `tm` 在 `opser_result != success` 时重启 `opser`，重试序号递增。
- 同一子任务内 `opser` 连续失败 3 次时升级人工介入。
- `opser` 只读取 tester 的结构化结果，不直接消费未完成的中间过程。
- 每次回执应至少包含 `summary`、`result`、`ack_result`、`timestamp`，并在对应下一层目录写入一条确认记录。

## 状态转移表

- `pm`: `intake -> waiting_builder -> waiting_user_ack -> exited`
- `builder`: `planned -> waiting_pm_ack -> exited`
- `tm`: `planned -> running -> waiting_coder -> waiting_tester -> waiting_opser -> waiting_ack -> exited`
- `coder`: `running -> waiting_tm_ack -> exited`
- `tester`: `running -> waiting_tm_ack -> exited`
- `opser`: `running -> waiting_tm_ack -> exited`

## 命名规范

- `run_id`: `0001` 这种四位零填充。
- `task_id`: `001_login-api` 这种前缀序号加短名。
- `attempt_id`: `attempt-0001` 这种固定前缀加四位零填充。
- `event_id`: `evt-00000001` 这种固定前缀加八位零填充。
- `reply_to`: 直接引用上游 `event_id`，不得空写。
- 同层目录内，角色文件必须唯一，例如 `coder.json`、`tester.json`、`opser.json` 各自独立，不互相覆盖。
