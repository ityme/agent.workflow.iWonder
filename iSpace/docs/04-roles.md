# 角色

本文说明默认角色模型和扩展方式。

## 默认开发 Profile 角色

- `pm`: 澄清需求、确认范围和验收标准。
- `builder`: 拆解任务、依赖和验收标准。
- `tm`: 串行编排单个任务。
- `coder`: 执行实现。
- `tester`: 验证当前任务。
- `opser`: 执行收口动作。

## 文档 Profile 角色

- `planner`: 设计文档结构。
- `writer`: 编写或修改文档。
- `reviewer`: 审查一致性、完整性和可读性。
- `publisher`: 归档、导出或准备发布材料。

## 数据分析 Profile 角色

- `analyst`: 执行分析。
- `verifier`: 校验数据和计算逻辑。
- `reporter`: 输出报告和证据引用。

## 运维变更 Profile 角色

- `planner`: 设计变更和回滚方案。
- `executor`: 执行变更。
- `validator`: 验证变更结果。
- `releaser`: 准备发布和审批材料。

## 角色边界

任何父级角色不得代替子级执行任务。父级只能下发、接收、确认、重试、阻塞或升级人工介入。
