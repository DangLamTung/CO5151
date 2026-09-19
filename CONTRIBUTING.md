# Contributing to LegalPilot-VN

Welcome to the **LegalPilot-VN** project repository for CO5151. This guide outlines our collaborative development workflow, coding conventions, and contribution standards to maintain a clean, reproducible codebase.

---

## 1. Local Development Setup

### Step 1: Clone the repository and configure virtual environment
```bash
git clone https://github.com/DangLamTung/CO5151.git
cd CO5151

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install runtime and development dependencies
make install-dev
```

### Step 2: Initialize databases and foundation
```bash
# Start Neo4j and Qdrant via Docker, initialize SQLite schema
./run.sh
```

---

## 2. Branching Strategy

All changes must be developed on separate branches and submitted via Pull Requests targeting `main`. Do not push commits directly to `main`.

| Prefix | Purpose | Example |
| :--- | :--- | :--- |
| `feat/` | New features or functional modules | `feat/selective-edge-traversal` |
| `fix/` | Bug fixes and defect resolutions | `fix/sqlite-wal-lock` |
| `eval/` | Benchmark scripts, ablation experiments, metrics | `eval/100-qa-benchmark` |
| `sec/` | Threat model updates, security enhancements | `sec/prompt-injection-defense` |
| `docs/` | Documentation, proposals, and LaTeX reports | `docs/update-d2-report` |
| `<member>/` | Personal feature or exploration branch | `paul/init`, `hung/auditor-engine` |

---

## 3. Commit Message Conventions

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```text
<type>(<scope>): <concise description in present tense>

[Optional body detailing rationale]
```

**Common types**:
- `feat`: New user-facing or system feature.
- `fix`: Bug fix or error resolution.
- `test`: Adding or updating test cases.
- `refactor`: Code changes that neither fix bugs nor add features.
- `docs`: Documentation updates.
- `chore`: Build configuration, CI/CD, or dependency maintenance.

---

## 4. Code Quality & Pre-Commit Standards

Run the following checks locally before submitting a pull request:

```bash
# 1. Format code and sort imports
make format

# 2. Run Ruff linter
make lint

# 3. Run Mypy static type checker
make typecheck

# 4. Run test suite with coverage report
make test-cov
```

**Pull Request Acceptance Criteria**:
1. All GitHub Actions CI checks (`ci.yml`, `docker-build.yml`, `codeql.yml`) must pass.
2. Complete the required fields in the [Pull Request Template](.github/pull_request_template.md).
3. Obtain at least one review approval from a team member.

---

## 5. Team Responsibilities (D1 Proposal)

- **Dang Lam Tung**: Agent Orchestrator, dynamic planning, backtracking controller, Web UI, repository packaging.
- **Nguyen Trung Phong**: Neo4j/Qdrant knowledge base, selective edge traversal algorithm, MCP tools, SQLite enterprise memory.
- **Vu Viet Hung**: Claim auditor engine, guarded actions gate, Threat Model v0 evaluation, 120-task benchmark suite.
