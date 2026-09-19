"""System configuration module using Pydantic Settings and YAML."""

from pathlib import Path
from typing import Any
import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.exceptions import ConfigurationError


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    APP_NAME: str = "legalpilot-vn"
    APP_VERSION: str = "0.1.0"
    LOG_LEVEL: str = "INFO"

    # LLM settings
    GEMINI_API_KEY: str | None = None
    GOOGLE_CLOUD_PROJECT: str | None = None
    GOOGLE_CLOUD_LOCATION: str = "global"
    GOOGLE_GENAI_USE_VERTEXAI: bool = False

    OPENAI_API_BASE: str = "http://localhost:8000/v1"
    OPENAI_API_KEY: str = "sk-local-dummy"
    DEFAULT_MODEL: str = "gemini-2.5-flash"
    LOCAL_FALLBACK_MODEL: str = "openai/llama3.2"

    # Database settings
    SQLITE_DB_PATH: str = "data/enterprise_compliance.db"
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "legalpilot2026"

    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_GRPC_PORT: int = 6334
    QDRANT_COLLECTION_NAME: str = "vietnamese_legal_clauses"

    # Orchestration & Security guardrails
    MAX_REFINE_LOOPS: int = 3
    MAX_RETRIEVAL_HOPS: int = 2
    MAX_DOC_TRAVERSALS: int = 5
    STATUTE_CACHE_TTL_SECONDS: int = 86400  # 24 hours
    HUMAN_GATE_REQUIRE_TOKEN: bool = True
    DOS_QUERY_TIMEOUT_SECONDS: int = 12


def load_yaml_config(config_path: str | Path) -> dict[str, Any]:
    """Loads a YAML configuration file safely."""
    path = Path(config_path)
    if not path.exists():
        raise ConfigurationError(f"Config file not found at: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        raise ConfigurationError(f"Failed to parse YAML config at {path}: {e}") from e


# Global settings instance
settings = Settings()
