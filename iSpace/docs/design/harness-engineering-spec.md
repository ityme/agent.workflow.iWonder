# Harness 工程规约设计文档

## 目标

构建一个高可用、组件齐全、开箱即用、平台无关的 AI Agent Harness 工程规约包。

这个规约包不仅包含 Markdown 文档，还应包含 profile、schema、模板、示例、Python 工具、调度器雏形、适配器配置、本地示例 worker、自动化测试、自检命令、审计报告和使用清单。用户拿到仓库后，应能在无外部 AI 平台依赖的情况下跑通一条完整 demo，并能把同一套 harness 迁移到真实项目中。

## 实现状态

第一版已完成可运行工程包：`selftest`、`demo`、`validate`、`audit`、`summarize` 均可在无第三方依赖时运行。后续增强应继续遵守本文的安全边界、profile/adapter 分层和 Python 标准库优先原则。

## 当前结论

- 文档中文优先。
- 不绑定任何单一 AI 平台、CLI、IDE 插件、模型供应商或运行时。
- Python 永远优先。
- Python 标准库优先，可选依赖增强。
- 第一版包含完整调度器雏形。
- 调度器按 profile 读取流程，按 adapter 配置调用 worker 命令。
- adapter 命令必须使用严格 allowlist。
- 第一版达到生产级高可用雏形。
- 第一版内置本地 Python 示例 worker，用于端到端演示和自测。
- 第一版完整实现四个 profile。
- 第一版包含标准库测试和可选增强测试。
- harness 核心工具默认只写 `iSpace/track`、`iSpace/tmp`、`iSpace/reports`。
- Windows、Linux、macOS 都是一等支持目标。

## 范围

第一版应交付一个可以直接使用的 harness 工程包，包含以下组件：

- 核心规约文档。
- 四个完整 profile。
- JSON Schema。
- 目录和事件模板。
- 成功、失败、阻塞、重试、人工介入示例。
- Python CLI 工具。
- 调度器雏形。
- adapter 规范和示例配置。
- 本地 Python 示例 worker。
- 标准库测试和可选增强测试。
- 自检命令。
- 审计和汇总报告。
- 新项目接入、profile 设计、任务启动、收口、发布前检查清单。

## 非目标

第一版不做以下事项：

- 不绑定具体 AI 平台。
- 不要求安装第三方依赖才能运行核心功能。
- 不默认启用 push、PR、merge、部署或远端写入。
- 不提供 Web UI。
- 不要求 worker 真正调用大模型。
- 不让 harness 核心工具直接修改业务项目文件。
- 不把 demo worker 当作真实业务实现。

## 目标目录结构

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
│  └─ design/
│     └─ harness-engineering-spec.md
├─ profiles/
│  ├─ default-development/
│  ├─ documentation/
│  ├─ data-analysis/
│  └─ ops-change/
├─ adapters/
│  ├─ README.md
│  ├─ manual/
│  ├─ local-python-workers/
│  ├─ cli-worker/
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
│  ├─ test_cli.py
│  ├─ test_paths.py
│  ├─ test_atomic.py
│  ├─ test_locks.py
│  ├─ test_schema.py
│  ├─ test_state_machine.py
│  ├─ test_adapter_allowlist.py
│  └─ test_demo_flow.py
├─ checklists/
│  ├─ adoption-checklist.md
│  ├─ task-start-checklist.md
│  ├─ profile-design-checklist.md
│  ├─ closeout-checklist.md
│  └─ release-readiness-checklist.md
├─ track/
│  └─ README.md
├─ tmp/
└─ reports/
```

## 核心模型

Harness 由四层组成：

1. 规约层：定义角色、状态机、事件协议、权限和错误处理。
2. 记录层：用 `track/` 记录 run、task、attempt、event、result、closeout 和 timeline。
3. 执行层：Python 调度器读取 profile 和 adapter，按规则调用 worker。
4. 审计层：校验 schema、状态转移、路径、权限、回执、敏感信息和完整性。

核心工具只管理 harness 自身状态，不直接修改业务项目。业务动作由 worker 执行，worker 的工作区必须由 adapter 显式声明。

## Profile

第一版完整实现四个 profile。

### default-development

适用于代码开发任务。

默认流程：

```text
pm -> builder -> tm -> coder -> tester -> opser -> tm -> pm
```

核心职责：

- `pm`: 澄清需求，确认范围和验收标准。
- `builder`: 拆解任务和依赖。
- `tm`: 串行编排单个任务。
- `coder`: 在受控 workspace 内实现。
- `tester`: 验证当前任务。
- `opser`: 在验证通过后执行收口动作。

### documentation

适用于文档写作和文档重构任务。

默认流程：

```text
pm -> planner -> writer -> reviewer -> publisher
```

核心职责：

- `planner`: 拆解文档结构和读者目标。
- `writer`: 生成或修改文档内容。
- `reviewer`: 检查一致性、完整性、可读性和事实风险。
- `publisher`: 归档文档、生成报告或准备发布说明。

### data-analysis

适用于数据分析、报表和结论生成任务。

默认流程：

```text
pm -> analyst -> verifier -> reporter
```

核心职责：

- `analyst`: 读取数据和生成分析结果。
- `verifier`: 校验数据来源、计算逻辑和异常值。
- `reporter`: 输出结构化报告和证据引用。

### ops-change

适用于运维变更、配置变更和发布前检查任务。

默认流程：

```text
pm -> planner -> executor -> validator -> releaser
```

核心职责：

- `planner`: 设计变更步骤、回滚方案和风险控制。
- `executor`: 在授权 workspace 或环境内执行变更。
- `validator`: 验证变更结果和健康状态。
- `releaser`: 准备发布、归档和人工审批材料。

## 调度器

调度器使用 Python 实现，入口为：

```text
iSpace/tools/harness.py
```

第一版命令：

```powershell
python iSpace/tools/harness.py init
python iSpace/tools/harness.py demo
python iSpace/tools/harness.py new-run --title "login api" --profile default-development
python iSpace/tools/harness.py new-task --run 0001 --name "login-api"
python iSpace/tools/harness.py dispatch --run 0001 --task 001_login-api --role coder
python iSpace/tools/harness.py run-task --run 0001 --task 001_login-api
python iSpace/tools/harness.py validate --run 0001
python iSpace/tools/harness.py audit --run 0001
python iSpace/tools/harness.py summarize --run 0001
python iSpace/tools/harness.py selftest
```

调度器模块：

```text
tools/harness_lib/
├─ cli.py
├─ paths.py
├─ locks.py
├─ atomic.py
├─ jsonio.py
├─ schema.py
├─ profile.py
├─ adapter.py
├─ state_machine.py
├─ track.py
├─ dispatcher.py
├─ retry.py
├─ audit.py
├─ summarize.py
└─ redact.py
```

## Adapter

Adapter 是 harness 规约和具体执行环境之间的转换层。它负责声明 worker 命令、输入输出文件、工作区、超时、权限和 allowlist。

Adapter 配置示例：

```json
{
  "adapter_id": "local-python-workers",
  "version": "1.0.0",
  "allowlist": [
    ["python", "iSpace/workers/default-development/coder_worker.py"],
    ["python", "iSpace/workers/default-development/tester_worker.py"],
    ["python", "iSpace/workers/default-development/opser_worker.py"]
  ],
  "roles": {
    "coder": {
      "command": ["python", "iSpace/workers/default-development/coder_worker.py"],
      "input_file": "{attempt_dir}/input.json",
      "output_file": "{attempt_dir}/result.json",
      "timeout_seconds": 60,
      "workspace": "{harness_root}/tmp/workspaces/{run_id}/{task_id}/coder"
    }
  }
}
```

调度器必须先校验 command 是否完整匹配 allowlist。未匹配的命令默认拒绝执行。

## 安全边界

第一版安全边界：

- 严格 allowlist。
- 不使用 shell 拼接命令。
- 使用 `subprocess.run([...])` 参数数组。
- 默认拒绝破坏性命令。
- 远端写入、push、PR、merge、部署默认禁用。
- 路径必须通过 `pathlib.Path` 解析和规范化。
- 核心工具默认只写 `iSpace/track`、`iSpace/tmp`、`iSpace/reports`。
- 业务文件修改只能由 worker 在 adapter 声明的 workspace 内完成。
- 写入 JSON 和 JSONL 使用原子写入。
- 并发运行使用锁文件保护。
- 校验失败必须 fail closed，并写入 `blocked`。
- 审计命令必须检查敏感信息、原始噪声、缺失回执和越权风险。

## 高可用能力

第一版生产级高可用雏形必须包含：

- 超时控制。
- 重试策略。
- 失败记录。
- 阻塞记录。
- 人工介入状态。
- 状态机 fail closed。
- 断点恢复。
- 幂等创建。
- 防重复事件。
- 审计报告。
- 锁文件。
- 防并发写冲突。
- 原子写入。
- 敏感信息扫描。
- 权限分级。
- 跨平台路径校验。
- adapter 命令 allowlist。
- 外部发布动作默认禁用。

## Schema

第一版 schema 至少覆盖：

- `run.schema.json`
- `task.schema.json`
- `handoff.schema.json`
- `progress-event.schema.json`
- `result.schema.json`
- `closeout.schema.json`
- `profile.schema.json`
- `adapter.schema.json`

无第三方依赖时，工具实现常用子集校验：

- 必填字段。
- 字段类型。
- 枚举值。
- 简单数组和对象。
- 基础路径字段。

安装可选依赖 `jsonschema` 后，启用完整 JSON Schema 校验。

## 测试

测试策略：

- 标准库测试必须可运行。
- 可选增强测试在依赖存在时运行，不存在时跳过。
- `selftest` 是用户接入后的总自检命令。

基础测试命令：

```powershell
python -m unittest discover iSpace/tests
```

自检命令：

```powershell
python iSpace/tools/harness.py selftest
```

测试覆盖：

- CLI 参数。
- 路径安全。
- 原子写入。
- 锁文件。
- JSON/JSONL。
- 状态机。
- adapter allowlist。
- schema 子集。
- demo 链路。
- 审计和汇总。
- Windows/POSIX 路径样例。

## Demo

第一版必须支持本地 demo：

```powershell
python iSpace/tools/harness.py demo
python iSpace/tools/harness.py validate --run 0001
python iSpace/tools/harness.py audit --run 0001
python iSpace/tools/harness.py summarize --run 0001
```

demo 应做到：

- 自动创建 demo run。
- 使用 `default-development` profile。
- 调用本地 Python 示例 worker。
- 完成 `coder -> tester -> opser` 链路。
- 写入完整 track。
- 生成 result、closeout 和 summary report。
- 不依赖任何外部 AI 平台。

## 跨平台要求

- Windows、Linux、macOS 都是一等支持目标。
- 路径统一通过 `pathlib.Path`。
- 示例命令同时说明 PowerShell 和 Bash 写法。
- 不硬编码平台专属命令。
- worker 示例只用 Python 标准库。
- 测试覆盖 Windows 风格路径和 POSIX 风格路径。
- 锁文件和原子写入必须跨平台可用。

## 验收标准

第一版完成时必须满足：

- `iSpace/README.md` 能在 10 分钟内引导新用户理解并运行 demo。
- `python iSpace/tools/harness.py demo` 可无第三方依赖跑通。
- `python iSpace/tools/harness.py selftest` 可无第三方依赖通过基础测试。
- 四个 profile 都有完整定义、adapter、worker、示例和说明。
- schema 覆盖核心文件类型。
- validate 能发现必填字段缺失、非法状态跳转、重复事件、无效 `reply_to`。
- audit 能发现敏感信息、缺失回执、越权路径、未闭环任务。
- summarize 能生成面向用户的 run 摘要报告。
- 所有工具默认只写 `track/tmp/reports`。
- 未在 allowlist 的 worker 命令不能执行。
- 文档说明每个工具的使用时机、输入、输出和失败处理。
- 不残留任何具体平台绑定。

## 风险

- 四个完整 profile 会显著扩大第一版范围，需要分阶段实现。
- 标准库-only 的 schema 校验不会等同完整 JSON Schema。
- 调度器雏形不能替代成熟工作流引擎。
- 示例 worker 只能证明 harness 链路，不能代表真实 AI 执行质量。
- allowlist 需要严格匹配命令数组，否则容易被参数注入绕过。
- 跨平台锁和原子写入需要测试覆盖，否则容易出现边界问题。

## 建议实施顺序

1. 建立目标目录结构和核心 README。
2. 编写 schema 和模板。
3. 实现 Python 基础库：路径、原子写入、JSON/JSONL、锁。
4. 实现 run/task/event 管理。
5. 实现 profile 和 adapter 读取。
6. 实现 allowlist 和 dispatch。
7. 实现 state machine、validate、audit、summarize。
8. 实现 demo worker 和 demo 命令。
9. 补齐四个 profile。
10. 补齐示例运行记录。
11. 补齐 unittest 和 selftest。
12. 整理工具使用文档、checklist 和发布前验收清单。
