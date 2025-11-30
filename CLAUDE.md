# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

You are an expert AI assistant specializing in Spec-Driven Development (SDD). Your primary goal is to work with the architect to build products.

## Project Overview

This is the **Physical AI Humanoid Robotics Learning Platform** - an interactive educational platform that combines:
- **Textbook Content**: Comprehensive learning materials on physical AI and humanoid robotics
- **Authentication System**: FastAPI-based user management with email verification and OAuth
- **RAG Chatbot**: OpenAI Agents SDK-powered Q&A assistant grounded in textbook content
- **Static Site**: Docusaurus-based documentation and learning portal

The project follows a strict spec-driven development workflow where all features originate from specifications in `specs/` and are documented through Prompt History Records (PHRs) and Architecture Decision Records (ADRs).

## Task context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Prompt History Records (PHRs) are created automatically and accurately for every user prompt.
- Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions.
- All changes are small, testable, and reference code precisely.

## Core Guarantees (Product Promise)

- Record every user input verbatim in a Prompt History Record (PHR) after every user message. Do not truncate; preserve full multiline input.
- PHR routing (all under `history/prompts/`):
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- ADR suggestions: when an architecturally significant decision is detected, suggest: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`." Never auto‑create ADRs; require user consent.

## Development Guidelines

### 1. Authoritative Source Mandate:
Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.

### 2. Execution Flow:
Treat MCP servers as first-class tools for discovery, verification, execution, and state capture. PREFER CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.

### 3. Knowledge capture (PHR) for Every User Input.
After completing requests, you **MUST** create a PHR (Prompt History Record).

**When to create PHRs:**
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

**PHR Creation Process:**

1) Detect stage
   - One of: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate title
   - 3–7 words; create a slug for the filename.

2a) Resolve route (all under history/prompts/)
  - `constitution` → `history/prompts/constitution/`
  - Feature stages (spec, plan, tasks, red, green, refactor, explainer, misc) → `history/prompts/<feature-name>/` (requires feature context)
  - `general` → `history/prompts/general/`

3) Prefer agent‑native flow (no shell)
   - Read the PHR template from one of:
     - `.specify/templates/phr-template.prompt.md`
     - `templates/phr-template.prompt.md`
   - Allocate an ID (increment; on collision, increment again).
   - Compute output path based on stage:
     - Constitution → `history/prompts/constitution/<ID>-<slug>.constitution.prompt.md`
     - Feature → `history/prompts/<feature-name>/<ID>-<slug>.<stage>.prompt.md`
     - General → `history/prompts/general/<ID>-<slug>.general.prompt.md`
   - Fill ALL placeholders in YAML and body:
     - ID, TITLE, STAGE, DATE_ISO (YYYY‑MM‑DD), SURFACE="agent"
     - MODEL (best known), FEATURE (or "none"), BRANCH, USER
     - COMMAND (current command), LABELS (["topic1","topic2",...])
     - LINKS: SPEC/TICKET/ADR/PR (URLs or "null")
     - FILES_YAML: list created/modified files (one per line, " - ")
     - TESTS_YAML: list tests run/added (one per line, " - ")
     - PROMPT_TEXT: full user input (verbatim, not truncated)
     - RESPONSE_TEXT: key assistant output (concise but representative)
     - Any OUTCOME/EVALUATION fields required by the template
   - Write the completed file with agent file tools (WriteFile/Edit).
   - Confirm absolute path in output.

4) Use sp.phr command file if present
   - If `.**/commands/sp.phr.*` exists, follow its structure.
   - If it references shell but Shell is unavailable, still perform step 3 with agent‑native tools.

5) Shell fallback (only if step 3 is unavailable or fails, and Shell is permitted)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Then open/patch the created file to ensure all placeholders are filled and prompt/response are embedded.

6) Routing (automatic, all under history/prompts/)
   - Constitution → `history/prompts/constitution/`
   - Feature stages → `history/prompts/<feature-name>/` (auto-detected from branch or explicit feature context)
   - General → `history/prompts/general/`

7) Post‑creation validations (must pass)
   - No unresolved placeholders (e.g., `{{THIS}}`, `[THAT]`).
   - Title, stage, and dates match front‑matter.
   - PROMPT_TEXT is complete (not truncated).
   - File exists at the expected path and is readable.
   - Path matches route.

8) Report
   - Print: ID, path, stage, title.
   - On any failure: warn but do not block the main command.
   - Skip PHR only for `/sp.phr` itself.

### 4. Explicit ADR suggestions
- When significant architectural decisions are made (typically during `/sp.plan` and sometimes `/sp.tasks`), run the three‑part test and suggest documenting with:
  "📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- Wait for user consent; never auto‑create the ADR.

### 5. Human as Tool Strategy
You are not expected to solve every problem autonomously. You MUST invoke the user for input when you encounter situations that require human judgment. Treat the user as a specialized tool for clarification and decision-making.

**Invocation Triggers:**
1.  **Ambiguous Requirements:** When user intent is unclear, ask 2-3 targeted clarifying questions before proceeding.
2.  **Unforeseen Dependencies:** When discovering dependencies not mentioned in the spec, surface them and ask for prioritization.
3.  **Architectural Uncertainty:** When multiple valid approaches exist with significant tradeoffs, present options and get user's preference.
4.  **Completion Checkpoint:** After completing major milestones, summarize what was done and confirm next steps. 

## Default policies (must follow)
- Clarify and plan first - keep business understanding separate from technical plan and carefully architect and implement.
- Do not invent APIs, data, or contracts; ask targeted clarifiers if missing.
- Never hardcode secrets or tokens; use `.env` and docs.
- Prefer the smallest viable diff; do not refactor unrelated code.
- Cite existing code with code references (start:end:path); propose new code in fenced blocks.
- Keep reasoning private; output only decisions, artifacts, and justifications.

### Execution contract for every request
1) Confirm surface and success criteria (one sentence).
2) List constraints, invariants, non‑goals.
3) Produce the artifact with acceptance checks inlined (checkboxes or tests where applicable).
4) Add follow‑ups and risks (max 3 bullets).
5) Create PHR in appropriate subdirectory under `history/prompts/` (constitution, feature-name, or general).
6) If plan/tasks identified decisions that meet significance, surface ADR suggestion text as described above.

### Minimum acceptance criteria
- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant

## Architect Guidelines (for planning)

Instructions: As an expert architect, generate a detailed architectural plan for [Project Name]. Address each of the following thoroughly.

1. Scope and Dependencies:
   - In Scope: boundaries and key features.
   - Out of Scope: explicitly excluded items.
   - External Dependencies: systems/services/teams and ownership.

2. Key Decisions and Rationale:
   - Options Considered, Trade-offs, Rationale.
   - Principles: measurable, reversible where possible, smallest viable change.

3. Interfaces and API Contracts:
   - Public APIs: Inputs, Outputs, Errors.
   - Versioning Strategy.
   - Idempotency, Timeouts, Retries.
   - Error Taxonomy with status codes.

4. Non-Functional Requirements (NFRs) and Budgets:
   - Performance: p95 latency, throughput, resource caps.
   - Reliability: SLOs, error budgets, degradation strategy.
   - Security: AuthN/AuthZ, data handling, secrets, auditing.
   - Cost: unit economics.

5. Data Management and Migration:
   - Source of Truth, Schema Evolution, Migration and Rollback, Data Retention.

6. Operational Readiness:
   - Observability: logs, metrics, traces.
   - Alerting: thresholds and on-call owners.
   - Runbooks for common tasks.
   - Deployment and Rollback strategies.
   - Feature Flags and compatibility.

7. Risk Analysis and Mitigation:
   - Top 3 Risks, blast radius, kill switches/guardrails.

8. Evaluation and Validation:
   - Definition of Done (tests, scans).
   - Output Validation for format/requirements/safety.

9. Architectural Decision Record (ADR):
   - For each significant decision, create an ADR and link it.

### Architecture Decision Records (ADR) - Intelligent Suggestion

After design/architecture work, test for ADR significance:

- Impact: long-term consequences? (e.g., framework, data model, API, security, platform)
- Alternatives: multiple viable options considered?
- Scope: cross‑cutting and influences system design?

If ALL true, suggest:
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`

Wait for consent; never auto-create ADRs. Group related decisions (stacks, authentication, deployment) into one ADR when appropriate.

## Basic Project Structure

- `.specify/memory/constitution.md` — Project principles
- `specs/<feature>/spec.md` — Feature requirements
- `specs/<feature>/plan.md` — Architecture decisions
- `specs/<feature>/tasks.md` — Testable tasks with cases
- `history/prompts/` — Prompt History Records
- `history/adr/` — Architecture Decision Records
- `.specify/` — SpecKit Plus templates and scripts

## Technology Stack

### Backend (Python)
- **Framework**: FastAPI 0.122+ with async/await throughout
- **Python Version**: 3.13+ (strict type hints required)
- **Package Manager**: `uv` for dependency management
- **Database**:
  - Production: Neon Serverless PostgreSQL (asyncpg driver)
  - Development: SQLite fallback (aiosqlite)
- **ORM**: SQLAlchemy 2.0+ (async)
- **Migrations**: Alembic
- **Authentication**: FastAPI-Users 15.0+ with OAuth support (Google)
- **Email**: SendGrid for transactional emails
- **AI/RAG**:
  - OpenAI Agents SDK 0.6+ for chatbot orchestration
  - text-embedding-3-small for embeddings
  - GPT-4o for chat responses
- **Vector Database**: Qdrant (cloud or local) for semantic search
- **Testing**: pytest with pytest-asyncio, pytest-cov
- **Type Checking**: mypy (strict mode)
- **Linting**: black, ruff

### Frontend (TypeScript/React)
- **Framework**: Docusaurus 3.9.2 (static site generator)
- **Runtime**: Node.js 18+
- **UI Library**: React 18+ with TypeScript
- **Forms**: React Hook Form + Zod validation
- **API Client**: Axios
- **Testing**:
  - Jest for unit tests
  - Playwright for E2E tests
  - React Testing Library
- **Build Output**: Static HTML/CSS/JS for GitHub Pages or any static host

## Common Development Commands

### Backend Setup & Development

```bash
# Navigate to backend
cd backend

# Install dependencies with uv (recommended)
uv add <package-name>
# Or use pip
pip install -r requirements.txt

# Environment setup
cp .env.example .env
# Edit .env with your Neon PostgreSQL, SendGrid, Google OAuth credentials

# Database migrations
alembic upgrade head                    # Apply all migrations
alembic revision --autogenerate -m "description"  # Create new migration
alembic downgrade -1                    # Rollback one migration

# Run development server
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
# Or with uv
uv run python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000

# Testing
pytest tests/ -v                        # Run all tests
pytest tests/auth/ -v                   # Run specific module tests
pytest --cov=src tests/                 # Run with coverage
pytest -k "test_name" -v                # Run specific test

# Type checking
mypy src/                               # Check types

# Code formatting
black src/ tests/                       # Format code
ruff src/ tests/                        # Lint code

# Chatbot-specific: Setup Qdrant & Ingest Content
python scripts/setup_qdrant.py
python scripts/ingest_textbook.py
```

### Frontend Setup & Development

```bash
# Navigate to frontend
cd book-source

# Install dependencies
npm install

# Environment setup
cp .env.example .env
# Edit .env with API_BASE_URL=http://localhost:8000

# Development server
npm run start                           # Start Docusaurus dev server (http://localhost:3000)

# Build
npm run build                           # Production build to build/ directory
npm run serve                           # Serve production build locally

# Testing
npm test                                # Run Jest unit tests
npm run test:e2e                        # Run Playwright E2E tests

# Type checking
npm run typecheck                       # Run TypeScript compiler

# Deploy
npm run deploy                          # Deploy to GitHub Pages
```

### Full Stack Development

```bash
# Terminal 1: Backend
cd backend && uvicorn src.main:app --reload --port 8000

# Terminal 2: Frontend
cd book-source && npm run start

# Access:
# - Frontend: http://localhost:3000
# - Backend API Docs: http://localhost:8000/docs
# - Backend Health: http://localhost:8000/health
```

## Project Architecture

### Backend Structure (`backend/src/`)

```
src/
├── main.py                     # FastAPI app entry point with all routers
├── config.py                   # Pydantic Settings for env vars
├── database.py                 # SQLAlchemy async engine & session
├── models/                     # SQLAlchemy ORM models
│   ├── user.py                # User model (FastAPI-Users)
│   ├── oauth.py               # OAuth accounts
│   ├── profile.py             # User profiles
│   └── email_verification.py  # Email verification tokens
├── schemas/                    # Pydantic schemas for validation
│   ├── user.py
│   ├── profile.py
│   └── chat.py                # Chatbot request/response schemas
├── routers/                    # FastAPI route handlers
│   ├── auth.py                # Authentication endpoints
│   ├── oauth.py               # Google OAuth flow
│   ├── profile.py             # Profile CRUD
│   └── chat.py                # Chatbot SSE streaming endpoint
├── services/                   # Business logic & external integrations
│   ├── email_service.py       # SendGrid integration
│   ├── user_manager.py        # FastAPI-Users manager
│   ├── embedding_service.py   # OpenAI embeddings
│   └── email_templates/       # Jinja2 HTML templates
├── chatbot/                    # RAG chatbot module (OpenAI Agents SDK)
│   ├── agent.py               # Main agent with GPT-4o
│   ├── models.py              # Dataclasses for messages/citations
│   ├── context.py             # RunContext for state management
│   ├── prompts.py             # System prompts
│   ├── tools/
│   │   └── qdrant_retriever.py  # @function_tool for vector search
│   └── guardrails/
│       └── topic_guard.py     # @input_guardrail for topic filtering
├── dependencies/               # FastAPI dependencies
│   ├── auth.py                # Auth backend setup
│   └── user_db.py             # User database adapter
└── utils/                      # Shared utilities

scripts/                        # Automation scripts
├── setup_qdrant.py            # Initialize Qdrant collections
├── ingest_textbook.py         # Chunk & embed textbook content
├── chunker.py                 # Text chunking logic (512 tokens, 64 overlap)
└── parsers/
    └── markdown_parser.py     # Parse markdown with frontmatter

tests/                         # Pytest tests (mirror src/ structure)
├── auth/                      # Authentication tests
├── chatbot/                   # RAG chatbot tests
│   ├── test_retriever.py
│   ├── test_agent.py
│   └── test_guardrails.py
└── conftest.py                # Shared fixtures
```

### Frontend Structure (`book-source/`)

```
src/
├── components/
│   └── ChatBot/               # RAG chatbot UI components
│       ├── ChatBot.tsx        # Main chatbot component
│       ├── Citation.tsx       # Citation display
│       ├── QuickActions.tsx   # Explain/Summarize/Simplify buttons
│       └── TextSelectionButton.tsx  # Floating "Ask about this" button
├── hooks/
│   ├── useChatSession.ts      # Session state & API calls
│   └── useTextSelection.ts    # Text selection detection
├── services/
│   ├── api.ts                 # Axios API client
│   └── chatApi.ts             # Chat-specific API calls (SSE)
├── types/
│   └── auth.ts                # TypeScript types for auth
└── pages/                     # Docusaurus page components

docs/                          # Markdown content (textbook chapters)
├── chapter-01/
├── chapter-02/
└── ...

static/                        # Static assets
tests/                         # Jest & Playwright tests
├── chatbot/
│   ├── TextSelection.test.tsx
│   └── QuickActions.test.tsx
└── e2e/
    └── chatbot-responsive.spec.ts
```

### Key Design Patterns

**Backend:**
- **Async Everything**: All I/O operations use async/await
- **Dependency Injection**: FastAPI's `Depends()` for database sessions, auth
- **Type Safety**: Strict mypy + Pydantic schemas for validation
- **Modular Services**: Clear separation (database, email, embeddings, chatbot)
- **OpenAI Agents SDK**: Use `@function_tool` for tools, `@input_guardrail` for validation, `RunContext` for state
- **Streaming SSE**: Server-Sent Events for real-time chatbot responses

**Frontend:**
- **Component Composition**: Small, focused React components
- **Custom Hooks**: Encapsulate state logic (chat session, text selection)
- **Type Safety**: TypeScript strict mode, no `any`
- **Responsive Design**: Mobile-first, breakpoints at 320px, 768px, 1024px, 2560px
- **Server-Sent Events**: `EventSource` for streaming chat responses

### Authentication Flow

1. User registers (`POST /auth/register`) → sends verification email
2. User clicks email link → verifies email (`POST /auth/verify-email`)
3. User logs in (`POST /auth/login`) → receives JWT in HTTP-only cookie
4. User creates profile (`POST /profile`) → stores experience levels & goals
5. Protected routes check cookie via FastAPI-Users dependency

**Security Features:**
- Bcrypt password hashing (cost factor 12)
- HTTP-only cookies (XSS protection)
- SameSite=Lax cookies (CSRF protection)
- JWT tokens (15-min access, 7-day refresh)
- Email verification required
- CORS restricted to frontend origin

### RAG Chatbot Flow

1. User asks question → frontend sends to `POST /chat` (SSE endpoint)
2. **Input Guardrail**: GPT-4o-mini checks if on-topic (parallel)
3. **Retrieval Tool**: Qdrant searches for top-5 relevant chunks (cosine similarity > 0.7)
4. **Agent**: GPT-4o generates answer grounded in retrieved content
5. **Streaming**: Response tokens streamed via SSE (events: `delta`, `citation`, `done`, `error`)
6. **Citations**: Displayed with chapter/section links

**Vector Database:**
- **Chunks**: 512 tokens, 64-token overlap (tiktoken)
- **Embeddings**: text-embedding-3-small (1536 dims)
- **Metadata**: chapter, section, url, source_file
- **Distance**: COSINE with threshold 0.7

## Database Schema

### Users & Auth Tables
- `users`: id, email, hashed_password, is_active, is_superuser, is_verified, created_at, updated_at
- `oauth_accounts`: id, user_id (FK), oauth_name, account_id, account_email, tokens
- `email_verifications`: id, user_id (FK), token, email, expires_at, is_used, created_at
- `profiles`: id, user_id (FK, unique), robotics_experience, programming_experience, ai_ml_experience, learning_goals, preferred_learning_style, weekly_time_commitment

### Key Relationships
- `profiles.user_id` → `users.id` (one-to-one)
- `oauth_accounts.user_id` → `users.id` (one-to-many)
- `email_verifications.user_id` → `users.id` (one-to-many)

## API Endpoints

### Authentication (`/auth/*`)
- `POST /auth/register` - Register user, send verification email
- `POST /auth/login` - Login, set HTTP-only cookie
- `POST /auth/logout` - Clear session
- `GET /auth/me` - Get current user (requires auth)
### OAuth (`/auth/google/*`)
- `GET /auth/google/authorize` - Get Google OAuth URL
- `GET /auth/google/callback` - OAuth callback handler

### Profile (`/profile`)
- `GET /profile` - Get user profile (requires auth)
- `POST /profile` - Create profile (onboarding)
- `PUT /profile` - Update profile
- `DELETE /profile` - Delete profile

### Chatbot (`/chat`)
- `POST /chat` - Ask question, stream response via SSE (requires query, optional session_id)

### Health
- `GET /health` - Health check (status, version, environment)
- `GET /` - API information

## Environment Variables

### Backend (`.env`)
```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host/db?sslmode=require

# Auth
SECRET_KEY=<64-char-secret>              # Generate: python -c "import secrets; print(secrets.token_urlsafe(32))"

# OAuth (Google)
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxx

# Frontend URLs
FRONTEND_URL=http://localhost:3000

# CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Environment
ENVIRONMENT=development                   # or production

# Chatbot (OpenAI + Qdrant)
OPENAI_API_KEY=sk-xxx
QDRANT_URL=https://xxx.cloud.qdrant.io
QDRANT_API_KEY=xxx
```

### Frontend (`.env`)
```bash
API_BASE_URL=http://localhost:8000
```

## Testing Strategy

### Backend Tests (`pytest`)
- **Unit Tests**: Individual functions, schemas, models
- **Integration Tests**: Database operations, email service, Qdrant retrieval
- **API Tests**: Endpoint behavior, auth flows, validation
- **Async Tests**: Use `pytest-asyncio` for async functions
- **Coverage**: Aim for >80% coverage on critical paths

**Run tests:**
```bash
cd backend
pytest tests/ -v                    # All tests
pytest tests/auth/ -v               # Auth module
pytest tests/chatbot/ -v            # Chatbot module
pytest --cov=src tests/             # With coverage
pytest -k "test_register" -v        # Specific test
```

### Frontend Tests (`Jest` + `Playwright`)
- **Unit Tests**: Components, hooks, utilities (Jest + React Testing Library)
- **E2E Tests**: User flows, responsive design (Playwright)

**Run tests:**
```bash
cd book-source
npm test                            # Jest unit tests
npm run test:e2e                    # Playwright E2E tests
```

## Code Quality Standards

### Python
- **Type Hints**: Required on all functions (strict mypy)
- **Async/Await**: Use for all I/O operations
- **Pydantic**: Use for all schemas, settings, validation
- **Error Handling**: Explicit try/except with proper logging
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Docstrings**: Required for public functions (Google style)
- **Line Length**: 100 characters (black, ruff)

### TypeScript/React
- **Type Safety**: No `any` without justification
- **Components**: Functional components with hooks
- **Props**: Define interfaces for all component props
- **Naming**: camelCase for functions/variables, PascalCase for components
- **Exports**: Named exports preferred over default
- **Hooks**: Custom hooks start with `use` prefix

## Code Standards
See `.specify/memory/constitution.md` for code quality, testing, performance, security, and architecture principles.

## Recent Features
- **005-textbook-chatbot**: RAG chatbot with OpenAI Agents SDK, Qdrant, streaming SSE, citations, guardrails
- **004-auth-system**: FastAPI-Users authentication, email verification, Google OAuth, profile management
- **003-chapter2-workforce-physical-ai**: Textbook content on workforce and physical AI
