# Security policy

Security fixes target the latest release and `main` branch.

## Reporting

Do not open a public issue containing Gmail credentials, App Passwords, gateway
addresses, private workflow logs, or exploit details. Use GitHub's
[private vulnerability reporting](https://github.com/Pigbibi/GoogleVoicePulseBot/security/advisories/new).
If that form is unavailable, ask for a private contact through information
published on the repository owner's GitHub profile without sharing technical
details publicly.

Include the affected commit, reproduction steps, required attacker access,
impact, and suggested mitigation in the private report.

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
