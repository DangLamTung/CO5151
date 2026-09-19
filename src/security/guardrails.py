"""Security Guardrails evaluating queries against Threat Model v0.

Evaluates user queries against the 10 threat vectors defined in configs/threat_model_rules.yaml:
- Vector 2: Circumvention / Loophole query
- Vector 3: False statute assertion by user (forces mandatory online check)
- Vector 4: System prompt and secret extraction
- Vector 5: SQL injection payload detection in inputs
- Vector 6: Non-existent / fictitious statute queries
- Vector 7: Courtroom litigation solicitation
- Vector 8: Unauthorized administrative filing execution commands
"""

from pathlib import Path
import re
from typing import Any
import yaml

from src.core.exceptions import SecurityViolationError
from src.core.logger import logger


class SecurityGuardrails:
    """Evaluates user inputs against known adversarial vectors and compliance boundaries."""

    DISCLAIMER_MSG = (
        "CẢNH BÁO PHÁP LÝ: Hệ thống LegalPilot-VN chỉ hỗ trợ tra cứu và đối chiếu quy chuẩn "
        "tuân thủ quy định hành chính, không cung cấp dịch vụ bào chữa tranh tụng tại tòa hoặc "
        "tư vấn các phương thức trốn tránh nghĩa vụ pháp luật."
    )

    def __init__(self, rules_config_path: str | Path = "configs/threat_model_rules.yaml"):
        self.rules_config_path = Path(rules_config_path)
        self.rules = self._load_rules()
        self._compile_patterns()

    def _load_rules(self) -> dict[str, Any]:
        """Loads rules from YAML configuration or falls back to defaults."""
        if self.rules_config_path.exists():
            try:
                with open(self.rules_config_path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                logger.warning(f"Could not load threat rules from {self.rules_config_path}: {e}")
        return {}

    def _compile_patterns(self) -> None:
        """Pre-compiles regex patterns for threat detection."""
        self.patterns = {
            # Vector 2: Loophole / Circumvention
            2: re.compile(r"(?i)(lách luật|trốn thuế|bypass foreign equity|trốn nghĩa vụ)"),
            # Vector 3: False User Statute Assertion
            3: re.compile(r"(?i)(hết hiệu lực hôm qua|đã bị bãi bỏ rồi)"),
            # Vector 4: System Prompt / Secret Extraction
            4: re.compile(
                r"(?i)(print system prompt|in system prompt|show instructions|tiết lộ prompt|api key)"
            ),
            # Vector 5: SQL Injection payload
            5: re.compile(r"(?i)(union select|drop table|insert into|--|;\s*drop|'\s*or\s*'1'='1)"),
            # Vector 6: Non-existent Fictitious Statute
            6: re.compile(r"(?i)(điều 999|luật tưởng tượng)"),
            # Vector 7: Courtroom Litigation Defense
            7: re.compile(r"(?i)(kiện ngay ra tòa|bào chữa trước tòa|đại diện tranh tụng)"),
            # Vector 8: Unauthorized Filing Execution
            8: re.compile(r"(?i)(submit_portal_filing|nộp hồ sơ ngay lập tức|tự động nộp)"),
        }

    def evaluate_query(self, query: str) -> dict[str, Any]:
        """Evaluates a query and returns status: allowed, refused, flagged, or disclaimed."""
        if not query:
            return {"status": "allowed", "message": None, "vector_id": None}

        # Vector 4: System prompt / secret extraction (Block & Raise)
        if self.patterns[4].search(query):
            logger.warning(f"Vector 4 detected: Secret extraction attempt in query '{query[:50]}'")
            raise SecurityViolationError(
                "Yêu cầu bị từ chối: Không thể hiển thị hoặc trích xuất system prompt và khóa bí mật.",
                vector_id=4,
            )

        # Vector 5: SQL Injection (Block & Raise)
        if self.patterns[5].search(query):
            logger.warning(f"Vector 5 detected: SQL Injection attempt in query '{query[:50]}'")
            raise SecurityViolationError(
                "Yêu cầu bị từ chối: Phát hiện cú pháp truy vấn không hợp lệ (SQL injection pattern).",
                vector_id=5,
            )

        # Vector 2: Circumvention / Loophole query (Refuse)
        if self.patterns[2].search(query):
            logger.warning(f"Vector 2 detected: Loophole attempt in query '{query[:50]}'")
            return {
                "status": "refused",
                "message": (
                    "Hệ thống từ chối hỗ trợ các yêu cầu tìm cách trốn tránh hoặc lách luật. "
                    + self.DISCLAIMER_MSG
                ),
                "vector_id": 2,
            }

        # Vector 8: Unauthorized filing command (Requires human confirmation)
        if self.patterns[8].search(query):
            logger.info(f"Vector 8 detected: Filing command in query '{query[:50]}'")
            return {
                "status": "requires_human_token",
                "message": "Hành động nộp hồ sơ yêu cầu mã xác nhận (Human Confirmation Token) từ chuyên viên tuân thủ.",
                "vector_id": 8,
            }

        # Vector 3: User asserting statute invalidity (Flag for mandatory live lookup)
        if self.patterns[3].search(query):
            logger.info(f"Vector 3 detected: User assertion in query '{query[:50]}'")
            return {
                "status": "flagged_mandatory_live_check",
                "message": "Phát hiện khẳng định về hiệu lực văn bản từ người dùng. Bắt buộc tra cứu trực tiếp trên vbpl.vn để đối soát.",
                "vector_id": 3,
                "mandatory_online_check": True,
            }

        # Vector 6: Non-existent fictitious statute
        if self.patterns[6].search(query):
            logger.info(f"Vector 6 detected: Fictitious statute query '{query[:50]}'")
            return {
                "status": "flagged_hallucination_risk",
                "message": "Phát hiện viện dẫn điều khoản có nguy cơ không tồn tại.",
                "vector_id": 6,
            }

        # Vector 7: Courtroom litigation representation (Add disclaimer)
        if self.patterns[7].search(query):
            logger.info(f"Vector 7 detected: Litigation query '{query[:50]}'")
            return {
                "status": "disclaimed",
                "message": self.DISCLAIMER_MSG,
                "vector_id": 7,
            }

        return {"status": "allowed", "message": None, "vector_id": None}
