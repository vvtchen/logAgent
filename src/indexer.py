"""
Code indexing pipeline that combines AST splitting, embedding, and vector storage.
"""

from typing import List, Dict, Any
from pathlib import Path
from .code_splitter import ASTCodeSplitter, CodeChunk
from .embedder import E5Embedder
from .vector_db import QdrantVectorDB


class CodeIndexer:
    """Orchestrates the code indexing pipeline."""

    def __init__(
        self,
        embedder: E5Embedder,
        vector_db: QdrantVectorDB,
        splitter: ASTCodeSplitter = None
    ):
        """
        Initialize the code indexer.

        Args:
            embedder: E5 embedding model
            vector_db: Qdrant vector database
            splitter: AST code splitter (creates default if not provided)
        """
        self.embedder = embedder
        self.vector_db = vector_db
        self.splitter = splitter or ASTCodeSplitter()

    def index_file(self, file_path: str) -> int:
        """
        Index a single Python file.

        Args:
            file_path: Path to the Python file

        Returns:
            Number of chunks indexed
        """
        print(f"Indexing file: {file_path}")

        # Split the file into chunks
        chunks = self.splitter.split_python_file(file_path)

        if not chunks:
            print(f"No chunks extracted from {file_path}")
            return 0

        # Generate embeddings
        code_texts = [chunk.content for chunk in chunks]
        embeddings = self.embedder.embed_batch(code_texts)

        # Prepare metadata
        metadatas = [chunk.get_metadata() for chunk in chunks]

        # Insert into vector database
        self.vector_db.insert_batch(embeddings, metadatas)

        print(f"Indexed {len(chunks)} chunks from {file_path}")
        return len(chunks)

    def index_directory(self, directory_path: str, pattern: str = "**/*.py") -> int:
        """
        Index all Python files in a directory.

        Args:
            directory_path: Path to the directory
            pattern: Glob pattern for files to index

        Returns:
            Total number of chunks indexed
        """
        print(f"Indexing directory: {directory_path}")

        dir_path = Path(directory_path)
        total_chunks = 0

        python_files = list(dir_path.glob(pattern))
        print(f"Found {len(python_files)} Python files")

        for file_path in python_files:
            if file_path.is_file():
                try:
                    num_chunks = self.index_file(str(file_path))
                    total_chunks += num_chunks
                except Exception as e:
                    print(f"Error indexing {file_path}: {e}")

        print(f"\nTotal chunks indexed: {total_chunks}")
        return total_chunks

    def search_similar_code(
        self,
        query: str,
        limit: int = 5,
        score_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Search for code chunks similar to a query.

        Args:
            query: Search query (error log, description, etc.)
            limit: Maximum number of results
            score_threshold: Minimum similarity score

        Returns:
            List of similar code chunks with metadata
        """
        # Generate query embedding
        query_vector = self.embedder.embed_query(query)

        # Search in vector database
        results = self.vector_db.search(
            query_vector=query_vector,
            limit=limit,
            score_threshold=score_threshold
        )

        return results

    def initialize_collection(self):
        """Initialize the vector database collection."""
        vector_size = self.embedder.get_embedding_dimension()
        self.vector_db.create_collection(vector_size=vector_size)
        print(f"Initialized collection with vector size: {vector_size}")
