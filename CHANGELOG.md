# Changelog

All notable changes to the **LegalPilot-VN** project are documented in this file using the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.

## [0.1.0] - 2026-09-19

### Added
- **Codebase Standards**: Configured `pyproject.toml` adhering to PEP 517/518/621 with Ruff, Mypy, and Pytest.
- **Container Infrastructure**: Added `docker-compose.yml` (Neo4j 5.23 with APOC, Qdrant v1.11.3) and production `Dockerfile`.
- **Startup Script & Tooling**: Added `run.sh` and `Makefile` for one-command environment setup.
- **System Configurations**: Added `configs/system_config.yaml` and `configs/threat_model_rules.yaml` covering the 10 threat vectors.
- **Core Modules (`src/core/`)**:
  - `config.py` with typed hierarchical settings.
  - `logger.py` with structured logging.
  - `exceptions.py` with custom exception classes.
- **Memory Layer (`src/memory/`)**:
  - `sqlite_manager.py` configured with WAL mode, foreign keys, and busy timeout.
  - Managed tables for `enterprise_profile`, `audit_history`, `statute_cache` (with TTL invalidation), and `pending_tokens`.
- **Security & Guardrails (`src/security/`)**:
  - `sanitizer.py` for zero-width character stripping and path traversal protection.
  - `token_gate.py` with SQLite-backed persistence for human confirmation gates.
  - `guardrails.py` for dynamic threat vector evaluation.
- **User Interface**: Streamlit dashboard skeleton in `src/ui/app.py`.
- **Test Suite**: 21 unit tests passing with 89% code coverage.
- **CI/CD & Templates**:
  - GitHub Actions workflows (`ci.yml`, `docker-build.yml`, `codeql.yml`).
  - Pull Request and Issue templates (Bug Report, Feature Request, Milestone Task).
  - Contribution guide `CONTRIBUTING.md` and security policy `SECURITY.md`.
