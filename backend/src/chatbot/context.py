"""
Agent context management using OpenAI Agents SDK RunContext.
"""

from typing import Optional, List
from .models import TextbookChunk, Citation


class ChatbotRunContext:
    """
    Context stored in OpenAI Agents SDK RunContext (ctx.context).
    This is used to share state across tool calls within a single run.
    """

    def __init__(self):
        """Initialize empty context."""
        self.selected_text: Optional[str] = None
        self.quick_action: Optional[str] = None
        self.retrieved_chunks: List[TextbookChunk] = []
        self.citations: List[Citation] = []

    def add_retrieval_result(self, chunks: List[TextbookChunk], scores: List[float]):
        """
        Add retrieval results to context.

        Args:
            chunks: Retrieved textbook chunks
            scores: Relevance scores for each chunk
        """
        self.retrieved_chunks = chunks

        # Generate citations from chunks
        self.citations = []
        for chunk, score in zip(chunks, scores):
            # Use heading as title if available, otherwise fall back to section_title
            if chunk.heading:
                title = f"{chunk.section_title} > {chunk.heading}"
            else:
                title = chunk.section_title
            
            citation = Citation(
                chapter=chunk.chapter,
                section=chunk.section,
                title=title,
                url=chunk.page_path,  # page_path now includes anchor (e.g., /docs/chapter-01/intro#heading)
                relevance_score=score,
                snippet=chunk.content[:150] + "..." if len(chunk.content) > 150 else chunk.content
            )
            self.citations.append(citation)

    def get_context_string(self) -> str:
        """
        Format retrieved chunks as context string for LLM.

        Returns:
            Formatted context with all retrieved chunks
        """
        if not self.retrieved_chunks:
            return "No relevant textbook content found."

        chunks_text = "\n\n---\n\n".join(
            f"[Source: {chunk.chapter_title} > {chunk.section_title}]\n{chunk.content}"
            for chunk in self.retrieved_chunks
        )

        return f"TEXTBOOK CONTENT:\n\n{chunks_text}"
