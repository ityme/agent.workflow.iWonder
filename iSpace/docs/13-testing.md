# 测试

本文说明测试策略。

## 基础测试

基础测试必须只依赖 Python 标准库。

```powershell
python -m unittest discover iSpace/tests
```

## 可选增强测试

如果检测到 `jsonschema`，启用完整 schema 校验测试。缺少可选依赖时，应跳过增强测试而不是失败。

## 自检

`selftest` 应运行：

- unittest。
- demo。
- validate。
- audit。
- summarize。

命令：

```powershell
python iSpace/tools/harness.py selftest
```

selftest 使用临时 harness 根目录运行 demo 链路，不会污染仓库内置的 `track` 样例。

## 覆盖范围

- CLI 参数。
- 路径安全。
- 原子写入。
- 锁文件。
- JSON/JSONL。
- 状态机。
- adapter allowlist。
- schema 子集。
- demo 链路。
- 审计和汇总。
