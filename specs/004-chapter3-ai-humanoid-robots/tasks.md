# Tasks: Chapter 3 — AI & Humanoid Robots

**Branch**: `004-chapter3-ai-humanoid-robots`  
**Date**: 2025-11-29  
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

---

## Overview

This document breaks down the Chapter 3 feature into atomic, testable implementation tasks organized by user story. Each task includes acceptance criteria and references to contracts and research.

**Output Path**: `book-source/docs/chapter3/`

---

## US1: Index Page — Chapter Overview (P1)

**Contract**: [index-contract.md](./contracts/index-contract.md)  
**Target**: `book-source/docs/chapter3/index.md`  
**Word Count**: ~1100 words (990–1210 acceptable)

### Task 1.1: Create index.md file structure
- [x] Create file `book-source/docs/chapter3/index.md`
- [x] Add Docusaurus front matter (title, sidebar_position, description)
- [x] Add chapter title as H1

**Acceptance**:
- File exists at correct path
- Front matter is valid YAML
- Title matches: "Chapter 3 — AI & Humanoid Robots: How Intelligence Powers Real-World Machines"

### Task 1.2: Write opening hook section
- [x] Write engaging paragraph explaining why AI + humanoid robots matter NOW
- [x] Incorporate 2025 context: Tesla Optimus, Boston Dynamics Atlas, Figure AI
- [x] Use simple language suitable for O-Level students (ages 14–16)

**Acceptance**:
- Opening captures attention
- Mentions at least 2 recent robotics developments
- No jargon; any technical terms explained

### Task 1.3: Write lesson preview summaries
- [x] Write 2-3 sentence preview for Lesson 1 (Why Humanoid Robots Matter)
- [x] Write 2-3 sentence preview for Lesson 2 (Automation & Flexibility)
- [x] Write 2-3 sentence preview for Lesson 3 (Service & Care)
- [x] Write 2-3 sentence preview for Lesson 4 (Challenges & Ethics)
- [x] Write 2-3 sentence preview for Lesson 5 (Future Skills)

**Acceptance**:
- Each preview clearly states what student will learn
- Previews build curiosity without giving away all details
- Total ~400-500 words for this section

### Task 1.4: Write 2025 breakthroughs section
- [x] Highlight key advances making robots more capable
- [x] Reference research: $7.3B investment H1 2025, +38% healthcare growth
- [x] Explain why this decade is different from past robotics attempts

**Acceptance**:
- At least 3 concrete advances mentioned
- Statistics from research.md integrated naturally
- Tone is optimistic but grounded

### Task 1.5: Write career outlook section
- [x] Describe future job opportunities in robotics/AI
- [x] Encourage early learning and exploration
- [x] End on hopeful, motivating note

**Acceptance**:
- At least 2 career paths mentioned
- Encouraging tone for teenage readers
- Natural conclusion to index page

### Task 1.6: Validate index.md
- [x] Verify word count is 990–1210 words
- [x] Check readability (Flesch-Kincaid Grade 8–10)
- [x] Confirm all 5 lesson previews present
- [x] Test MDX renders correctly in Docusaurus

**Acceptance**:
- Word count within ±10% of 1100
- No broken MDX syntax
- Renders properly in local dev server

---

## US2: Lesson 1 — Why Humanoid Robots Matter (P1)

**Contract**: [lesson-1-contract.md](./contracts/lesson-1-contract.md)  
**Target**: `book-source/docs/chapter3/lesson-1.md`  
**Word Count**: ~1300 words (1170–1430 acceptable)  
**Sources**: Fundación Bankinter, AA News

### Task 2.1: Create lesson-1.md file structure
- [x] Create file `book-source/docs/chapter3/lesson-1.md`
- [x] Add Docusaurus front matter
- [x] Add lesson title as H1: "Why Humanoid Robots Matter Today & Tomorrow"

**Acceptance**:
- File exists at correct path
- Front matter is valid
- Title matches data-model.md specification

### Task 2.2: Write H2.1 — What Makes Humanoid Robots Special
- [x] Write H2 heading: "What Makes Humanoid Robots Special"
- [x] Write H3.1: "The Human-Like Shape" (~130 words)
- [x] Write H3.2: "Sensors and Balance" (~130 words)
- [x] Write H3.3: "AI Thinking and Learning" (~130 words)

**Acceptance**:
- Each H3 subsection ~130 words
- Content explains humanoid robot characteristics simply
- Uses analogies (e.g., sensors like human senses)

### Task 2.3: Add Expert Insight #1
- [x] Add `:::info Expert Insight: Why the Human-Like Form Helps Adaptation`
- [x] Write 4-5 lines of content
- [x] Place after H2.1 section

**Acceptance**:
- Uses correct Docusaurus admonition syntax
- Content is 4-5 lines
- Provides professional perspective in simple language

### Task 2.4: Write H2.2 — Why Humanoid Robots Are Rising Now
- [x] Write H2 heading: "Why Humanoid Robots Are Rising Now"
- [x] Write H3.1: "Better Motors and Cheaper Parts" (~130 words)
- [x] Write H3.2: "Powerful AI Breakthroughs" (~130 words)
- [x] Write H3.3: "Growing Industry Interest" (~130 words)

**Acceptance**:
- Incorporates Fundación Bankinter insights (5 trends)
- References price trajectory from AA News ($175K → $50K)
- Explains why 2025 is a turning point

### Task 2.5: Add Expert Insight #2
- [x] Add `:::info Expert Insight: Recent Breakthroughs Changing Everything`
- [x] Write 4-5 lines of content
- [x] Place after H2.2 section

**Acceptance**:
- Uses correct admonition syntax
- References concrete breakthroughs
- Maintains O-Level appropriate language

### Task 2.6: Write H2.3 — Where Humanoid Robots Are Heading
- [x] Write H2 heading: "Where Humanoid Robots Are Heading"
- [x] Write H3.1: "From Labs to Real Life" (~130 words)
- [x] Write H3.2: "Companies Leading the Way" (~130 words)
- [x] Write H3.3: "What the Future Holds" (~130 words)

**Acceptance**:
- Mentions real companies (Tesla, Figure AI, Neura Robotics)
- Projects from research: ~1 billion robots by 2050
- Ends on forward-looking, optimistic note

### Task 2.7: Validate lesson-1.md
- [x] Verify word count is 1170–1430 words
- [x] Confirm exactly 3 H2 headings
- [x] Confirm exactly 9 H3 subheadings
- [x] Confirm exactly 2 Expert Insight blocks
- [x] Test MDX renders correctly

**Acceptance**:
- Structure matches data-model.md template
- Word count within tolerance
- No broken MDX

---

## US3: Lesson 2 — Automation & Flexibility (P1)

**Contract**: [lesson-2-contract.md](./contracts/lesson-2-contract.md)  
**Target**: `book-source/docs/chapter3/lesson-2.md`  
**Word Count**: ~1300 words (1170–1430 acceptable)  
**Sources**: GlobeNewswire, WEForum

### Task 3.1: Create lesson-2.md file structure
- [x] Create file `book-source/docs/chapter3/lesson-2.md`
- [x] Add Docusaurus front matter
- [x] Add lesson title as H1: "Automation & Flexibility: How AI-Driven Humanoid Robots Change Work"

**Acceptance**:
- File exists at correct path
- Front matter is valid
- Title matches specification

### Task 3.2: Write H2.1 — From Fixed Machines to Flexible Helpers
- [x] Write H2 heading: "From Fixed Machines to Flexible Helpers"
- [x] Write H3.1: "How Old Robots Worked" (~130 words)
- [x] Write H3.2: "Why Flexibility Matters Now" (~130 words)
- [x] Write H3.3: "AI Makes the Difference" (~130 words)

**Acceptance**:
- Contrasts traditional caged robots with modern flexible robots
- Explains automation-to-autonomy shift (GlobeNewswire)
- Simple explanations with examples

### Task 3.3: Write H2.2 — Robots Working Alongside Humans
- [x] Write H2 heading: "Robots Working Alongside Humans"
- [x] Write H3.1: "Cobots: Collaborative Robots" (~130 words)
- [x] Write H3.2: "Safe Human-Robot Teams" (~130 words)
- [x] Write H3.3: "Real Factory Examples" (~130 words)

**Acceptance**:
- Explains cobots concept from Fundación Bankinter
- Includes BMW/Mercedes-Benz examples (GlobeNewswire)
- Addresses safety in human-robot collaboration

### Task 3.4: Add Expert Insight #1
- [x] Add `:::info Expert Insight: Robots Working Beside Humans`
- [x] Write 4-5 lines of content
- [x] Place after H2.2 section

**Acceptance**:
- Correct admonition syntax
- Reflects collaborative robotics perspective
- 4-5 lines

### Task 3.5: Write H2.3 — Learning and Adapting on the Job
- [x] Write H2 heading: "Learning and Adapting on the Job"
- [x] Write H3.1: "How Robots Learn Tasks" (~130 words)
- [x] Write H3.2: "Switching Between Jobs" (~130 words)
- [x] Write H3.3: "The Smart Factory of Tomorrow" (~130 words)

**Acceptance**:
- Explains AI learning, digital twins
- References Amazon example (750K robots, 9 categories)
- Forward-looking conclusion

### Task 3.6: Add Expert Insight #2
- [x] Add `:::info Expert Insight: Why AI Gives Robots Flexibility`
- [x] Write 4-5 lines of content
- [x] Place after H2.3 section

**Acceptance**:
- Correct admonition syntax
- Ties AI capabilities to flexibility
- O-Level appropriate language

### Task 3.7: Validate lesson-2.md
- [x] Verify word count is 1170–1430 words
- [x] Confirm structure: 3 H2, 9 H3, 2 Expert Insights
- [x] Test MDX renders correctly

**Acceptance**:
- All structural requirements met
- Word count within tolerance
- No broken syntax

---

## US4: Lesson 3 — Service & Care (P2)

**Contract**: [lesson-3-contract.md](./contracts/lesson-3-contract.md)  
**Target**: `book-source/docs/chapter3/lesson-3.md`  
**Word Count**: ~1300 words (1170–1430 acceptable)  
**Sources**: Fundación Bankinter, AA News

### Task 4.1: Create lesson-3.md file structure
- [x] Create file `book-source/docs/chapter3/lesson-3.md`
- [x] Add Docusaurus front matter
- [x] Add lesson title as H1: "Service & Care: Robots in Homes, Hospitals, and Everyday Life"

**Acceptance**:
- File exists at correct path
- Front matter is valid
- Title matches specification

### Task 4.2: Write H2.1 — Robots in Healthcare
- [x] Write H2 heading: "Robots in Healthcare"
- [x] Write H3.1: "Helping Doctors and Nurses" (~130 words)
- [x] Write H3.2: "Caring for Elderly Patients" (~130 words)
- [x] Write H3.3: "Medication and Monitoring" (~130 words)

**Acceptance**:
- Covers surgical assistance, patient monitoring
- References +38% healthcare growth statistic
- Addresses aging population context

### Task 4.3: Add Expert Insight #1
- [x] Add `:::info Expert Insight: Robots Helping Elderly Safely`
- [x] Write 4-5 lines of content
- [x] Place after H2.1 section

**Acceptance**:
- Reflects Realbotix/AA News insights on elderly care
- Andrew Kiguel quote context (loneliness epidemic)
- 4-5 lines

### Task 4.4: Write H2.2 — Robots in Our Homes
- [x] Write H2 heading: "Robots in Our Homes"
- [x] Write H3.1: "Household Chores and Tasks" (~130 words)
- [x] Write H3.2: "Companionship and Communication" (~130 words)
- [x] Write H3.3: "Safety and Emergency Help" (~130 words)

**Acceptance**:
- Covers garbage handling, dishwashers, daily tasks
- Addresses companionship (Aria robot, emotional connection)
- Emergency alert capabilities

### Task 4.5: Add Expert Insight #2
- [x] Add `:::info Expert Insight: Daily-Life Tasks Robots Can Learn`
- [x] Write 4-5 lines of content
- [x] Place after H2.2 section

**Acceptance**:
- Practical focus on learnable tasks
- Simple language
- 4-5 lines

### Task 4.6: Write H2.3 — Robots in Public Spaces
- [x] Write H2 heading: "Robots in Public Spaces"
- [x] Write H3.1: "Shops and Customer Service" (~130 words)
- [x] Write H3.2: "Hotels and Reception" (~130 words)
- [x] Write H3.3: "Museums and Information" (~130 words)

**Acceptance**:
- Covers retail inventory, customer assistance
- Hotel reception applications
- Information services in public venues

### Task 4.7: Validate lesson-3.md
- [x] Verify word count is 1170–1430 words
- [x] Confirm structure: 3 H2, 9 H3, 2 Expert Insights
- [x] Test MDX renders correctly

**Acceptance**:
- All structural requirements met
- Word count within tolerance
- No broken syntax

---

## US5: Lesson 4 — Challenges & Ethics (P2)

**Contract**: [lesson-4-contract.md](./contracts/lesson-4-contract.md)  
**Target**: `book-source/docs/chapter3/lesson-4.md`  
**Word Count**: ~1300 words (1170–1430 acceptable)  
**Sources**: WEForum, AA News

### Task 5.1: Create lesson-4.md file structure
- [x] Create file `book-source/docs/chapter3/lesson-4.md`
- [x] Add Docusaurus front matter
- [x] Add lesson title as H1: "Challenges & Ethics: What We Must Think About When Robots Join Society"

**Acceptance**:
- File exists at correct path
- Front matter is valid
- Title matches specification

### Task 5.2: Write H2.1 — Jobs and Work in a Robot World
- [x] Write H2 heading: "Jobs and Work in a Robot World"
- [x] Write H3.1: "Will Robots Take Our Jobs?" (~130 words)
- [x] Write H3.2: "New Jobs Robots Create" (~130 words)
- [x] Write H3.3: "Working Together, Not Replacing" (~130 words)

**Acceptance**:
- Balanced perspective on job displacement
- Highlights new roles (training, monitoring, collaborating)
- References WEForum "disruption and promise" framing

### Task 5.3: Write H2.2 — Privacy, Safety, and Trust
- [x] Write H2 heading: "Privacy, Safety, and Trust"
- [x] Write H3.1: "Who Controls Robot Data?" (~130 words)
- [x] Write H3.2: "What If Robots Make Mistakes?" (~130 words)
- [x] Write H3.3: "Building Trust with Technology" (~130 words)

**Acceptance**:
- Addresses data privacy concerns
- Accountability question (elderly care malfunction scenario)
- Trust-building approaches

### Task 5.4: Add Expert Insight #1
- [x] Add `:::info Expert Insight: Balancing Progress and Safety`
- [x] Write 4-5 lines of content
- [x] Place after H2.2 section

**Acceptance**:
- Multi-tiered guardrails concept (engineers, corporations, governments)
- 4-5 lines
- Balanced tone

### Task 5.5: Write H2.3 — Rules and Responsibility
- [x] Write H2 heading: "Rules and Responsibility"
- [x] Write H3.1: "Why We Need Robot Rules" (~130 words)
- [x] Write H3.2: "Who Is Responsible?" (~130 words)
- [x] Write H3.3: "Making Fair Decisions" (~130 words)

**Acceptance**:
- Legal framework needs explained simply
- Responsibility chain (makers, users, regulators)
- Fairness in AI decisions

### Task 5.6: Add Expert Insight #2
- [x] Add `:::info Expert Insight: Why Ethics Matter in Robotics`
- [x] Write 4-5 lines of content
- [x] Place after H2.3 section

**Acceptance**:
- David Reger quote context ("no bad robots, but...")
- Importance of ethical design
- 4-5 lines

### Task 5.7: Validate lesson-4.md
- [x] Verify word count is 1170–1430 words
- [x] Confirm structure: 3 H2, 9 H3, 2 Expert Insights
- [x] Test MDX renders correctly

**Acceptance**:
- All structural requirements met
- Word count within tolerance
- No broken syntax

---

## US6: Lesson 5 — Future Skills (P2)

**Contract**: [lesson-5-contract.md](./contracts/lesson-5-contract.md)  
**Target**: `book-source/docs/chapter3/lesson-5.md`  
**Word Count**: ~1300 words (1170–1430 acceptable)  
**Sources**: Fundación Bankinter, GlobeNewswire

### Task 6.1: Create lesson-5.md file structure
- [x] Create file `book-source/docs/chapter3/lesson-5.md`
- [x] Add Docusaurus front matter
- [x] Add lesson title as H1: "Future Skills: How You Can Be Ready for a Robot-AI Future"

**Acceptance**:
- File exists at correct path
- Front matter is valid
- Title matches specification

### Task 6.2: Write H2.1 — Skills That Matter Most
- [x] Write H2 heading: "Skills That Matter Most"
- [x] Write H3.1: "Creativity and Problem-Solving" (~130 words)
- [x] Write H3.2: "Logical Thinking and Math Basics" (~130 words)
- [x] Write H3.3: "Teamwork and Communication" (~130 words)

**Acceptance**:
- Covers human skills that complement robots
- Explains why these skills matter in robot era
- Encouraging, accessible tone

### Task 6.3: Add Expert Insight #1
- [x] Add `:::info Expert Insight: Skills Employers Need in the Robot Era`
- [x] Write 4-5 lines of content
- [x] Place after H2.1 section

**Acceptance**:
- References workforce trends (GlobeNewswire)
- Skills gaps context
- 4-5 lines

### Task 6.4: Write H2.2 — Getting Started with Technology
- [x] Write H2 heading: "Getting Started with Technology"
- [x] Write H3.1: "Basic Programming Ideas" (~130 words)
- [x] Write H3.2: "Understanding How AI Works" (~130 words)
- [x] Write H3.3: "Hands-On Robotics Projects" (~130 words)

**Acceptance**:
- Practical entry points for learning
- Simple explanations of programming/AI
- Suggests beginner-friendly activities

### Task 6.5: Write H2.3 — Your Path Forward
- [x] Write H2 heading: "Your Path Forward"
- [x] Write H3.1: "School Subjects That Help" (~130 words)
- [x] Write H3.2: "Activities and Clubs to Join" (~130 words)
- [x] Write H3.3: "Careers in Robotics and AI" (~130 words)

**Acceptance**:
- Concrete school subjects (math, science, computing)
- Extracurricular suggestions
- Career paths overview

### Task 6.6: Add Expert Insight #2
- [x] Add `:::info Expert Insight: Learning Path for Teens`
- [x] Write 4-5 lines of content
- [x] Place after H2.3 section

**Acceptance**:
- Actionable advice for O-Level students
- Encouraging tone
- 4-5 lines

### Task 6.7: Validate lesson-5.md
- [x] Verify word count is 1170–1430 words
- [x] Confirm structure: 3 H2, 9 H3, 2 Expert Insights
- [x] Test MDX renders correctly

**Acceptance**:
- All structural requirements met
- Word count within tolerance
- No broken syntax

---

## Final Validation Tasks

### Task 7.1: Full chapter validation
- [x] Run word count check on all 6 files
- [x] Verify all files render in Docusaurus
- [x] Check cross-references between lessons work
- [x] Validate sidebar navigation correct

**Acceptance**:
- All files pass word count checks
- No rendering errors
- Navigation works as expected

### Task 7.2: Content quality review
- [x] Review for consistent tone across all files
- [x] Check readability (Flesch-Kincaid Grade 8–10)
- [x] Verify research insights integrated (not just cited)
- [x] Confirm no broken links or references

**Acceptance**:
- Consistent O-Level appropriate language
- Research naturally woven into content
- No technical errors

---

## Task Summary

| User Story | Priority | Tasks | Output File |
|------------|----------|-------|-------------|
| US1: Index Page | P1 | 1.1–1.6 | `docs/chapter3/index.md` |
| US2: Lesson 1 | P1 | 2.1–2.7 | `docs/chapter3/lesson-1.md` |
| US3: Lesson 2 | P1 | 3.1–3.7 | `docs/chapter3/lesson-2.md` |
| US4: Lesson 3 | P2 | 4.1–4.7 | `docs/chapter3/lesson-3.md` |
| US5: Lesson 4 | P2 | 5.1–5.7 | `docs/chapter3/lesson-4.md` |
| US6: Lesson 5 | P2 | 6.1–6.7 | `docs/chapter3/lesson-5.md` |
| Validation | — | 7.1–7.2 | All files |

**Total Tasks**: 44 checklist items across 7 user stories

---

## Implementation Order

**Phase 1 (P1 — Core)**:
1. US1: Index page (sets context for entire chapter)
2. US2: Lesson 1 (foundational understanding)
3. US3: Lesson 2 (practical applications)

**Phase 2 (P2 — Extended)**:
4. US4: Lesson 3 (daily life applications)
5. US5: Lesson 4 (critical thinking about challenges)
6. US6: Lesson 5 (actionable future skills)

**Phase 3 (Validation)**:
7. Final validation across all content

