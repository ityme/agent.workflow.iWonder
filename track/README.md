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
│     ├─ progress.jsonl
│     └─ handoff.json
├─ builder/
│  └─ 0001/
│     ├─ progress.jsonl
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
│  │        ├─ progress.jsonl
│  │        ├─ coder/
│  │        │  └─ attempt-0001/
│  │        │     ├─ coder.json
│  │        │     ├─ progress.jsonl
│  │        │     ├─ worktree.json
│  │        │     ├─ solution-summary.json
│  │        │     └─ result.json
│  │        ├─ tester/
│  │        │  └─ attempt-0001/
│  │        │     ├─ tester.json
│  │        │     ├─ progress.jsonl
│  │        │     ├─ test-summary.json
│  │        │     └─ result.json
│  │        └─ opser/
│  │           └─ attempt-0001/
│  │              ├─ opser.json
│  │              ├─ progress.jsonl
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
- `state`: `intake` / `clarifying` / `ready_for_builder` / `planned` / `running` / `waiting_ack` / `passed` / `failed` / `blocked` / `exited`。
- `confirmation_basis`: 用户明确确认或明确授权继续的依据；进入 `builder` 前必须存在。
- `open_questions`: 未决问题列表；进入 `builder` 前必须为空。
- `parent_role`: 当前角色的直属上级；除 `pm` 外不得为空。
- `assigned_role`: 当前任务被下发给的角色。
- `handoff_input_summary`: 上游交接输入摘要。
- `current_phase`: 当前阶段，如 `received` / `inspect` / `planning` / `implementing` / `testing` / `closing` / `retrying` / `blocked` / `exiting`。
- `progress_summary`: 当前进度摘要，描述正在处理什么、已完成什么。
- `progress_source`: 进度来源，如 `self` / `child` / `aggregated_child`。
- `aggregated_from`: 被当前事件汇总的下游 `event_id` 列表。
- `completed_actions`: 已完成动作列表。
- `evidence_refs`: 证据引用列表，可包含文件路径、命令、产物、track 事件或结果文件。
- `blockers`: 当前阻塞点列表。
- `last_progress_at`: 最近一次有效进度时间戳。
- `wait_reason`: 当前等待原因。
- `stall_check_count`: 连续无进展检查次数；达到 3 且存在阻塞证据时才可停止等待。
- `blocked_evidence`: 判定阻塞所依据的证据列表。
- `wait_decision`: `continue_waiting` / `retry_child` / `mark_blocked` / `escalate_human`。
- `next_step`: 下一步动作；父级不得把下一步写成代替子级执行任务。
- `handoff_allowed`: 是否允许继续交接到下一角色；缺少必要回执或确认时必须为 `false`。
- `role_boundary_check`: 角色边界检查结果，记录是否存在越权风险。
- `user_visible`: 当前进度事件是否可由 PM 转述给用户。
- `redaction_notes`: 已过滤的敏感信息或原始噪声说明。
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
2. `pm/<run_id>/progress.jsonl`
3. `pm/<run_id>/handoff.json`
4. `builder/<run_id>/progress.jsonl`
5. `builder/<run_id>/plan.json`
6. `task/<task_id>/tm/<run_id>/progress.jsonl`
7. `task/<task_id>/tm/<run_id>/tm.json`
8. 对应 `coder`、`tester`、`opser` 的 `progress.jsonl`
9. 对应 `coder`、`tester`、`opser` 的 `result.json`
10. `timeline.jsonl`

## 时序约束

- 任何父级角色都不得接管、补做或代做子级角色职责；子级失败时只能重试、阻塞或升级人工介入。
- 子级执行慢不等于阻塞；父级不得因为等待时间较长就停止等待。
- 父级只有在收到明确失败/阻塞回执，或 `stall_check_count >= 3` 且 `blocked_evidence` 非空时，才允许停止等待。
- 无进展检查必须写入进度事件，并将 `wait_decision` 设为 `continue_waiting`、`retry_child`、`mark_blocked` 或 `escalate_human`。
- 任何子级角色都不得绕过直属上级或横向联系其他 worker。
- 每个角色在接收任务、开始阶段、完成阶段、失败、阻塞、重试和退出时都应写入 `progress.jsonl`。
- 进度事件逐级传播：子级写入自己的 `progress.jsonl`，直属父级读取并汇总为 `progress_source = aggregated_child` 的父级进度事件，再继续向上汇报。
- `pm` 可以读取 `builder/tm` 的进度事件，以及经 `tm` 汇总后的 `coder/tester/opser` 进度事件，用于向用户说明执行进度。
- 进度事件可以用户可见，但必须过滤隐藏指令、内部推理链、凭据、敏感环境信息和未筛选原始日志。
- `tester` 无论通过与否都先回报 `tm`，然后退出。
- `tm` 只在 `tester_result = passed` 时启动 `opser`。
- `opser` 无论通过与否都先回报 `tm`，然后退出。
- `tm` 只在 `opser_result = success` 时退出。
- `tm` 在 `opser_result != success` 时重启 `opser`，重试序号递增。
- 同一子任务内 `opser` 连续失败 3 次时升级人工介入。
- `opser` 只读取 tester 的结构化结果，不直接消费未完成的中间过程。
- 每次回执应至少包含 `summary`、`result`、`ack_result`、`timestamp`，并在对应下一层目录写入一条确认记录。

## 状态转移表

- `pm`: `intake -> clarifying -> ready_for_builder -> waiting_builder -> waiting_user_ack -> exited`
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
