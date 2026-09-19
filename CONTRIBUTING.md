# Hướng dẫn Đóng góp (Contribution Guide) — LegalPilot-VN

Chào mừng các thành viên nhóm **CO5151 (HK261)** tham gia đóng góp mã nguồn cho dự án **LegalPilot-VN**. Tài liệu này thiết lập các tiêu chuẩn và quy trình làm việc chung để đảm bảo tính nhất quán, chất lượng mã nguồn và khả năng tái lập.

---

## 1. Thiết lập Môi trường Cục bộ (Local Setup)

### Bước 1: Clone và kích hoạt môi trường ảo
```bash
git clone https://github.com/DangLamTung/CO5151.git
cd CO5151

# Tạo môi trường ảo và cài đặt dependencies
python3 -m venv .venv
source .venv/bin/activate
make install-dev
```

### Bước 2: Khởi động cơ sở dữ liệu và xác thực foundation
```bash
# Khởi động Neo4j và Qdrant qua Docker, khởi tạo SQLite
./run.sh
```

---

## 2. Quy ước Đặt tên Nhánh (Branching Model)

Mọi thay đổi **bắt buộc** phải được thực hiện trên nhánh riêng và mở Pull Request vào `main`. Không commit trực tiếp vào `main`.

| Tiền tố nhánh | Mục đích | Ví dụ |
| :--- | :--- | :--- |
| `feat/` | Tính năng mới, module mới | `feat/selective-edge-traversal` |
| `fix/` | Sửa lỗi hệ thống | `fix/sqlite-wal-lock` |
| `eval/` | Benchmark, ablation studies, đo metrics | `eval/100-qa-benchmark` |
| `sec/` | Cập nhật Threat Model, bảo mật | `sec/prompt-injection-defense` |
| `docs/` | Cập nhật tài liệu, proposal, báo cáo LaTeX | `docs/update-d2-report` |
| `<member>/` | Nhánh cá nhân của thành viên | `paul/init`, `hung/auditor-engine` |

---

## 3. Quy ước Commit Message (Conventional Commits)

Commit message cần tuân theo chuẩn [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(<scope>): <mô tả ngắn gọn bằng tiếng Anh hoặc tiếng Việt>

[Nội dung chi tiết nếu cần]
```

**Các type được chấp nhận**:
- `feat`: Thêm tính năng mới (ví dụ: `feat(knowledge): add selective edge traversal cypher query`).
- `fix`: Sửa lỗi (ví dụ: `fix(sqlite): resolve connection leak with contextmanager`).
- `test`: Thêm hoặc cập nhật unit tests (ví dụ: `test(security): add 8 test cases for threat model`).
- `refactor`: Tái cấu trúc mã nguồn không làm thay đổi tính năng.
- `docs`: Cập nhật tài liệu (ví dụ: `docs: update milestone roadmap in CONTRIBUTING.md`).
- `chore`: Thay đổi cấu hình build, CI/CD, dependencies (ví dụ: `chore(ci): update ruff lint command`).

---

## 4. Tiêu chuẩn Mã nguồn & Kiểm tra Chất lượng (Quality Gates)

Trước khi commit hoặc mở PR, chạy lệnh sau để đảm bảo mã nguồn vượt qua toàn bộ kiểm tra:

```bash
# 1. Tự động sửa lỗi format và imports
make format

# 2. Kiểm tra linter
make lint

# 3. Kiểm tra kiểu tĩnh (Mypy)
make typecheck

# 4. Chạy toàn bộ Unit Tests & đo Coverage
make test-cov
```

**Tiêu chí chấp thuận PR (Definition of Done)**:
1. Tất cả các bước trong GitHub Actions CI (`ci.yml`, `docker-build.yml`) phải **xanh 100%**.
2. Điền đầy đủ thông tin theo mẫu [Pull Request Template](.github/pull_request_template.md).
3. Có ít nhất **1 approval** từ thành viên khác trong nhóm.

---

## 5. Phân công Trách nhiệm theo Đề cương D1

- **Đặng Lâm Tùng**: Agent Orchestrator, Dynamic Planning, Backtracking Controller, Streamlit UI, Packaging.
- **Nguyễn Trung Phong**: Neo4j/Qdrant Knowledge Base, Selective Edge Traversal, MCP Tools, SQLite Enterprise Memory.
- **Vũ Việt Hùng**: Claim Auditor Engine, Guarded Actions Gate, Threat Model v0, 120-task Benchmark & Ablations.
