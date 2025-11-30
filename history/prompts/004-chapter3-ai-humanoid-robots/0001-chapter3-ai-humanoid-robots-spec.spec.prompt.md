---
id: 0001
title: Chapter 3 AI Humanoid Robots Spec
stage: spec
date: 2025-11-29
surface: agent
model: Claude Opus 4.5 (Preview)
feature: 004-chapter3-ai-humanoid-robots
branch: 004-chapter3-ai-humanoid-robots
user: agent
command: /sp.specify
labels: ["chapter3", "ai-humanoid-robots", "education", "o-level", "specification"]
links:
  spec: specs/004-chapter3-ai-humanoid-robots/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-chapter3-ai-humanoid-robots/spec.md
  - specs/004-chapter3-ai-humanoid-robots/checklists/requirements.md
tests:
  - null
---

## Prompt

[CHAPTER_NAME]
Chapter 3 — AI & Humanoid Robots: How Intelligence Powers Real-World Machines

[PURPOSE]
This chapter teaches O-Level students how modern AI and humanoid robots work together to sense, think, and act — explaining robotics mechanics, AI decision-making, and real-world applications in a simple, accessible way. The chapter uses recent 2025 research and industry reports to ground lessons in reality, helping students understand why robotics + AI matters now and how it shapes the future.

[CHAPTER_INDEX_REQUIREMENTS]
Produce an index.md file of approximately 1100 words.
Tone: Clear, simple, engaging — suitable for teenagers or early learners.
Include: Overview of why AI + humanoid robots are important, what students will learn in this chapter (brief intros to each lesson), short explanation of how recent robotics advances (2025) make robots powerful, a hopeful note about future careers and opportunities in robotics + AI.

[LESSON_COUNT] 5

[LESSON_FORMAT_RULES]
For each lesson (1–5): Generate content of ~1300 words. Use structure: three main headings (H2), each with three subheadings (H3). Include exactly 2 Expert Insight blocks (4–5 lines each). Use simple language, analogies, and avoid heavy math. Lessons should feel like classroom teaching, with examples, stories, and clear explanations.

[LESSONS]
- Lesson 1: Why Humanoid Robots Matter Today & Tomorrow (References: Fundacion Bankinter, AA.com.tr)
- Lesson 2: Automation & Flexibility: How AI-Driven Humanoid Robots Change Work (References: GlobeNewswire, WEForum)
- Lesson 3: Service & Care: Robots in Homes, Hospitals, and Everyday Life (References: QITP, Fundacion Bankinter)
- Lesson 4: Challenges & Ethics: What We Must Think About When Robots Join Society (References: WEForum, AA.com.tr)
- Lesson 5: Future Skills: How You Can Be Ready for a Robot-AI Future (References: Fundacion Bankinter, GlobeNewswire)

[OUTPUT_FILES] index.md, lesson-1.md, lesson-2.md, lesson-3.md, lesson-4.md, lesson-5.md

[GOAL]
Produce a beginner-friendly but scientifically grounded chapter teaching O-Level students how AI-driven humanoid robots work and why they matter — preparing them intellectually and morally for a robot-integrated future.

## Response snapshot

Created feature specification for Chapter 3 — AI & Humanoid Robots. Key deliverables:

1. **Branch**: `004-chapter3-ai-humanoid-robots` created and checked out
2. **Spec file**: `specs/004-chapter3-ai-humanoid-robots/spec.md` with:
   - 6 user stories (index page + 5 lessons)
   - 23 functional requirements covering structure, content, and references
   - 10 measurable success criteria
   - Key entities, assumptions, and dependencies documented
3. **Quality checklist**: All items passed (no clarifications needed)

Specification is ready for `/sp.plan` phase.

## Outcome

- ✅ Impact: Complete specification for Chapter 3 educational content
- 🧪 Tests: N/A (specification phase)
- 📁 Files: spec.md, checklists/requirements.md
- 🔁 Next prompts: /sp.plan to create implementation plan
- 🧠 Reflection: Clear requirements with well-defined structure and measurable success criteria

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - all quality checklist items satisfied
- Prompt variant (if applicable): Standard /sp.specify flow
- Next experiment (smallest change to try): None needed
