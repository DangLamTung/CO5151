"""Tests for SQLiteMemoryManager and schema."""

import time

from src.memory.sqlite_manager import SQLiteMemoryManager
from src.memory.state_models import AuditHistoryRecord, EnterpriseProfile, StatuteCacheEntry


def test_enterprise_profile_crud(temp_sqlite_db: SQLiteMemoryManager):
    """Verify saving and retrieving enterprise profile."""
    profile = EnterpriseProfile(
        company_name="Công ty TNHH Giải Pháp Công Nghệ",
        entity_type="TNHH",
        charter_capital=5000000000.0,
        sector_code="J6201",
        headcount=30,
        foreign_ownership_ratio=0.0,
    )
    profile_id = temp_sqlite_db.save_enterprise_profile(profile)
    assert profile_id > 0

    retrieved = temp_sqlite_db.get_latest_enterprise_profile()
    assert retrieved is not None
    assert retrieved.company_name == profile.company_name
    assert retrieved.charter_capital == 5000000000.0
    assert retrieved.headcount == 30


def test_statute_cache_and_ttl(temp_sqlite_db: SQLiteMemoryManager):
    """Verify caching statute and TTL expiration behavior."""
    entry = StatuteCacheEntry(
        law_id="ND_152_2020",
        document_number="152/2020/NĐ-CP",
        title="Nghị định quy định về người lao động nước ngoài làm việc tại Việt Nam",
        effective_date="2021-02-15",
        status="partially_expired",
        raw_metadata={"amended_by": ["70/2023/NĐ-CP"]},
        ttl_seconds=1,  # Short TTL for test
    )
    temp_sqlite_db.set_cached_statute(entry)

    # Immediately should be valid
    cached = temp_sqlite_db.get_cached_statute("ND_152_2020")
    assert cached is not None
    assert cached.document_number == "152/2020/NĐ-CP"

    # Wait for TTL to expire
    time.sleep(1.2)
    expired_lookup = temp_sqlite_db.get_cached_statute("ND_152_2020")
    assert expired_lookup is None


def test_audit_history_logging_and_approval(temp_sqlite_db: SQLiteMemoryManager):
    """Verify logging audit history and recording human token approval."""
    record = AuditHistoryRecord(
        session_id="sess-001",
        query="Kiểm tra điều kiện chuyên gia nước ngoài",
        compliance_matrix_path="./workspace/dossiers/matrix_001.md",
        auditor_score=0.95,
    )
    audit_id = temp_sqlite_db.log_audit_history(record)
    assert audit_id > 0

    # Update approval
    success = temp_sqlite_db.update_audit_approval("sess-001", "CONFIRM-ABCD1234")
    assert success is True
