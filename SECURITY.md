# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do not** open a public GitHub issue
2. Email the maintainers directly or use GitHub's private vulnerability reporting
3. Include steps to reproduce and any relevant details

We will acknowledge receipt within 48 hours and aim to release a fix within 7 days for critical issues.

## Scope

Uncanny runs entirely locally — no data leaves your machine. The main security considerations are:

- **Input handling**: Uncanny reads files from disk. It does not execute file contents.
- **ML models** (optional): When using `--deep` mode, models are downloaded from Hugging Face. These are standard open-source models (GPT-2).
- **No network calls**: The core tool makes zero network requests during analysis.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |
