"""Human Confirmation Token Gate for Guarded Actions (Requirement R2 & Vector 8)."""

import secrets
import time
from typing import Any

from src.core.exceptions import GateAuthorizationError
from src.core.logger import logger


class HumanTokenGate:
    """Manages one-time tokens required to execute irreversible write actions."""

    def __init__(self, token_expiry_seconds: int = 300):
        self.token_expiry_seconds = token_expiry_seconds
        self._pending_tokens: dict[str, dict[str, Any]] = {}

    def generate_token(self, action_name: str, payload_summary: str) -> str:
        """Generates a secure, short-lived token for an action requiring human approval."""
        token = f"CONFIRM-{secrets.token_hex(4).upper()}"
        self._pending_tokens[token] = {
            "action_name": action_name,
            "payload_summary": payload_summary,
            "created_at": time.time(),
        }
        logger.info(
            f"Generated Human Confirmation Token '{token}' for action '{action_name}'. "
            f"Requires approval within {self.token_expiry_seconds}s."
        )
        return token

    def verify_token(self, token: str, action_name: str) -> bool:
        """Verifies and consumes a confirmation token. Raises error if invalid or expired."""
        record = self._pending_tokens.get(token)
        if not record:
            logger.warning(f"Rejected invalid confirmation token: '{token}'")
            raise GateAuthorizationError(f"Invalid or unknown confirmation token: {token}")

        if time.time() - record["created_at"] > self.token_expiry_seconds:
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
