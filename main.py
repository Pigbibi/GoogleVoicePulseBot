import smtplib
import os
import random
from collections import namedtuple
from email.mime.text import MIMEText
from datetime import datetime

SMTP_TIMEOUT_SECONDS = 30

# The deployment supplies these names through repository secrets; a role is
# added here and nowhere else.
SETTINGS_ENV = {
    'username': 'GMAIL_USER',
    'password': 'GMAIL_PASSWORD',
    'receiver': 'GV_GATEWAY',
}
Settings = namedtuple('Settings', tuple(SETTINGS_ENV))


def load_settings() -> Settings | None:
    values = {name: os.environ.get(variable) for name, variable in SETTINGS_ENV.items()}
    if not all(values.values()):
        return None
    return Settings(**values)


def send_mail() -> int:
    settings = load_settings()
    if settings is None:
        print("Error: Missing secrets. Please check your configuration.")
        return 1

    msgs = [
        "Update: System is running smoothly.",
        "Reminder: Keep active and stay connected.",
        "Monthly check-in: Hello world!",
        "Status: All systems go."
    ]
    content = f"{random.choice(msgs)} | Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    msg = MIMEText(content)
    msg['Subject'] = 'GV Maintenance'
    msg['From'] = settings.username
    msg['To'] = settings.receiver

    try:
        with smtplib.SMTP_SSL(
            'smtp.gmail.com', 465, timeout=SMTP_TIMEOUT_SECONDS
        ) as server:
            server.login(settings.username, settings.password)
            server.sendmail(settings.username, [settings.receiver], msg.as_string())
        print("SMTP submission accepted; gateway delivery is not confirmed.")
        return 0
    except Exception:
        print("Failed to submit email: SMTP operation failed.")
        return 1

if __name__ == "__main__":
    raise SystemExit(send_mail())
