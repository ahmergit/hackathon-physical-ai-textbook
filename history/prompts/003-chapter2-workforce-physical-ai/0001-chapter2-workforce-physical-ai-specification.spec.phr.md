---
id: 0001
title: Chapter 2 Workforce Physical AI Specification
stage: spec
date: 2025-11-28
surface: agent
model: Claude Opus 4.5 (Preview)
feature: 003-chapter2-workforce-physical-ai
branch: 003-chapter2-workforce-physical-ai
user: agent
command: /sp.specify
labels: ["chapter2", "workforce", "physical-ai", "humanoid-robotics", "specification"]
links:
  spec: specs/003-chapter2-workforce-physical-ai/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-chapter2-workforce-physical-ai/spec.md
  - specs/003-chapter2-workforce-physical-ai/checklists/requirements.md
tests:
  - Specification quality checklist validation (all items passed)
---

## Prompt

Chapter 2 — Humans, Agents & Robots: The Emerging Workforce of Physical AI

PURPOSE: Define the central role of humans, AI agents, and humanoid robots as a unified collaborative workforce. This chapter explains why Physical AI reshapes skills, productivity, and society, drawing heavily on insights from McKinsey's "Agents, Robots, and Us" report. It sets the foundation for understanding how embodied intelligence transforms real-world work.

CHAPTER_INDEX_REQUIREMENTS:
- Produce an index.md file of approximately 800 words
- Tone: professional, educational, forward-looking, suitable for university-level learners
- Must include high-level explanation of human-AI-robot collaboration, why chapter is core building block, 1-2 paragraph intro for each lesson, concluding perspective on workforce reshaping

LESSON_COUNT: 5

LESSON_FORMAT_RULES:
- Length: ~1200 words per lesson
- Structure: 3 main headings (H2), each with 3 subheadings (H3)
- 2 Expert Insights per lesson (4-5 lines each)
- Professional, educational writing style with strong Physical AI linkage

LESSONS:
1. The New Partnership Paradigm: People + Agents + Robots
2. Skills Under Transformation: What Humans Still Bring
3. Hybrid Roles: Where Embodied AI Meets Human Judgment
4. Societal Impact & Economic Shifts in Robotics-Enabled Work
5. Preparing for the Workforce of 2030: Education, Ethics & Adaptability

OUTPUT_FILES: index.md, lesson-1.md through lesson-5.md

## Response snapshot

Created comprehensive specification for Chapter 2 with:
- 6 user stories covering all 5 lessons plus index.md (5 P1 priority, 1 P2 priority)
- 35 functional requirements organized by category (index, lesson structure, content quality, lesson-specific)
- 6 key entities defining core content types
- 11 measurable success criteria
- 8 documented assumptions
- 4 edge cases identified
- Quality checklist created and validated (all items passed)

Branch created: 003-chapter2-workforce-physical-ai
Spec file: specs/003-chapter2-workforce-physical-ai/spec.md

## Outcome

- ✅ Impact: Complete specification ready for planning phase, defines full content structure for Chapter 2
- 🧪 Tests: Quality checklist validation passed all items
- 📁 Files: spec.md (195 lines), checklists/requirements.md (35 lines)
- 🔁 Next prompts: /sp.plan to create architecture plan, /sp.tasks to generate implementation tasks
- 🧠 Reflection: Specification follows established pattern from Chapter 1 specs, comprehensive requirements capture all lesson structure and content needs

## Evaluation notes (flywheel)

- Failure modes observed: None - specification completed successfully following template
- Graders run and results (PASS/FAIL): Manual quality checklist - PASS
- Prompt variant (if applicable): Standard /sp.specify with detailed chapter requirements
- Next experiment (smallest change to try): N/A - proceed to planning phase
