# GoogleVoicePulseBot

[简体中文](README_CN.md)

[![Workflow](https://github.com/Pigbibi/GoogleVoicePulseBot/actions/workflows/main.yml/badge.svg)](https://github.com/Pigbibi/GoogleVoicePulseBot/actions/workflows/main.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Send a periodic message to a configured Google Voice SMS gateway address
through Gmail SMTP. The included GitHub Actions workflow runs monthly and can
also be triggered manually.

## Important limitation

This project can only submit an email to the configured gateway. It cannot
guarantee that Google Voice accepts or delivers the message, or that a number
remains active. Gateway behavior, account state, and Google Voice policy may
change. Check the workflow output and the actual number regularly, and follow
Google's applicable terms.

## How it works

```text
GitHub Actions schedule
        │
        ▼
Python signs in to Gmail SMTP
        │
        ▼
message sent to the configured @txt.voice.google.com address
```

The workflow runs at `00:00 UTC` on the first day of each month. It also appends
a `keepalive.log` entry on the `logs` branch to provide a separate run record.

The log entry is not a delivery receipt. Use the Python step output and the
actual account state to determine whether the operation worked.

## Configuration

Add these GitHub Actions secrets:

| Secret | Purpose |
| --- | --- |
| `GMAIL_USER` | Full Gmail address used to send the message |
| `GMAIL_PASSWORD` | Gmail App Password, not the normal account password |
| `GV_GATEWAY` | Destination address ending in `@txt.voice.google.com` |

Enable two-step verification on the Gmail account and create a dedicated App
Password for this workflow.

## Deploy

1. Create a private repository from a reviewed copy of this source.
2. Enable workflows in that private deployment repository.
3. Add the three secrets under **Settings → Secrets and variables → Actions**.
4. Confirm the workflow's `GITHUB_TOKEN` may write repository contents so it can
   update the `logs` branch.
5. Run **Google Voice Keep Alive & Auto Log** manually once.
6. Inspect the Python step and confirm the result from the account side.

Edit the cron expression in `.github/workflows/main.yml` to change the schedule.
GitHub Actions cron uses UTC and scheduled runs may start later than the exact
configured time.

## Run locally

The script uses only the Python standard library:

```bash
GMAIL_USER='name@gmail.com' \
GMAIL_PASSWORD='app-password' \
GV_GATEWAY='recipient@txt.voice.google.com' \
python main.py
```

This command sends a real message. Do not run it with unverified settings.

## Security

- Never commit Gmail credentials, App Passwords, or gateway addresses.
- Do not paste secrets into issues, screenshots, or workflow logs.
- Review a fork's workflow before providing credentials to it.
- Revoke and replace the App Password immediately after suspected exposure.
- Remember that Actions logs in a public repository are public.

Follow [SECURITY.md](SECURITY.md) for vulnerability reports.

## Contributing and support

Read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a change. See
[SUPPORT.md](SUPPORT.md) for usage questions and bug reports. Participation is
governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

GoogleVoicePulseBot is available under the [MIT License](LICENSE).
