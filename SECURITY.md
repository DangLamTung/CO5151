# Security Policy & Threat Model v0 — LegalPilot-VN

## 1. Security Scope

LegalPilot-VN assists corporate legal counsel and compliance officers with statutory assessment. Due to the sensitive nature of regulatory filings and corporate data, the system implements **Threat Model v0** (Requirement R6 from the D1 Proposal).

### Ten Threat Vectors Covered:
1. **Zero-width / Hidden Font Injection**: Removes invisible characters and byte order marks (`[\u200B-\u200D\uFEFF]`) via `InputSanitizer`.
2. **Loophole & Tax Evasion Solicitations**: Automatically refuses circumvention requests and attaches statutory disclaimers.
3. **False Statute Assertions**: Detects user claims regarding repealed statutes to enforce mandatory live validation against official gazettes (`vbpl.vn`).
4. **System Prompt & Secret Extraction**: Blocks attempts to reveal system instructions, environment variables, or API keys.
5. **SQL Injection**: Enforces 100% parameterized queries on SQLite and detects malicious SQL syntax in inputs.
6. **Fictitious Statutes**: Flags non-existent legal articles and potential model hallucinations.
7. **Courtroom Litigation Defense**: Declines litigation representation requests with appropriate legal disclaimers.
8. **Unauthorized Administrative Filing Execution**: Requires an explicit one-time confirmation token from a human compliance officer before executing irreversible actions.
9. **Denial of Service (Token Bloat & Infinite Traversal)**: Imposes bounds on input length (≤ 8,000 characters), traversal depth (≤ 2 hops), and retrieved documents (≤ 5).
10. **Path Traversal**: Strips directory traversal sequences (`../`) and strictly confines file export operations to `./workspace/dossiers/`.

---

## 2. Reporting a Vulnerability

If you identify a security vulnerability or a prompt injection vector that bypasses current guardrails:
1. Do not open a public GitHub issue.
2. Share the details (reproduction payload, observed behavior, logs) directly with the development team or open a draft Security Advisory on GitHub.
3. The team will investigate, update `configs/threat_model_rules.yaml`, and deploy a mitigation promptly.
