---
id: 0002
title: Chapter 3 AI Humanoid Robots Plan
stage: plan
date: 2025-11-29
surface: agent
model: Claude Opus 4.5 (Preview)
feature: 004-chapter3-ai-humanoid-robots
branch: 004-chapter3-ai-humanoid-robots
user: agent
command: /sp.plan
labels: ["chapter3", "ai-humanoid-robots", "education", "planning", "content-architecture"]
links:
  spec: specs/004-chapter3-ai-humanoid-robots/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-chapter3-ai-humanoid-robots/plan.md
  - specs/004-chapter3-ai-humanoid-robots/research.md
  - specs/004-chapter3-ai-humanoid-robots/data-model.md
  - specs/004-chapter3-ai-humanoid-robots/quickstart.md
  - specs/004-chapter3-ai-humanoid-robots/contracts/index-contract.md
  - specs/004-chapter3-ai-humanoid-robots/contracts/lesson-1-contract.md
  - specs/004-chapter3-ai-humanoid-robots/contracts/lesson-2-contract.md
  - specs/004-chapter3-ai-humanoid-robots/contracts/lesson-3-contract.md
  - specs/004-chapter3-ai-humanoid-robots/contracts/lesson-4-contract.md
  - specs/004-chapter3-ai-humanoid-robots/contracts/lesson-5-contract.md
tests:
  - null
---

## Prompt

[CHAPTER_NAME] Chapter 3 — AI & Humanoid Robots: How Intelligence Powers Real-World Machines

[CHAPTER_ARCHITECTURE] Create a structured chapter blueprint for writers who will produce index.md (~1100 words) and five lessons (each ~1300 words). Tone: Friendly, simple, and accessible for O-Level students. Focus: Explain how AI + humanoid robots work together, why they matter, how they impact homes, industries, and society, and what skills students need for the future.

[LESSON_PLANS]
- Lesson 1: Why Humanoid Robots Matter Today & Tomorrow (References: Fundación Bankinter, AA News)
- Lesson 2: Automation & Flexibility (References: GlobeNewswire, WEForum)
- Lesson 3: Service & Care (References: QITP, Fundación Bankinter)
- Lesson 4: Challenges & Ethics (References: WEForum, AA News)
- Lesson 5: Future Skills (References: Fundación Bankinter, GlobeNewswire)

[OUTPUT_FILES] index.md, lesson-1.md through lesson-5.md

[GOAL] Deliver complete instructional plan for chapter writers with real 2025 articles naturally integrated.

## Response snapshot

Created comprehensive implementation plan for Chapter 3 with:

1. **plan.md**: Technical context, constitution check (all PASS), project structure
2. **research.md**: Consolidated insights from 4 industry sources (Fundación Bankinter, AA News, GlobeNewswire, WEForum) with key statistics, expert quotes, and themes
3. **data-model.md**: Entity definitions (Chapter, Lesson, H2Section, H3Subsection, ExpertInsight), lesson structure templates with exact H2/H3 headings
4. **quickstart.md**: Writing guide for content creators with style rules, examples, checklists
5. **contracts/**: 6 detailed content contracts (index + 5 lessons) specifying exact requirements, acceptance criteria, and source integration

Key research findings incorporated:
- $7.3B robotics investment in H1 2025
- ~1 billion humanoid robots by 2050 projection
- Healthcare robotics +38% growth
- Key companies: Tesla Optimus, Boston Dynamics, PAL Robotics, Figure AI, Neura Robotics

## Outcome

- ✅ Impact: Complete chapter architecture ready for content writers
- 🧪 Tests: N/A (planning phase)
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, 6 contracts
- 🔁 Next prompts: /sp.tasks to create implementation tasks
- 🧠 Reflection: Research from actual 2025 sources provides strong foundation for credible, current content

## Evaluation notes (flywheel)

- Failure modes observed: QITP PDF source unavailable (worked around with other sources)
- Graders run and results (PASS/FAIL): PASS - constitution check passed all gates
- Prompt variant (if applicable): Standard /sp.plan flow
- Next experiment (smallest change to try): None needed
