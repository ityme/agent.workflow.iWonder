# 工具

本文说明 Python CLI 工具的目标命令和使用时机。

## 工具入口

```powershell
python iSpace/tools/harness.py <command>
```

## 命令

- `init`: 初始化 harness 目录。
- `demo`: 运行本地示例链路。
- `new-run`: 创建 run。
- `new-task`: 创建 task。
- `dispatch`: 调度单个角色。
- `run-task`: 按 profile 执行任务。
- `validate`: 校验 schema、状态和引用。
- `audit`: 审计敏感信息、越权路径和缺失回执。
- `summarize`: 生成报告。
- `selftest`: 运行自检。

## 使用时机

- 新项目接入后先运行 `init`。
- 开始任务前运行 `new-run` 和 `new-task`。
- 调试单角色时运行 `dispatch`。
- 执行完整任务时运行 `run-task`。
- 提交前运行 `validate`、`audit`、`summarize`。
- 发布前运行 `selftest`。

## 依赖策略

无第三方依赖时必须可运行基础能力。安装 `jsonschema` 后增强 schema 校验。
