import os
import contextlib
import io
import unittest
from email import message_from_string
from pathlib import Path
from unittest.mock import MagicMock, patch

import main

WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "main.yml"

CONFIGURED = {
    "GMAIL_USER": "synthetic-sender@example.invalid",
    "GMAIL_PASSWORD": "SYNTHETIC_PASSWORD",
    "GV_GATEWAY": "synthetic-destination@example.invalid",
}


class RecordingSMTP:
    """Stands in for smtplib.SMTP_SSL and keeps what one session received."""

    sessions = []

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.login_args = ()
        self.sender = None
        self.recipients = []
        self.message = ""
        RecordingSMTP.sessions.append(self)

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        return False

    def login(self, username, password):
        self.login_args = (username, password)

    def sendmail(self, sender, recipients, message):
        self.sender = sender
        self.recipients = recipients
        self.message = message


class SendMailTests(unittest.TestCase):
    def setUp(self):
        RecordingSMTP.sessions = []
        self.addCleanup(setattr, RecordingSMTP, "sessions", [])

    def run_send(self, environ=None, transport=RecordingSMTP):
        output = io.StringIO()
        with (
            patch.dict(
                os.environ, CONFIGURED if environ is None else environ, clear=True
            ),
            patch("main.smtplib.SMTP_SSL", transport),
            contextlib.redirect_stdout(output),
            contextlib.redirect_stderr(output),
        ):
            return main.send_mail(), output.getvalue()

    def test_submits_one_bounded_session_as_the_configured_sender(self):
        code, _ = self.run_send()

        self.assertEqual(code, 0)
        self.assertEqual(len(RecordingSMTP.sessions), 1)
        session = RecordingSMTP.sessions[0]
        self.assertEqual((session.host, session.port), ("smtp.gmail.com", 465))
        self.assertEqual(session.timeout, 30)
        self.assertEqual(
            session.login_args,
            (CONFIGURED["GMAIL_USER"], CONFIGURED["GMAIL_PASSWORD"]),
        )
        self.assertEqual(session.sender, CONFIGURED["GMAIL_USER"])
        self.assertEqual(session.recipients, [CONFIGURED["GV_GATEWAY"]])

    def test_message_carries_a_canned_line_timestamp_and_configured_addresses(self):
        self.run_send()

        message = message_from_string(RecordingSMTP.sessions[0].message)
        self.assertEqual(message["Subject"], "GV Maintenance")
        self.assertEqual(message["From"], CONFIGURED["GMAIL_USER"])
        self.assertEqual(message["To"], CONFIGURED["GV_GATEWAY"])
        line, separator, timestamp = message.get_payload().partition(" | Time: ")
        self.assertEqual(separator, " | Time: ")
        self.assertIn(line, main.MESSAGE_LINES)
        self.assertRegex(timestamp, r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$")

    def test_any_missing_setting_fails_before_contacting_the_server(self):
        partial = {
            missing: {
                name: value for name, value in CONFIGURED.items() if name != missing
            }
            for missing in CONFIGURED
        }
        for name, environ in {**partial, "nothing": {}}.items():
            with self.subTest(name):
                RecordingSMTP.sessions = []
                code, _ = self.run_send(environ=environ)
                self.assertEqual(code, 1)
                self.assertEqual(RecordingSMTP.sessions, [])

    def test_smtp_failure_fails(self):
        code, _ = self.run_send(
            transport=MagicMock(side_effect=TimeoutError("timed out"))
        )
        self.assertEqual(code, 1)

    def test_output_never_reveals_addresses_credentials_or_provider_detail(self):
        marker = "SYNTHETIC_PROVIDER_PRIVATE_DETAIL"
        scenarios = (
            ("accepted", RecordingSMTP, 0),
            ("rejected", MagicMock(side_effect=RuntimeError(marker)), 1),
        )
        for name, transport, expected in scenarios:
            with self.subTest(name):
                code, output = self.run_send(transport=transport)
                self.assertEqual(code, expected)
                for sensitive in (*CONFIGURED.values(), marker):
                    self.assertNotIn(sensitive, output)

    def test_workflow_exports_every_setting_read_from_the_environment(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        for role, variable in main.SETTINGS_ENV.items():
            with self.subTest(role=role):
                self.assertIn(f"{variable}: ${{{{ secrets.{variable} }}}}", workflow)


if __name__ == "__main__":
    unittest.main()
