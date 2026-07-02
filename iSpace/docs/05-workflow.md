# 工作流

本文说明任务从需求到收口的生命周期。

## 标准生命周期

```text
intake -> clarify -> plan -> dispatch -> verify -> closeout -> summarize
```

## 需求确认

进入拆解前必须确认：

- 范围清晰。
- 变更点清晰。
- 验收标准可验证。
- 非目标明确。
- 未决问题为空。
- 用户明确确认或授权继续。

## 任务拆解

builder 根据已确认需求生成任务、依赖和验收标准。

## 调度执行

tm 或对应协调角色按 profile 顺序调度 worker。调度器必须检查 adapter allowlist。

## 验证

验证角色必须输出结构化结果。失败时不得直接进入收口。

## 收口

收口策略由 profile 定义。外部发布动作默认禁用。

## 汇总

summarize 命令应根据 track 生成用户可读报告。
