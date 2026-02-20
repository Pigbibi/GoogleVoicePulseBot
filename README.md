# 📡 GV-Pulse: Google Voice Keep-Alive Bot

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![GitHub Actions](https://img.shields.io/badge/Automation-GitHub--Actions-blueviolet)

**GV-Pulse** is an automated utility designed to prevent Google Voice numbers from expiring due to inactivity. It uses the Gmail SMTP service to send periodic text messages via the official Google Voice SMS gateway, simulating active usage with zero maintenance.

## ✨ Features

- **Automated Pulse**: Sends a monthly SMS to maintain your number's active status.
- **Repository Keep-Alive**: Automatically commits to `keepalive.log` after each run to prevent GitHub from disabling the workflow due to repository inactivity.
- **Ultra-Lightweight**: No heavy dependencies; runs entirely on GitHub's free-tier runners.
- **Private & Secure**: Uses GitHub Secrets to protect your sensitive credentials.

## 🏗️ How It Works

1. **Activity Logic**: The Python script sends an email through your Gmail account addressed to a specific Google Voice SMS gateway address (`@txt.voice.google.com`). This is processed by Google as an outgoing SMS from your GV number.
2. **Workflow Retention**: GitHub Actions normally disables scheduled workflows if the repository has no activity for 60 days. This bot bypasses that by updating a log file automatically during every run.

## 🛠️ Setup Instructions

### 1. Prerequisites
- **Gmail App Password**: Generate a 16-character **App Password** from your Google Account security settings (Standard login passwords will not work).
- **Target Gateway Address**: Send a text message from any mobile number to your Google Voice number. Reply to that message via Gmail and look for the recipient address ending in `@txt.voice.google.com`.

### 2. Configure GitHub Secrets
Go to your repository `Settings > Secrets and variables > Actions` and add the following:

| Secret Name | Description |
| :--- | :--- |
| `GMAIL_USER` | Your full Gmail address |
| `GMAIL_PASSWORD` | The 16-character Gmail App Password |
| `GV_GATEWAY` | The target `@txt.voice.google.com` address |

### 3. Workflow Schedule
- **Default Frequency**: Runs at **00:00 UTC on the 1st of every month**.
- To change the timing, modify the `cron` expression in `.github/workflows/keepalive.yml`.

## 📝 Execution Logs
Check the [keepalive.log](./keepalive.log) file for a history of successful operations.

## 📜 Disclaimer
This project is for personal use only. Use it responsibly and in accordance with Google's Terms of Service.

## ⚖️ License
Distributed under the MIT License.
