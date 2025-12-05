"""
Configuration settings for LogAgent.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class LogAgentConfig:
    """Configuration for LogAgent system."""

    # Qdrant settings
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    collection_name: str = "code_chunks"
    use_memory_db: bool = False

    # Embedding settings
    embedding_model: str = "intfloat/e5-base-v2"
    device: Optional[str] = None  # 'cuda', 'cpu', or None for auto-detect

    # Code splitting settings
    small_file_threshold: int = 1000  # Characters

    # Search settings
    default_num_results: int = 5
    default_min_score: float = 0.3

    @classmethod
    def for_development(cls):
        """Get configuration for development/testing."""
        return cls(
            use_memory_db=True,
            embedding_model="intfloat/e5-small-v2"  # Faster for dev
        )

    @classmethod
    def for_production(cls):
        """Get configuration for production."""
        return cls(
            use_memory_db=False,
            qdrant_host="localhost",
            qdrant_port=6333,
            embedding_model="intfloat/e5-base-v2"
        )
