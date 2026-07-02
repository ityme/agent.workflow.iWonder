# 总览

本文说明 iWonder Agent Harness 的目标、边界和组成。

## 定位

iWonder Agent Harness 是一个平台无关的 AI Agent 协作工程包。它定义多角色任务流、状态机、事件协议、权限边界、运行记录、调度器接口和审计规则。

第一版目标不是绑定某个 AI 平台，而是提供一套可复制、可校验、可审计、可扩展的 harness 工程基础。

## 组成

- 规约文档：说明角色、流程、状态和安全边界。
- profile：定义不同任务场景的角色和流程。
- adapter：把通用 harness 规则映射到具体 worker 命令。
- schema：定义结构化文件格式。
- templates：提供可复制的初始文件。
- examples：展示成功、失败、阻塞、重试和人工介入。
- tools：提供 Python CLI、调度、校验、审计和汇总能力。
- tests：保证核心工具和示例链路可用。
- track：记录每次运行的事件、结果和证据。

## 第一版原则

- 中文文档优先。
- Python 优先。
- 标准库优先，可选依赖增强。
- 严格 allowlist。
- 默认不写业务项目文件。
- 外部发布动作默认禁用。
- Windows、Linux、macOS 都是一等支持目标。

## 阅读顺序

1. `01-quickstart.md`
2. `02-concepts.md`
3. `03-architecture.md`
4. `05-workflow.md`
5. `07-event-protocol.md`
6. `11-tools.md`
7. `12-adapters.md`
8. `14-security.md`
