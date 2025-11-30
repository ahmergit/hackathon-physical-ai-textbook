---
id: 002
title: Create Docusaurus Implementation Plan
stage: plan
date: 2025-11-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: docusaurus-site-structure
branch: master
user: human
command: /sp.plan
labels: ["planning", "architecture", "docusaurus", "implementation-design", "adr"]
links:
  spec: specs/docusaurus-site-structure/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/docusaurus-site-structure/plan.md
  - history/prompts/docusaurus-site-structure/002-create-docusaurus-implementation-plan.plan.prompt.md
tests:
  - N/A (planning phase)
---

## Prompt

/sp.plan

We are defining the final technical implementation plan for the Docusaurus 3.9.2 book website as a single, clear, implementation-focused paragraph.

The site will be built using Docusaurus 3.9.2 with React 18 and TypeScript, using MDX for all book pages organized into Parts → Chapters → Lessons stored under /docs. All custom UI will be implemented through reusable React components in /src/components—including the Header, HomepageHero, TagBlock, BookLayout, and AITools—while all documentation pages will use a custom Docs layout override placed in /src/theme/DocItem/ to inject breadcrumbs, AI tool buttons, and a right-hand table of contents. The homepage will feature a dark-themed sticky header with the book title on the left and a GitHub link on the right, followed by a centered hero section containing the book cover, main title, subtitle, a "Start Reading" button linking to /docs/preface, and a tag block showing "Open Source" and "Embodied Intelligence." Book pages will use a three-column layout consisting of a left sidebar (auto-generated from sidebars.ts to show all Parts, Chapters, and Lessons), a central reading column rendering MDX text with clean typography, and a right sticky TOC showing H2/H3 headings. Each chapter will contain exactly three lessons, stored as /docs/part-x/chapter-y/lesson-z.md, each with a main heading and subsection headings to support Docusaurus TOC generation. Mobile layouts will collapse the left sidebar and hide the right TOC, preserving readability. Configuration updates include enabling dark mode by default in docusaurus.config.ts, adding navbar items (title, GitHub), registering custom components, and enabling full static export for GitHub Pages deployment. The final deliverables are a complete Docusaurus site with a polished homepage, structured book navigation, responsive three-column reading layout, integrated AI tool buttons, and a fully deployable static website.

## Response snapshot

Created comprehensive architectural implementation plan for Docusaurus 3.9.2 static site structure following constitution architect guidelines.

**Plan Summary:**

**1. Scope and Dependencies:**
- **In Scope**: Docusaurus 3.9.2 with TypeScript/React 18, homepage (header, hero, tags), three-column book layout (sidebar, content, TOC), custom components (Header, HomepageHero, TagBlock, BookLayout, AITools), theme override for breadcrumbs, Parts → Chapters → Lessons hierarchy, responsive design, GitHub Pages deployment
- **Out of Scope**: AI-generated content, RAG assistant implementation, advanced search, analytics, multi-language support
- **External Dependencies**: Node.js 18+, npm, Docusaurus 3.9.2, React 18, TypeScript 5.x, MDX 3.x, GitHub Pages
- **Internal Dependencies**: Constitution, spec.md, Git repository

**2. Key Decisions (8 decisions with rationale):**
- Docusaurus 3.9.2 as static site generator (vs Next.js, Gatsby, VuePress)
- MDX for all book content (vs plain Markdown, AsciiDoc)
- Three-tier hierarchy: Parts → Chapters → Lessons (vs two-tier or flat)
- Custom theme override via swizzling (vs custom plugin or fork)
- Auto-generated sidebar from folder structure (vs manual config)
- Dark mode as default (vs light mode or system preference)
- Exactly 3 lessons per chapter (consistency and predictability)
- GitHub Pages for deployment (vs Netlify, Vercel, AWS)

**3. Interface Contracts:**
- Folder structure: `/docs/part-{N}-{slug}/chapter-{M}-{slug}/lesson-{K}-{slug}.md`
- `_category_.json` schema for parts/chapters metadata
- Lesson frontmatter schema (id, title, sidebar_label, position, description, keywords)
- Component interfaces: Header, HomepageHero, TagBlock, BookLayout, AITools
- Configuration contracts: `docusaurus.config.ts`, `sidebars.ts`

**4. Non-Functional Requirements:**
- Performance: Build < 60s, FCP < 1.5s, TTI < 3s, Lighthouse > 90
- Reliability: 100% build success for valid content, error handling for broken links
- Security: No secrets in code, npm audit before deployment, XSS prevention
- Accessibility: WCAG 2.1 AA compliance, keyboard navigation, screen reader support
- SEO: Unique meta tags, sitemap, Open Graph tags

**5. Data Management:**
- Source of truth: MDX files in `/docs/` (version-controlled)
- Generated artifacts: Static HTML in `/build/` (not version-controlled)
- Schema evolution: Backward-compatible frontmatter changes
- Rollback: Git-based revert to previous commit

**6. Operational Readiness:**
- Observability: Build logs, GitHub Actions monitoring
- Alerting: Build failures, deployment failures, performance regression
- Runbooks: Build failure, deployment failure, performance regression
- Deployment: Blue-green via GitHub Pages, GitHub Actions workflow
- Backward compatibility: Docusaurus version pinning, theme override testing

**7. Risk Analysis:**
- Risk 1: Theme override breaks on Docusaurus upgrade (HIGH impact, MEDIUM likelihood) — Mitigation: Pin version, test upgrades in branch
- Risk 2: Large content slows build time (MEDIUM impact, MEDIUM likelihood) — Mitigation: Optimize images, monitor build times, incremental builds
- Risk 3: Broken links accumulate (MEDIUM impact, MEDIUM likelihood) — Mitigation: Docusaurus link checking, pre-commit hooks

**8. Implementation Roadmap (6 phases, 14 days):**
- Phase 1: Project setup (Days 1-2) — Install Docusaurus, configure Git, configure docusaurus.config.ts
- Phase 2: Homepage implementation (Days 3-4) — Header, HomepageHero, TagBlock components
- Phase 3: Documentation structure (Days 5-7) — Folder structure, _category_.json, sidebars.ts
- Phase 4: Custom layout and theme override (Days 8-10) — Swizzle DocItem/Layout, BookLayout, AITools, breadcrumbs
- Phase 5: Styling and polish (Days 11-12) — Custom CSS, optimize images, favicon, dark/light mode
- Phase 6: Testing and deployment (Days 13-14) — Build tests, Lighthouse, accessibility, cross-browser, GitHub Pages

**9. ADR Suggestions (4 significant decisions):**
1. Static Site Generator Selection (Docusaurus vs Next.js vs Gatsby)
2. Content Format Selection (MDX vs Markdown vs AsciiDoc)
3. Theme Customization Strategy (Swizzling vs Custom Plugin vs Fork)
4. Deployment Platform Selection (GitHub Pages vs Netlify vs Vercel)

**Testing Strategy:**
- Build tests: npm build, TypeScript compilation, link checking
- Visual regression tests: Manual testing on Chrome/Firefox/Safari (desktop + mobile)
- Performance tests: Lighthouse audits (Performance > 90, FCP < 1.5s)
- Accessibility tests: Lighthouse, keyboard navigation, screen reader testing
- Cross-browser tests: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

**Success Metrics:**
- Build time < 60 seconds
- Lighthouse Performance/Accessibility > 90
- Mobile-responsive on 320px+ screens
- All functional requirements met (FR-1 to FR-9)

## Outcome

- ✅ Impact: Complete, production-ready architectural plan created following constitution architect guidelines. Covers scope, decisions, contracts, NFRs, data management, operational readiness, risks, roadmap, and ADR suggestions.
- 🧪 Tests: Planning phase - no tests yet. Comprehensive testing strategy defined in plan (build, visual, performance, accessibility, cross-browser).
- 📁 Files: Created `specs/docusaurus-site-structure/plan.md` (comprehensive plan document ~1000 lines)
- 🔁 Next prompts: Document ADRs using `/sp.adr <title>` for 4 significant decisions, then run `/sp.tasks` to break down implementation into executable tasks
- 🧠 Reflection: Plan aligns with constitution principles (automation-first, type safety, performance targets, modularity). All decisions have clear rationale and trade-offs. 14-day roadmap with 6 phases provides clear implementation path. 4 ADRs identified for architectural decisions.

## Evaluation notes (flywheel)

- Failure modes observed: None - plan complete and compliant with constitution architect guidelines
- Graders run and results (PASS/FAIL): Manual review - PASS (all sections complete per architect template: scope, decisions, contracts, NFRs, data mgmt, ops, risks, validation, ADRs)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to `/sp.adr` for 4 significant decisions, then `/sp.tasks` for task breakdown
