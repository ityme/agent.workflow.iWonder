# Harness 工具

入口：

```powershell
python iSpace/tools/harness.py <command>
```

Bash 写法相同：

```bash
python iSpace/tools/harness.py <command>
```

## 命令

### `demo`

使用时机：首次接入或验证本地 worker 链路。

```powershell
python iSpace/tools/harness.py demo
```

输出：创建或复用 `0001` run 和 `001_demo-task`，执行 `coder -> tester -> opser`。

失败处理：如果命令非 0 退出，先查看对应角色的 `result.json`。

### `new-run`

使用时机：开始一次新的任务协作。

```powershell
python iSpace/tools/harness.py new-run --title "login api" --profile default-development
```

输出：`iSpace/track/runs/<run_id>/run.json`。

### `new-task`

使用时机：给 run 增加可执行任务。

```powershell
python iSpace/tools/harness.py new-task --run 0001 --name "login api" --acceptance "接口返回 200。"
```

输出：`iSpace/track/task/<task_id>/task.json`，并更新 run 的 `task_ids`。

### `run-task`

使用时机：按 profile 对单个 task 执行本地 worker 链路。

```powershell
python iSpace/tools/harness.py run-task --run 0001 --task 001_demo-task --profile default-development
```

输出：每个角色的 `result.json`，收口角色额外输出 `closeout.json`。

失败处理：worker 非 0 退出会记录为 `fail`，不会覆盖旧 attempt。

### `validate`

使用时机：提交前、调度后或接入新 profile 后。

```powershell
python iSpace/tools/harness.py validate --run 0001
python iSpace/tools/harness.py validate --profile default-development
```

输出：校验成功打印 `valid`；失败时打印 schema 或结构错误。

### `audit`

使用时机：提交前、汇总前、交付前。

```powershell
python iSpace/tools/harness.py audit --run 0001
```

检查：敏感字符串、本机绝对路径、JSON 格式、缺失 task/result/closeout。

### `summarize`

使用时机：需要给用户或上游角色交付 run 摘要时。

```powershell
python iSpace/tools/harness.py summarize --run 0001
```

输出：`iSpace/reports/run-0001-summary.md`。

### `selftest`

使用时机：接入后总自检、发布前检查。

```powershell
python iSpace/tools/harness.py selftest
```

行为：在临时 harness 根目录中依次运行 unittest、demo、validate、audit、summarize，并打印执行过的命令。

## 可选依赖

核心功能只使用 Python 标准库。安装 `jsonschema` 后，后续版本可以启用完整 JSON Schema 校验；当前基础校验覆盖必填字段、类型、枚举、数组和嵌套对象。
