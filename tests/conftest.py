"""Pytest fixtures for LegalPilot-VN test suite."""

from pathlib import Path

import pytest

from src.memory.sqlite_manager import SQLiteMemoryManager
from src.security.sanitizer import InputSanitizer
from src.security.token_gate import HumanTokenGate


@pytest.fixture
def temp_sqlite_db(tmp_path: Path) -> SQLiteMemoryManager:
    """Provides a fresh SQLite memory manager using a temporary database file."""
    db_file = tmp_path / "test_compliance.db"
    return SQLiteMemoryManager(db_path=str(db_file))


@pytest.fixture
def sanitizer(tmp_path: Path) -> InputSanitizer:
    """Provides an InputSanitizer with a temporary export directory."""
    export_dir = tmp_path / "workspace" / "dossiers"
    return InputSanitizer(max_input_length=1000, allowed_export_dir=str(export_dir))


@pytest.fixture
def token_gate() -> HumanTokenGate:
    """Provides a HumanTokenGate with a short expiration for testing."""
    return HumanTokenGate(token_expiry_seconds=2)
