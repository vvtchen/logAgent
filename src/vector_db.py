"""
Qdrant vector database handler for fast similarity search.
"""

from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)
from qdrant_client.http import models
import uuid


class QdrantVectorDB:
    """Handles interactions with Qdrant vector database."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        collection_name: str = "code_chunks",
        use_memory: bool = False
    ):
        """
        Initialize Qdrant client.

        Args:
            host: Qdrant server host
            port: Qdrant server port
            collection_name: Name of the collection to use
            use_memory: If True, use in-memory storage (for testing)
        """
        if use_memory:
            self.client = QdrantClient(":memory:")
        else:
            self.client = QdrantClient(host=host, port=port)

        self.collection_name = collection_name

    def create_collection(self, vector_size: int, distance: Distance = Distance.COSINE):
        """
        Create a new collection.

        Args:
            vector_size: Dimension of the embedding vectors
            distance: Distance metric to use (COSINE, EUCLID, DOT)
        """
        try:
            # Check if collection exists
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            if self.collection_name in collection_names:
                print(f"Collection '{self.collection_name}' already exists")
                return

            # Create collection
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=distance)
            )
            print(f"Created collection '{self.collection_name}' with vector size {vector_size}")

        except Exception as e:
            print(f"Error creating collection: {e}")
            raise

    def delete_collection(self):
        """Delete the collection."""
        try:
            self.client.delete_collection(collection_name=self.collection_name)
            print(f"Deleted collection '{self.collection_name}'")
        except Exception as e:
            print(f"Error deleting collection: {e}")

    def insert_chunk(
        self,
        vector: List[float],
        metadata: Dict[str, Any],
        chunk_id: Optional[str] = None
    ) -> str:
        """
        Insert a single code chunk into the database.

        Args:
            vector: Embedding vector
            metadata: Metadata about the code chunk
            chunk_id: Optional ID for the chunk (auto-generated if not provided)

        Returns:
            ID of the inserted chunk
        """
        if chunk_id is None:
            chunk_id = str(uuid.uuid4())

        point = PointStruct(
            id=chunk_id,
            vector=vector,
            payload=metadata
        )

        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )

        return chunk_id

    def insert_batch(
        self,
        vectors: List[List[float]],
        metadatas: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Insert multiple code chunks into the database.

        Args:
            vectors: List of embedding vectors
            metadatas: List of metadata dictionaries

        Returns:
            List of IDs for the inserted chunks
        """
        if len(vectors) != len(metadatas):
            raise ValueError("Number of vectors and metadatas must match")

        points = []
        ids = []

        for vector, metadata in zip(vectors, metadatas):
            chunk_id = str(uuid.uuid4())
            ids.append(chunk_id)

            point = PointStruct(
                id=chunk_id,
                vector=vector,
                payload=metadata
            )
            points.append(point)

        # Insert in batches
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            self.client.upsert(
                collection_name=self.collection_name,
                points=batch
            )

        print(f"Inserted {len(points)} chunks into the database")
        return ids

    def search(
        self,
        query_vector: List[float],
        limit: int = 5,
        score_threshold: Optional[float] = None,
        filter_conditions: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar code chunks.

        Args:
            query_vector: Query embedding vector
            limit: Maximum number of results to return
            score_threshold: Minimum similarity score (0-1)
            filter_conditions: Optional filters (e.g., {'chunk_type': 'function'})

        Returns:
            List of search results with metadata and scores
        """
        search_params = {
            "collection_name": self.collection_name,
            "query_vector": query_vector,
            "limit": limit
        }

        if score_threshold is not None:
            search_params["score_threshold"] = score_threshold

        if filter_conditions:
            # Build filter
            conditions = []
            for key, value in filter_conditions.items():
                conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    )
                )

            search_params["query_filter"] = Filter(must=conditions)

        results = self.client.search(**search_params)

        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.id,
                "score": result.score,
                "metadata": result.payload
            })

        return formatted_results

    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection."""
        try:
            info = self.client.get_collection(collection_name=self.collection_name)
            return {
                "name": self.collection_name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": info.status
            }
        except Exception as e:
            return {"error": str(e)}
