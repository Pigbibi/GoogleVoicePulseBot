# Security policy

Security fixes target the latest release and `main` branch.

## Reporting a vulnerability

Report security vulnerabilities through [GitHub private vulnerability reporting](https://github.com/Pigbibi/GoogleVoicePulseBot/security/advisories/new). Do not post exploit details, credentials, private sessions or personal data in public issues or PRs. Include the affected version, impact and minimal redacted reproduction. The maintainer handles reports on a best-effort basis; no bounty or response-time guarantee is implied.

## Relevant issues

- exposure of GitHub Actions secrets;
- untrusted workflow changes that can exfiltrate credentials;
- command or header injection through environment variables;
- accidental secret disclosure in logs;
- unsafe repository permissions.

Issues in Gmail, Google Voice, or GitHub Actions themselves should be reported
to the corresponding provider unless this repository's integration creates the
exposure.

If a secret may be compromised, revoke it immediately. Do not wait for a code
change or maintainer response.
