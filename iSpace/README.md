# iWonder Agent Harness

`iWonder Agent Harness` 是一套平台无关、Python 优先、中文文档优先的 AI Agent 协作工程包。它用于定义多角色任务编排、状态转移、事件回执、权限边界、可观测运行记录、调度器接口和审计规则。

当前仓库正在从文档级规约演进为完整 harness 工程包。目标是让用户复制 `iSpace/` 后，可以通过文档、schema、profile、adapter、Python 工具、示例 worker、测试和清单，开箱运行并审计一次完整 agent 协作任务。

## 快速入口

建议按以下顺序阅读：

1. [快速开始](docs/01-quickstart.md)
2. [核心概念](docs/02-concepts.md)
3. [架构](docs/03-architecture.md)
4. [角色](docs/04-roles.md)
5. [工作流](docs/05-workflow.md)
6. [状态机](docs/06-state-machine.md)
7. [事件协议](docs/07-event-protocol.md)
8. [工具](docs/11-tools.md)
9. [Adapter](docs/12-adapters.md)
10. [安全](docs/14-security.md)

设计和计划：

- [Harness 工程规约设计文档](docs/design/harness-engineering-spec.md)
- [Harness 工程实施计划](docs/plans/harness-engineering-implementation-plan.md)

## 目录说明

```text
iSpace/
├─ README.md
├─ docs/
│  ├─ 00-overview.md
│  ├─ 01-quickstart.md
│  ├─ 02-concepts.md
│  ├─ 03-architecture.md
│  ├─ 04-roles.md
│  ├─ 05-workflow.md
│  ├─ 06-state-machine.md
│  ├─ 07-event-protocol.md
│  ├─ 08-permissions.md
│  ├─ 09-observability.md
│  ├─ 10-error-handling.md
│  ├─ 11-tools.md
│  ├─ 12-adapters.md
│  ├─ 13-testing.md
│  ├─ 14-security.md
│  ├─ design/
│  ├─ plans/
│  ├─ agents/
│  └─ rules/
└─ track/
   └─ README.md
```

后续阶段会继续补齐：

- `profiles/`
- `adapters/`
- `schemas/`
- `templates/`
- `examples/`
- `workers/`
- `tools/`
- `tests/`
- `checklists/`
- `tmp/`
- `reports/`

## 当前阶段

当前已完成：

- 通用 harness 文档定位。
- 设计文档。
- 总实施计划。
- 编号文档骨架。
- track 协议说明。
- 默认角色配置样例。

后续按 [实施计划](docs/plans/harness-engineering-implementation-plan.md) 分阶段推进。

## 核心原则

- 不绑定任何单一 AI 平台、CLI、IDE 插件、模型供应商或运行时。
- Markdown 正文中文优先，必要专业术语保留英文。
- Python 永远优先。
- Python 标准库优先，可选依赖增强。
- 核心工具默认只写 `iSpace/track`、`iSpace/tmp`、`iSpace/reports`。
- worker 只能在 adapter 声明的 workspace 内执行业务操作。
- adapter command 必须严格匹配 allowlist。
- 外部发布动作默认禁用。
- 状态校验失败时 fail closed。
- Windows、Linux、macOS 都是一等支持目标。

## Profile

第一版目标包含四个完整 profile：

- `default-development`: 代码开发任务。
- `documentation`: 文档写作和文档重构任务。
- `data-analysis`: 数据分析、报表和结论生成任务。
- `ops-change`: 运维变更、配置变更和发布前检查任务。

每个 profile 都应包含角色定义、流程定义、状态转移、adapter 配置、本地 Python worker、示例和验收说明。

## 工具目标

完整实现后，Python CLI 入口为：

```powershell
python iSpace/tools/harness.py <command>
```

目标命令：

- `init`
- `demo`
- `new-run`
- `new-task`
- `dispatch`
- `run-task`
- `validate`
- `audit`
- `summarize`
- `selftest`

当前阶段尚未实现这些命令，后续会按实施计划逐步补齐。

## Track

`track/` 是运行记录目录。它保存 run、task、attempt、event、result、closeout 和 timeline，是校验、恢复、审计和汇总的主要依据。

详见 [track 协议](track/README.md)。

## 安全边界

默认禁止：

- 未在 allowlist 声明的命令。
- shell 拼接命令。
- 远端写入。
- push。
- PR。
- merge。
- 部署。
- 修改 adapter 未授权的业务路径。

任何权限升级都必须记录原因、范围、风险和用户确认依据。
