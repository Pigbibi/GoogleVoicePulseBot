import smtplib
import os
import random
from email.mime.text import MIMEText
from datetime import datetime

SMTP_TIMEOUT_SECONDS = 30


def send_mail() -> int:
    username = os.environ.get('GMAIL_USER')
    password = os.environ.get('GMAIL_PASSWORD')
    receiver = os.environ.get('GV_GATEWAY')

    if not all([username, password, receiver]):
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
    msg['From'] = username
    msg['To'] = receiver

    try:
        with smtplib.SMTP_SSL(
            'smtp.gmail.com', 465, timeout=SMTP_TIMEOUT_SECONDS
        ) as server:
            server.login(username, password)
            server.sendmail(username, [receiver], msg.as_string())
        print("SMTP submission accepted; gateway delivery is not confirmed.")
        return 0
    except Exception:
        print("Failed to submit email: SMTP operation failed.")
        return 1

if __name__ == "__main__":
    raise SystemExit(send_mail())
