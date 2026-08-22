# Contributing

Focused bug fixes, documentation improvements, and security hardening are
welcome.

## Development

The application is one Python script with no third-party runtime dependency.
Check syntax without sending a message:

```bash
python -m py_compile main.py
```

Do not run `main.py` during validation unless you intend to send a real message
to a test gateway.

## Pull requests

- Work from the latest `main` on a separate branch.
- Keep one pull request focused on one problem.
- Preserve the `GMAIL_USER`, `GMAIL_PASSWORD`, and `GV_GATEWAY` interface unless
  the change explicitly updates configuration and documentation.
- Add testable validation where possible without contacting real accounts.
- Keep the English and Simplified Chinese README aligned.
- Use placeholders in examples; never include real credentials or gateway
  addresses.
- Explain workflow permission or schedule changes in the pull request.

Use [SECURITY.md](SECURITY.md) for vulnerabilities and follow the
[Code of Conduct](CODE_OF_CONDUCT.md).

Contributions are licensed under the repository's [MIT License](LICENSE).
