import os
import contextlib
import io
import unittest
from unittest.mock import MagicMock, patch

import main


class SendMailTests(unittest.TestCase):
    def test_logs_never_include_destination_or_provider_detail(self):
        values = {
            "GMAIL_USER": "synthetic-sender@example.invalid",
            "GMAIL_PASSWORD": "SYNTHETIC_PASSWORD",
            "GV_GATEWAY": "synthetic-destination@example.invalid",
        }
        marker = "SYNTHETIC_PROVIDER_PRIVATE_DETAIL"
        for failure in (None, RuntimeError(marker)):
            with self.subTest(failure=bool(failure)):
                output = io.StringIO()
                with (
                    patch.dict(os.environ, values, clear=True),
                    patch("main.smtplib.SMTP_SSL", side_effect=failure),
                    contextlib.redirect_stdout(output),
                    contextlib.redirect_stderr(output),
                ):
                    self.assertEqual(main.send_mail(), int(failure is not None))
                for sensitive in (*values.values(), marker):
                    self.assertNotIn(sensitive, output.getvalue())

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_configuration_fails(self):
        self.assertEqual(main.send_mail(), 1)

    @patch.dict(
        os.environ,
        {
            "GMAIL_USER": "sender@example.com",
            "GMAIL_PASSWORD": "app-password",
            "GV_GATEWAY": "receiver@example.com",
        },
        clear=True,
    )
    @patch("main.smtplib.SMTP_SSL")
    def test_success_uses_bounded_smtp_connection(self, smtp_ssl):
        server = MagicMock()
        smtp_ssl.return_value.__enter__.return_value = server

        self.assertEqual(main.send_mail(), 0)

        smtp_ssl.assert_called_once_with(
            "smtp.gmail.com", 465, timeout=main.SMTP_TIMEOUT_SECONDS
        )
        server.login.assert_called_once_with("sender@example.com", "app-password")
        self.assertEqual(server.sendmail.call_count, 1)

    @patch.dict(
        os.environ,
        {
            "GMAIL_USER": "sender@example.com",
            "GMAIL_PASSWORD": "app-password",
            "GV_GATEWAY": "receiver@example.com",
        },
        clear=True,
    )
    @patch("main.smtplib.SMTP_SSL", side_effect=TimeoutError("timed out"))
    def test_smtp_failure_fails(self, _smtp_ssl):
        self.assertEqual(main.send_mail(), 1)


if __name__ == "__main__":
    unittest.main()
