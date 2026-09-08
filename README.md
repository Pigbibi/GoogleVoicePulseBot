# GoogleVoicePulseBot

[简体中文](README_CN.md)

Send a periodic email through Gmail SMTP to a configured Google Voice SMS gateway address. Run it manually or with the included monthly GitHub Actions schedule.

SMTP acceptance is the only delivery result this script can verify. It does not prove SMS delivery or guarantee that a Google Voice number stays active.

## Quick start

1. Create a private copy of this repository for your deployment.
2. Add the following **Actions secrets** under **Settings → Secrets and variables → Actions**.
3. Enable Actions and run **Google Voice Keep Alive & Auto Log**.
4. Check both the send step and the destination account.

| Secret | Value |
| --- | --- |
| `GMAIL_USER` | Sender's Gmail address |
| `GMAIL_PASSWORD` | Gmail App Password |
| `GV_GATEWAY` | Destination ending in `@txt.voice.google.com` |

Use a dedicated Gmail App Password with two-step verification enabled. Keep credentials and destination addresses out of the repository and logs.

## Schedule and results

The [workflow](.github/workflows/main.yml) runs at 00:00 UTC on the first day of each month. Edit its cron expression to change the schedule. Scheduled runs may be delayed.

Runs are serialized and limited to 15 minutes; SMTP has a 30-second timeout. A send error fails the run. The workflow writes a timestamped record to `keepalive.log` on the `logs` branch, which requires `contents: write` permission. This record is not a delivery receipt.

## Local use and development

Python's standard library is sufficient. Supply the three settings through your trusted environment or secret manager, then run:

```bash
python main.py
```

This sends a real message. To run the isolated unit tests instead:

```bash
python -m unittest discover -s tests
```

If SMTP authentication fails, check the account and App Password. If SMTP accepts the message but the destination does not receive it, check the gateway and account directly rather than repeatedly resending.

## Support and contributing

[Support](SUPPORT.md) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Code of conduct](CODE_OF_CONDUCT.md)

## License

[MIT](LICENSE).
