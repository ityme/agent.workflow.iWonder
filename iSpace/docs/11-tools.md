# 工具

本文说明 Python CLI 工具的命令和使用时机。详细参数见 `iSpace/tools/README.md`。

## 工具入口

```powershell
python iSpace/tools/harness.py <command>
```

## 命令

- `demo`: 运行本地示例链路。
- `new-run`: 创建 run。
- `new-task`: 创建 task。
- `run-task`: 按 profile 执行任务。
- `validate`: 校验 schema、状态和引用。
- `audit`: 审计敏感信息、越权路径和缺失回执。
- `summarize`: 生成报告。
- `selftest`: 运行自检。

## 使用时机

- 新项目接入后先运行 `selftest`。
- 开始任务前运行 `new-run` 和 `new-task`。
- 执行完整任务时运行 `run-task`。
- 提交前运行 `validate`、`audit`、`summarize`。
- 发布前运行 `selftest`。

## 常用命令

```powershell
python iSpace/tools/harness.py selftest
python iSpace/tools/harness.py demo
python iSpace/tools/harness.py validate --run 0001
python iSpace/tools/harness.py audit --run 0001
python iSpace/tools/harness.py summarize --run 0001
```

Bash 写法相同，只需保持路径分隔符适配当前 shell。

## 依赖策略

无第三方依赖时必须可运行基础能力。安装 `jsonschema` 后增强 schema 校验。
