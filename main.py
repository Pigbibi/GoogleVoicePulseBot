import smtplib
import os
import random
from email.mime.text import MIMEText
from datetime import datetime

def send_mail():
    username = os.environ.get('GMAIL_USER')
    password = os.environ.get('GMAIL_PASSWORD')
    receiver = os.environ.get('GV_GATEWAY')

    if not all([username, password, receiver]):
        print("Error: Secrets 缺失，请检查配置。")
        return

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
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(username, password)
            server.sendmail(username, [receiver], msg.as_string())
        print(f"[{datetime.now()}] 成功发送至: {receiver}")
    except Exception as e:
        print(f"发送失败: {e}")

if __name__ == "__main__":
    send_mail()
