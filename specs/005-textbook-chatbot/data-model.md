# Data Model: Physical AI Textbook Chatbot

**Feature**: 005-textbook-chatbot  
**Date**: 2024-11-29

## Overview

This document defines the data entities for the textbook chatbot. Note: No persistent storage for conversations—all chat data exists only in memory/client state during the session.

---

## Entities

### 1. TextbookChunk (Qdrant)

Represents an indexed chunk of textbook content stored in Qdrant.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | UUID | Unique chunk identifier | `550e8400-e29b-41d4-a716-446655440000` |
| `vector` | float[1536] | Embedding from text-embedding-3-small | `[0.023, -0.041, ...]` |
| `content` | string | Raw text content of the chunk | "Physical AI refers to..." |
| `chapter` | string | Chapter identifier | "chapter-01" |
| `chapter_title` | string | Human-readable chapter title | "Introduction to Physical AI" |
| `section` | string | Section identifier | "section-1-2" |
| `section_title` | string | Human-readable section title | "What is Embodied Intelligence?" |
| `page_path` | string | URL path in Docusaurus site | "/docs/chapter-01/intro" |
| `chunk_index` | integer | Position of chunk within document | 3 |
| `token_count` | integer | Number of tokens in chunk | 487 |
| `created_at` | datetime | When chunk was indexed | "2024-11-29T10:30:00Z" |

**Qdrant Collection Configuration**:
```python
{
    "collection_name": "physical_ai_textbook",
    "vectors_config": VectorParams(
        size=1536,
        distance=Distance.COSINE,
    ),
    "payload_schema": {
        "chapter": PayloadSchemaType.KEYWORD,
        "section": PayloadSchemaType.KEYWORD,
        "page_path": PayloadSchemaType.KEYWORD,
        "chunk_index": PayloadSchemaType.INTEGER,
    }
}
```

---

### 2. ChatMessage (Client-side only)

Represents a single message in the conversation. Stored in React state, not persisted.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Unique message ID (client-generated) | "msg_1732880123456" |
| `role` | enum | "user" \| "assistant" | "assistant" |
| `content` | string | Message text (may include markdown) | "Physical AI is..." |
| `citations` | Citation[] | References to textbook sections | See Citation entity |
| `timestamp` | datetime | When message was created | "2024-11-29T10:30:00Z" |
| `status` | enum | "streaming" \| "complete" \| "error" | "complete" |

**TypeScript Definition**:
```typescript
interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
  timestamp: Date;
  status: 'streaming' | 'complete' | 'error';
}
```

---

### 3. Citation

Reference to a specific textbook location, included in assistant messages.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `chapter` | string | Chapter identifier | "chapter-02" |
| `section` | string | Section identifier | "section-2-3" |
| `title` | string | Section title | "Humanoid Robot Design" |
| `url` | string | Deep link to textbook page | "/docs/chapter-02/design#section-2-3" |
| `relevance_score` | float | Similarity score from retrieval | 0.89 |
| `snippet` | string | Brief excerpt from cited content | "...key principles of..." |

**TypeScript Definition**:
```typescript
interface Citation {
  chapter: string;
  section: string;
  title: string;
  url: string;
  relevance_score: number;
  snippet?: string;
}
```

---

### 4. ChatSession (Client-side only)

Represents the current chat session state. Managed in React context.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `sessionId` | string | Client-generated session ID | "session_abc123" |
| `messages` | ChatMessage[] | Conversation history | [...messages] |
| `isStreaming` | boolean | Whether response is being streamed | false |
| `selectedText` | string \| null | Currently selected textbook text | "Physical AI refers to..." |
| `lastQuickAction` | string \| null | Last quick action used | "explain" |

**TypeScript Definition**:
```typescript
interface ChatSession {
  sessionId: string;
  messages: ChatMessage[];
  isStreaming: boolean;
  selectedText: string | null;
  lastQuickAction: 'explain' | 'summarize' | 'simplify' | null;
}
```

---

### 5. ChatRequest (API)

Request payload sent to the `/chat` endpoint.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | Yes | User's question or query |
| `conversation_history` | ConversationMessage[] | No | Previous messages for context |
| `selected_text` | string | No | Text selected from textbook page |
| `quick_action` | string | No | "explain" \| "summarize" \| "simplify" |

**Pydantic Definition**:
```python
from pydantic import BaseModel, Field
from typing import Literal

class ConversationMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    conversation_history: list[ConversationMessage] = Field(default_factory=list)
    selected_text: str | None = Field(None, max_length=5000)
    quick_action: Literal["explain", "summarize", "simplify"] | None = None
```

---

### 6. ChatStreamEvent (API Response)

SSE event sent during streaming response.

| Event Type | Payload | Description |
|------------|---------|-------------|
| `delta` | `{ content: string }` | Incremental text token |
| `citation` | `Citation` | Citation reference found |
| `done` | `{ citations: Citation[] }` | Stream complete |
| `error` | `{ message: string, code: string }` | Error occurred |

**TypeScript Event Definitions**:
```typescript
type ChatStreamEvent =
  | { type: 'delta'; content: string }
  | { type: 'citation'; citation: Citation }
  | { type: 'done'; citations: Citation[] }
  | { type: 'error'; message: string; code: string };
```

---

### 7. RetrievalResult (Internal)

Result from Qdrant vector search, used internally by the agent.

| Field | Type | Description |
|-------|------|-------------|
| `chunks` | TextbookChunk[] | Retrieved chunks |
| `scores` | float[] | Relevance scores |
| `total_tokens` | integer | Total tokens in retrieved context |

**Python Definition**:
```python
@dataclass
class RetrievalResult:
    chunks: list[TextbookChunk]
    scores: list[float]
    total_tokens: int
    
    def to_context_string(self) -> str:
        """Format chunks as context for LLM."""
        return "\n\n---\n\n".join(
            f"[{c.chapter_title} > {c.section_title}]\n{c.content}"
            for c in self.chunks
        )
```

---

### 8. AgentContext (Internal)

Context passed through OpenAI Agents SDK `RunContextWrapper`.

| Field | Type | Description |
|-------|------|-------------|
| `conversation_history` | list[dict] | Messages for LLM context |
| `selected_text` | str \| None | User-selected text |
| `quick_action` | str \| None | Quick action modifier |
| `retrieved_chunks` | list[TextbookChunk] | Retrieved context |
| `citations` | list[Citation] | Citations to include in response |

**Python Definition**:
```python
from dataclasses import dataclass, field

@dataclass
class AgentContext:
    conversation_history: list[dict] = field(default_factory=list)
    selected_text: str | None = None
    quick_action: str | None = None
    retrieved_chunks: list[TextbookChunk] = field(default_factory=list)
    citations: list[Citation] = field(default_factory=list)
```

---

## Entity Relationships

```
┌─────────────────┐
│  ChatSession    │ (Client-side React state)
│  - messages[]   │
│  - selectedText │
└────────┬────────┘
         │ contains
         ▼
┌─────────────────┐
│  ChatMessage    │ (Client-side)
│  - citations[]  │
└────────┬────────┘
         │ references
         ▼
┌─────────────────┐
│   Citation      │ (Links to textbook)
│   - url         │
└────────┬────────┘
         │ points to
         ▼
┌─────────────────┐
│ TextbookChunk   │ (Qdrant storage)
│ - content       │
│ - chapter       │
│ - section       │
│ - page_path     │
└─────────────────┘
```

---

## State Transitions

### Message Lifecycle
```
[User Types] → [Streaming] → [Complete]
                    │
                    └─→ [Error] (on failure)
```

### Session Lifecycle
```
[New Session] → [Active] → [Cleared]
     │              │           │
     │              │           └─→ [New Session] (on Clear Chat)
     │              │
     │              └─→ [Active] (continues with messages)
     │
     └─→ [Closed] (on page navigation/refresh - all data lost)
```

---

## Validation Rules

| Entity | Field | Rule |
|--------|-------|------|
| ChatRequest | message | 1-5000 characters |
| ChatRequest | selected_text | Max 5000 characters |
| ChatRequest | conversation_history | Max 50 messages |
| TextbookChunk | token_count | Max 512 tokens |
| Citation | relevance_score | 0.0-1.0 range |
