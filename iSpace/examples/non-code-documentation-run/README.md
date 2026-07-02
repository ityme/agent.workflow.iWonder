# 非代码文档运行

本示例对应 `documentation` profile，用于文档写作、规约维护和内容重构。

建议命令：

```powershell
python iSpace/tools/harness.py new-run --title "文档优化" --profile documentation
python iSpace/tools/harness.py new-task --run 0002 --name "优化快速开始" --acceptance "读者能在 10 分钟内跑通 demo。"
python iSpace/tools/harness.py run-task --run 0002 --task 001_task --profile documentation
```

预期角色链路：

- `planner`: 规划结构。
- `writer`: 编写正文。
- `reviewer`: 检查一致性和可读性。
- `publisher`: 归档或准备发布材料。

非代码语义：

- 收口动作通常是 `archive_artifact`，不是本地 commit。
- 验收标准应关注读者目标、完整性、可维护性和事实风险。
- 不应把文档任务强行套用代码开发的 `coder/tester/opser` 名称。
