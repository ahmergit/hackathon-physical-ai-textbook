---
id: 0002
title: Chapter 1 Architecture Planning
stage: plan
date: 2025-11-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-chapter-1-physical-ai
branch: 001-chapter-1-physical-ai
user: user
command: /sp.plan
labels: ["architecture", "docusaurus", "react-components", "content-structure"]
links:
  spec: specs/001-chapter-1-physical-ai/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-chapter-1-physical-ai/plan.md
 - specs/001-chapter-1-physical-ai/research.md
 - specs/001-chapter-1-physical-ai/data-model.md
 - specs/001-chapter-1-physical-ai/quickstart.md
 - specs/001-chapter-1-physical-ai/contracts/react-components.ts
 - specs/001-chapter-1-physical-ai/contracts/content-schema.json
 - specs/001-chapter-1-physical-ai/contracts/category-schema.json
tests:
 - Constitution compliance validated (all 10 principles)
 - JSON schemas created for frontmatter and category configs
 - Component contracts defined with TypeScript interfaces
---

## Prompt

We are building Chapter 1 of the book "The Rise of Physical AI: From Digital to Embodied Intelligence" as part of the Docusaurus 3.9.2 site. Each lesson in this chapter will be fully structured and formatted for maximum clarity, interactivity, and readability. The chapter contains five lessons, each ranging from 900 to 1100 words, with nested subheadings and expert insights embedded under each main subheading.

Lesson 1, Introduction to Physical AI, will introduce the concept, define its scope, and differentiate it from purely digital AI. Subheadings include Definition and Scope, Historical Context, and Key Applications Today. Each of these subheadings contains two sub-subheadings, and under each main subheading, a four-line Expert Insight explains the significance of the content.

Lesson 2, Why Embodied Intelligence Matters, explains the limitations of purely digital intelligence, emphasizes the need for sensorimotor grounding, and details how real-world feedback loops support adaptive behavior. Its subheadings are Intelligence Beyond Code, Grounding in Physical World, and Sensorimotor Feedback Loops, each with two nested sub-subheadings and expert insights.

Lesson 3, Evolution of AI: From LLMs to Vision-Language-Action Systems, covers the shift from language-only models to multimodal systems capable of perception and action. Subheadings include From Digital AI to Multimodal Systems, Integrating Action in AI, and Case Studies. Each contains two sub-subheadings and expert insights explaining real-world applications and research examples.

Lesson 4, The Embodied AI Pipeline: Perception → Planning → Action, focuses on the robot intelligence workflow. Subheadings are Perception and Sensing, Planning and Decision-Making, and Physical Action Execution. Each main subheading has two nested sub-subheadings and four-line expert insights highlighting the pipeline from sensing to actuation.

Lesson 5, Traditional Physical AI Falls Short, discusses the limitations of classical robotics approaches, and how modern embodied AI overcomes them. Its subheadings are Limitations of Classical Robotics, Modern Embodied AI Solutions, and Comparative Analysis, each with two sub-subheadings and expert insights illustrating why learning-based and adaptive systems are superior.

The file structure for this chapter will follow Docusaurus conventions: /docs/part-01/chapter-01/lesson-01.md through /lesson-05.md. The left sidebar will display the Part → Chapter → Lesson hierarchy, breadcrumbs will show Home > Part 1 > Chapter 1 > Lesson X, and a sticky right-hand TOC will automatically display H2 and H3 headings. AI tools, such as Summary and Personalize buttons, will appear near the main heading of each lesson. The entire chapter will use a fully responsive dark theme with clean typography and optional diagrams or visual aids where relevant.

## Response snapshot

Created comprehensive architectural plan for Chapter 1 with the following deliverables:

**Phase 0: Research** (research.md)
- 10 key technology decisions documented with rationale and alternatives
- Confirmed Docusaurus 3.9.2 as static site generator
- Established content structure: /docs/part-01/chapter-01/lesson-{NN}.md
- Selected Mermaid for diagrams, Docusaurus admonitions for expert insights
- Defined React components for AI tools (SummaryButton, PersonalizeButton)

**Phase 1: Design** (data-model.md, contracts/, quickstart.md)
- Defined 11 content entities (Part, Chapter, Lesson, Section, Subsection, etc.)
- Created TypeScript interfaces for all React components
- JSON schemas for frontmatter and category configuration validation
- Entity relationship diagram showing Part → Chapter → Lesson → Section hierarchy
- Validation rules: word count (900-1100), heading structure (H1→H2→H3→H4), expert insights (3 per lesson)

**API Contracts**:
- react-components.ts: SummaryButtonProps, PersonalizeButtonProps, LessonFrontmatter, CategoryConfig
- content-schema.json: Validates sidebar_position, description, keywords, etc.
- category-schema.json: Validates label, position, collapsible, collapsed

**Implementation Guide** (quickstart.md):
- 7-step process: directory structure → components → content → visuals → validation → commit → deploy
- Component code examples (SummaryButton.tsx, PersonalizeButton.tsx with CSS modules)
- Lesson template with MDX imports and admonitions
- Validation commands (word count, heading structure, type checking, build)
- Estimated implementation time: 6-8 hours

**Technical Architecture**:
- Hierarchical Markdown files with auto-generated sidebar
- H2/H3 headings in right TOC, breadcrumbs from folder structure
- React components embedded via MDX imports
- Dark theme default, responsive design, <2s page load target
- Mermaid diagrams for Lessons 3 (evolution timeline) and 4 (pipeline)

## Outcome

- ✅ Impact: Complete architectural plan with research, data model, contracts, and quickstart guide ready for implementation
- 🧪 Tests: Constitution compliance validated, JSON schemas created, component contracts defined
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, 3 contract files
- 🔁 Next prompts: /sp.tasks to generate granular task breakdown, then implement following quickstart.md
- 🧠 Reflection: Plan balances Docusaurus conventions with custom requirements (word count, expert insights, AI tools). Manual content writing ensures quality over AI-generated filler. Reusable structure supports future chapters.

## Evaluation notes (flywheel)

- Failure modes observed: None - all requirements mapped to technical solutions
- Graders run and results (PASS/FAIL): PASS - Constitution check validated all 10 principles
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Consider ADR for Docusaurus platform choice (long-term decision affecting all chapters)
