# 快速开始

本文说明如何在新项目中接入并验证 harness。

## 前置条件

- 已安装 Python 3。
- 当前目录是一个可写工作区。
- 不需要安装第三方依赖即可运行基础能力。

## 推荐流程

```powershell
python iSpace/tools/harness.py demo
python iSpace/tools/harness.py validate --run 0001
python iSpace/tools/harness.py audit --run 0001
python iSpace/tools/harness.py summarize --run 0001
```

Bash 写法相同：

```bash
python iSpace/tools/harness.py demo
python iSpace/tools/harness.py validate --run 0001
python iSpace/tools/harness.py audit --run 0001
python iSpace/tools/harness.py summarize --run 0001
```

也可以直接运行总自检：

```powershell
python iSpace/tools/harness.py selftest
```

## 运行结果

快速开始流程会生成：

- `iSpace/track` 下的运行记录。
- `iSpace/reports` 下的汇总报告。
- 可通过 validate 和 audit 的结构化事件。

## 失败处理

- 如果 validate 失败，优先查看 schema 错误和状态机错误。
- 如果 audit 失败，优先查看敏感信息、缺失回执和越权路径。
- 如果 demo 失败，优先查看对应角色的 `result.json`。

## 下一步

阅读 `02-concepts.md` 理解核心概念。
