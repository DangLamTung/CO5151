"""Security input sanitizer for LegalPilot-VN.

Enforces:
- Vector 1: Stripping zero-width font layers and hidden text.
- Vector 10: Path traversal sanitization restricting writes to ./workspace/dossiers/.
- Input length limits to prevent DoS token bloat.
"""

import re
from pathlib import Path

from src.core.exceptions import SecurityViolationError


class InputSanitizer:
    """Sanitizes incoming text and file paths against adversarial payloads."""

    # Zero-width spaces, joiners, and BOM marks
    ZERO_WIDTH_REGEX = re.compile(r"[\u200B-\u200D\uFEFF\u00A0]")

    # Dangerous prompt injection delimiters
    OVERRIDE_TAGS_REGEX = re.compile(
        r"(\[OVERRIDE:.*?\]|<\|im_start\|>|<\|im_end\|>|\[SYSTEM_PROMPT\])",
        re.IGNORECASE,
    )

    def __init__(
        self, max_input_length: int = 8000, allowed_export_dir: str = "./workspace/dossiers"
    ):
        self.max_input_length = max_input_length
        self.allowed_export_dir = Path(allowed_export_dir).resolve()
        self.allowed_export_dir.mkdir(parents=True, exist_ok=True)

    def sanitize_text(self, text: str) -> str:
        """Strips hidden characters and checks input length."""
        if not text:
            return ""

        if len(text) > self.max_input_length:
            raise SecurityViolationError(
                f"Input text exceeds maximum allowed length ({len(text)} > {self.max_input_length})",
                vector_id=9,
            )

        # Strip zero-width characters (Vector 1)
        cleaned = self.ZERO_WIDTH_REGEX.sub("", text)

        # Sanitize dangerous system instruction overrides
        cleaned = self.OVERRIDE_TAGS_REGEX.sub("[REDACTED_OVERRIDE]", cleaned)

        return cleaned.strip()

    def sanitize_export_path(self, target_filename: str) -> Path:
        """Ensures export paths cannot escape the designated dossiers directory (Vector 10)."""
        # Strip directory separators from filename to prevent traversal
        safe_name = Path(target_filename).name

        # Resolve final path
        resolved_path = (self.allowed_export_dir / safe_name).resolve()

        # Check if resolved path is strictly within allowed directory
        if not resolved_path.is_relative_to(self.allowed_export_dir):
            raise SecurityViolationError(
                f"Path traversal detected: {target_filename} attempts to escape {self.allowed_export_dir}",
                vector_id=10,
            )

        return resolved_path
