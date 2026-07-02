# Harness 工程实施计划

> **给 agent worker 的要求：** 执行本计划时，优先使用 `superpowers:subagent-driven-development`，也可以使用 `superpowers:executing-plans`。必须按任务逐项推进，步骤使用复选框记录状态。

**目标：** 构建一个平台无关、Python 优先、具备生产级高可用雏形的 AI Agent Harness 工程包，覆盖文档、schema、profile、adapter、调度器、示例 worker、校验、审计、汇总和测试。

**架构：** Harness 分为规约层、记录层、执行层和审计层。核心工具默认只写 `iSpace/track`、`iSpace/tmp`、`iSpace/reports`；业务侧变更只能由 worker 在 adapter 声明的 workspace 内完成。Python CLI 读取 profile 和 adapter，校验 allowlist，调度 worker，原子写入 track，校验状态并生成审计与汇总报告。

**技术栈：** Python 3 标准库优先，主要使用 `argparse`、`json`、`pathlib`、`subprocess`、`tempfile`、`unittest`、`datetime`、`os`、`shutil`；可选使用 `jsonschema` 增强 schema 校验；文档使用 Markdown；结构化协议使用 JSON Schema 和 JSON 模板。

**完成状态：** 本计划的第一版交付已完成，当前仓库可通过 `python iSpace/tools/harness.py selftest` 做总体验收。本文后续作为历史实施记录、回归验收清单和后续增强参考。

---

## 范围说明

本计划是 `iSpace/docs/design/harness-engineering-spec.md` 的顶层 builder 实施计划。范围较大，必须按阶段交付。每个阶段都应独立提交，并保持仓库处于可理解、可继续推进的状态。

本计划不展开完整调度器的每一行代码。进入每个阶段前，应为该阶段编写更细的子计划，明确测试、实现步骤和验收命令。

## 目标文件结构

需要创建或更新这些区域：

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
│  ├─ design/harness-engineering-spec.md
│  └─ plans/harness-engineering-implementation-plan.md
├─ profiles/
│  ├─ default-development/
│  ├─ documentation/
│  ├─ data-analysis/
│  └─ ops-change/
├─ adapters/
│  ├─ README.md
│  ├─ local-python-workers/
│  ├─ cli-worker/
│  ├─ manual/
│  └─ template/
├─ schemas/
│  ├─ run.schema.json
│  ├─ task.schema.json
│  ├─ handoff.schema.json
│  ├─ progress-event.schema.json
│  ├─ result.schema.json
│  ├─ closeout.schema.json
│  ├─ profile.schema.json
│  └─ adapter.schema.json
├─ templates/
│  ├─ track/
│  ├─ events/
│  ├─ roles/
│  ├─ profiles/
│  └─ adapters/
├─ examples/
│  ├─ minimal-success-run/
│  ├─ failed-and-retry-run/
│  ├─ blocked-run/
│  ├─ human-escalation-run/
│  └─ non-code-documentation-run/
├─ workers/
│  ├─ default-development/
│  ├─ documentation/
│  ├─ data-analysis/
│  └─ ops-change/
├─ tools/
│  ├─ harness.py
│  ├─ harness_lib/
│  └─ README.md
├─ tests/
├─ checklists/
├─ track/
├─ tmp/
└─ reports/
```

## 阶段 1：文档骨架和导航

**文件：**
- 修改：`iSpace/README.md`
- 新建：`iSpace/docs/00-overview.md`
- 新建：`iSpace/docs/01-quickstart.md`
- 新建：`iSpace/docs/02-concepts.md`
- 新建：`iSpace/docs/03-architecture.md`
- 新建：`iSpace/docs/04-roles.md`
- 新建：`iSpace/docs/05-workflow.md`
- 新建：`iSpace/docs/06-state-machine.md`
- 新建：`iSpace/docs/07-event-protocol.md`
- 新建：`iSpace/docs/08-permissions.md`
- 新建：`iSpace/docs/09-observability.md`
- 新建：`iSpace/docs/10-error-handling.md`
- 新建：`iSpace/docs/11-tools.md`
- 新建：`iSpace/docs/12-adapters.md`
- 新建：`iSpace/docs/13-testing.md`
- 新建：`iSpace/docs/14-security.md`

- [x] 创建上述文档文件，正文中文优先。
- [x] 更新 `iSpace/README.md`，链接编号文档，并说明完整目标工程包。
- [x] 保持 `iSpace/docs/design/harness-engineering-spec.md` 作为权威设计来源。
- [x] 检查没有残留具体平台绑定。

运行：

```powershell
rg -n "C[o]dex|c[o]dex|\\.c[o]dex|gpt-5\\.5|T[B]D|T[O]DO" iSpace
```

预期：无匹配。

提交：

```powershell
git add iSpace/README.md iSpace/docs
git commit -m "docs: add harness documentation skeleton"
```

## 阶段 2：Schema 和模板

**文件：**
- 新建：`iSpace/schemas/run.schema.json`
- 新建：`iSpace/schemas/task.schema.json`
- 新建：`iSpace/schemas/handoff.schema.json`
- 新建：`iSpace/schemas/progress-event.schema.json`
- 新建：`iSpace/schemas/result.schema.json`
- 新建：`iSpace/schemas/closeout.schema.json`
- 新建：`iSpace/schemas/profile.schema.json`
- 新建：`iSpace/schemas/adapter.schema.json`
- 新建：`iSpace/templates/track/run.json`
- 新建：`iSpace/templates/track/task.json`
- 新建：`iSpace/templates/events/progress-event.json`
- 新建：`iSpace/templates/events/handoff.json`
- 新建：`iSpace/templates/events/result.json`
- 新建：`iSpace/templates/events/closeout.json`
- 新建：`iSpace/templates/profiles/profile.json`
- 新建：`iSpace/templates/adapters/adapter.json`

- [x] 根据 `iSpace/track/README.md` 定义必填字段、枚举值和对象结构。
- [x] 保持 schema 足够简单，使标准库子集校验器可以覆盖核心规则。
- [x] 增加能通过对应 schema 的 JSON 模板。
- [x] 在 `iSpace/docs/07-event-protocol.md` 说明 schema 使用方式。

运行：

```powershell
python -m json.tool iSpace/schemas/progress-event.schema.json
python -m json.tool iSpace/templates/events/progress-event.json
```

预期：两个命令都能格式化输出 JSON，并以 0 退出。

提交：

```powershell
git add iSpace/schemas iSpace/templates iSpace/docs/07-event-protocol.md
git commit -m "feat: add harness schemas and templates"
```

## 阶段 3：Python 核心工具库

**文件：**
- 新建：`iSpace/tools/harness.py`
- 新建：`iSpace/tools/harness_lib/__init__.py`
- 新建：`iSpace/tools/harness_lib/paths.py`
- 新建：`iSpace/tools/harness_lib/atomic.py`
- 新建：`iSpace/tools/harness_lib/jsonio.py`
- 新建：`iSpace/tools/harness_lib/locks.py`
- 新建：`iSpace/tests/test_paths.py`
- 新建：`iSpace/tests/test_atomic.py`
- 新建：`iSpace/tests/test_locks.py`
- 新建：`iSpace/tests/test_jsonio.py`

- [x] 实现路径工具，解析 harness 根目录，并限制核心工具只写 `track`、`tmp`、`reports`。
- [x] 实现 JSON 和 JSONL 原子写入工具。
- [x] 实现跨平台锁文件工具。
- [x] 实现 JSON/JSONL 读取和追加工具。
- [x] 使用 `unittest` 和 `tempfile` 编写无依赖测试。

运行：

```powershell
python -m unittest discover iSpace/tests
```

预期：当前测试全部通过。

提交：

```powershell
git add iSpace/tools iSpace/tests
git commit -m "feat: add harness core utilities"
```

## 阶段 4：Track、Schema 子集和状态机校验

**文件：**
- 新建：`iSpace/tools/harness_lib/schema.py`
- 新建：`iSpace/tools/harness_lib/state_machine.py`
- 新建：`iSpace/tools/harness_lib/track.py`
- 新建：`iSpace/tests/test_schema.py`
- 新建：`iSpace/tests/test_state_machine.py`
- 新建：`iSpace/tests/test_track.py`
- 修改：`iSpace/tools/harness.py`

- [x] 实现标准库 schema 子集校验，覆盖必填字段、类型、枚举、数组和嵌套对象。
- [x] 检测可选依赖 `jsonschema`，存在时启用完整 JSON Schema 校验。
- [x] 实现四个 profile 的状态转移校验。
- [x] 实现 run、task、attempt、event 创建工具，并保证幂等。
- [x] 暴露 CLI 命令：`new-run`、`new-task`、`validate`。

运行：

```powershell
python -m unittest discover iSpace/tests
python iSpace/tools/harness.py new-run --title "demo" --profile default-development
python iSpace/tools/harness.py validate --run 0001
```

预期：测试通过；命令以 0 退出；文件只写入 `iSpace/track`。

提交：

```powershell
git add iSpace/tools iSpace/tests iSpace/track
git commit -m "feat: add track and validation commands"
```

## 阶段 5：Profile 和 Adapter

**文件：**
- 新建：`iSpace/profiles/default-development/profile.json`
- 新建：`iSpace/profiles/documentation/profile.json`
- 新建：`iSpace/profiles/data-analysis/profile.json`
- 新建：`iSpace/profiles/ops-change/profile.json`
- 新建：`iSpace/adapters/README.md`
- 新建：`iSpace/adapters/local-python-workers/default-development.json`
- 新建：`iSpace/adapters/local-python-workers/documentation.json`
- 新建：`iSpace/adapters/local-python-workers/data-analysis.json`
- 新建：`iSpace/adapters/local-python-workers/ops-change.json`
- 新建：`iSpace/adapters/template/adapter.json`
- 新建：`iSpace/adapters/manual/README.md`
- 新建：`iSpace/adapters/cli-worker/README.md`
- 新建：`iSpace/tools/harness_lib/profile.py`
- 新建：`iSpace/tools/harness_lib/adapter.py`
- 新建：`iSpace/tests/test_adapter_allowlist.py`
- 新建：`iSpace/tests/test_profile.py`

- [x] 定义四个完整 profile，包含角色、流程顺序、状态转移、重试策略和收口策略。
- [x] 定义本地 Python 示例 worker 的 adapter 配置。
- [x] 实现 profile 读取和 adapter 读取。
- [x] 强制 command 与 allowlist 完整匹配。
- [x] 拒绝未在 adapter allowlist 声明的命令数组。

运行：

```powershell
python -m unittest discover iSpace/tests
python iSpace/tools/harness.py validate --profile default-development
```

预期：测试通过；profile 校验以 0 退出。

提交：

```powershell
git add iSpace/profiles iSpace/adapters iSpace/tools iSpace/tests
git commit -m "feat: add profiles and adapter allowlist"
```

## 阶段 6：调度器和示例 Worker

**文件：**
- 新建：`iSpace/tools/harness_lib/dispatcher.py`
- 新建：`iSpace/tools/harness_lib/retry.py`
- 新建：`iSpace/workers/default-development/coder_worker.py`
- 新建：`iSpace/workers/default-development/tester_worker.py`
- 新建：`iSpace/workers/default-development/opser_worker.py`
- 新建：`iSpace/workers/documentation/planner_worker.py`
- 新建：`iSpace/workers/documentation/writer_worker.py`
- 新建：`iSpace/workers/documentation/reviewer_worker.py`
- 新建：`iSpace/workers/documentation/publisher_worker.py`
- 新建：`iSpace/workers/data-analysis/analyst_worker.py`
- 新建：`iSpace/workers/data-analysis/verifier_worker.py`
- 新建：`iSpace/workers/data-analysis/reporter_worker.py`
- 新建：`iSpace/workers/ops-change/planner_worker.py`
- 新建：`iSpace/workers/ops-change/executor_worker.py`
- 新建：`iSpace/workers/ops-change/validator_worker.py`
- 新建：`iSpace/workers/ops-change/releaser_worker.py`
- 新建：`iSpace/tests/test_dispatcher.py`
- 新建：`iSpace/tests/test_demo_flow.py`
- 修改：`iSpace/tools/harness.py`

- [x] 实现 `dispatch`，按 adapter 命令、超时、输入文件、输出文件和 workspace 调度单个角色。
- [x] 实现 `run-task`，按选定 profile 的流程执行任务。
- [x] 实现 `demo`，创建 `default-development` run，并执行本地 worker 链路。
- [x] 确保所有 worker 只使用 Python 标准库，并输出结构化 result JSON。
- [x] 确保 worker 失败 exit code 会写入 track，不产生未记录状态。

运行：

```powershell
python -m unittest discover iSpace/tests
python iSpace/tools/harness.py demo
python iSpace/tools/harness.py validate --run 0001
```

预期：测试通过；demo 以 0 退出；validate 以 0 退出。

提交：

```powershell
git add iSpace/tools iSpace/workers iSpace/tests iSpace/track
git commit -m "feat: add dispatcher and demo workers"
```

## 阶段 7：审计、脱敏和汇总报告

**文件：**
- 新建：`iSpace/tools/harness_lib/audit.py`
- 新建：`iSpace/tools/harness_lib/redact.py`
- 新建：`iSpace/tools/harness_lib/summarize.py`
- 新建：`iSpace/tests/test_audit.py`
- 新建：`iSpace/tests/test_redact.py`
- 新建：`iSpace/tests/test_summarize.py`
- 修改：`iSpace/tools/harness.py`

- [x] 实现 `audit` 检查：敏感字符串、缺失确认、无效 `reply_to`、重复 `event_id`、workspace 路径越界、未闭环任务。
- [x] 实现 `summarize`，在 `iSpace/reports` 下生成 Markdown 报告。
- [x] 实现脱敏工具和告警输出。
- [x] 暴露 CLI 命令：`audit`、`summarize`。

运行：

```powershell
python -m unittest discover iSpace/tests
python iSpace/tools/harness.py audit --run 0001
python iSpace/tools/harness.py summarize --run 0001
```

预期：测试通过；干净 demo 的 audit 以 0 退出；summary 报告写入 `iSpace/reports`。

提交：

```powershell
git add iSpace/tools iSpace/tests iSpace/reports
git commit -m "feat: add audit and summary reports"
```

## 阶段 8：示例和清单

**文件：**
- 新建：`iSpace/examples/minimal-success-run/README.md`
- 新建：`iSpace/examples/failed-and-retry-run/README.md`
- 新建：`iSpace/examples/blocked-run/README.md`
- 新建：`iSpace/examples/human-escalation-run/README.md`
- 新建：`iSpace/examples/non-code-documentation-run/README.md`
- 新建：`iSpace/checklists/adoption-checklist.md`
- 新建：`iSpace/checklists/task-start-checklist.md`
- 新建：`iSpace/checklists/profile-design-checklist.md`
- 新建：`iSpace/checklists/closeout-checklist.md`
- 新建：`iSpace/checklists/release-readiness-checklist.md`

- [x] 增加示例 README，说明命令、预期 track 文件和失败语义。
- [x] 增加接入、任务启动、profile 设计、收口、发布前检查清单。
- [x] 从 `iSpace/README.md` 链接示例和清单。

运行：

```powershell
rg -n "examples|minimal-success-run|release-readiness" iSpace/README.md iSpace/examples iSpace/checklists
```

预期：能看到新增示例和清单的可发现引用。

提交：

```powershell
git add iSpace/examples iSpace/checklists iSpace/README.md
git commit -m "docs: add examples and checklists"
```

## 阶段 9：工具文档和自检

**文件：**
- 新建：`iSpace/tools/README.md`
- 修改：`iSpace/docs/01-quickstart.md`
- 修改：`iSpace/docs/11-tools.md`
- 修改：`iSpace/docs/12-adapters.md`
- 修改：`iSpace/docs/13-testing.md`
- 修改：`iSpace/docs/14-security.md`
- 修改：`iSpace/tools/harness.py`

- [x] 说明每个 CLI 命令的使用时机、输入、输出和失败处理。
- [x] 增加 `selftest` 命令，依次运行 unittest、demo、validate、audit、summarize。
- [x] 说明可选依赖 `jsonschema` 的增强行为。
- [x] 同时提供 PowerShell 和 Bash 命令示例。

运行：

```powershell
python iSpace/tools/harness.py selftest
```

预期：selftest 以 0 退出，并打印它执行过的命令。

提交：

```powershell
git add iSpace/tools iSpace/docs iSpace/README.md
git commit -m "feat: add selftest and tool documentation"
```

## 阶段 10：最终验证和发布就绪

**文件：**
- 修改：`iSpace/README.md`
- 按需修改：`iSpace/docs/design/harness-engineering-spec.md`
- 按需修改：`iSpace/docs/plans/harness-engineering-implementation-plan.md`

- [x] 运行完整 selftest。
- [x] 检查平台绑定残留。
- [x] 检查占位词残留。
- [x] 确认所有核心工具写入都在 `track`、`tmp`、`reports` 下；worker workspace 必须由 adapter 声明。
- [x] 确认四个 profile 可以运行或校验。
- [x] 更新最终 README 链接和发布前检查清单。

运行：

```powershell
python iSpace/tools/harness.py selftest
rg -n "C[o]dex|c[o]dex|\\.c[o]dex|gpt-5\\.5|T[B]D|T[O]DO" iSpace
git status --short
```

预期：selftest 以 0 退出；搜索无匹配；提交前 `git status` 只显示预期的最终文档更新。

提交：

```powershell
git add iSpace
git commit -m "docs: finalize harness engineering package"
```

## 依赖顺序

1. 阶段 1 必须先完成，后续文档引用才有稳定落点。
2. 阶段 2 必须先完成，schema 校验实现才有目标。
3. 阶段 3 必须先完成，后续命令才能安全写 track。
4. 阶段 4 必须先完成，调度器才有状态和记录基础。
5. 阶段 5 必须先完成，调度器才知道可调用哪些 worker 命令。
6. 阶段 6 必须先完成，示例、审计、汇总和 selftest 才有真实输入。
7. 阶段 7 必须先完成，最终 selftest 才有审计和报告能力。
8. 阶段 8 和阶段 9 可以在阶段 6 后并行推进，但应在阶段 7 后统一收口。
9. 阶段 10 负责最终发布就绪。

## 最终验收

- `python iSpace/tools/harness.py demo` 在无第三方依赖时以 0 退出。
- `python iSpace/tools/harness.py selftest` 在无第三方依赖时以 0 退出。
- `python -m unittest discover iSpace/tests` 以 0 退出。
- demo 后运行 `python iSpace/tools/harness.py validate --run 0001` 以 0 退出。
- 干净 demo 后运行 `python iSpace/tools/harness.py audit --run 0001` 以 0 退出。
- `python iSpace/tools/harness.py summarize --run 0001` 在 `iSpace/reports` 下生成报告。
- 四个 profile 都包含 profile 配置、adapter 配置、本地 Python worker、文档和至少一个示例。
- adapter allowlist 能拒绝未声明命令。
- 核心工具只写 `iSpace/track`、`iSpace/tmp`、`iSpace/reports`。
- 文档说明每个工具命令的使用时机和用法。
- 不残留具体平台绑定。

