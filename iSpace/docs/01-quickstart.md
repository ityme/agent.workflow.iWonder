# 快速开始

本文说明如何在新项目中接入并验证 harness。

## 前置条件

- 已安装 Python 3。
- 当前目录是一个可写工作区。
- 不需要安装第三方依赖即可运行基础能力。

## 推荐流程

```powershell
python iSpace/tools/harness.py init
python iSpace/tools/harness.py demo
python iSpace/tools/harness.py validate --run 0001
python iSpace/tools/harness.py audit --run 0001
python iSpace/tools/harness.py summarize --run 0001
```

在工具实现前，以上命令是目标用法。当前阶段先建立文档骨架，后续阶段会逐步补齐工具。

## 运行结果

完整实现后，快速开始流程应生成：

- `iSpace/track/<run_id>` 下的运行记录。
- `iSpace/reports` 下的汇总报告。
- 可通过 validate 和 audit 的结构化事件。

## 失败处理

- 如果命令不存在，说明工具阶段尚未实现。
- 如果 validate 失败，优先查看 schema 错误和状态机错误。
- 如果 audit 失败，优先查看敏感信息、缺失回执和越权路径。

## 下一步

阅读 `02-concepts.md` 理解核心概念。
