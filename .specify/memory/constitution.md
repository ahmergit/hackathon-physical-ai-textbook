# AI-Generated Book + Static Site + RAG Assistant Constitution

## Core Principles

### I. Spec-Driven Development
All deliverables (book, site, assistant, backend) originate exclusively from formal specifications, never ad-hoc writing or coding.

**Requirements:**
- Every feature, content section, or component must have a corresponding spec before implementation
- No code or content may be written without a spec that defines its purpose, inputs, outputs, and acceptance criteria
- Specs are the single source of truth for what to build and how to build it
- Any deviation from spec must be documented and approved

### II. Single Source of Truth
Specs define all content and behavior; generated artifacts (markdown, site, embeddings, ingestion scripts) must not diverge from the spec.

**Requirements:**
- Specs are authoritative; generated artifacts reflect spec content exactly
- No manual edits to generated artifacts without updating the source spec
- All content flows: Spec → Generator → Artifact
- Traceability required: every artifact must reference its source spec

### III. Automation-First & Reproducible
The entire system must be fully regenerable from specs using scripts or generators, ensuring deterministic outputs.

**Requirements:**
- Every generation step must be scripted and version-controlled
- Re-running generators on the same spec produces identical output
- No manual steps in the generation pipeline
- All generators accept specs as input and produce artifacts as output
- Build process must be fully automated and documented

### IV. Code Quality & Type Safety
All backend and script code uses strict typing (Python type hints, TypeScript) and follows clean, maintainable architectural patterns.

**Requirements:**
- Python: strict type hints on all functions, classes, and modules
- TypeScript: strict mode enabled, no `any` types without justification
- Code must pass linting (mypy, pylint for Python; ESLint for TypeScript)
- Follow language-specific style guides (PEP 8 for Python, Airbnb/Standard for TypeScript)
- Clear separation of concerns: generators, validators, pipelines, and utilities must be modular

### V. Testing & Validation
Critical generation pipelines, schemas, and ingestion logic require automated tests, validations, or lint rules before deployment.

**Requirements:**
- Unit tests for all generators and pipeline logic
- Schema validation for all structured data (book specs, metadata, embeddings)
- Integration tests for ingestion → vector DB → retrieval flow
- Smoke tests for site builds and deployments
- All tests must pass before merging or deploying

### VI. Performance & UX Consistency
The site and assistant must meet performance targets and present a consistent user experience across desktop, tablet, and mobile.

**Requirements:**
- Static site build time < 60 seconds for typical book size
- Page load time < 2 seconds (Lighthouse score > 90)
- RAG assistant response time < 3 seconds for typical queries
- Responsive design: mobile-first, works on 320px+ screens
- Consistent branding, typography, and navigation across all pages

### VII. Content Accuracy & Integrity
Generated book content must not contain filler, placeholders, repeated explanations, or internal scaffolding. All claims must be traceable.

**Requirements:**
- No placeholder text (e.g., "Lorem ipsum", "[TODO]", "Coming soon")
- No repeated explanations across chapters
- No internal scaffolding or agent instructions in output
- All factual claims must cite sources or reference spec
- Content must be reviewed for accuracy before publication

### VIII. Separation of Concerns
Internal instructions, agent logic, or system scaffolding must never appear in reader-facing book or website content.

**Requirements:**
- Generator logic, prompts, and internal comments stay in code/specs
- Book content contains only reader-facing material
- No debugging output, technical notes, or meta-commentary in published content
- Clear boundaries: internal tooling vs. public artifacts

### IX. Minimal & Sufficient Content
Every chapter and section provides only what is necessary to teach the concept—no fluff, no redundancy, no meta-commentary.

**Requirements:**
- Each section has a clear learning objective
- No unnecessary introductions or summaries
- No repetition of concepts already covered
- Concise explanations with examples where needed
- Remove content that doesn't serve the learning objective

### X. Modularity & Maintainability
Code, content, and config must be modular, documented, and organized for long-term maintainability and regeneration.

**Requirements:**
- Clear project structure with documented conventions
- Each module/component has a single, well-defined responsibility
- README files for each major directory or subsystem
- Inline documentation for complex logic
- Config files use standard formats (YAML, JSON, TOML) with schemas

## Technical Guidelines

### Technology Stack

**Backend & Automation:**
- **Python 3.11+** with strict type hints for all backend, ingestion, generation, and pipeline automation
- **`uv`** for Python package management; all dependencies in `pyproject.toml`
- **mypy** for static type checking (strict mode)
- **pytest** for testing

**Frontend & Site:**
- **TypeScript** for frontend automation, site scripting, and CLI tools
- **Docusaurus 3.9.2** as the static site generator
- Output: static React suitable for GitHub Pages or any static host
- **Node 18+** with npm/yarn for package management

**Vector Database & RAG:**
- **Qdrant** (local or cloud) as the vector database for RAG
- Ingestion and querying must be modular and version-controlled
- Embeddings stored with metadata for traceability

### Dependency Management
- Use `uv` for Python; all dependencies declared in `pyproject.toml`
- Use Node/npm for frontend; all dependencies declared in `package.json`
- No global or ad-hoc dependencies
- Lock files committed to ensure deterministic installs

### Security & Configuration
- Use environment variables for secrets and API keys
- No secrets or keys in code, specs, or config files
- `.env` files for local development; never committed
- `.env.example` provided with placeholder values

### Documentation
- All external dependencies explicitly listed in README
- Setup instructions assume fresh environment
- No hidden or implicit requirements
- API contracts and schemas documented

## Development Workflow

### Feature Development Process
1. **Spec First**: Write or update spec in `specs/<feature>/spec.md`
2. **Plan**: Create architecture plan in `specs/<feature>/plan.md`
3. **Tasks**: Break down into testable tasks in `specs/<feature>/tasks.md`
4. **Implement**: Build according to spec and plan
5. **Validate**: Run tests, linters, and validators
6. **Generate**: Run generators to produce artifacts
7. **Review**: Verify output matches spec and constitution
8. **Commit**: Use PHR to document the work

### Quality Gates
- All code must pass type checking (mypy for Python, tsc for TypeScript)
- All code must pass linting (pylint, ESLint)
- All tests must pass (pytest, Jest)
- All schemas must validate
- All generated content must be free of placeholders and scaffolding
- Site must build successfully

### Prompt History Records (PHR)
- Create PHR after every significant user interaction or completed task
- Route PHRs to appropriate subdirectory:
  - Constitution work → `history/prompts/constitution/`
  - Feature-specific work → `history/prompts/<feature-name>/`
  - General work → `history/prompts/general/`
- PHRs must capture full user input and key assistant output
- No truncation or placeholder text in PHRs

### Architecture Decision Records (ADR)
- Suggest ADR for architecturally significant decisions:
  - Framework or library choices
  - Data model or schema design
  - API or interface contracts
  - Security or authentication approaches
  - Platform or infrastructure decisions
- Use three-part test: Impact + Alternatives + Scope
- Suggest: "📋 Architectural decision detected: [brief]. Document? Run `/sp.adr [title]`"
- Wait for user consent; never auto-create ADRs
- Store ADRs in `history/adr/`

## Governance

### Constitutional Authority
- This constitution is the stable foundation for the entire project
- All specs, plans, tasks, and implementations must comply with this constitution
- The constitution supersedes all other practices and conventions
- New features must align with the constitution unless formally amended

### Amendment Process
- Amendments follow semantic versioning:
  - **MAJOR**: Breaking changes to core principles or technical stack
  - **MINOR**: New principles or significant guideline changes
  - **PATCH**: Clarifications or minor corrections
- All amendments must be documented with rationale
- Amendment history tracked in this file

### Compliance & Enforcement
- All PRs and reviews must verify constitution compliance
- Any intentional deviation must be explicitly justified and recorded
- Complexity or exceptions must be documented
- Constitution violations are blockers for merge/deploy

### Migration & Versioning
- When constitution changes, migration plan required for existing code/content
- Version bumps trigger review of all active specs and features
- Breaking changes require explicit approval and communication

---

**Version**: 1.0.0
**Ratified**: 2025-11-28
**Last Amended**: 2025-11-28
