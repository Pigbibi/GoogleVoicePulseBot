import smtplib
import os
import random
from collections import namedtuple
from email.mime.text import MIMEText
from datetime import datetime

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465
SMTP_TIMEOUT_SECONDS = 30

SUBJECT = 'GV Maintenance'
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M'
MESSAGE_LINES = (
    "Update: System is running smoothly.",
    "Reminder: Keep active and stay connected.",
    "Monthly check-in: Hello world!",
    "Status: All systems go.",
)

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


def compose_message(settings: Settings, line: str) -> MIMEText:
    content = f"{line} | Time: {datetime.now().strftime(TIMESTAMP_FORMAT)}"
    message = MIMEText(content)
    message['Subject'] = SUBJECT
    message['From'] = settings.username
    message['To'] = settings.receiver
    return message


def submit(settings: Settings, message: MIMEText) -> None:
    with smtplib.SMTP_SSL(
        SMTP_HOST, SMTP_PORT, timeout=SMTP_TIMEOUT_SECONDS
    ) as server:
        server.login(settings.username, settings.password)
        server.sendmail(settings.username, [settings.receiver], message.as_string())


def send_mail() -> int:
    settings = load_settings()
    if settings is None:
        print("Error: Missing secrets. Please check your configuration.")
        return 1

    message = compose_message(settings, random.choice(MESSAGE_LINES))

    try:
        submit(settings, message)
        print("SMTP submission accepted; gateway delivery is not confirmed.")
        return 0
    except Exception:
        # SMTP errors quote the recipient and the server response, and this
        # output goes to a published CI log; report the failure without them.
        print("Failed to submit email: SMTP operation failed.")
        return 1

if __name__ == "__main__":
    raise SystemExit(send_mail())
