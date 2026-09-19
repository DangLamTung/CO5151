"""Human Confirmation Token Gate for Guarded Actions (Requirement R2 & Vector 8).

Supports both SQLite-backed persistence (for surviving Streamlit reruns and multi-worker restarts)
and in-memory storage for lightweight operations.
"""

from typing import Any
import secrets
import time

from src.core.exceptions import GateAuthorizationError
from src.core.logger import logger


class HumanTokenGate:
    """Manages one-time tokens required to execute irreversible write actions."""

    def __init__(self, token_expiry_seconds: int = 300, sqlite_mgr: Any = None):
        self.token_expiry_seconds = token_expiry_seconds
        self.sqlite_mgr = sqlite_mgr
        self._pending_tokens: dict[str, dict[str, Any]] = {}

    def generate_token(self, action_name: str, payload_summary: str) -> str:
        """Generates a secure, short-lived token for an action requiring human approval."""
        token = f"CONFIRM-{secrets.token_hex(4).upper()}"
        now = time.time()
        expires_at = now + self.token_expiry_seconds

        if self.sqlite_mgr:
            self.sqlite_mgr.save_pending_token(
                token=token,
                action_name=action_name,
                payload_summary=payload_summary,
                created_at=now,
                expires_at=expires_at,
            )
        else:
            self._pending_tokens[token] = {
                "action_name": action_name,
                "payload_summary": payload_summary,
                "created_at": now,
                "expires_at": expires_at,
            }

        logger.info(
            f"Generated Human Confirmation Token '{token}' for action '{action_name}'. "
            f"Requires approval within {self.token_expiry_seconds}s."
        )
        return token

    def verify_token(self, token: str, action_name: str) -> bool:
        """Verifies and consumes a confirmation token. Raises error if invalid or expired."""
        if self.sqlite_mgr:
            record = self.sqlite_mgr.get_valid_pending_token(token)
            if not record:
                logger.warning(f"Rejected invalid or expired confirmation token: '{token}'")
                raise GateAuthorizationError(f"Invalid or expired confirmation token: {token}")

            if record["action_name"] != action_name:
                logger.warning(
                    f"Token {token} was issued for '{record['action_name']}', not '{action_name}'"
                )
                raise GateAuthorizationError(
                    f"Token mismatch: issued for {record['action_name']} but used for {action_name}"
                )

            consumed = self.sqlite_mgr.consume_pending_token(token)
            if not consumed:
                raise GateAuthorizationError(f"Token {token} has already been consumed")

            logger.info(f"Human Confirmation Token '{token}' verified and consumed for '{action_name}'.")
            return True

        # In-memory fallback
        record = self._pending_tokens.get(token)
        if not record:
            logger.warning(f"Rejected invalid confirmation token: '{token}'")
            raise GateAuthorizationError(f"Invalid or unknown confirmation token: {token}")

        if time.time() > record["expires_at"]:
            del self._pending_tokens[token]
            logger.warning(f"Rejected expired confirmation token: '{token}'")
            raise GateAuthorizationError(f"Confirmation token {token} has expired")

        if record["action_name"] != action_name:
            logger.warning(
                f"Token {token} was issued for '{record['action_name']}', not '{action_name}'"
            )
            raise GateAuthorizationError(
                f"Token mismatch: issued for {record['action_name']} but used for {action_name}"
            )

        # Token is valid: consume it (one-time use)
        del self._pending_tokens[token]
        logger.info(f"Human Confirmation Token '{token}' verified and consumed for '{action_name}'.")
        return True
