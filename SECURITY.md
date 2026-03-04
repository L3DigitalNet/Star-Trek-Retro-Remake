# Security Policy

## Supported Versions

Security fixes apply to the latest release only. Older versions are not patched — please update to the latest release.

| Version | Supported |
|---------|-----------|
| Latest  | ✅        |
| Older   | ❌        |

## Reporting a Vulnerability

**Please do not report security vulnerabilities via public GitHub issues.**

Use GitHub's private vulnerability reporting:

1. Go to the [Security tab](https://github.com/L3DigitalNet/Star-Trek-Retro-Remake/security)
2. Click **"Report a vulnerability"**
3. Fill in the details

You can expect:

- **Acknowledgement** within 48 hours
- **Status update** within 7 days
- A fix or public advisory as soon as reasonably possible, depending on severity

## Scope

This is a Python game application (Pygame-CE + PySide6). Relevant security concerns include:

- Exploits in save file loading or configuration file parsing
- Path traversal vulnerabilities in file I/O
- Dependency vulnerabilities in game libraries

## Out of Scope

- Vulnerabilities in Python, Pygame-CE, or PySide6 themselves (report to those projects directly)
- Game balance issues or exploits that do not affect system security
