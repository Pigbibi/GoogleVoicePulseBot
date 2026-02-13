# Account Keeper (Google-Voice-Keep-Alive)

![Python](https://img.shields.io/badge/language-python-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![GitHub Actions](https://img.shields.io/badge/automation-GitHub--Actions-blueviolet.svg)

这个仓库旨在通过自动化脚本（Gmail SMTP）维持 Google Voice 号码的活跃状态，并自动更新日志以防止 GitHub Actions 停用。

## 🛠 功能原理

1. **保号逻辑**：利用 Python 脚本通过 Gmail 的邮件转短信网关发送信息，每月触发一次主动发出行为。
2. **保活逻辑**：脚本执行完成后会自动向 `keepalive.log` 提交记录，确保仓库保持活跃，避免 GitHub Actions 60 天自动关停。

## 🚀 部署指南

### 1. 准备工作
- 获取你的 **Gmail 应用专用密码**（16 位，非登录密码）。
- 向目标号码发送短信，在 Gmail 邮件回复中获取 `txt.voice.google.com` 格式的专属地址。

### 2. 配置 Secrets
在仓库的 `Settings` -> `Secrets and variables` -> `Actions` 中添加以下变量：

| Secret 名称 | 说明 |
| :--- | :--- |
| `GMAIL_USER` | 你的 Gmail 地址 |
| `GMAIL_PASSWORD` | 16 位 Gmail 应用专用密码 |
| `GV_GATEWAY` | 目标映射地址 |

### 3. 运行频率
- 默认设置：**每月 1 号 UTC 00:00** 运行。
- 你可以在 `.github/workflows/keepalive.yml` 中修改 `cron` 表达式。

## 📝 执行记录
最近一次运行详情请查看 [keepalive.log](./keepalive.log)。

