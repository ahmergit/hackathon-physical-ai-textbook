# Quickstart Guide: Physical AI Textbook Chatbot

**Feature**: 005-textbook-chatbot  
**Date**: 2024-11-29

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (for local Qdrant, optional)
- OpenAI API key
- Qdrant Cloud account (or local instance)

---

## 1. Environment Setup

### Create `.env` file in `backend/`

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-api-key-here

# Qdrant Configuration
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION=physical_ai_textbook

# Model Configuration
CHAT_MODEL=gpt-4o
EMBEDDING_MODEL=text-embedding-3-small
MAX_TOKENS=8000
EMBEDDING_DIMENSION=1536
CHUNK_SIZE=512
CHUNK_OVERLAP=64

# Optional: For local Qdrant
# QDRANT_URL=http://localhost:6333
# QDRANT_API_KEY=
```

### Create `.env` file in `book-source/`

```env
# API endpoint for chatbot
VITE_CHATBOT_API_URL=http://localhost:8000/api
```

---

## 2. Backend Setup

### Install dependencies

```bash
cd backend
pip install -r requirements.txt

# Chatbot-specific packages
pip install openai-agents>=0.6.0 qdrant-client>=1.7.0 tiktoken>=0.5.0
```

### Verify installation

```bash
python -c "import agents; print(agents.__version__)"
python -c "from qdrant_client import QdrantClient; print('Qdrant OK')"
```

### Start the backend

```bash
uvicorn src.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

---

## 3. Content Ingestion

### Run the ingestion script

```bash
cd backend
python scripts/ingest_textbook.py
```

This will:
1. Scan `book-source/docs/` for markdown files
2. Parse content and extract metadata
3. Chunk into 512-token segments
4. Generate embeddings via OpenAI
5. Upsert to Qdrant collection

### Verify ingestion

```bash
# Check collection stats
python -c "
from qdrant_client import QdrantClient
import os

client = QdrantClient(
    url=os.getenv('QDRANT_URL'),
    api_key=os.getenv('QDRANT_API_KEY')
)
info = client.get_collection('physical_ai_textbook')
print(f'Points: {info.points_count}')
print(f'Status: {info.status}')
"
```

---

## 4. Frontend Setup

### Install dependencies

```bash
cd book-source
npm install

# ChatKit packages
npm install @openai/chatkit-react
```

### Start development server

```bash
npm run start
```

Frontend will be available at `http://localhost:3000`

---

## 5. Test the Chatbot

### Using curl

```bash
# Health check
curl http://localhost:8000/api/health

# Simple question (streaming)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is physical AI?"}' \
  -N
```

### Using the UI

1. Open `http://localhost:3000/docs/chapter-01/intro`
2. Click the chat icon in the bottom-right corner
3. Ask: "What is physical AI?"
4. Verify response streams with citations

### Test text selection

1. Select any text on a textbook page
2. Click the "Ask AI" button that appears
3. Verify the chatbot provides an explanation

---

## 6. Common Commands

### Backend

```bash
# Run tests
cd backend
pytest tests/chatbot/

# Type checking
mypy src/chatbot/

# Linting
pylint src/chatbot/
```

### Frontend

```bash
# Run tests
cd book-source
npm test

# Build production
npm run build

# Type checking
npx tsc --noEmit
```

---

## 7. Local Qdrant (Optional)

If you prefer local development without Qdrant Cloud:

```bash
# Start Qdrant with Docker
docker run -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant

# Update .env
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=
```

---

## 8. Troubleshooting

### "OPENAI_API_KEY not set"
- Ensure `.env` file exists in `backend/`
- Verify the key is valid: `echo $OPENAI_API_KEY`

### "Qdrant connection failed"
- Check `QDRANT_URL` is correct
- For Qdrant Cloud, verify API key is set
- Test connection: `curl $QDRANT_URL/collections`

### "No chunks found"
- Run the ingestion script first
- Check collection exists: `curl $QDRANT_URL/collections/physical_ai_textbook`

### "Out of scope" for valid questions
- Check guardrail configuration in `src/chatbot/guardrails/topic_guard.py`
- Adjust topic keywords if needed

### Slow responses
- Reduce `MAX_TOKENS` for faster initial response
- Check network latency to OpenAI API
- Consider using `gpt-4o-mini` for faster (but less capable) responses

---

## 9. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Docusaurus Frontend                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  TextBook   │  │   ChatBot   │  │  Text Selection    │  │
│  │   Pages     │  │   Widget    │  │     Handler        │  │
│  └─────────────┘  └──────┬──────┘  └──────────┬──────────┘  │
│                          │                     │             │
│                          └──────────┬──────────┘             │
└─────────────────────────────────────┼───────────────────────┘
                                      │ SSE Stream
                                      ▼
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  /api/chat  │──│   Agent     │──│    Guardrails       │  │
│  │  Endpoint   │  │  (Agents    │  │  (Topic Check)      │  │
│  └─────────────┘  │    SDK)     │  └─────────────────────┘  │
│                   └──────┬──────┘                            │
│                          │                                   │
│  ┌─────────────┐  ┌──────▼──────┐  ┌─────────────────────┐  │
│  │  Embedding  │◀─│  Qdrant     │──│   OpenAI API        │  │
│  │  Service    │  │  Retriever  │  │   (GPT-4o)          │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Qdrant Cloud                              │
│                physical_ai_textbook collection               │
└─────────────────────────────────────────────────────────────┘
```

---

## Next Steps

After completing the quickstart:

1. Review the full [spec.md](./spec.md) for requirements
2. Check [research.md](./research.md) for implementation details
3. See [contracts/chat-api.yaml](./contracts/chat-api.yaml) for API reference
4. Run tests to validate functionality
