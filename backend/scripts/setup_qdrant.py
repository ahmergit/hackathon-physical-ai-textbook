"""
Script to set up Qdrant collection for the Physical AI textbook.
Creates the collection with proper schema if it doesn't exist.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PayloadSchemaType
from config import settings


async def setup_qdrant_collection():
    """
    Create Qdrant collection with proper configuration.
    """
    print(f"Connecting to Qdrant at {settings.qdrant_url}...")

    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key if settings.qdrant_api_key else None,
    )

    collection_name = settings.qdrant_collection

    # Check if collection exists
    try:
        collection_info = client.get_collection(collection_name)
        print(f"✓ Collection '{collection_name}' already exists")
        print(f"  Points count: {collection_info.points_count}")
        print(f"  Status: {collection_info.status}")
        return
    except Exception:
        print(f"Collection '{collection_name}' does not exist. Creating...")

    # Create collection
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=settings.embedding_dimension,
            distance=Distance.COSINE,
        ),
    )

    # Create payload index for filtering
    client.create_payload_index(
        collection_name=collection_name,
        field_name="chapter",
        field_schema=PayloadSchemaType.KEYWORD,
    )

    client.create_payload_index(
        collection_name=collection_name,
        field_name="section",
        field_schema=PayloadSchemaType.KEYWORD,
    )

    client.create_payload_index(
        collection_name=collection_name,
        field_name="page_path",
        field_schema=PayloadSchemaType.KEYWORD,
    )

    print(f"✓ Created collection '{collection_name}'")
    print(f"  Vector size: {settings.embedding_dimension}")
    print(f"  Distance metric: COSINE")
    print(f"  Payload indexes: chapter, section, page_path")


if __name__ == "__main__":
    asyncio.run(setup_qdrant_collection())
