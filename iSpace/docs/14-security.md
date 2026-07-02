# 安全

本文说明 harness 的安全约束。

## 命令安全

- 使用参数数组调用命令。
- 禁止 shell 拼接。
- command 必须在 adapter allowlist 中完整匹配。
- 未声明命令默认拒绝。

## 路径安全

- 使用 `pathlib.Path`。
- 核心工具只写 `iSpace/track`、`iSpace/tmp`、`iSpace/reports`。
- worker 只能写 adapter 声明的 workspace。
- 路径越界必须阻塞。

## 数据安全

audit 应检查：

- token。
- 密钥。
- 凭据。
- 大段原始日志。
- 隐藏指令。
- 未脱敏环境信息。

## 发布安全

以下动作默认禁用：

- push。
- PR。
- merge。
- 部署。
- 远端写入。

启用这些动作必须有明确 profile 配置和用户确认依据。
