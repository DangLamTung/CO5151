"""Tests for HumanTokenGate security mechanism."""

import time
import pytest
from src.core.exceptions import GateAuthorizationError
from src.security.token_gate import HumanTokenGate


def test_token_generation_and_valid_consumption(token_gate: HumanTokenGate):
    """Verify generating and consuming a valid token."""
    token = token_gate.generate_token(
        action_name="submit_portal_filing",
        payload_summary="Submitting work permit filing for 1 specialist",
    )
    assert token.startswith("CONFIRM-")

    # Verify consumption
    consumed = token_gate.verify_token(token, action_name="submit_portal_filing")
    assert consumed is True

    # One-time use: second attempt should fail
    with pytest.raises(GateAuthorizationError):
        token_gate.verify_token(token, action_name="submit_portal_filing")


def test_token_expiration(token_gate: HumanTokenGate):
    """Verify expired token is rejected."""
    token = token_gate.generate_token(
        action_name="submit_portal_filing",
        payload_summary="Submitting tax deferral dossier",
    )
    time.sleep(2.2)  # Exceed 2s TTL
    with pytest.raises(GateAuthorizationError):
        token_gate.verify_token(token, action_name="submit_portal_filing")


def test_token_action_mismatch(token_gate: HumanTokenGate):
    """Verify token issued for one action cannot be used for another."""
    token = token_gate.generate_token(
        action_name="export_dossier",
        payload_summary="Exporting local matrix",
    )
    with pytest.raises(GateAuthorizationError):
        token_gate.verify_token(token, action_name="submit_portal_filing")


def test_sqlite_backed_token_gate(temp_sqlite_db):
    """Verify token persistence across restarts using SQLite."""
    # Create gate with SQLite backend
    gate_1 = HumanTokenGate(token_expiry_seconds=10, sqlite_mgr=temp_sqlite_db)
    token = gate_1.generate_token(
        action_name="submit_portal_filing",
        payload_summary="Enterprise compliance filing",
    )

    # Simulate app restart / new instance
    gate_2 = HumanTokenGate(token_expiry_seconds=10, sqlite_mgr=temp_sqlite_db)
    assert gate_2.verify_token(token, action_name="submit_portal_filing") is True

    # Ensure it cannot be reused
    with pytest.raises(GateAuthorizationError):
        gate_2.verify_token(token, action_name="submit_portal_filing")
