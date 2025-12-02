<!--
  SYNC IMPACT REPORT
  ==================
  Version Change: 1.0.0 → 1.1.0
  
  Modified Principles:
    - None renamed
  
  Added Sections:
    - XI. Chapter Structural Consistency
    - XII. Modular Content Architecture
    - XIII. Technical Clarity & Actionability
    - XIV. Terminology & Style Alignment
    - XV. Reproducible Examples & Visuals
    - XVI. Implementation-Friendly Accuracy
    - XVII. Cross-Reference Integration
    - XVIII. Explicit Assumptions & Dependencies
    - XIX. Visual & Code Standards
    - XX. Textbook Quality Mission
  
  Removed Sections:
    - None
  
  Templates Requiring Updates:
    - .specify/templates/plan-template.md ✅ (Constitution Check aligns)
    - .specify/templates/spec-template.md ✅ (scope/requirements align)
    - .specify/templates/tasks-template.md ✅ (task types reflect new principles)
  
  Follow-up TODOs:
    - None
-->

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

### XI. Chapter Structural Consistency
All new chapters MUST follow a consistent structural template defined by the project's specification.

**Requirements:**
- Every chapter MUST use the approved chapter template structure
- Section headings, ordering, and hierarchy MUST match the template
- Front matter (metadata, prerequisites, learning objectives) MUST be present and complete
- Chapter numbering and naming MUST follow established conventions
- Deviations from template require explicit justification in the spec

### XII. Modular Content Architecture
Chapters MUST be written using clear, modular sections that enable future expansion without breaking coherence.

**Requirements:**
- Each section MUST be self-contained with clear entry and exit points
- Sections MUST support insertion of new content without restructuring existing material
- Avoid tight coupling between sections; use explicit references instead of implicit dependencies
- Content modules MUST have defined interfaces (prerequisites, outputs, linkable concepts)
- Expansion points MUST be documented for each major section

### XIII. Technical Clarity & Actionability
Each chapter MUST translate complex technical ideas into structured, actionable explanations.

**Requirements:**
- Abstract concepts MUST be accompanied by concrete examples or applications
- Explanations MUST progress from foundational to advanced logically
- Every technical claim MUST be verifiable or demonstrable
- Action steps MUST be explicit: "Do X to achieve Y"
- Avoid vague language ("might", "could", "somewhat"); use precise terminology

### XIV. Terminology & Style Alignment
All content MUST align with established terminology, formatting rules, and style guidelines across the project.

**Requirements:**
- Use glossary terms consistently; define new terms on first use
- Follow the project style guide for formatting (headings, code blocks, callouts)
- Maintain consistent voice (instructional, second-person where appropriate)
- Acronyms MUST be expanded on first use per chapter
- Units, notation, and conventions MUST match project standards

### XV. Reproducible Examples & Visuals
Chapters MUST include reproducible examples, diagrams, or workflows wherever the subject matter requires it.

**Requirements:**
- Code examples MUST be complete, runnable, and tested
- Diagrams MUST have source files (e.g., Mermaid, Draw.io) committed alongside renders
- Step-by-step workflows MUST be executable in sequence without hidden prerequisites
- Data used in examples MUST be provided or generated deterministically
- All visuals MUST have alt-text and captions

### XVI. Implementation-Friendly Accuracy
All explanations MUST stay technically accurate, implementation-friendly, and free from unnecessary abstraction.

**Requirements:**
- Descriptions MUST map to real implementations or APIs
- Avoid over-abstraction that obscures how to actually build or use something
- Include version numbers, compatibility notes, and known limitations
- Error handling and edge cases MUST be addressed, not ignored
- Performance implications MUST be stated where relevant

### XVII. Cross-Reference Integration
Any new chapter MUST integrate seamlessly into the project's internal cross-referencing system.

**Requirements:**
- All related chapters, sections, and concepts MUST be linked bidirectionally
- Use defined link syntax (e.g., `[Chapter X: Title](/path)`) consistently
- Update existing chapters to reference new content where appropriate
- Navigation (sidebar, TOC, breadcrumbs) MUST be updated on chapter addition
- Broken links MUST be detected and fixed before merge

### XVIII. Explicit Assumptions & Dependencies
Contributors MUST document assumptions, dependencies, and required background knowledge explicitly.

**Requirements:**
- Prerequisites section MUST list all required prior knowledge or completed chapters
- External dependencies (tools, libraries, accounts) MUST be listed with versions
- Assumptions about reader knowledge MUST be stated, not implied
- Environmental requirements (OS, hardware, network) MUST be documented
- Knowledge gaps MUST link to resources or preceding sections

### XIX. Visual & Code Standards
Visuals, examples, and code MUST follow the project's standards for clarity, naming, and maintainability.

**Requirements:**
- Code MUST use project naming conventions (camelCase, snake_case as defined)
- Variable and function names MUST be descriptive and self-documenting
- Diagrams MUST use consistent color schemes, fonts, and iconography
- Screenshots MUST be current, high-resolution, and annotated where helpful
- All code MUST pass linting and formatting checks before inclusion

### XX. Textbook Quality Mission
Every chapter addition MUST reinforce the project's core mission: creating a precise, consistent, and high-quality technical textbook.

**Requirements:**
- Content MUST meet academic or professional reference quality standards
- Every section MUST contribute to the reader's measurable learning outcomes
- Quality MUST be validated through review (automated checks, peer review, or testing)
- Chapters MUST be valuable standalone and as part of the complete textbook
- Continuous improvement: identified issues MUST be logged and addressed

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

**Version**: 1.1.0
**Ratified**: 2025-11-28
**Last Amended**: 2025-12-01
