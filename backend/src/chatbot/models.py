"""
Data models for the chatbot feature.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class TextbookChunk:
    """
    Represents an indexed chunk of textbook content stored in Qdrant.
    """
    id: UUID
    content: str
    chapter: str
    chapter_title: str
    section: str
    section_title: str
    page_path: str  # Full URL with anchor (e.g., /docs/chapter-01/intro#heading)
    chunk_index: int
    token_count: int
    created_at: datetime
    heading: Optional[str] = None  # The specific section heading
    anchor: Optional[str] = None   # URL anchor fragment (e.g., "the-scale-of-transformation")

    def __post_init__(self):
        """Validate chunk data."""
        if self.token_count > 512:
            raise ValueError(f"Chunk token count {self.token_count} exceeds maximum of 512")
        if not self.content.strip():
            raise ValueError("Chunk content cannot be empty")


@dataclass
class Citation:
    """
    Reference to a specific textbook location.
    """
    chapter: str
    section: str
    title: str
    url: str
    relevance_score: float
    snippet: Optional[str] = None

    def __post_init__(self):
        """Validate citation data."""
        if not 0.0 <= self.relevance_score <= 1.0:
            raise ValueError(f"Relevance score {self.relevance_score} must be between 0.0 and 1.0")


@dataclass
class RetrievalResult:
    """
    Result from Qdrant vector search.
    """
    chunks: list[TextbookChunk]
    scores: list[float]
    total_tokens: int

    def to_context_string(self) -> str:
        """Format chunks as context for LLM."""
        return "\n\n---\n\n".join(
            f"[{chunk.chapter_title} > {chunk.section_title}]\n{chunk.content}"
            for chunk in self.chunks
        )


@dataclass
class AgentContext:
    """
    Context passed through the agent execution.
    """
    conversation_history: list[dict] = field(default_factory=list)
    selected_text: Optional[str] = None
    quick_action: Optional[str] = None
    retrieved_chunks: list[TextbookChunk] = field(default_factory=list)
    citations: list[Citation] = field(default_factory=list)
