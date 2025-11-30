# Implementation Plan: Chapter 1 - The Rise of Physical AI

**Branch**: `001-chapter-1-physical-ai` | **Date**: 2025-11-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-chapter-1-physical-ai/spec.md`

## Summary

Create Chapter 1 "The Rise of Physical AI: From Digital to Embodied Intelligence" as part of a Docusaurus 3.9.2 static site. The chapter contains 5 comprehensive lessons (900-1100 words each) covering: (1) Introduction to Physical AI, (2) Why Embodied Intelligence Matters, (3) Evolution from LLMs to Vision-Language-Action Systems, (4) The Embodied AI Pipeline (Perception → Planning → Action), and (5) Why Traditional Physical AI Falls Short.

**Technical Approach**: Use existing Docusaurus setup with hierarchical file structure (`/docs/part-01/chapter-01/lesson-{01-05}.md`), auto-generated sidebars, custom React components (SummaryButton, PersonalizeButton) embedded via MDX, Docusaurus admonitions for expert insights, and Mermaid diagrams for visual aids. Content will be manually written following strict word count and heading structure guidelines.

---

## Technical Context

**Language/Version**: TypeScript 5.2 (React components), Markdown/MDX (content)
**Primary Dependencies**: Docusaurus 3.9.2, React 18, @mdx-js/react 3.0, @docusaurus/theme-mermaid 3.9.2
**Storage**: Static Markdown files in `/docs` directory
**Testing**: Manual content validation (word count, heading structure), TypeScript type checking, Docusaurus build validation
**Target Platform**: Static site (browser), deployed to GitHub Pages or similar static host
**Project Type**: Web (static documentation site)
**Performance Goals**:
- Build time <60 seconds for full site
- Page load time <2 seconds (Lighthouse >90)
- Time to Interactive <3 seconds
**Constraints**:
- 900-1100 words per lesson (strict)
- H1 → H2 → H3 → H4 heading hierarchy (no H5)
- Exactly 3 expert insights per lesson
- Dark theme default with responsive design
**Scale/Scope**:
- 5 lessons in Chapter 1
- 2 React components (SummaryButton, PersonalizeButton)
- 5-7 Mermaid diagrams across lessons
- Expected total: ~5000 words of content

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Spec-Driven Development ✓
- [x] Feature has formal specification (`spec.md`)
- [x] All requirements documented with acceptance criteria
- [x] No ad-hoc content or component development

### II. Single Source of Truth ✓
- [x] Spec defines all content structure and behavior
- [x] Markdown files are generated/written from spec requirements
- [x] React components follow contracts in `contracts/react-components.ts`

### III. Automation-First & Reproducible ✓
- [x] Content follows template structure (reusable for future chapters)
- [x] Category configs (`_category_.json`) follow JSON schema
- [x] Validation scripts planned for word count and heading structure

### IV. Code Quality & Type Safety ✓
- [x] TypeScript strict mode enabled (`tsconfig.json`)
- [x] React components have typed props interfaces
- [x] No `any` types in component code

### V. Testing & Validation ✓
- [x] JSON schemas for frontmatter and category configs
- [x] Manual validation process documented in quickstart
- [x] Docusaurus build serves as integration test

### VI. Performance & UX Consistency ✓
- [x] Performance targets defined (build time, page load, TTI)
- [x] Responsive design via Docusaurus defaults
- [x] Dark theme configured as default

### VII. Content Accuracy & Integrity ✓
- [x] No placeholders allowed in final content
- [x] No AI-generated filler or scaffolding
- [x] Expert insights must add value, not repeat content

### VIII. Separation of Concerns ✓
- [x] Internal instructions stay in specs/, not in lesson markdown
- [x] Component logic separate from content
- [x] No meta-commentary in published lessons

### IX. Minimal & Sufficient Content ✓
- [x] Each lesson has clear learning objective (FR-002)
- [x] No unnecessary repetition across lessons (FR-014)
- [x] Word count enforced (900-1100 per lesson)

### X. Modularity & Maintainability ✓
- [x] Clear project structure (`docs/part-01/chapter-01/`)
- [x] Reusable components (`SummaryButton`, `PersonalizeButton`)
- [x] Documentation in `quickstart.md`

**Status**: ✅ All constitution gates pass

---

## Project Structure

### Documentation (this feature)

```text
specs/001-chapter-1-physical-ai/
├── plan.md                           # This file
├── research.md                       # Technology decisions (Phase 0)
├── data-model.md                     # Content entities and structure (Phase 1)
├── quickstart.md                     # Implementation guide (Phase 1)
├── contracts/                        # API contracts (Phase 1)
│   ├── react-components.ts           # Component interfaces
│   ├── content-schema.json           # Frontmatter JSON schema
│   └── category-schema.json          # Category config JSON schema
├── checklists/                       # Validation checklists
│   └── requirements.md               # Spec quality checklist
└── spec.md                           # Feature specification
```

### Source Code (book-source directory)

```text
book-source/
├── docs/
│   ├── part-01/
│   │   ├── _category_.json           # Part 1 config
│   │   └── chapter-01/
│   │       ├── _category_.json       # Chapter 1 config
│   │       ├── lesson-01.md          # Introduction to Physical AI
│   │       ├── lesson-02.md          # Why Embodied Intelligence Matters
│   │       ├── lesson-03.md          # Evolution of AI
│   │       ├── lesson-04.md          # Embodied AI Pipeline
│   │       └── lesson-05.md          # Traditional Physical AI Falls Short
│   ├── intro.md                      # Existing intro page
│   └── preface.md                    # Existing preface
├── src/
│   ├── components/
│   │   ├── SummaryButton.tsx         # AI Summary component
│   │   ├── SummaryButton.module.css  # Styles
│   │   ├── PersonalizeButton.tsx     # Level personalization component
│   │   └── PersonalizeButton.module.css # Styles
│   └── css/
│       └── custom.css                # Global styles (existing)
├── static/
│   └── img/
│       └── chapter-01/               # Optional: diagrams/images
├── docusaurus.config.ts              # Site config (update for Mermaid)
├── sidebars.ts                       # Sidebar config (no changes needed)
├── package.json                      # Dependencies (add theme-mermaid)
└── tsconfig.json                     # TypeScript config (existing)
```

**Structure Decision**: Web application (documentation site) with React components embedded in Markdown. Content organized hierarchically: Part → Chapter → Lesson. All lesson files follow the same template structure for consistency and reusability.

---

## Complexity Tracking

No violations detected. All requirements align with constitution principles:
- Content structure is simple and hierarchical
- Components are minimal (2 total, both straightforward)
- No database, API, or backend complexity
- Static site generation is appropriate for read-only content

---

## Phase 0: Research Summary

**Document**: [research.md](./research.md)

### Key Decisions

1. **Static Site Generator**: Docusaurus 3.9.2 (already installed)
2. **Content Structure**: `/docs/part-01/chapter-01/lesson-{NN}.md`
3. **Word Count**: 900-1100 words per lesson
4. **Heading Hierarchy**: H2 for sections, H3 for subheadings, H4 for sub-subheadings
5. **Expert Insights**: Docusaurus admonitions (`:::tip`)
6. **AI Tools**: React components (SummaryButton, PersonalizeButton) via MDX
7. **Visual Aids**: Mermaid diagrams for timelines and pipelines
8. **Theme**: Dark mode default with responsive design
9. **Sidebar**: Auto-generated from folder structure
10. **Content Generation**: Manual writing (no AI-generated filler)

### Technologies Confirmed

- **Frontend**: React 18, TypeScript 5.2
- **Markdown**: MDX 3.0 (supports React component imports)
- **Diagrams**: Mermaid (via @docusaurus/theme-mermaid)
- **Styling**: CSS modules for components, custom.css for global styles
- **Validation**: JSON Schema for frontmatter and category configs

### Integration Patterns

- Components imported in MDX: `import SummaryButton from '@site/src/components/SummaryButton';`
- Admonitions for insights: `:::tip Expert Insight`
- Mermaid code blocks: `` ```mermaid ``
- Category configs: `_category_.json` files with JSON schema validation

---

## Phase 1: Design & Contracts Summary

### Data Model

**Document**: [data-model.md](./data-model.md)

**Core Entities**:
1. **Part**: Top-level category (Part 1: Foundations)
2. **Chapter**: Major thematic unit (Chapter 1: Rise of Physical AI)
3. **Lesson**: Self-contained learning module (5 lessons total)
4. **Section**: H2-level thematic division (3-5 per lesson)
5. **Subsection**: H3-level topic detail (2+ per section)
6. **Sub-subsection**: H4-level granular detail (0-2 per subsection)
7. **Expert Insight**: Highlighted commentary (3 per lesson)
8. **Key Takeaways**: Summary bullets (1 per lesson)
9. **Visual Aid**: Diagram or image (0-2 per lesson, optional)

**Component Entities**:
10. **SummaryButton**: React component for AI lesson summaries
11. **PersonalizeButton**: React component for skill level adaptation

### API Contracts

**Document**: [contracts/](./contracts/)

**Files Created**:
- `react-components.ts`: TypeScript interfaces for all components
- `content-schema.json`: JSON Schema for lesson frontmatter
- `category-schema.json`: JSON Schema for `_category_.json` files

**Key Interfaces**:
```typescript
SummaryButtonProps { lessonId, title?, className?, icon? }
PersonalizeButtonProps { lessonId, levels?, defaultLevel?, className? }
LessonFrontmatter { sidebar_position, description?, keywords?, slug?, title? }
CategoryConfig { label, position, collapsible, collapsed, link? }
```

### Implementation Guide

**Document**: [quickstart.md](./quickstart.md)

**7-Step Process**:
1. Create directory structure and category configs
2. Create React components (SummaryButton, PersonalizeButton)
3. Write lesson content (5 lessons × 900-1100 words)
4. Add visual aids (Mermaid diagrams in Lessons 3, 4)
5. Validate implementation (type check, build, test)
6. Git commit and push to feature branch
7. Deploy to GitHub Pages (optional)

**Estimated Time**: 6-8 hours total

---

## Implementation Checklist

### Phase 1 Artifacts (✅ Complete)

- [x] `research.md` - Technology decisions and patterns
- [x] `data-model.md` - Content entities and validation rules
- [x] `contracts/react-components.ts` - Component interfaces
- [x] `contracts/content-schema.json` - Frontmatter schema
- [x] `contracts/category-schema.json` - Category config schema
- [x] `quickstart.md` - Step-by-step implementation guide

### Next Phase: Tasks (Not created by /sp.plan)

Run `/sp.tasks` to generate:
- Granular task breakdown for each lesson
- Test cases for content validation
- Acceptance criteria for each functional requirement

---

## Risk Analysis

### Low Risks

**Content Quality**:
- **Risk**: Lessons may not achieve 900-1100 word target
- **Mitigation**: Use word count validation script in quickstart, iterate during writing

**Component Complexity**:
- **Risk**: SummaryButton/PersonalizeButton may not integrate cleanly with MDX
- **Mitigation**: Test components early in development, use simple prop interfaces

### Minimal Technical Risks

- Docusaurus 3.9.2 is stable and well-documented
- React components are straightforward (no complex state management)
- Static site generation eliminates backend/API risks
- No database or external service dependencies

---

## Success Metrics

From spec.md success criteria (SC-001 through SC-010):

**Content Metrics**:
- SC-001: 80%+ comprehension quiz accuracy (manual testing with readers)
- SC-002: 90% can explain Physical AI vs digital AI (user feedback)
- SC-003: Can trace AI evolution with 3+ examples (content review)
- SC-004: Can describe Perception-Planning-Action pipeline (content review)
- SC-005: Can identify 3+ traditional limitations and solutions (content review)

**Quality Metrics**:
- SC-007: 10-15 minute reading time per lesson (word count validation)
- SC-008: 4.5/5 technical accuracy (expert review)
- SC-009: 4/5 clarity for beginners (user testing)
- SC-010: 4/5 example relevance (reader feedback)

**Structural Metrics**:
- SC-006: Chapter structure reusable for future chapters (template adherence)

---

## Dependencies

### External Dependencies

1. **Docusaurus 3.9.2**: Already installed in `book-source/`
2. **Node.js 18+**: Required for Docusaurus build
3. **npm**: Package management
4. **@docusaurus/theme-mermaid**: For diagram support (to be installed)

### Internal Dependencies

1. **Spec completion**: ✅ Complete (spec.md)
2. **Research phase**: ✅ Complete (research.md)
3. **Data model**: ✅ Complete (data-model.md)
4. **Contracts**: ✅ Complete (contracts/)
5. **Quickstart**: ✅ Complete (quickstart.md)

### Content Dependencies

- Access to current (2025) Physical AI research and examples
- Technical review from robotics/AI domain experts
- Pedagogical review for beginner accessibility
- Visual design resources for diagrams (Mermaid code)

---

## Architectural Decisions

📋 **Potential ADR**: Using Docusaurus for educational content platform

**Decision**: Use Docusaurus 3.9.2 as the static site generator for the Physical AI book.

**Context**: Need a platform for publishing educational content with:
- Hierarchical content organization
- Interactive components (AI tools)
- Search, navigation, and mobile responsiveness
- Dark theme and modern UX

**Alternatives Considered**:
- Gatsby: More complex, overkill for documentation
- Next.js: Adds SSR complexity, unnecessary for static content
- VitePress: Vue ecosystem, different from existing setup
- Custom React app: Reinventing features Docusaurus provides

**Rationale**:
- Already installed and configured
- Built-in documentation features (sidebar, TOC, breadcrumbs)
- MDX support for React components
- Optimized for performance (static generation)
- Large community and ecosystem

**Impact**: Long-term platform choice affecting all future chapters.

**Recommendation**: Document this decision with `/sp.adr docusaurus-platform-choice` if user approves.

---

## Next Steps

1. **User Review**: Review this plan for approval
2. **Run /sp.tasks**: Generate granular task breakdown
3. **Implement**: Follow quickstart.md to build Chapter 1
4. **Validate**: Run content validation and test with readers
5. **ADR (Optional)**: Document Docusaurus platform decision

---

**Planning Status**: ✅ Complete
**Ready for**: `/sp.tasks` command to generate implementation tasks
**Branch**: `001-chapter-1-physical-ai`
**Artifacts Created**: research.md, data-model.md, contracts/, quickstart.md
