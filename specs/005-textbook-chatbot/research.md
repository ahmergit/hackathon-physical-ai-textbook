# Research: Physical AI Textbook Chatbot

**Feature**: 005-textbook-chatbot  
**Date**: 2024-11-29  
**Status**: Complete

## Research Tasks

### 1. OpenAI Agents SDK Integration

**Decision**: Use OpenAI Agents SDK v0.6.x with custom function tools for Qdrant retrieval

**Rationale**:
- Native streaming support via `Runner.run_streamed()` with `RawResponsesStreamEvent` for token-by-token display
- Built-in guardrails system (`@input_guardrail`, `@output_guardrail`) for domain restriction
- Context management via `RunContextWrapper` for session-scoped state
- Custom function tools via `@function_tool` decorator for Qdrant integration
- Python-first design aligns with FastAPI backend

**Alternatives Considered**:
- LangChain: Too heavyweight, many abstractions not needed
- Raw OpenAI API: Would require manual agent loop, tool handling, and streaming
- Assistants API: Requires server-side session storage (violates no-persistence requirement)

**Key Patterns**:
```python
# Agent with custom tool
from agents import Agent, Runner, function_tool

@function_tool
async def search_textbook(query: str) -> str:
    """Search the Physical AI textbook for relevant content."""
    # Qdrant search implementation
    pass

agent = Agent(
    name="Physical AI Assistant",
    instructions="...",
    tools=[search_textbook],
    input_guardrails=[topic_guardrail],
)

# Streaming response
result = Runner.run_streamed(agent, input=user_message, context=session_context)
async for event in result.stream_events():
    if event.type == "raw_response_event":
        yield event.data.delta  # Token by token
```

---

### 2. Qdrant Vector Database Configuration

**Decision**: Use Qdrant Cloud with AsyncQdrantClient, COSINE distance, and payload filtering

**Rationale**:
- Async client integrates cleanly with FastAPI's async endpoints
- Cloud-hosted eliminates infrastructure management
- Payload filtering enables chapter/section-based filtering for citations
- Native Python client with type hints

**Configuration**:
```python
QDRANT_CONFIG = {
    "collection_name": "physical_ai_textbook",
    "vector_size": 1536,  # text-embedding-3-small
    "distance": Distance.COSINE,
    "payload_schema": {
        "chapter": "keyword",
        "section": "keyword", 
        "title": "text",
        "page": "integer",
        "content": "text",
    }
}
```

**Alternatives Considered**:
- Pinecone: Similar capabilities, but Qdrant has better local dev experience
- Chroma: Good for local, but less suitable for production cloud deployment
- PostgreSQL pgvector: Would add complexity to existing auth database

---

### 3. Embedding Strategy

**Decision**: Use OpenAI `text-embedding-3-small` with 512-token chunks and 64-token overlap

**Rationale**:
- 1536 dimensions provides good accuracy/cost balance
- 512 tokens ≈ 380 words, suitable for coherent textbook paragraphs
- 64-token overlap (12.5%) maintains context across chunk boundaries
- Lower cost than `text-embedding-3-large` with acceptable quality

**Chunking Strategy**:
```python
CHUNKING_CONFIG = {
    "chunk_size": 512,       # tokens
    "chunk_overlap": 64,     # tokens
    "separator": "\n\n",     # Prefer paragraph boundaries
    "length_function": tiktoken_len,
}
```

**Alternatives Considered**:
- text-embedding-3-large (3072 dims): Higher cost, marginal quality improvement
- text-embedding-ada-002: Legacy, replaced by text-embedding-3-small
- Sentence transformers: Would require self-hosting

---

### 4. Streaming Implementation

**Decision**: Use SSE (Server-Sent Events) via FastAPI's `StreamingResponse` with OpenAI Agents SDK streaming

**Rationale**:
- SSE is simpler than WebSockets for unidirectional streaming
- Native browser EventSource support
- FastAPI StreamingResponse works with async generators
- OpenAI Agents SDK provides `stream_events()` for token streaming

**Implementation Pattern**:
```python
from fastapi.responses import StreamingResponse

@router.post("/chat")
async def chat(request: ChatRequest):
    async def generate():
        result = Runner.run_streamed(agent, input=request.message, context=ctx)
        async for event in result.stream_events():
            if event.type == "raw_response_event":
                if isinstance(event.data, ResponseTextDeltaEvent):
                    yield f"data: {json.dumps({'type': 'delta', 'content': event.data.delta})}\n\n"
        yield f"data: {json.dumps({'type': 'done', 'citations': citations})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")
```

**Alternatives Considered**:
- WebSockets: More complex, bidirectional not needed
- Long polling: Poor UX for streaming
- Chunked transfer encoding: Less browser support than SSE

---

### 5. Session Context Management

**Decision**: Use in-memory context per request with conversation history passed as input

**Rationale**:
- No server-side persistence required (per spec)
- Frontend maintains conversation history in React state
- Each request includes full conversation context
- OpenAI Agents SDK `RunContextWrapper` for per-request metadata

**Context Structure**:
```python
@dataclass
class ChatSession:
    messages: list[dict]  # Conversation history from frontend
    selected_text: str | None  # Text selection context
    quick_action: str | None  # "explain", "summarize", "simplify"
```

**Alternatives Considered**:
- Server-side session storage: Violates no-persistence requirement
- JWT-encoded history: History can be large, exceeds token limits
- Redis session cache: Adds infrastructure, unnecessary complexity

---

### 6. Guardrails for Domain Restriction

**Decision**: Use OpenAI Agents SDK input guardrails with a topic-checking agent

**Rationale**:
- Native guardrail system handles tripwire logic automatically
- Parallel execution mode for low latency (guardrail runs with agent)
- Can use cheaper/faster model for guardrail checks
- Clean integration with agent lifecycle

**Implementation Pattern**:
```python
from agents import input_guardrail, GuardrailFunctionOutput, Agent, Runner

guardrail_agent = Agent(
    name="Topic Guard",
    model="gpt-4o-mini",  # Fast/cheap for classification
    instructions="Determine if the question relates to Physical AI or humanoid robotics.",
    output_type=TopicCheckOutput,
)

@input_guardrail
async def topic_guardrail(ctx, agent, input) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        tripwire_triggered=not result.final_output.is_on_topic,
        output_info=result.final_output,
    )
```

**Alternatives Considered**:
- Keyword filtering: Too brittle, false positives
- Embedding similarity threshold: Computationally expensive per request
- Post-processing filter: Bad UX (user waits for response then rejection)

---

### 7. Frontend ChatKit Integration

**Decision**: Use ChatKit React SDK with custom session token endpoint

**Rationale**:
- Pre-built chat UI components (message list, input, streaming)
- Theming and customization support
- React hooks for session management
- Markdown and code rendering built-in

**Integration Pattern**:
```typescript
import { ChatKit, useChatKit } from '@openai/chatkit-react';

export function TextbookChat() {
  const { control } = useChatKit({
    api: {
      async getClientSecret(existing) {
        const res = await fetch('/api/chatbot/session', { method: 'POST' });
        const { client_secret } = await res.json();
        return client_secret;
      },
    },
  });
  
  return <ChatKit control={control} className="chatbot-container" />;
}
```

**Note**: For custom backend (not OpenAI-hosted), we'll use the Advanced Integration pattern with custom streaming endpoint and ChatKit widgets for UI.

**Alternatives Considered**:
- Custom chat UI: Significant development effort
- Third-party chat widget: Less control, may not support streaming
- Headless approach: More flexible but more work

---

### 8. Text Selection Query Flow

**Decision**: Custom React component with Selection API and floating button

**Rationale**:
- Native Selection API is well-supported
- Floating button provides clear affordance
- Selected text passed as context to chat
- No special backend changes needed

**Implementation Pattern**:
```typescript
function useTextSelection() {
  const [selection, setSelection] = useState<string | null>(null);
  
  useEffect(() => {
    const handleSelection = () => {
      const text = window.getSelection()?.toString().trim();
      setSelection(text && text.length > 0 ? text : null);
    };
    document.addEventListener('selectionchange', handleSelection);
    return () => document.removeEventListener('selectionchange', handleSelection);
  }, []);
  
  return selection;
}
```

---

### 9. Citation Format

**Decision**: Inline citations with chapter/section references and deep links

**Rationale**:
- Citations appear in response text: "According to [Chapter 2, Section 2.3]..."
- Clickable links navigate to textbook location
- Metadata stored in Qdrant payload enables precise references

**Citation Structure**:
```typescript
interface Citation {
  chapter: string;
  section: string;
  title: string;
  url: string;  // Deep link to textbook page/anchor
  relevance_score: number;
}
```

---

### 10. Ingestion Pipeline

**Decision**: Python script processing Markdown files with metadata extraction

**Rationale**:
- Docusaurus content is Markdown-based
- Script reads frontmatter for chapter/section metadata
- Splits into chunks and generates embeddings
- Upserts to Qdrant with payload

**Pipeline Steps**:
1. Scan `book-source/docs/` for `.md` and `.mdx` files
2. Parse frontmatter for metadata (title, sidebar_position, etc.)
3. Extract chapter/section from directory structure
4. Clean markdown (remove JSX components, code blocks optionally)
5. Chunk with tiktoken tokenizer
6. Generate embeddings via OpenAI API
7. Upsert to Qdrant with metadata payload

---

## Dependencies to Add

### Backend (`backend/requirements.txt`)
```
# Chatbot dependencies
openai-agents>=0.6.0
qdrant-client>=1.7.0
tiktoken>=0.5.0
```

### Frontend (`book-source/package.json`)
```json
{
  "dependencies": {
    "@openai/chatkit-react": "^0.1.0"
  }
}
```

---

## Environment Variables

```env
# Chatbot Configuration
OPENAI_API_KEY=sk-...
QDRANT_URL=https://xxx.qdrant.io
QDRANT_API_KEY=...
QDRANT_COLLECTION=physical_ai_textbook

# Model Configuration  
CHAT_MODEL=gpt-4o
EMBEDDING_MODEL=text-embedding-3-small
MAX_TOKENS=8000
EMBEDDING_DIMENSION=1536
CHUNK_SIZE=512
CHUNK_OVERLAP=64
```

---

## Risk Mitigations

| Risk | Mitigation |
|------|------------|
| Hallucination despite RAG | Guardrails + strict system prompt + citation requirement |
| Slow retrieval | Qdrant HNSW indexing, limit to top-5 chunks |
| Large conversation context | Truncate older messages, summarize if needed |
| API rate limits | Implement exponential backoff, cache embeddings |
| Cost overrun | Use gpt-4o-mini for guardrails, monitor usage |
