"""
Textbook ingestion pipeline.
Reads markdown files from book-source/docs/, chunks content, embeds, and stores in Qdrant.
"""

import asyncio
import os
import sys
import uuid
from pathlib import Path
from datetime import datetime
from typing import List

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

import openai
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from parsers.markdown_parser import MarkdownParser
from chunker import TextChunker

# Settings from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION_NAME", os.getenv("QDRANT_COLLECTION", "textbook_chunks"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "512"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))

# Initialize OpenAI client
openai_client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)


async def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for multiple texts."""
    if not texts:
        return []
    response = await openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )
    return [item.embedding for item in response.data]


async def ingest_textbook():
    """
    Main ingestion pipeline:
    1. Scan book-source/docs/ for markdown files
    2. Parse content and extract metadata
    3. Chunk into 512-token segments
    4. Generate embeddings
    5. Upsert to Qdrant
    """
    print("=" * 60)
    print("TEXTBOOK INGESTION PIPELINE")
    print("=" * 60)

    # Initialize components
    parser = MarkdownParser()
    chunker = TextChunker(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY if QDRANT_API_KEY else None,
        timeout=120,  # Increase timeout to 120 seconds for cloud operations
    )

    # Ensure collection exists (recreate to fix vector config)
    from qdrant_client.models import VectorParams, Distance
    try:
        # Delete existing collection to reset
        client.delete_collection(QDRANT_COLLECTION)
        print(f"📦 Deleted existing collection '{QDRANT_COLLECTION}'")
    except:
        pass
    
    print(f"📦 Creating collection '{QDRANT_COLLECTION}'...")
    client.create_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    )
    print(f"  ✓ Collection created")

    # Find book-source directory
    project_root = Path(__file__).parent.parent.parent
    docs_dir = project_root / "book-source" / "docs"

    if not docs_dir.exists():
        print(f"✗ Error: Docs directory not found at {docs_dir}")
        return

    print(f"📁 Scanning: {docs_dir}")

    # Find all markdown files
    md_files = list(docs_dir.glob("**/*.md")) + list(docs_dir.glob("**/*.mdx"))
    print(f"📄 Found {len(md_files)} markdown files")

    if not md_files:
        print("✗ No markdown files found")
        return

    # Process each file
    all_points = []
    total_chunks = 0

    for file_path in md_files:
        print(f"\n📖 Processing: {file_path.relative_to(docs_dir)}")

        try:
            # Parse markdown by sections (each section gets its own anchor)
            sections = parser.parse_file_by_sections(file_path)

            if not sections:
                print(f"  ⚠ Skipping empty file")
                continue

            print(f"  📑 Found {len(sections)} sections")

            for section in sections:
                if not section["content"].strip():
                    continue

                # Chunk this section's content
                chunks = chunker.chunk_with_metadata(
                    text=section["content"],
                    metadata=section
                )

                heading_info = f" [{section['heading']}]" if section.get('heading') else ""
                print(f"    📝 Section{heading_info}: {len(chunks)} chunks -> {section['page_path']}")

                # Generate embeddings in batch
                texts = [chunk["text"] for chunk in chunks]
                embeddings = await generate_embeddings_batch(texts)

                # Create Qdrant points
                for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                    point_id = str(uuid.uuid4())

                    payload = {
                        "content": chunk["text"],
                        "chapter": section["chapter"],
                        "chapter_title": section["chapter_title"],
                        "section": section["section"],
                        "section_title": section["section_title"],
                        "heading": section.get("heading"),  # The specific heading for this section
                        "anchor": section.get("anchor"),    # The anchor fragment
                        "page_path": section["page_path"],  # Full URL with anchor
                        "base_page_path": section.get("base_page_path", section["page_path"]),
                        "chunk_index": chunk["chunk_index"],
                        "token_count": chunk["token_count"],
                        "created_at": datetime.utcnow().isoformat(),
                    }

                    point = PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload=payload
                    )

                    all_points.append(point)
                    total_chunks += 1

        except Exception as e:
            print(f"  ✗ Error processing file: {e}")
            import traceback
            traceback.print_exc()
            continue

    # Upsert all points to Qdrant
    if all_points:
        print(f"\n📤 Uploading {len(all_points)} chunks to Qdrant...")

        # Upload in smaller batches of 20 for better reliability with cloud instances
        batch_size = 20
        for i in range(0, len(all_points), batch_size):
            batch = all_points[i:i + batch_size]
            try:
                client.upsert(
                    collection_name=QDRANT_COLLECTION,
                    points=batch
                )
                print(f"  ✓ Uploaded batch {i // batch_size + 1} ({len(batch)} points)")
            except Exception as e:
                print(f"  ⚠ Batch {i // batch_size + 1} failed, retrying with smaller batch...")
                # Retry with individual points if batch fails
                for j, point in enumerate(batch):
                    try:
                        client.upsert(
                            collection_name=QDRANT_COLLECTION,
                            points=[point]
                        )
                    except Exception as e2:
                        print(f"    ✗ Point {i + j} failed: {e2}")

        print(f"\n✅ Ingestion complete!")
        print(f"  Total files processed: {len(md_files)}")
        print(f"  Total chunks created: {total_chunks}")

        # Verify collection
        collection_info = client.get_collection(QDRANT_COLLECTION)
        print(f"  Collection points count: {collection_info.points_count}")

    else:
        print("\n✗ No content to upload")


if __name__ == "__main__":
    asyncio.run(ingest_textbook())
