# 核心概念

本文定义 harness 中的核心名词。

## Harness

Harness 是一套约束和工具组合，用来组织 AI Agent 或人工 worker 的协作过程。它负责定义流程、记录事实、校验状态和生成审计结果。

## Profile

Profile 是某类任务场景的流程定义。例如：

- `default-development`
- `documentation`
- `data-analysis`
- `ops-change`

profile 定义角色、执行顺序、状态转移、重试策略和收口策略。

## Adapter

Adapter 是 harness 和具体执行环境之间的转换层。它声明 worker 命令、输入输出文件、workspace、超时和 allowlist。

## Worker

Worker 是执行单个角色任务的进程、脚本、人工代理或 AI Agent。Harness 不要求 worker 来自特定平台。

## Track

Track 是运行记录目录。它保存 run、task、attempt、event、result、closeout 和 timeline。

## Event

Event 是一次可审计事件。它必须包含 `event_id`、`reply_to`、`correlation_id`、`state` 等字段。

## Closeout

Closeout 是任务收口动作。代码开发场景中可以是本地 commit；文档或数据场景中可以是报告导出、归档或审批材料。
