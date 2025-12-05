"""
Embedding generator using E5 model for converting code into semantic vectors.
"""

from typing import List, Union
from sentence_transformers import SentenceTransformer
import torch


class E5Embedder:
    """Handles code embedding generation using E5 model."""

    def __init__(self, model_name: str = "intfloat/e5-base-v2", device: str = None):
        """
        Initialize the E5 embedder.

        Args:
            model_name: Name of the E5 model to use
            device: Device to run the model on ('cuda', 'cpu', or None for auto-detect)
        """
        if device is None:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'

        print(f"Loading E5 model '{model_name}' on device: {device}")
        self.model = SentenceTransformer(model_name, device=device)
        self.device = device
        self.embedding_dim = self.model.get_sentence_embedding_dimension()

    def embed_code(self, code: str, prefix: str = "passage: ") -> List[float]:
        """
        Generate embedding for a single code snippet.

        Args:
            code: The code string to embed
            prefix: Prefix for the model (E5 models use 'passage:' for documents)

        Returns:
            List of floats representing the embedding vector
        """
        # E5 models expect a prefix for better performance
        text = f"{prefix}{code}"
        embedding = self.model.encode(text, convert_to_tensor=False, normalize_embeddings=True)
        return embedding.tolist()

    def embed_batch(self, codes: List[str], prefix: str = "passage: ") -> List[List[float]]:
        """
        Generate embeddings for multiple code snippets efficiently.

        Args:
            codes: List of code strings to embed
            prefix: Prefix for the model

        Returns:
            List of embedding vectors
        """
        # Add prefix to all texts
        texts = [f"{prefix}{code}" for code in codes]

        embeddings = self.model.encode(
            texts,
            convert_to_tensor=False,
            normalize_embeddings=True,
            batch_size=32,
            show_progress_bar=True
        )

        return embeddings.tolist()

    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a search query.

        Args:
            query: The query string (e.g., error log or question)

        Returns:
            List of floats representing the embedding vector
        """
        # For queries, E5 models use 'query:' prefix
        text = f"query: {query}"
        embedding = self.model.encode(text, convert_to_tensor=False, normalize_embeddings=True)
        return embedding.tolist()

    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embedding vectors."""
        return self.embedding_dim
