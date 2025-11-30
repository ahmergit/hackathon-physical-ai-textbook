---
id: "0002"
title: "Chapter 1 Lessons 2-5 Architecture Planning"
stage: plan
date: 2025-11-28
surface: agent
model: Claude Opus 4.5
feature: 002-chapter1-lessons-2-5
branch: 002-chapter1-lessons-2-5
user: user
command: /sp.plan
labels: ["chapter-1", "lessons", "architecture", "content-planning"]
links:
  spec: specs/002-chapter1-lessons-2-5/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-chapter1-lessons-2-5/plan.md
  - specs/002-chapter1-lessons-2-5/research.md
  - specs/002-chapter1-lessons-2-5/data-model.md
  - specs/002-chapter1-lessons-2-5/quickstart.md
  - specs/002-chapter1-lessons-2-5/contracts/content-schema.json
tests:
  - Constitution check passed
---

## Prompt

— Chapter 1, Lessons 2–5 (Detailed)

We are planning the generation of Chapter 1, Lessons 2 through 5 for "Physical AI & Humanoid Robotics". Each lesson must have approximately 1200 words, structured with three main headings (H3) representing the lesson's primary sections, and each main heading will have three subheadings (H4) where necessary to clarify detailed concepts. Every subheading must include an Expert Insight paragraph of about 4 lines to highlight practical applications, research examples, or key considerations.

Lesson 2 — Why Embodied Intelligence Matters:
Main Headings: Importance of Physical Grounding, Interaction with the Environment, Real-World Learning Challenges

Lesson 3 — Evolution of AI: From LLMs to Vision-Language-Action Systems:
Main Headings: Digital-Only AI Systems, Multimodal Intelligence Integration, Action-Oriented Embodied AI

Lesson 4 — The Embodied AI Pipeline: Perception → Planning → Action:
Main Headings: Perception Systems in Robotics, Planning and Decision-Making, Action Execution and Feedback

Lesson 5 — Traditional Physical AI Falls Short:
Main Headings: Limitations of Classical Robotics, Challenges in Unstructured Environments, Modern Embodied AI Solutions

## Response snapshot

Created complete implementation plan with Phase 0 (research) and Phase 1 (design) artifacts:
- plan.md: Technical context, constitution check (passed), content architecture for 4 lessons
- research.md: Research findings for each lesson topic with key systems and milestones
- data-model.md: Entity definitions (Lesson, MainSection, Subsection, ExpertInsight)
- quickstart.md: Step-by-step implementation guide
- contracts/content-schema.json: JSON schema for content validation

Content inventory: 4 lessons × 3 H3 × 3 H4 = 36 expert insights, ~4800 total words

## Outcome

- ✅ Impact: Complete architecture plan for Chapter 1 Lessons 2-5 content generation
- 🧪 Tests: Constitution check passed all 10 principles
- 📁 Files: 5 artifacts created (plan.md, research.md, data-model.md, quickstart.md, content-schema.json)
- 🔁 Next prompts: /sp.tasks to generate implementation tasks
- 🧠 Reflection: User provided detailed structure requirements that mapped directly to content architecture

## Evaluation notes (flywheel)

- Failure modes observed: None - clear requirements and existing template (Lesson 1)
- Graders run and results (PASS/FAIL): Constitution check PASS
- Prompt variant (if applicable): Standard /sp.plan flow
- Next experiment (smallest change to try): None needed
