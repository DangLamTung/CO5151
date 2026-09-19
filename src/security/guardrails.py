"""Security Guardrails evaluating queries against Threat Model v0."""

import re
from typing import Any

from src.core.exceptions import SecurityViolationError
from src.core.logger import logger


class SecurityGuardrails:
    """Evaluates user inputs against known adversarial vectors and compliance boundaries."""

    DISCLAIMER_MSG = (
        "CẢNH BÁO PHÁP LÝ: Hệ thống LegalPilot-VN chỉ hỗ trợ tra cứu và đối chiếu quy chuẩn "
        "tuân thủ quy định hành chính, không cung cấp dịch vụ bào chữa tranh tụng tại tòa hoặc "
        "tư vấn các phương thức trốn tránh nghĩa vụ pháp luật."
    )

    def __init__(self, rules_config: dict[str, Any] | None = None):
        self.rules = rules_config or {}
        # Pre-compile threat vector patterns
        self.loophole_pattern = re.compile(
            r"(?i)(lách luật|trốn thuế|bypass foreign equity|trốn nghĩa vụ)"
        )
        self.secret_extract_pattern = re.compile(
            r"(?i)(print system prompt|in system prompt|show instructions|tiết lộ prompt|api key)"
        )
        self.litigation_pattern = re.compile(
            r"(?i)(kiện ngay ra tòa|bào chữa trước tòa|đại diện tranh tụng)"
        )

    def evaluate_query(self, query: str) -> dict[str, Any]:
        """Evaluates a query and returns status: allowed, refused, or disclaimed."""
        # Vector 4: System prompt disclosure attempt
        if self.secret_extract_pattern.search(query):
            logger.warning(f"Vector 4 detected: Secret extraction attempt in query '{query[:50]}'")
            raise SecurityViolationError(
                "Yêu cầu bị từ chối: Không thể hiển thị hoặc trích xuất system prompt và khóa bí mật.",
                vector_id=4,
            )

        # Vector 2: Circumvention / Loophole query
        if self.loophole_pattern.search(query):
            logger.warning(f"Vector 2 detected: Loophole attempt in query '{query[:50]}'")
            return {
                "status": "refused",
                "message": (
                    "Hệ thống từ chối hỗ trợ các yêu cầu tìm cách trốn tránh hoặc lách luật. "
                    + self.DISCLAIMER_MSG
                ),
                "vector_id": 2,
            }

        # Vector 7: Courtroom litigation representation
        if self.litigation_pattern.search(query):
            logger.info(f"Vector 7 detected: Litigation query '{query[:50]}'")
            return {
                "status": "disclaimed",
                "message": self.DISCLAIMER_MSG,
                "vector_id": 7,
            }

        return {"status": "allowed", "message": None, "vector_id": None}
