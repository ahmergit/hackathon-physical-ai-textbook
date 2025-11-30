---
id: 0002
title: Chapter 2 Architecture Planning
stage: plan
date: 2025-11-28
surface: agent
model: Claude Opus 4.5 (Preview)
feature: 003-chapter2-workforce-physical-ai
branch: 003-chapter2-workforce-physical-ai
user: agent
command: /sp.plan
labels: ["chapter2", "architecture", "planning", "docusaurus", "mdx"]
links:
  spec: specs/003-chapter2-workforce-physical-ai/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-chapter2-workforce-physical-ai/plan.md
  - specs/003-chapter2-workforce-physical-ai/spec.md (updated with research sources)
tests:
  - Constitution check passed all 10 principles
  - Post-design re-check passed
---

## Prompt

Create implementation plan for Chapter 2 in Docusaurus 3.9.2 with:
- MDX files in /docs/chapter-02/
- index.md (~800 words) + 5 lessons (~1200 words each)
- Automatic sidebar via sidebars.ts
- Breadcrumbs and sticky TOC enabled
- Dark theme via BookLayout and DocItem components

Research sources to integrate:
- Lesson 1: McKinsey "Agents, Robots, and Us" - https://www.mckinsey.com/mgi/our-research/agents-robots-and-us-skill-partnerships-in-the-age-of-ai
- Lesson 2: WEF human skills - https://www.weforum.org/agenda/2023/08/ai-human-skills-future-of-work/
- Lesson 3: Brookings automation - https://www.brookings.edu/articles/automation-and-artificial-intelligence-how-machines-affect-people-and-places/
- Lesson 4: OECD robotics economy - https://www.oecd.org/digital/robotics-impact-on-economy/
- Lesson 5: UNESCO AI education - https://www.unesco.org/en/digital-education/ai-skills-future

Structure: 3 H2 headings × 3 H3 subheadings per lesson, 2 expert insights each.

## Response snapshot

Created comprehensive plan.md with:
- Technical context (Docusaurus 3.9.2, MDX, dark theme)
- Research sources table with all 5 URLs and focus areas
- Constitution check (all 10 principles passed)
- Project structure for specs and source files
- Complete lesson content architecture with all headings
- Implementation phases (Research → Design → Generation → Validation)
- Risks and mitigations matrix
- Success metrics

Also updated spec.md with Research Sources by Lesson section containing all 5 authoritative sources.

## Outcome

- ✅ Impact: Complete architecture plan ready for task generation
- 🧪 Tests: Constitution check passed, post-design re-check passed
- 📁 Files: plan.md (320 lines), spec.md updated with research sources
- 🔁 Next prompts: /sp.tasks to generate implementation tasks
- 🧠 Reflection: Plan follows Chapter 1 pattern, adds research grounding for authenticity

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed successfully
- Graders run and results (PASS/FAIL): Constitution check - PASS
- Prompt variant (if applicable): Architecture planning with external research sources
- Next experiment (smallest change to try): N/A - proceed to task generation
