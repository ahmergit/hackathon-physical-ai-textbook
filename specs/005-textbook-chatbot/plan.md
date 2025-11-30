# Implementation Plan: Physical AI Textbook Chatbot

**Branch**: `005-textbook-chatbot` | **Date**: 2024-11-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-textbook-chatbot/spec.md`

## Summary

Build a RAG-based chatbot strictly grounded in the Physical AI textbook content. The system uses FastAPI backend with OpenAI Agents SDK for AI orchestration, Qdrant Cloud for vector retrieval, and ChatKit React components for the frontend UI embedded in the Docusaurus textbook site. Key features include streaming responses, session-only memory (no persistence), text selection queries, topic guardrails, and responsive design.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.x (frontend)  
**Primary Dependencies**:
- Backend: FastAPI, OpenAI Agents SDK (`openai-agents`), Qdrant Client, OpenAI API
- Frontend: React 18, ChatKit React (`@openai/chatkit-react`), Docusaurus 3.9.2
**Storage**: Qdrant Cloud (vector database for embeddings) - No persistent chat storage  
**Testing**: pytest (backend), Jest/Playwright (frontend)  
**Target Platform**: Web (static Docusaurus site + FastAPI backend)  
**Project Type**: Web application (frontend + backend)  
**Performance Goals**: 
- Initial response token < 1s
- Full response < 5s for typical questions
- Streaming at model generation speed
**Constraints**: 
- Session-only memory (no database persistence for conversations)
- Strictly grounded in textbook content (no external knowledge)
- Responsive UI (320px - 2560px)
**Scale/Scope**: Single textbook (~50-100 sections), single-user sessions, no concurrent user limits on client-side

### Technology Configuration

| Component | Technology | Configuration |
|-----------|------------|---------------|
| Chat Model | GPT-4o | MAX_TOKENS=8000 |
| Embedding Model | text-embedding-3-small | EMBEDDING_DIMENSION=1536 |
| Vector Database | Qdrant Cloud | Collection: `physical_ai_textbook` |
| Chunking | Custom | CHUNK_SIZE=512 tokens, OVERLAP=64 tokens |
| Agent Framework | OpenAI Agents SDK | Streaming + Guardrails + Custom Tools |

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | ✅ PASS | All implementation derives from spec.md |
| II. Single Source of Truth | ✅ PASS | Textbook content is authoritative source |
| III. Automation-First | ✅ PASS | Ingestion pipeline fully scriptable |
| IV. Code Quality & Type Safety | ✅ PASS | Strict typing in Python + TypeScript |
| V. Testing & Validation | ✅ PASS | pytest + Jest + Playwright planned |
| VI. Performance & UX | ✅ PASS | Response < 3s, responsive 320px+ |
| VII. Content Accuracy | ✅ PASS | RAG ensures grounded responses with citations |
| VIII. Separation of Concerns | ✅ PASS | Agent logic separate from content |
| IX. Minimal & Sufficient | ✅ PASS | Only textbook content, no fluff |
| X. Modularity & Maintainability | ✅ PASS | Clear separation: agent, retriever, API |

## Project Structure

### Documentation (this feature)

```text
specs/005-textbook-chatbot/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 research findings
├── data-model.md        # Entity definitions
├── quickstart.md        # Developer quickstart guide
├── contracts/           # API contracts
│   ├── chat-api.yaml    # OpenAPI spec for chat endpoint
│   └── events.md        # SSE event schema
├── checklists/
│   └── requirements.md  # Quality validation checklist
└── tasks.md             # Phase 2 tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── chatbot/                   # NEW: Chatbot module
│   │   ├── __init__.py
│   │   ├── agent.py               # OpenAI Agents SDK agent definition
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   └── qdrant_retriever.py # Custom Qdrant retrieval tool
│   │   ├── guardrails/
│   │   │   ├── __init__.py
│   │   │   └── topic_guard.py     # Domain restriction guardrail
│   │   ├── context.py             # Session context management
│   │   └── prompts.py             # System prompts and templates
│   ├── routers/
│   │   └── chat.py                # NEW: /chat streaming endpoint
│   ├── schemas/
│   │   └── chat.py                # NEW: Pydantic models for chat
│   ├── services/
│   │   └── embedding_service.py   # NEW: Embedding generation
│   └── config.py                  # Add chatbot config settings
├── scripts/
│   └── ingest_textbook.py         # NEW: Content ingestion pipeline
└── tests/
    └── chatbot/                   # NEW: Chatbot tests
        ├── test_agent.py
        ├── test_retriever.py
        └── test_guardrails.py

book-source/
├── src/
│   ├── components/
│   │   ├── ChatBot/               # NEW: Chatbot React components
│   │   │   ├── ChatBot.tsx        # Main chatbot component
│   │   │   ├── ChatBot.module.css # Responsive styles
│   │   │   ├── TextSelectionButton.tsx
│   │   │   ├── QuickActions.tsx
│   │   │   └── Citation.tsx
│   │   └── index.ts               # Export chatbot components
│   ├── hooks/
│   │   └── useChatSession.ts      # NEW: Chat session hook
│   ├── services/
│   │   └── chatApi.ts             # NEW: Backend API client
│   └── theme/
│       └── DocItem/               # Swizzled for chat integration
└── static/
    └── chatbot/
        └── chatbot.css            # Global chatbot styles
```

**Structure Decision**: Web application pattern with existing `backend/` and `book-source/` directories. New chatbot module added to backend, ChatKit components integrated into Docusaurus frontend.

## Complexity Tracking

No constitution violations requiring justification.
