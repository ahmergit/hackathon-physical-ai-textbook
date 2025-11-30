"""
Text chunking logic for splitting textbook content into embedable chunks.
Uses tiktoken for accurate token counting with OpenAI models.
"""

import tiktoken
from typing import List


class TextChunker:
    """
    Chunks text into segments with specified token size and overlap.
    """

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 64, encoding_name: str = "cl100k_base"):
        """
        Initialize the chunker.

        Args:
            chunk_size: Maximum tokens per chunk
            chunk_overlap: Number of tokens to overlap between chunks
            encoding_name: Tiktoken encoding to use (cl100k_base for text-embedding-3-small)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding = tiktoken.get_encoding(encoding_name)

    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks based on token count.

        Args:
            text: Text to chunk

        Returns:
            List of text chunks
        """
        if not text.strip():
            return []

        # Encode text to tokens
        tokens = self.encoding.encode(text)

        # If text is smaller than chunk size, return as is
        if len(tokens) <= self.chunk_size:
            return [text]

        chunks = []
        start = 0

        while start < len(tokens):
            # Get chunk of tokens
            end = start + self.chunk_size
            chunk_tokens = tokens[start:end]

            # Decode back to text
            chunk_text = self.encoding.decode(chunk_tokens)
            chunks.append(chunk_text)

            # Move start position with overlap
            start += self.chunk_size - self.chunk_overlap

            # Prevent infinite loop
            if start >= len(tokens):
                break

        return chunks

    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text.

        Args:
            text: Text to count tokens for

        Returns:
            Number of tokens
        """
        return len(self.encoding.encode(text))

    def chunk_with_metadata(self, text: str, metadata: dict) -> List[dict]:
        """
        Chunk text and attach metadata to each chunk.

        Args:
            text: Text to chunk
            metadata: Metadata to attach to each chunk

        Returns:
            List of dictionaries with 'text', 'metadata', 'chunk_index', and 'token_count'
        """
        chunks = self.chunk_text(text)

        return [
            {
                "text": chunk,
                "metadata": metadata,
                "chunk_index": i,
                "token_count": self.count_tokens(chunk),
            }
            for i, chunk in enumerate(chunks)
        ]
