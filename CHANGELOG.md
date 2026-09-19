# Changelog

Tất cả các thay đổi đáng chú ý của dự án **LegalPilot-VN** sẽ được ghi lại trong tài liệu này theo chuẩn [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.1.0] - 2026-09-19

### Đã thêm (Added)
- **Codebase Standards**: Thiết lập `pyproject.toml` theo chuẩn PEP 517/518/621 với cấu hình Ruff, Mypy và Pytest.
- **Hạ tầng Container**: Tích hợp `docker-compose.yml` (Neo4j 5.23 APOC, Qdrant v1.11.3) và `Dockerfile` production.
- **Startup Script**: Bổ sung script thực thi một chạm `run.sh` và `Makefile`.
- **Cấu hình Hệ thống**: `system_config.yaml` và `threat_model_rules.yaml` (bao phủ 10 vector kiểm thử an toàn).
- **Core Modules (`src/core/`)**: 
  - `config.py` với typed nested settings.
  - `logger.py` structured logging.
  - `exceptions.py` phân tầng ngoại lệ rõ ràng.
- **Memory Layer (`src/memory/`)**:
  - `sqlite_manager.py` hỗ trợ WAL mode, foreign keys, và timeout chống lock.
  - Quản lý `enterprise_profile`, `audit_history`, `statute_cache` (với TTL invalidation), và `pending_tokens`.
- **Security & Guardrails (`src/security/`)**:
  - `sanitizer.py` lọc ký tự tàng hình và chống path traversal.
  - `token_gate.py` hỗ trợ SQLite persistence cho cơ chế Human-in-the-loop.
  - `guardrails.py` đánh giá động 10 vector tấn công.
- **UI**: Giao diện Streamlit mẫu `src/ui/app.py`.
- **Testing**: Bộ 21 unit tests vượt qua 100% với 89% code coverage.
- **CI/CD & Templates**:
  - GitHub Actions CI (`ci.yml`, `docker-build.yml`, `codeql.yml`).
  - Pull Request Template và các Issue Templates (Bug Report, Feature Request, Milestone Task).
  - Tài liệu hướng dẫn đóng góp `CONTRIBUTING.md` và chính sách bảo mật `SECURITY.md`.
