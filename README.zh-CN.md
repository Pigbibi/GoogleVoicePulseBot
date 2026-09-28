# GoogleVoicePulseBot

[English](README.md)

通过 Gmail SMTP，定期向指定的 Google Voice 短信网关地址发送邮件。支持手动运行和 GitHub Actions 每月定时运行。

脚本只能确认 SMTP 是否接受邮件，不能证明短信送达，也不能保证 Google Voice 号码持续保活。

## 快速开始

1. 为个人部署创建本仓库的私有副本。
2. 在 **Settings → Secrets and variables → Actions** 添加下列 secrets。
3. 启用 Actions，运行 **Google Voice Keep Alive & Auto Log**。
4. 检查发送步骤，并到目标账户确认结果。

| Secret | 内容 |
| --- | --- |
| `GMAIL_USER` | 发件 Gmail 地址 |
| `GMAIL_PASSWORD` | Gmail 应用专用密码 |
| `GV_GATEWAY` | 以 `@txt.voice.google.com` 结尾的目标地址 |

为 Gmail 开启两步验证，并使用专门的应用密码。凭据和目标地址不应进入仓库或日志。

## 运行时间与结果

[工作流](.github/workflows/main.yml)默认在每月 1 日 00:00 UTC 运行，可修改 cron 表达式调整时间。定时任务可能延迟启动。

运行互斥，最长 15 分钟；SMTP 连接超时为 30 秒。发送错误会使任务失败。工作流会在 `logs` 分支的 `keepalive.log` 中记录运行时间，因此需要 `contents: write` 权限；这份记录不是送达回执。

## 本地使用与开发

仅需 Python 标准库。通过可信环境或密钥管理器提供三个配置值，再运行：

```bash
python main.py
```

这会真实发送邮件。仅运行隔离单元测试时使用：

```bash
python -m unittest discover -s tests
```

SMTP 认证失败时检查账户和应用密码；SMTP 已接受但目标未收到时，应核对网关和目标账户，不要反复重发。

## 支持与贡献

[问题与支持](SUPPORT.md) · [贡献指南](CONTRIBUTING.md) · [安全问题](SECURITY.md) · [行为准则](CODE_OF_CONDUCT.md)

## 许可证

[MIT](LICENSE)。
