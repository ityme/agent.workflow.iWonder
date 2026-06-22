# agent.workflow.iWonder

`agent.workflow.iWonder` 是一套面向 Codex 多角色协作的约束文档与任务流协议。

当前项目只维护角色规则、任务流约束、回执规范和 `track/` 留痕结构；它不是运行时编排器，也不会在代码层强制启动或阻断 agent。

## 使用说明

### 1. 让 Codex 读取项目规则

在项目根目录保留这些文件：

```text
AGENTS.md
.codex/
track/README.md
README.md
```

其中：

- `AGENTS.md`: 全局交互规则、角色边界、任务编排规则。
- `.codex/agents/`: `pm`、`builder`、`tm`、`coder`、`tester`、`opser` 的角色配置。
- `.codex/rules/default.rules`: 安装软件或安装包时的审批规则。
- `track/README.md`: 运行记录目录结构、字段、状态机和命名规范。
- `README.md`: 项目使用说明和设计思路。

### 2. 需求确认

接到新任务后，`pm` 必须先进行需求确认。

确认内容至少包括：

- 范围。
- 变更点。
- 验收标准。
- 非目标。
- 未决问题。

需求确认完成前，不进入 `builder` 拆解，也不进入实现。

### 3. 推荐的新任务流程

接到一个新任务时，默认按以下顺序推进：

```text
user -> pm -> builder -> pm -> tm -> coder -> tm -> tester -> tm -> opser -> tm -> pm -> user
```

要求：

- `pm` 先和用户澄清需求，不直接改代码。
- `builder` 只接受已经完成需求确认的任务，负责拆解任务、依赖和验收标准，不改源码。
- `tm` 只负责一个子任务的串行编排。
- `coder` 完成实现后必须回报 `tm`，再退出。
- `tester` 无论通过与否必须回报 `tm`，再退出。
- `opser` 无论成功与否必须回报 `tm`，再退出。
- `tm` 只有在收到 `tester` 通过后才能启动 `opser`。
- `tm` 只有在收到 `opser` 成功后才能退出并回报 `pm`。

### 4. Track 留痕

所有任务过程应写入 `track/`，保持追加式、可追踪、按时间排序。

推荐先阅读：

```text
track/README.md
```

核心编号：

- `run_id`: `0001`
- `task_id`: `001_login-api`
- `attempt_id`: `attempt-0001`
- `event_id`: `evt-00000001`

每条关键回执至少包含：

- `event_id`
- `reply_to`
- `correlation_id`
- `state`
- `role`
- `summary`
- `result`
- `ack_result`
- `timestamp`

### 5. 权限与 Git

默认允许：

- 工作区内阅读。
- 工作区内编辑。
- 测试和检查。
- 常规 git 操作。

需要单独确认：

- 安装软件。
- 安装包。
- 启用 `push`。
- 创建或更新 PR。
- merge。

`push`、`PR`、`merge` 当前只作为禁用字段和未来流程预留，不默认启用。

### 6. 迁移到新仓库

如果要把当前规则迁移到同级目录的新仓库，例如 `agent.workflow.iWonder/`，至少复制：

```powershell
Copy-Item -Recurse .\ai\AGENTS.md .\agent.workflow.iWonder\
Copy-Item -Recurse .\ai\.codex .\agent.workflow.iWonder\
Copy-Item -Recurse .\ai\track .\agent.workflow.iWonder\
Copy-Item .\ai\README.md .\agent.workflow.iWonder\
```

注意：普通的 `cp ai/* agent.workflow.iWonder/` 不会复制 `.codex` 这种隐藏目录。

## 当前阶段边界

当前项目仍是文档级约束。

这些规则可以指导 Codex 行为，但不能从运行时层面强制阻断错误流程。未来如果要做到强制校验，需要额外实现：

- schema 校验。
- 状态机 validator。
- worker 启动器。
- track 事件写入器。
- `event_id/reply_to/correlation_id` 校验。
- 失败重试和人工介入判断。

## 设计思路

### 项目定位

本项目的目标不是立即做一个复杂编排器，而是先把多 agent 协作中的角色边界、通信方式、回执机制、失败处理和留痕结构定义清楚。

先完善约束，再实现编排器。这样可以避免在规则尚未稳定时过早写死流程。

### 角色拓扑

默认拓扑为：

```text
pm -> builder -> tm -> coder/tester/opser
```

角色职责：

- `pm`: 只负责和用户沟通、澄清需求、做最终裁决。
- `builder`: 负责把需求拆成带序号的小任务、依赖和验收标准。
- `tm`: 负责单个子任务的串行编排。
- `coder`: 只执行单个实现任务。
- `tester`: 只验证当前子任务。
- `opser`: 只在测试通过后做受控 git 收口。

### 降低记忆污染

`pm` 不直接消费 `coder/tester/opser` 的原始过程，只读取 `builder` 和 `tm` 的结构化摘要。

这样可以让 PM 保持高层判断能力，避免被低层日志、失败细节和临时尝试污染上下文。

### 需求确认先行

需求确认阶段必须先压实需求，再进入任务拆解。

需求确认的作用是把用户需求压实为范围、变更点、验收标准、非目标和未决问题。只有这些内容清晰后，`pm` 才能启动 `builder`。

如果需求确认结果仍然含糊，`pm` 应继续追问用户，`builder` 应返回阻塞原因，而不是强行拆解。

### 明确回执

所有关键步骤采用“发出 + 确认”两段式回执。

每个 worker 完成当前子任务后，必须先向直属上级回报结果，再退出。下一层收到结果后，也要写入已接收或已处理确认。

这个设计的目的，是让任务链能追踪到：

- 谁发起了动作。
- 谁收到了动作。
- 谁确认了结果。
- 哪一步失败或阻塞。
- 重试是否发生过。

### 串行优先

虽然 `tm` 未来可以并发执行多个子任务，但当前默认禁用并发。

先采用串行执行可以降低任务依赖、worktree 隔离、track 写入和失败回滚的复杂度。

### Worktree 隔离

`coder` 应在独立 git worktree 内完成子任务，`tester` 验证对应 worktree，`opser` 只处理已经通过测试的 worktree。

不同子任务之间应保持目录、记录和上下文隔离。

### 未来编排器方向

未来如果实现运行时编排器，应遵循：

- 以 `track/` 为唯一事实源。
- 所有 worker 必须由编排器启动。
- 所有 worker 输出必须是结构化 JSON。
- 状态推进前必须校验当前状态、回执字段、重试次数和任务归属。
- 校验失败时 fail closed，即停止推进并记录 `blocked`。
- PM 只读取结构化摘要，不读取 worker 原始日志。
