# 发布就绪检查清单

用于提交、发布或交付 harness 包前。

- [ ] `python -m unittest discover iSpace/tests` 通过。
- [ ] `python iSpace/tools/harness.py validate --run 0001` 通过。
- [ ] `python iSpace/tools/harness.py audit --run 0001` 通过。
- [ ] `python iSpace/tools/harness.py summarize --run 0001` 能生成报告。
- [ ] 文档中没有具体平台绑定残留。
- [ ] track 示例中没有本机绝对路径。
- [ ] adapter allowlist 能拒绝未声明命令。
- [ ] 核心工具只写 `track/tmp/reports`。
- [ ] 临时目录和缓存不会进入提交。
- [ ] README 已链接示例和清单。
