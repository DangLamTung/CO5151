"""SQLite Enterprise Memory Manager for LegalPilot-VN.

Stores enterprise profile, audit history, cached statute validities with TTL,
and persistent confirmation tokens for human-in-the-loop actions.
Configured with WAL mode and parameterized queries for high concurrency and safety.
"""

import json
from pathlib import Path
import sqlite3
import time
from typing import Any

from src.core.logger import logger
from src.memory.state_models import AuditHistoryRecord, EnterpriseProfile, StatuteCacheEntry


class SQLiteMemoryManager:
    """Manages persistent SQLite memory for enterprise compliance."""

    def __init__(self, db_path: str = "data/enterprise_compliance.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_tables()

    def _get_connection(self) -> sqlite3.Connection:
        """Creates a thread-safe connection with row_factory, WAL mode, and busy timeout."""
        conn = sqlite3.connect(str(self.db_path), timeout=30.0)
        conn.row_factory = sqlite3.Row
        # Enable WAL mode and foreign keys for multi-agent concurrency
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        return conn

    def init_tables(self) -> None:
        """Initializes tables for profile, audit history, statute cache, and pending tokens."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # 1. Enterprise profile table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS enterprise_profile (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_name TEXT NOT NULL,
                    entity_type TEXT NOT NULL,
                    charter_capital REAL NOT NULL,
                    sector_code TEXT NOT NULL,
                    headcount INTEGER NOT NULL,
                    foreign_ownership_ratio REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 2. Audit history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    query TEXT NOT NULL,
                    compliance_matrix_path TEXT NOT NULL,
                    auditor_score REAL NOT NULL,
                    human_token TEXT,
                    approved_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 3. Statute cache table with TTL
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS statute_cache (
                    law_id TEXT PRIMARY KEY,
                    document_number TEXT NOT NULL,
                    title TEXT NOT NULL,
                    effective_date TEXT NOT NULL,
                    status TEXT NOT NULL,
                    raw_metadata TEXT,
                    cached_at REAL NOT NULL,
                    ttl_seconds INTEGER DEFAULT 86400
                );
            """)

            # 4. Pending tokens table for guarded actions persistence
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pending_tokens (
                    token TEXT PRIMARY KEY,
                    action_name TEXT NOT NULL,
                    payload_summary TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    expires_at REAL NOT NULL,
                    is_consumed INTEGER DEFAULT 0
                );
            """)

            conn.commit()
            logger.debug(f"SQLite tables verified at {self.db_path}")

    # --------------------------------------------------------------------------
    # Enterprise Profile Methods
    # --------------------------------------------------------------------------
    def save_enterprise_profile(self, profile: EnterpriseProfile) -> int:
        """Saves or updates an enterprise profile."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO enterprise_profile (
                    company_name, entity_type, charter_capital, sector_code,
                    headcount, foreign_ownership_ratio
                ) VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    profile.company_name,
                    profile.entity_type,
                    profile.charter_capital,
                    profile.sector_code,
                    profile.headcount,
                    profile.foreign_ownership_ratio,
                ),
            )
            conn.commit()
            return cursor.lastrowid or 0

    def get_latest_enterprise_profile(self) -> EnterpriseProfile | None:
        """Retrieves the most recently saved enterprise profile."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM enterprise_profile ORDER BY id DESC LIMIT 1"
            )
            row = cursor.fetchone()
            if not row:
                return None
            return EnterpriseProfile(
                id=row["id"],
                company_name=row["company_name"],
                entity_type=row["entity_type"],
                charter_capital=row["charter_capital"],
                sector_code=row["sector_code"],
                headcount=row["headcount"],
                foreign_ownership_ratio=row["foreign_ownership_ratio"],
                created_at=row["created_at"],
            )

    # --------------------------------------------------------------------------
    # Statute Cache Methods (TTL Invalidation)
    # --------------------------------------------------------------------------
    def get_cached_statute(self, law_id: str) -> StatuteCacheEntry | None:
        """Retrieves a cached statute if still valid under TTL."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT law_id, document_number, title, effective_date, status,
                       raw_metadata, cached_at, ttl_seconds
                FROM statute_cache
                WHERE law_id = ?
            """,
                (law_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None

            elapsed_seconds = time.time() - float(row["cached_at"])
            if elapsed_seconds > row["ttl_seconds"]:
                logger.info(f"Cache expired for statute {law_id}. Evicting...")
                self.evict_cached_statute(law_id)
                return None

            metadata = json.loads(row["raw_metadata"]) if row["raw_metadata"] else {}
            return StatuteCacheEntry(
                law_id=row["law_id"],
                document_number=row["document_number"],
                title=row["title"],
                effective_date=row["effective_date"],
                status=row["status"],
                raw_metadata=metadata,
                cached_at=float(row["cached_at"]),
                ttl_seconds=row["ttl_seconds"],
            )

    def set_cached_statute(self, entry: StatuteCacheEntry) -> None:
        """Caches or replaces a statute validity lookup."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO statute_cache (
                    law_id, document_number, title, effective_date, status,
                    raw_metadata, cached_at, ttl_seconds
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    entry.law_id,
                    entry.document_number,
                    entry.title,
                    entry.effective_date,
                    entry.status,
                    json.dumps(entry.raw_metadata, ensure_ascii=False),
                    entry.cached_at,
                    entry.ttl_seconds,
                ),
            )
            conn.commit()

    def evict_cached_statute(self, law_id: str) -> None:
        """Evicts a specific statute from the cache."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM statute_cache WHERE law_id = ?", (law_id,))
            conn.commit()

    # --------------------------------------------------------------------------
    # Pending Confirmation Tokens (Persistence for Guarded Actions)
    # --------------------------------------------------------------------------
    def save_pending_token(
        self,
        token: str,
        action_name: str,
        payload_summary: str,
        created_at: float,
        expires_at: float,
    ) -> None:
        """Saves a pending human confirmation token to SQLite."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO pending_tokens (
                    token, action_name, payload_summary, created_at, expires_at, is_consumed
                ) VALUES (?, ?, ?, ?, ?, 0)
            """,
                (token, action_name, payload_summary, created_at, expires_at),
            )
            conn.commit()

    def get_valid_pending_token(self, token: str) -> dict[str, Any] | None:
        """Retrieves token record if it exists, is not consumed, and has not expired."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT token, action_name, payload_summary, created_at, expires_at, is_consumed
                FROM pending_tokens
                WHERE token = ? AND is_consumed = 0
            """,
                (token,),
            )
            row = cursor.fetchone()
            if not row:
                return None

            now = time.time()
            if now > float(row["expires_at"]):
                # Mark as expired / delete
                cursor.execute("DELETE FROM pending_tokens WHERE token = ?", (token,))
                conn.commit()
                return None

            return dict(row)

    def consume_pending_token(self, token: str) -> bool:
        """Marks a pending token as consumed."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE pending_tokens SET is_consumed = 1 WHERE token = ? AND is_consumed = 0",
                (token,),
            )
            conn.commit()
            return cursor.rowcount > 0

    # --------------------------------------------------------------------------
    # Audit History Methods
    # --------------------------------------------------------------------------
    def log_audit_history(self, record: AuditHistoryRecord) -> int:
        """Logs a compliance audit run."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO audit_history (
                    session_id, query, compliance_matrix_path, auditor_score,
                    human_token, approved_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    record.session_id,
                    record.query,
                    record.compliance_matrix_path,
                    record.auditor_score,
                    record.human_token,
                    record.approved_at,
                ),
            )
            conn.commit()
            return cursor.lastrowid or 0

    def update_audit_approval(self, session_id: str, human_token: str) -> bool:
        """Records human approval token for a completed audit session."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE audit_history
                SET human_token = ?, approved_at = CURRENT_TIMESTAMP
                WHERE session_id = ?
            """,
                (human_token, session_id),
            )
            conn.commit()
            return cursor.rowcount > 0
