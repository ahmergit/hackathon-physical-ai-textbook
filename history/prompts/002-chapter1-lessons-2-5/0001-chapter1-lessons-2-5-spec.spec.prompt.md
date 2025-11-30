---
id: "0001"
title: "Chapter 1 Lessons 2-5 Specification"
stage: spec
date: 2025-11-28
surface: agent
model: Claude Opus 4.5
feature: 002-chapter1-lessons-2-5
branch: 002-chapter1-lessons-2-5
user: user
command: /sp.specify
labels: ["chapter-1", "lessons", "content-generation", "physical-ai"]
links:
  spec: specs/002-chapter1-lessons-2-5/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-chapter1-lessons-2-5/spec.md
  - specs/002-chapter1-lessons-2-5/checklists/requirements.md
tests:
  - null
---

## Prompt

— Chapter 1 Lessons 2–5 Instruction

Context: Chapter 1 — The Rise of Physical AI: From Digital to Embodied Intelligence
We are generating Lessons 2 through 5. Each lesson must follow the structure of Lesson 1 that was successfully generated.

Requirements for Each Lesson:

Word Count: 900–1100 words per lesson.

Content Structure:

Main Heading: H1 for the lesson title.

Subheadings: At least 3–4 subheadings (H2) per lesson.

Sub-subheadings: Each H2 should have at least 2 H3 sub-subheadings where appropriate.

Expert Insight: For each main subheading, include 1–2 expert insight paragraphs (~4 lines each) explaining the key concept.

Content Quality:

Clear, accurate, and professional explanation of AI concepts.

Maintain dark-theme-friendly formatting suitable for Docusaurus MDX.

Avoid filler content; each paragraph must contribute to understanding the lesson topic.

Lesson-Specific Topics:

Lesson 2 — Why Embodied Intelligence Matters: Explain why AI needs real-world grounding, perception, and action; include examples of robots or embodied systems.

Lesson 3 — Evolution of AI: From LLMs to Vision-Language-Action Systems: Explain the transition from digital-only AI to multimodal AI with action capabilities. Include timeline and key milestones.

Lesson 4 — The Embodied AI Pipeline: Perception → Planning → Action: Detail each stage with examples, challenges, and modern approaches.

Lesson 5 — Traditional Physical AI Falls Short: Analyze classical robotics limitations and how modern approaches address them. Include comparisons with modern embodied AI methods.

Formatting:

Use Markdown/MDX headings correctly.

Include bullet points or numbered lists where helpful.

Keep all content ready for direct insertion into /docs/part-01/chapter-01/lesson-XX.md.

Consistency:

Follow the same tone, style, and depth as Lesson 1.

Ensure smooth transitions between lessons, as all lessons form a coherent chapter.

Goal: Generate fully fleshed lessons 2–5 for Chapter 1, ready for MDX integration in the Docusaurus book.

## Response snapshot

Created feature branch `002-chapter1-lessons-2-5` and specification document with:
- 4 user stories (P1-P2) covering all 4 lessons
- 19 functional requirements for content structure, format, and topic coverage
- 7 measurable success criteria
- Quality checklist (all items passed)
- No clarifications needed - requirements clear from detailed user input

## Outcome

- ✅ Impact: Specification complete for Chapter 1 Lessons 2-5 content generation
- 🧪 Tests: Checklist validation passed all items
- 📁 Files: spec.md, checklists/requirements.md created
- 🔁 Next prompts: /sp.plan to create implementation plan
- 🧠 Reflection: User provided exceptionally detailed requirements including word counts, structure, and reference to Lesson 1 template

## Evaluation notes (flywheel)

- Failure modes observed: None - clear requirements from user
- Graders run and results (PASS/FAIL): Checklist validation PASS
- Prompt variant (if applicable): Standard /sp.specify flow
- Next experiment (smallest change to try): None needed
