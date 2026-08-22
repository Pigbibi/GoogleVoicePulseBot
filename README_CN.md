# GoogleVoicePulseBot

[English](README.md)

[![Workflow](https://github.com/Pigbibi/GoogleVoicePulseBot/actions/workflows/main.yml/badge.svg)](https://github.com/Pigbibi/GoogleVoicePulseBot/actions/workflows/main.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

使用 Gmail SMTP 定期向 Google Voice 短信网关地址发送一条消息。项目通过 GitHub
Actions 每月运行，也支持手动触发。

## 重要说明

本项目只能按配置发送邮件，无法保证 Google Voice 会接受、投递该消息，也无法保证
号码一定保持活跃。网关行为、账号状态和 Google Voice 政策都可能变化。请定期检查
GitHub Actions 输出和实际号码状态，并遵守 Google 的服务条款。

## 工作流程

```text
GitHub Actions 定时任务
        │
        ▼
Python 脚本登录 Gmail SMTP
        │
        ▼
向配置的 @txt.voice.google.com 地址发送消息
```

workflow 默认在每月 1 日 `00:00 UTC` 运行。每次运行还会在 `logs` 分支追加一条
`keepalive.log` 记录，用来保持独立的执行记录。

该日志不是短信投递回执。是否发送成功应以 Actions 中 Python 步骤的输出和实际账号
状态为准。

## 配置

需要以下 GitHub Actions secrets：

| Secret | 用途 |
| --- | --- |
| `GMAIL_USER` | 用于发送消息的完整 Gmail 地址 |
| `GMAIL_PASSWORD` | Gmail App Password，不是普通登录密码 |
| `GV_GATEWAY` | 目标 `@txt.voice.google.com` 地址 |

建议为 Gmail 启用两步验证，并创建只供此 workflow 使用的 App Password。

## 部署

1. 审查源码后，把它复制到一个新的私有仓库。
2. 在该私有部署仓库中启用 workflow。
3. 在 **Settings → Secrets and variables → Actions** 添加三个 secrets。
4. 确认 Actions 的 `GITHUB_TOKEN` 可以写入仓库内容，以便更新 `logs` 分支。
5. 打开 **Actions → Google Voice Keep Alive & Auto Log**，手动运行一次。
6. 检查 Python 步骤输出，并确认账号侧实际收到或处理了消息。

修改 `.github/workflows/main.yml` 中的 cron 可以调整运行时间。GitHub Actions cron
使用 UTC，且定时任务可能延迟执行。

## 本地运行

Python 脚本只使用标准库：

```bash
GMAIL_USER='name@gmail.com' \
GMAIL_PASSWORD='app-password' \
GV_GATEWAY='recipient@txt.voice.google.com' \
python main.py
```

该命令会真实发送消息。不要在不确定配置时运行。

## 安全

- 不要把 Gmail 密码、App Password 或网关地址提交到仓库。
- 不要在 issue、截图或 Actions 日志中粘贴 secret。
- Fork 后检查 workflow 内容，再向它提供凭据。
- 怀疑凭据泄露时，立即撤销 App Password 并创建新密码。
- 公共仓库中的 Actions 日志默认对所有人可见。

安全问题请按 [SECURITY.md](SECURITY.md) 报告。

## 贡献与支持

提交改动前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。使用问题和 bug 报告渠道见
[SUPPORT.md](SUPPORT.md)。参与社区时请遵守
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

## 许可证

本项目使用 [MIT License](LICENSE)。
