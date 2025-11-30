# Tasks: Physical AI Textbook Chatbot

**Input**: Design documents from `/specs/005-textbook-chatbot/`  
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: Tests are included per spec requirement for validation of RAG retrieval and guardrails.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/` for Python FastAPI code
- **Frontend**: `book-source/src/` for React/Docusaurus components
- **Tests**: `backend/tests/` and `book-source/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for chatbot feature

- [ ] T001 Create chatbot module directory structure in `backend/src/chatbot/` per plan.md
- [ ] T002 Add chatbot dependencies to `backend/requirements.txt` (openai-agents, qdrant-client, tiktoken)
- [ ] T003 [P] Create chatbot configuration in `backend/src/config.py` (OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY, collection name, embedding model, chunk size)
- [ ] T004 [P] Create environment variables template in `backend/.env.chatbot.example`
- [ ] T005 [P] Add ChatKit React dependencies to `book-source/package.json` (@chatscope/chat-ui-kit-react)
- [ ] T006 Create chatbot component directory structure in `book-source/src/components/ChatBot/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Qdrant Setup & Content Ingestion

- [ ] T007 Create TextbookChunk dataclass in `backend/src/chatbot/models.py` with all fields from data-model.md
- [ ] T008 Create Qdrant collection setup script in `backend/scripts/setup_qdrant.py` (creates collection with proper schema)
- [ ] T009 Implement embedding service in `backend/src/services/embedding_service.py` using text-embedding-3-small
- [ ] T010 Implement markdown parser in `backend/scripts/parsers/markdown_parser.py` for extracting textbook content
- [ ] T011 Implement chunking logic in `backend/scripts/chunker.py` (512 tokens, 64 overlap using tiktoken)
- [ ] T012 Create textbook ingestion pipeline in `backend/scripts/ingest_textbook.py` that reads `book-source/docs/`, chunks content, embeds, and stores in Qdrant
- [ ] T013 Run ingestion script to populate Qdrant with textbook content

### OpenAI Agents SDK Foundation

- [ ] T014 Create base agent prompts in `backend/src/chatbot/prompts.py` (system prompt with textbook grounding instructions)
- [ ] T015 Create AgentContext dataclass in `backend/src/chatbot/context.py` per data-model.md
- [ ] T016 Implement Qdrant retriever tool in `backend/src/chatbot/tools/qdrant_retriever.py` using AsyncQdrantClient
- [ ] T017 Create topic guardrail in `backend/src/chatbot/guardrails/topic_guard.py` to restrict responses to textbook content
- [ ] T018 Create main textbook agent in `backend/src/chatbot/agent.py` using OpenAI Agents SDK with retriever tool and guardrail

### Backend API Foundation

- [ ] T019 Create Pydantic schemas in `backend/src/schemas/chat.py` (ChatRequest, ConversationMessage per data-model.md)
- [ ] T020 Create streaming chat router in `backend/src/routers/chat.py` with SSE endpoint `/api/chat`
- [ ] T021 Register chat router in `backend/src/main.py`
- [ ] T022 [P] Add CORS configuration for book-source domain in `backend/src/main.py`

### Frontend Foundation

- [ ] T023 Create chat API client in `book-source/src/services/chatApi.ts` with SSE streaming support
- [ ] T024 Create useChatSession hook in `book-source/src/hooks/useChatSession.ts` managing ChatSession state
- [ ] T025 Create Citation component in `book-source/src/components/ChatBot/Citation.tsx`
- [ ] T026 Create base ChatBot component shell in `book-source/src/components/ChatBot/ChatBot.tsx`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - General Textbook Q&A (Priority: P1) 🎯 MVP

**Goal**: Users can ask questions and receive AI-generated answers grounded in textbook content with citations

**Independent Test**: Ask "What is Physical AI?" and receive a response with at least one citation linking to Chapter 1

### Tests for User Story 1

- [ ] T027 [P] [US1] Create retriever unit test in `backend/tests/chatbot/test_retriever.py` verifying relevant chunks returned
- [ ] T028 [P] [US1] Create agent integration test in `backend/tests/chatbot/test_agent.py` verifying grounded response with citations
- [ ] T029 [P] [US1] Create chat endpoint test in `backend/tests/routers/test_chat.py` verifying SSE streaming

### Implementation for User Story 1

- [ ] T030 [US1] Implement retrieval logic in `backend/src/chatbot/tools/qdrant_retriever.py` with top-k=5, score threshold, and citation extraction
- [ ] T031 [US1] Implement agent run method in `backend/src/chatbot/agent.py` that retrieves context, generates response, extracts citations
- [ ] T032 [US1] Implement SSE streaming in `backend/src/routers/chat.py` emitting delta, citation, done events per contracts/events.md
- [ ] T033 [US1] Add error handling for empty results, API errors in `backend/src/routers/chat.py`
- [ ] T034 [US1] Implement chat input and message display in `book-source/src/components/ChatBot/ChatBot.tsx`
- [ ] T035 [US1] Connect ChatBot component to API client with streaming in `book-source/src/components/ChatBot/ChatBot.tsx`
- [ ] T036 [US1] Display citations as clickable links in messages using `book-source/src/components/ChatBot/Citation.tsx`
- [ ] T037 [US1] Add loading state and streaming indicator to ChatBot component

**Checkpoint**: User Story 1 complete - users can ask questions and get cited answers

---

## Phase 4: User Story 2 - Text Selection Query (Priority: P1) 🎯 MVP

**Goal**: Users can select text on textbook pages and ask questions about the selection

**Independent Test**: Select text on a textbook page, click "Ask about this", receive response referencing the selected text

### Tests for User Story 2

- [ ] T038 [P] [US2] Create text selection test in `book-source/tests/chatbot/TextSelection.test.tsx`
- [ ] T039 [P] [US2] Create API test for selected_text parameter in `backend/tests/routers/test_chat.py`

### Implementation for User Story 2

- [ ] T040 [US2] Create TextSelectionButton component in `book-source/src/components/ChatBot/TextSelectionButton.tsx`
- [ ] T041 [US2] Implement text selection detection hook in `book-source/src/hooks/useTextSelection.ts`
- [ ] T042 [US2] Handle selected_text in agent context in `backend/src/chatbot/agent.py` (prepend to user message)
- [ ] T043 [US2] Update system prompt to handle selected text context in `backend/src/chatbot/prompts.py`
- [ ] T044 [US2] Integrate TextSelectionButton with ChatBot component in `book-source/src/components/ChatBot/ChatBot.tsx`
- [ ] T045 [US2] Add visual indicator for text selection mode in ChatBot UI

**Checkpoint**: User Story 2 complete - text selection queries work independently

---

## Phase 5: User Story 3 - Streaming Responses (Priority: P2)

**Goal**: Users see responses appear progressively as they are generated

**Independent Test**: Send a question, observe text appearing word-by-word with visible streaming indicator

### Tests for User Story 3

- [ ] T046 [P] [US3] Create streaming display test in `book-source/tests/chatbot/Streaming.test.tsx`

### Implementation for User Story 3

- [ ] T047 [US3] Implement token-by-token display in `book-source/src/components/ChatBot/ChatBot.tsx`
- [ ] T048 [US3] Add streaming status indicator (typing animation) in ChatBot component
- [ ] T049 [US3] Handle stream interruption gracefully (partial content preservation)
- [ ] T050 [US3] Add cancel stream button during active streaming

**Checkpoint**: User Story 3 complete - streaming responses display progressively

---

## Phase 6: User Story 4 - Follow-up Questions (Priority: P2)

**Goal**: Users can ask follow-up questions that reference previous conversation context

**Independent Test**: Ask an initial question, then ask "Can you explain more?" and receive a contextual response

### Tests for User Story 4

- [ ] T051 [P] [US4] Create conversation context test in `backend/tests/chatbot/test_agent.py`

### Implementation for User Story 4

- [ ] T052 [US4] Implement conversation history management in `book-source/src/hooks/useChatSession.ts`
- [ ] T053 [US4] Pass conversation_history in ChatRequest from frontend to backend
- [ ] T054 [US4] Update agent to include conversation history in context in `backend/src/chatbot/agent.py`
- [ ] T055 [US4] Limit conversation history to last 10 messages to manage token usage

**Checkpoint**: User Story 4 complete - follow-up questions work with context

---

## Phase 7: User Story 5 - Clear Chat (Priority: P2)

**Goal**: Users can clear conversation history and start fresh

**Independent Test**: Have a conversation, click "Clear Chat", verify all messages removed and new session started

### Tests for User Story 5

- [ ] T056 [P] [US5] Create clear chat test in `book-source/tests/chatbot/ClearChat.test.tsx`

### Implementation for User Story 5

- [ ] T057 [US5] Add Clear Chat button to ChatBot component in `book-source/src/components/ChatBot/ChatBot.tsx`
- [ ] T058 [US5] Implement clearSession in `book-source/src/hooks/useChatSession.ts` resetting all state
- [ ] T059 [US5] Add confirmation dialog before clearing (optional, skip if simple UX preferred)
- [ ] T060 [US5] Verify no data persists after clear (memory-only validation)

**Checkpoint**: User Story 5 complete - clear chat works independently

---

## Phase 8: User Story 6 - Quick Actions (Priority: P3)

**Goal**: Users can apply quick actions (Explain more, Summarize, Simplify) to responses

**Independent Test**: Receive a response, click "Summarize", receive a summarized version of the previous response

### Tests for User Story 6

- [ ] T061 [P] [US6] Create quick actions test in `book-source/tests/chatbot/QuickActions.test.tsx`
- [ ] T062 [P] [US6] Create quick action API test in `backend/tests/routers/test_chat.py`

### Implementation for User Story 6

- [ ] T063 [US6] Create QuickActions component in `book-source/src/components/ChatBot/QuickActions.tsx`
- [ ] T064 [US6] Handle quick_action in ChatRequest schema in `backend/src/schemas/chat.py`
- [ ] T065 [US6] Update agent prompt to handle quick_action modifiers in `backend/src/chatbot/prompts.py`
- [ ] T066 [US6] Implement quick action logic in agent in `backend/src/chatbot/agent.py`
- [ ] T067 [US6] Display QuickActions below each assistant message in ChatBot component

**Checkpoint**: User Story 6 complete - quick actions work independently

---

## Phase 9: User Story 7 - Out-of-Scope Handling (Priority: P3)

**Goal**: Chatbot politely refuses questions outside textbook scope and redirects to relevant chapters

**Independent Test**: Ask "What's the weather today?" and receive a polite refusal with suggestion to ask about Physical AI topics

### Tests for User Story 7

- [ ] T068 [P] [US7] Create guardrail test in `backend/tests/chatbot/test_guardrails.py` verifying off-topic rejection
- [ ] T069 [P] [US7] Create redirection test verifying chapter suggestions for edge-case questions

### Implementation for User Story 7

- [ ] T070 [US7] Enhance topic guardrail in `backend/src/chatbot/guardrails/topic_guard.py` with off-topic detection
- [ ] T071 [US7] Create off-topic response template with chapter suggestions in `backend/src/chatbot/prompts.py`
- [ ] T072 [US7] Implement chapter suggestion logic based on partial topic matches
- [ ] T073 [US7] Display friendly off-topic message in ChatBot UI

**Checkpoint**: User Story 7 complete - off-topic handling works independently

---

## Phase 10: User Story 8 - Responsive UI (Priority: P3)

**Goal**: Chatbot UI works seamlessly across desktop, tablet, and mobile devices

**Independent Test**: Open chatbot on 320px mobile viewport, verify all functionality accessible and usable

### Tests for User Story 8

- [ ] T074 [P] [US8] Create responsive UI test in `book-source/tests/e2e/chatbot-responsive.spec.ts` using Playwright

### Implementation for User Story 8

- [ ] T075 [US8] Add responsive CSS to `book-source/src/components/ChatBot/ChatBot.module.css` (breakpoints: 320px, 768px, 1024px, 2560px)
- [ ] T076 [US8] Implement collapsible chat panel for mobile in ChatBot component
- [ ] T077 [US8] Adjust input area and buttons for touch targets (min 44px)
- [ ] T078 [US8] Test and fix layout issues across all breakpoints
- [ ] T079 [US8] Add swipe gesture to expand/collapse chat on mobile

**Checkpoint**: User Story 8 complete - responsive UI works across all devices

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T080 [P] Create README for chatbot module in `backend/src/chatbot/README.md`
- [ ] T081 [P] Add type hints and docstrings to all Python modules
- [ ] T082 [P] Add JSDoc comments to all TypeScript components
- [ ] T083 Code review and refactor for consistency across chatbot module
- [ ] T084 [P] Add logging throughout chatbot flow for debugging
- [ ] T085 Performance optimization: cache embeddings, optimize chunk retrieval
- [ ] T086 Security review: validate all inputs, sanitize outputs
- [ ] T087 Run quickstart.md validation end-to-end
- [ ] T088 Update project README with chatbot feature documentation

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup) ──────────────┐
                              ▼
Phase 2 (Foundational) ───────┤ BLOCKS all user stories
                              │
         ┌────────────────────┴────────────────────┐
         ▼                                         ▼
Phase 3 (US1: Q&A)                    Phase 4 (US2: Text Selection)
         │                                         │
         └────────────────────┬────────────────────┘
                              ▼
              Phase 5-9 (US3-US7) - Can run in parallel
                              │
                              ▼
              Phase 10 (US8: Responsive UI)
                              │
                              ▼
              Phase 11 (Polish)
```

### User Story Dependencies

| Story | Depends On | Can Parallel With |
|-------|------------|-------------------|
| US1 (Q&A) | Phase 2 | US2 |
| US2 (Text Selection) | Phase 2 | US1 |
| US3 (Streaming) | US1 | US4, US5, US6, US7 |
| US4 (Follow-ups) | US1 | US3, US5, US6, US7 |
| US5 (Clear Chat) | US1 | US3, US4, US6, US7 |
| US6 (Quick Actions) | US1 | US3, US4, US5, US7 |
| US7 (Out-of-Scope) | US1 | US3, US4, US5, US6 |
| US8 (Responsive) | US1, US2 | - |

### MVP Scope

**Minimum Viable Product**: Phase 1 + Phase 2 + Phase 3 (US1) + Phase 4 (US2)

This delivers:
- ✅ Ask questions about textbook content
- ✅ Receive AI-generated answers with citations
- ✅ Select text and ask about it
- ✅ Streaming responses (basic)

---

## Parallel Opportunities

### Phase 2 Parallelization

```
T007 ─┬─ T014 ─┬─ T019 ─┬─ T023
T008 ─┤  T015 ─┤  T020 ─┤  T024
T009 ─┤  T016 ─┤  T021 ─┤  T025
T010 ─┤  T017 ─┤  T022 ─┘  T026
T011 ─┤  T018 ─┘
T012 ─┘
T013 (sequential - needs T007-T012)
```

### Cross-Story Parallelization

Once Phase 2 completes:
- **Team A**: US1 (General Q&A) - T027-T037
- **Team B**: US2 (Text Selection) - T038-T045
- **Solo**: US3-US7 can all start once US1 is complete

---

## Task Summary

| Phase | Tasks | Story |
|-------|-------|-------|
| Phase 1: Setup | T001-T006 (6) | - |
| Phase 2: Foundational | T007-T026 (20) | - |
| Phase 3: US1 Q&A | T027-T037 (11) | P1 MVP |
| Phase 4: US2 Text Selection | T038-T045 (8) | P1 MVP |
| Phase 5: US3 Streaming | T046-T050 (5) | P2 |
| Phase 6: US4 Follow-ups | T051-T055 (5) | P2 |
| Phase 7: US5 Clear Chat | T056-T060 (5) | P2 |
| Phase 8: US6 Quick Actions | T061-T067 (7) | P3 |
| Phase 9: US7 Out-of-Scope | T068-T073 (6) | P3 |
| Phase 10: US8 Responsive | T074-T079 (6) | P3 |
| Phase 11: Polish | T080-T088 (9) | - |
| **Total** | **88 tasks** | |

---

## Implementation Strategy

1. **MVP First** (Phases 1-4): Focus on core Q&A and text selection - 45 tasks
2. **Enhanced UX** (Phases 5-7): Add streaming, follow-ups, clear chat - 15 tasks
3. **Polish Features** (Phases 8-10): Quick actions, guardrails, responsive - 19 tasks
4. **Final Polish** (Phase 11): Documentation, optimization, security - 9 tasks

**Estimated Effort**: 
- MVP: 2-3 days
- Full feature: 5-7 days
