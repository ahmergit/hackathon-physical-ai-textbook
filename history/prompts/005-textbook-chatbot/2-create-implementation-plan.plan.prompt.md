---
id: 2
title: Create Textbook Chatbot Implementation Plan
stage: plan
date: 2024-11-29
surface: agent
model: Claude Opus 4.5
feature: textbook-chatbot
branch: 005-textbook-chatbot
user: developer
command: /sp.plan
labels: [plan, architecture, RAG, OpenAI-Agents-SDK, Qdrant, FastAPI, ChatKit]
links:
  spec: specs/005-textbook-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-textbook-chatbot/plan.md
  - specs/005-textbook-chatbot/research.md
  - specs/005-textbook-chatbot/data-model.md
  - specs/005-textbook-chatbot/quickstart.md
  - specs/005-textbook-chatbot/contracts/chat-api.yaml
  - specs/005-textbook-chatbot/contracts/events.md
tests:
  - null
---

## Prompt

Follow instructions in sp.plan.prompt.md.
The backend will use FastAPI to host the chat API and handle streaming responses.
The AI workflow will be built using the OpenAI Agents SDK: https://openai.github.io/openai-agents-python/.
Vector retrieval will follow a custom Qdrant tool built using: https://openai.github.io/openai-agents-python/tools/#customizing-tool-agents.
All textbook content will be chunked into segments of 512 tokens with an overlap of 64.
Embeddings will be generated using text-embedding-3-small with EMBEDDING_DIMENSION=1536.
All embeddings and metadata will be stored in Qdrant Cloud collections.
The agent will always retrieve relevant chunks before generating an answer.
The chat model used for generation will be gpt-4o with MAX_TOKENS=8000.
Streaming output will use the SDK's streaming utilities: https://openai.github.io/openai-agents-python/streaming/.
Session-only memory will be implemented using the context API: https://openai.github.io/openai-agents-python/context/.
A "Clear Chat" button will remove all agent context and fully reset the session.
Guardrails will restrict the chatbot to Physical AI and humanoid robotics topics: https://openai.github.io/openai-agents-python/guardrails/.
If a user asks about anything outside this domain, the agent will say it has no knowledge beyond the textbook.
The backend will expose a /chat route that forwards messages to the agent and streams tokens back.
All answers must cite retrieved textbook chunks to stay fully grounded.
The frontend chatbot will use ChatKit React components: https://platform.openai.com/docs/guides/chatkit.
The widget will be embedded inside the Docusaurus textbook as a floating or inline assistant.
Users can select text in the book and click an "Ask AI" button to send that text to the chatbot.
The interface will support real-time streaming, markdown, and code rendering.
The ingestion pipeline will process markdown, generate embeddings, and sync updated chunks into Qdrant.
The goal is to build a precise, domain-limited, book-grounded AI assistant with no user data storage.
use all link to research and make sure use this standard.

## Response snapshot

Created comprehensive implementation plan with Phase 0 research and Phase 1 design artifacts:

**Research Findings (research.md)**:
- OpenAI Agents SDK v0.6.x for agent orchestration with streaming, guardrails, and custom tools
- Qdrant Cloud with AsyncQdrantClient for vector retrieval
- SSE (Server-Sent Events) for streaming responses via FastAPI
- In-memory session context (no persistence) with conversation history passed per request
- Input guardrails using topic-checking agent (gpt-4o-mini)
- ChatKit React SDK for frontend with custom session endpoint
- 512-token chunks with 64-token overlap using text-embedding-3-small

**Data Model (data-model.md)**:
- TextbookChunk: Qdrant-stored indexed content with chapter/section metadata
- ChatMessage/ChatSession: Client-side only (React state)
- Citation: References to textbook locations
- ChatRequest/ChatStreamEvent: API schema for request/response

**API Contracts (contracts/)**:
- OpenAPI 3.1 spec for POST /api/chat (SSE streaming)
- Event schema: delta, citation, done, error events
- Health check endpoint

**Quickstart Guide (quickstart.md)**:
- Environment setup, installation, ingestion, testing instructions
- Architecture overview diagram

## Outcome

- ✅ Impact: Complete Phase 0-1 planning artifacts ready for tasks phase
- 🧪 Tests: N/A (plan phase)
- 📁 Files: 6 artifacts created (plan.md, research.md, data-model.md, quickstart.md, contracts/*)
- 🔁 Next prompts: /sp.tasks to create implementation task breakdown
- 🧠 Reflection: Research confirmed all technologies work well together; SSE streaming with OpenAI Agents SDK is well-documented

## Evaluation notes (flywheel)

- Failure modes observed: None - all research URLs were accessible and documented the needed patterns
- Graders run and results (PASS/FAIL): Constitution check PASS on all 10 principles
- Prompt variant (if applicable): N/A
- Next experiment: Validate API contract with frontend team before implementation
