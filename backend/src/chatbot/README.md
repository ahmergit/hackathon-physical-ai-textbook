# Chatbot Module

AI-powered chatbot for the Physical AI textbook, using OpenAI Agents SDK and Qdrant vector database.

## Architecture

```
chatbot/
├── agent.py              # Main textbook agent
├── models.py             # Data models (TextbookChunk, Citation, etc.)
├── context.py            # Run context management
├── prompts.py            # System prompts and templates
├── tools/
│   └── qdrant_retriever.py  # Vector search tools
└── guardrails/
    └── topic_guard.py       # Topic restriction guardrail
```

## Components

### Agent (`agent.py`)

The main textbook agent configured with:
- **Model**: GPT-4o (configurable via settings)
- **Tools**: `search_textbook`, `search_textbook_by_chapter`
- **Guardrails**: `topic_guardrail` (restricts to textbook topics)
- **Parallel tool calls**: Enabled for performance

### Tools (`tools/qdrant_retriever.py`)

**`search_textbook(query, top_k=5)`**
- Performs semantic search over entire textbook
- Returns top-k most relevant chunks
- Minimum relevance score: 0.7

**`search_textbook_by_chapter(chapter, query, top_k=3)`**
- Searches within a specific chapter
- Useful for focused queries

### Guardrails (`guardrails/topic_guard.py`)

**`topic_guardrail`**
- Input guardrail that checks if questions are on-topic
- Uses GPT-4o-mini for fast classification
- Provides suggested topics if off-topic
- Runs in parallel with main agent (low latency)

### Context (`context.py`)

**`ChatbotRunContext`**
- Stores state during agent execution
- Manages retrieved chunks and citations
- Shared across tools via `ctx.context`

### Models (`models.py`)

- **TextbookChunk**: Indexed content in Qdrant
- **Citation**: Reference to textbook location
- **RetrievalResult**: Vector search results
- **AgentContext**: Agent execution context

## Usage

### Basic Query

```python
from agents import Runner
from chatbot.agent import create_textbook_agent
from chatbot.context import ChatbotRunContext

# Create agent
agent = create_textbook_agent()

# Create run context
ctx = ChatbotRunContext()

# Run query
result = await Runner.run(
    agent=agent,
    messages=[{"role": "user", "content": "What is Physical AI?"}],
    context=ctx
)

print(result.final_output)
print(ctx.citations)  # Citations generated during execution
```

### With Text Selection

```python
agent = create_textbook_agent(
    selected_text="Physical AI systems interact with the real world"
)

result = await Runner.run(agent, messages=[...], context=ctx)
```

### With Quick Actions

```python
agent = create_textbook_agent(quick_action="summarize")
result = await Runner.run(agent, messages=[...], context=ctx)
```

### Streaming

```python
result = Runner.run_streamed(agent, messages=[...], context=ctx)

async for event in result.stream_events():
    if event.type == "raw_response_event":
        print(event.data.delta, end="", flush=True)
```

## Configuration

Set in `backend/src/config.py`:

```python
openai_api_key: str              # OpenAI API key
qdrant_url: str                  # Qdrant instance URL
qdrant_api_key: str              # Qdrant API key
qdrant_collection: str           # Collection name ("physical_ai_textbook")
chat_model: str                  # GPT model ("gpt-4o")
embedding_model: str             # Embedding model ("text-embedding-3-small")
max_tokens: int                  # Max tokens per response (8000)
embedding_dimension: int         # Embedding dimensions (1536)
chunk_size: int                  # Chunk size in tokens (512)
chunk_overlap: int               # Overlap between chunks (64)
```

## Testing

```bash
# Run unit tests
pytest tests/chatbot/

# Run specific test
pytest tests/chatbot/test_agent.py -v

# Run with coverage
pytest tests/chatbot/ --cov=chatbot --cov-report=html
```

## Data Ingestion

See `scripts/ingest_textbook.py` for populating Qdrant with textbook content.

```bash
# Setup Qdrant collection
python scripts/setup_qdrant.py

# Ingest textbook
python scripts/ingest_textbook.py
```

## Prompts

System prompts are defined in `prompts.py`:
- **SYSTEM_PROMPT**: Base instructions for the agent
- **SELECTED_TEXT_PROMPT**: Context when user selects text
- **QUICK_ACTION_PROMPTS**: Modifiers for explain/summarize/simplify
- **OFF_TOPIC_RESPONSE**: Response for out-of-scope questions

## Citations

Citations are automatically generated during retrieval:
- Each retrieved chunk creates a citation
- Citations include chapter, section, title, URL, relevance score
- Stored in `ctx.context.citations`
- Returned with API responses

## Error Handling

- **Empty search results**: Returns "No relevant content found"
- **Off-topic questions**: Guardrail triggers, suggests relevant topics
- **API errors**: Logged and returned as error events in streaming
- **Invalid input**: Validated by Pydantic schemas

## Performance

- **Initial response**: < 1s (token generation)
- **Full response**: < 5s (typical questions)
- **Retrieval**: ~100-200ms (Qdrant)
- **Embedding**: ~50-100ms (OpenAI)
- **Topic check**: ~200-300ms (GPT-4o-mini, parallel)

## Security

- API keys stored in environment variables
- Input validation via Pydantic
- Maximum message length: 5000 characters
- Maximum conversation history: 50 messages (10 used)
- No persistent storage of conversations
