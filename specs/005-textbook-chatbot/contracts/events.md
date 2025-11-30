# SSE Events Schema

**Feature**: 005-textbook-chatbot  
**Date**: 2024-11-29

## Overview

The chat endpoint uses Server-Sent Events (SSE) to stream responses to the client. Each event follows the standard SSE format with a `data:` prefix and double newline terminator.

## Event Format

```
data: <JSON payload>\n\n
```

All payloads are JSON objects with a `type` field that indicates the event type.

---

## Event Types

### 1. Delta Event

Sent for each token/chunk of the response as it's generated.

```json
{
  "type": "delta",
  "content": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `"delta"` |
| `content` | string | The incremental text token (1-50 characters typically) |

**Example**:
```
data: {"type": "delta", "content": "Physical"}

data: {"type": "delta", "content": " AI"}

data: {"type": "delta", "content": " refers"}

data: {"type": "delta", "content": " to"}

data: {"type": "delta", "content": "..."}

```

---

### 2. Citation Event

Sent when a citation is identified during response generation.

```json
{
  "type": "citation",
  "citation": {
    "chapter": "string",
    "section": "string",
    "title": "string",
    "url": "string",
    "relevance_score": 0.0-1.0,
    "snippet": "string (optional)"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `"citation"` |
| `citation` | object | Citation details |
| `citation.chapter` | string | Chapter identifier (e.g., "chapter-01") |
| `citation.section` | string | Section identifier (e.g., "section-1-2") |
| `citation.title` | string | Human-readable title |
| `citation.url` | string | Deep link to textbook page |
| `citation.relevance_score` | float | Similarity score (0.0-1.0) |
| `citation.snippet` | string? | Brief excerpt (optional) |

**Example**:
```
data: {"type": "citation", "citation": {"chapter": "chapter-01", "section": "section-1-1", "title": "Introduction to Physical AI", "url": "/docs/chapter-01/intro", "relevance_score": 0.92, "snippet": "Physical AI represents a paradigm..."}}

```

---

### 3. Done Event

Sent when the response is complete. Contains all citations used.

```json
{
  "type": "done",
  "citations": [
    {
      "chapter": "string",
      "section": "string",
      "title": "string",
      "url": "string",
      "relevance_score": 0.0-1.0
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `"done"` |
| `citations` | array | All citations referenced in the response |

**Example**:
```
data: {"type": "done", "citations": [{"chapter": "chapter-01", "section": "section-1-1", "title": "Introduction to Physical AI", "url": "/docs/chapter-01/intro", "relevance_score": 0.92}, {"chapter": "chapter-02", "section": "section-2-1", "title": "Humanoid Robots Overview", "url": "/docs/chapter-02/overview", "relevance_score": 0.85}]}

```

---

### 4. Error Event

Sent when an error occurs during streaming.

```json
{
  "type": "error",
  "message": "string",
  "code": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `"error"` |
| `message` | string | Human-readable error message |
| `code` | string | Error code for programmatic handling |

**Error Codes**:
- `retrieval_failed` - Qdrant search failed
- `generation_failed` - LLM generation failed
- `timeout` - Request timed out
- `out_of_scope` - Question outside textbook domain
- `unknown` - Unexpected error

**Example**:
```
data: {"type": "error", "message": "Unable to retrieve relevant textbook sections. Please try again.", "code": "retrieval_failed"}

```

---

## Client Implementation

### JavaScript/TypeScript

```typescript
async function streamChat(request: ChatRequest, onEvent: (event: ChatStreamEvent) => void) {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (reader) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n\n');
    buffer = lines.pop() || '';

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6));
        onEvent(data);
      }
    }
  }
}
```

### React Hook

```typescript
function useChatStream() {
  const [content, setContent] = useState('');
  const [citations, setCitations] = useState<Citation[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);

  const sendMessage = async (message: string, history: ConversationMessage[]) => {
    setIsStreaming(true);
    setContent('');
    setCitations([]);

    await streamChat(
      { message, conversation_history: history },
      (event) => {
        switch (event.type) {
          case 'delta':
            setContent((prev) => prev + event.content);
            break;
          case 'citation':
            setCitations((prev) => [...prev, event.citation]);
            break;
          case 'done':
            setCitations(event.citations);
            setIsStreaming(false);
            break;
          case 'error':
            console.error(event.message);
            setIsStreaming(false);
            break;
        }
      }
    );
  };

  return { content, citations, isStreaming, sendMessage };
}
```

---

## Event Sequence

Typical successful response:

```
1. data: {"type": "delta", "content": "Physical"}
2. data: {"type": "delta", "content": " AI"}
3. data: {"type": "delta", "content": " is"}
   ... (many delta events)
4. data: {"type": "citation", "citation": {...}}
   ... (citation events as they're identified)
5. data: {"type": "delta", "content": "."}
6. data: {"type": "done", "citations": [...]}
```

Error during streaming:

```
1. data: {"type": "delta", "content": "Based on"}
2. data: {"type": "error", "message": "Generation interrupted", "code": "generation_failed"}
```

Out-of-scope question (immediate):

```
1. data: {"type": "error", "message": "This question is outside the scope...", "code": "out_of_scope"}
```

---

## Rate Limiting

SSE connections are subject to standard rate limits:
- Max concurrent connections per client: 3
- Max message length: 5000 characters
- Timeout: 60 seconds per response

---

## Browser Compatibility

SSE is supported in all modern browsers:
- Chrome 6+
- Firefox 6+
- Safari 5+
- Edge 79+

For older browsers, consider a polyfill or fallback to long polling.
