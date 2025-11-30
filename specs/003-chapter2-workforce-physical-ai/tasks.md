# Tasks: Chapter 2 — Humans, Agents & Robots: The Emerging Workforce of Physical AI

**Input**: Design documents from `/specs/003-chapter2-workforce-physical-ai/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Not requested - this is a content generation feature, not code. Validation is done via structural and word count checks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. User Stories 1-5 correspond to Lessons 1-5, and User Story 6 is the index.md.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Content files**: `book-source/docs/chapter-02/`
- **Spec files**: `specs/003-chapter2-workforce-physical-ai/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create chapter directory structure and category configuration

- [x] T001 Create chapter directory at book-source/docs/chapter-02/
- [x] T002 Create _category_.json with label "Chapter 2: Humans, Agents & Robots" and position 2 in book-source/docs/chapter-02/_category_.json

---

## Phase 2: Foundational (Research & Reference Materials)

**Purpose**: Fetch and analyze research sources to ground all content

**⚠️ CRITICAL**: Content quality depends on understanding these sources first

- [x] T003 [P] Fetch McKinsey research and extract key insights for Lesson 1 (used alternative URL with partnership content)
- [x] T004 [P] Fetch WEF "Future of Jobs Report 2025" and extract key insights for Lesson 2 (updated source)
- [x] T005 [P] Fetch Brookings "Automation and AI" and extract key insights for Lesson 3
- [x] T006 [P] Fetch OECD AI policy research and extract key insights for Lesson 4 (alternative source)
- [x] T007 [P] Research compilation for Lesson 5 (synthesis of all sources)
- [x] T008 Review Chapter 1 lesson-01.md structure as template reference in book-source/docs/chapter-01/lesson-01.md

**Checkpoint**: Research complete - content generation can now begin

---

## Phase 3: User Story 6 - Chapter Index Overview (Priority: P2) 🎯 MVP

**Goal**: Create ~800-word chapter overview that explains human-AI-robot collaboration and previews all 5 lessons

**Independent Test**: Reader can open index.md, understand the chapter scope, and see 1-2 paragraph previews for each lesson

### Implementation for User Story 6

- [x] T009 [US6] Create MDX frontmatter with sidebar_position: 0, title, description, keywords in book-source/docs/chapter-02/index.md
- [x] T010 [US6] Write Chapter Introduction section (~150 words) explaining human-AI-robot collaboration in book-source/docs/chapter-02/index.md
- [x] T011 [US6] Write "Why This Chapter Matters" section (~100 words) positioning chapter as course building block in book-source/docs/chapter-02/index.md
- [x] T012 [US6] Write Lesson 1 preview (~90 words) on partnership paradigm in book-source/docs/chapter-02/index.md
- [x] T013 [US6] Write Lesson 2 preview (~90 words) on skills transformation in book-source/docs/chapter-02/index.md
- [x] T014 [US6] Write Lesson 3 preview (~90 words) on hybrid roles in book-source/docs/chapter-02/index.md
- [x] T015 [US6] Write Lesson 4 preview (~90 words) on societal impact in book-source/docs/chapter-02/index.md
- [x] T016 [US6] Write Lesson 5 preview (~90 words) on workforce 2030 preparation in book-source/docs/chapter-02/index.md
- [x] T017 [US6] Write concluding perspective section (~100 words) on workforce transformation in book-source/docs/chapter-02/index.md
- [x] T018 [US6] Validate index.md word count is 800±50 words in book-source/docs/chapter-02/index.md

**Checkpoint**: Index complete - readers can now navigate to chapter overview

---

## Phase 4: User Story 1 - The New Partnership Paradigm (Priority: P1)

**Goal**: Create ~1200-word Lesson 1 explaining human-AI-robot collaboration with real-world examples

**Independent Test**: Reader can open Lesson 1, find 3 H2 headings with 3 H3 subheadings each, 2 expert insights, and understand augmentation vs. replacement

### Implementation for User Story 1

- [x] T019 [US1] Create MDX frontmatter with sidebar_position: 1, title "The New Partnership Paradigm", keywords, slug in book-source/docs/chapter-02/lesson-01.md
- [x] T020 [US1] Import SummaryButton and PersonalizeButton components in book-source/docs/chapter-02/lesson-01.md
- [x] T021 [US1] Write H2 "The Shift from Human-Only Labor" with 3 H3 subheadings (~350 words) in book-source/docs/chapter-02/lesson-01.md
- [x] T022 [US1] Write H3 "Historical Context of Work and Automation" in book-source/docs/chapter-02/lesson-01.md
- [x] T023 [US1] Write H3 "The Emergence of Collaborative Ecosystems" in book-source/docs/chapter-02/lesson-01.md
- [x] T024 [US1] Write H3 "Augmentation vs. Replacement Philosophy" in book-source/docs/chapter-02/lesson-01.md
- [x] T025 [US1] Write Expert Insight #1 (4-5 lines) on collaborative workforce dynamics in book-source/docs/chapter-02/lesson-01.md
- [x] T026 [US1] Write H2 "Real-World Partnership Examples" with 3 H3 subheadings (~350 words) in book-source/docs/chapter-02/lesson-01.md
- [x] T027 [US1] Write H3 "Logistics and Warehouse Automation" in book-source/docs/chapter-02/lesson-01.md
- [x] T028 [US1] Write H3 "Healthcare Robotics and Patient Care" in book-source/docs/chapter-02/lesson-01.md
- [x] T029 [US1] Write H3 "Home AI Companions and Assistance" in book-source/docs/chapter-02/lesson-01.md
- [x] T030 [US1] Write H2 "Industrial Embodied Systems" with 3 H3 subheadings (~350 words) in book-source/docs/chapter-02/lesson-01.md
- [x] T031 [US1] Write H3 "Manufacturing Cobots and Human Workers" in book-source/docs/chapter-02/lesson-01.md
- [x] T032 [US1] Write H3 "Construction and Heavy Industry Applications" in book-source/docs/chapter-02/lesson-01.md
- [x] T033 [US1] Write H3 "The Future of Human-Robot Teams" in book-source/docs/chapter-02/lesson-01.md
- [x] T034 [US1] Write Expert Insight #2 (4-5 lines) on Physical AI partnership value in book-source/docs/chapter-02/lesson-01.md
- [x] T035 [US1] Write Key Takeaways section (4-6 bullet points) in book-source/docs/chapter-02/lesson-01.md
- [x] T036 [US1] Write transition statement to Lesson 2 in book-source/docs/chapter-02/lesson-01.md
- [x] T037 [US1] Validate lesson-01.md word count is 1200±100 words and has correct structure in book-source/docs/chapter-02/lesson-01.md

**Checkpoint**: Lesson 1 complete and independently readable

---

## Phase 5: User Story 2 - Skills Under Transformation (Priority: P1)

**Goal**: Create ~1200-word Lesson 2 explaining essential human capabilities that remain irreplaceable

**Independent Test**: Reader can identify 5+ human capabilities that Physical AI enhances rather than replaces

### Implementation for User Story 2

- [x] T038 [US2] Create MDX frontmatter with sidebar_position: 2, title "Skills Under Transformation", keywords, slug in book-source/docs/chapter-02/lesson-02.md
- [x] T039 [US2] Import SummaryButton and PersonalizeButton components in book-source/docs/chapter-02/lesson-02.md
- [x] T040 [US2] Write H2 "Essential Human Capabilities" with 3 H3 subheadings (~350 words) in book-source/docs/chapter-02/lesson-02.md
- [x] T041 [US2] Write H3 "Contextual Judgment and Intuition" in book-source/docs/chapter-02/lesson-02.md
- [x] T042 [US2] Write H3 "Creative Problem-Solving" in book-source/docs/chapter-02/lesson-02.md
- [x] T043 [US2] Write H3 "Empathy and Emotional Intelligence" in book-source/docs/chapter-02/lesson-02.md
- [x] T044 [US2] Write Expert Insight #1 (4-5 lines) on enduring human capabilities in book-source/docs/chapter-02/lesson-02.md
- [x] T045 [US2] Write H2 "Skill Categories in Transition" with 3 H3 subheadings (~350 words) in book-source/docs/chapter-02/lesson-02.md
- [x] T046 [US2] Write H3 "Rising Skills in Physical AI Environments" in book-source/docs/chapter-02/lesson-02.md
- [x] T047 [US2] Write H3 "Declining Routine Task Skills" in book-source/docs/chapter-02/lesson-02.md
- [x] T048 [US2] Write H3 "McKinsey's Skill Shift Predictions" in book-source/docs/chapter-02/lesson-02.md
- [x] T049 [US2] Write H2 "Human Intelligence Enhancement" with 3 H3 subheadings (~350 words) in book-source/docs/chapter-02/lesson-02.md
- [x] T050 [US2] Write H3 "Ethical Oversight and Moral Reasoning" in book-source/docs/chapter-02/lesson-02.md
- [x] T051 [US2] Write H3 "Adaptability and Continuous Learning" in book-source/docs/chapter-02/lesson-02.md
- [x] T052 [US2] Write H3 "Why AI Amplifies Human Value" in book-source/docs/chapter-02/lesson-02.md
- [x] T053 [US2] Write Expert Insight #2 (4-5 lines) on skill evolution in robotics environments in book-source/docs/chapter-02/lesson-02.md
- [x] T054 [US2] Write Key Takeaways section (4-6 bullet points) in book-source/docs/chapter-02/lesson-02.md
- [x] T055 [US2] Write transition statement to Lesson 3 in book-source/docs/chapter-02/lesson-02.md
- [x] T056 [US2] Validate lesson-02.md word count is 1200±100 words and has correct structure in book-source/docs/chapter-02/lesson-02.md

**Checkpoint**: Lesson 2 complete and independently readable

---

## Phase 6: User Story 3 - Hybrid Roles (Priority: P1)

**Goal**: Create ~1200-word Lesson 3 defining new hybrid job roles and task-sharing frameworks

**Independent Test**: Reader can describe 4+ hybrid job roles and explain the task-sharing framework

### Implementation for User Story 3

- [x] T057 [US3] Create MDX frontmatter with sidebar_position: 3, title "Hybrid Roles", keywords, slug in book-source/docs/chapter-02/lesson-03.md
- [x] T058 [US3] Import SummaryButton and PersonalizeButton components in book-source/docs/chapter-02/lesson-03.md
- [x] T059 [US3] Write H2 "Emerging Hybrid Job Categories" with 3 H3 subheadings (~350 words) in book-source/docs/chapter-02/lesson-03.md
- [x] T060 [US3] Write H3 "Robot Supervisors and Fleet Managers" in book-source/docs/chapter-02/lesson-03.md
- [x] T061 [US3] Write H3 "AI Workflow Designers and Orchestrators" in book-source/docs/chapter-02/lesson-03.md
- [x] T062 [US3] Write H3 "Safety Operators and Compliance Officers" in book-source/docs/chapter-02/lesson-03.md
- [x] T063 [US3] Write Expert Insight #1 (4-5 lines) on emerging job roles in book-source/docs/chapter-02/lesson-03.md
- [x] T064 [US3] Write H2 "Task-Sharing Frameworks" with 3 H3 subheadings (~350 words) in book-source/docs/chapter-02/lesson-03.md
- [x] T065 [US3] Write H3 "What Robots Do Best: Precision and Endurance" in book-source/docs/chapter-02/lesson-03.md
- [x] T066 [US3] Write H3 "What AI Agents Automate: Data and Decisions" in book-source/docs/chapter-02/lesson-03.md
- [x] T067 [US3] Write H3 "What Humans Must Manage: Context and Exceptions" in book-source/docs/chapter-02/lesson-03.md
- [x] T068 [US3] Write H2 "Career Positioning in the New Workforce" with 3 H3 subheadings (~350 words) in book-source/docs/chapter-02/lesson-03.md
- [x] T069 [US3] Write H3 "Household Robotics Coordinators" in book-source/docs/chapter-02/lesson-03.md
- [x] T070 [US3] Write H3 "Human-Robot Interaction Specialists" in book-source/docs/chapter-02/lesson-03.md
- [x] T071 [US3] Write H3 "Pathways to Hybrid Role Careers" in book-source/docs/chapter-02/lesson-03.md
- [x] T072 [US3] Write Expert Insight #2 (4-5 lines) on task division in book-source/docs/chapter-02/lesson-03.md
- [x] T073 [US3] Write Key Takeaways section (4-6 bullet points) in book-source/docs/chapter-02/lesson-03.md
- [x] T074 [US3] Write transition statement to Lesson 4 in book-source/docs/chapter-02/lesson-03.md
- [x] T075 [US3] Validate lesson-03.md word count is 1200±100 words and has correct structure in book-source/docs/chapter-02/lesson-03.md

**Checkpoint**: Lesson 3 complete and independently readable

---

## Phase 7: User Story 4 - Societal Impact & Economic Shifts (Priority: P1)

**Goal**: Create ~1200-word Lesson 4 analyzing global effects of robotics-enabled work

**Independent Test**: Reader can discuss 5+ societal/economic impacts and key governance considerations

### Implementation for User Story 4

- [x] T076 [US4] Create MDX frontmatter with sidebar_position: 4, title "Societal Impact & Economic Shifts", keywords, slug in book-source/docs/chapter-02/lesson-04.md
- [x] T077 [US4] Import SummaryButton and PersonalizeButton components in book-source/docs/chapter-02/lesson-04.md
- [x] T078 [US4] Write H2 "Economic Transformation" with 3 H3 subheadings (~350 words) in book-source/docs/chapter-02/lesson-04.md
- [x] T079 [US4] Write H3 "Productivity Acceleration and GDP Growth" in book-source/docs/chapter-02/lesson-04.md
- [x] T080 [US4] Write H3 "Regional Job Displacement Patterns" in book-source/docs/chapter-02/lesson-04.md
- [x] T081 [US4] Write H3 "New Job Creation and Industry Emergence" in book-source/docs/chapter-02/lesson-04.md
- [x] T082 [US4] Write Expert Insight #1 (4-5 lines) on economic implications in book-source/docs/chapter-02/lesson-04.md
- [x] T083 [US4] Write H2 "Infrastructure and Resource Demands" with 3 H3 subheadings (~350 words) in book-source/docs/chapter-02/lesson-04.md
- [x] T084 [US4] Write H3 "Compute and Energy Requirements" in book-source/docs/chapter-02/lesson-04.md
- [x] T085 [US4] Write H3 "Robotics Deployment and Supply Chains" in book-source/docs/chapter-02/lesson-04.md
- [x] T086 [US4] Write H3 "Inequality Challenges and Digital Divides" in book-source/docs/chapter-02/lesson-04.md
- [x] T087 [US4] Write H2 "Governance and Coexistence" with 3 H3 subheadings (~350 words) in book-source/docs/chapter-02/lesson-04.md
- [x] T088 [US4] Write H3 "Regulatory Frameworks and Safety Standards" in book-source/docs/chapter-02/lesson-04.md
- [x] T089 [US4] Write H3 "Ethical Constraints on Automation" in book-source/docs/chapter-02/lesson-04.md
- [x] T090 [US4] Write H3 "Human-Robot Workplace Coexistence" in book-source/docs/chapter-02/lesson-04.md
- [x] T091 [US4] Write Expert Insight #2 (4-5 lines) on governance needs in book-source/docs/chapter-02/lesson-04.md
- [x] T092 [US4] Write Key Takeaways section (4-6 bullet points) in book-source/docs/chapter-02/lesson-04.md
- [x] T093 [US4] Write transition statement to Lesson 5 in book-source/docs/chapter-02/lesson-04.md
- [x] T094 [US4] Validate lesson-04.md word count is 1200±100 words and has correct structure in book-source/docs/chapter-02/lesson-04.md

**Checkpoint**: Lesson 4 complete and independently readable

---

## Phase 8: User Story 5 - Preparing for the Workforce of 2030 (Priority: P1)

**Goal**: Create ~1200-word Lesson 5 providing actionable career preparation guidance

**Independent Test**: Reader can identify 5+ skills to develop and understand education system evolution

### Implementation for User Story 5

- [x] T095 [US5] Create MDX frontmatter with sidebar_position: 5, title "Preparing for the Workforce of 2030", keywords, slug in book-source/docs/chapter-02/lesson-05.md
- [x] T096 [US5] Import SummaryButton and PersonalizeButton components in book-source/docs/chapter-02/lesson-05.md
- [x] T097 [US5] Write H2 "Education System Evolution" with 3 H3 subheadings (~350 words) in book-source/docs/chapter-02/lesson-05.md
- [x] T098 [US5] Write H3 "Robotics Literacy as Core Curriculum" in book-source/docs/chapter-02/lesson-05.md
- [x] T099 [US5] Write H3 "AI-Agent Fluency and Digital Skills" in book-source/docs/chapter-02/lesson-05.md
- [x] T100 [US5] Write H3 "Hands-On Embodied Robotics Experience" in book-source/docs/chapter-02/lesson-05.md
- [x] T101 [US5] Write Expert Insight #1 (4-5 lines) on education evolution in book-source/docs/chapter-02/lesson-05.md
- [x] T102 [US5] Write H2 "Ethical Frameworks and Safety Design" with 3 H3 subheadings (~350 words) in book-source/docs/chapter-02/lesson-05.md
- [x] T103 [US5] Write H3 "Responsible AI Development Principles" in book-source/docs/chapter-02/lesson-05.md
- [x] T104 [US5] Write H3 "Safety-First Design Methodologies" in book-source/docs/chapter-02/lesson-05.md
- [x] T105 [US5] Write H3 "Human-Centered Automation Ethics" in book-source/docs/chapter-02/lesson-05.md
- [x] T106 [US5] Write H2 "Student Career Preparation" with 3 H3 subheadings (~350 words) in book-source/docs/chapter-02/lesson-05.md
- [x] T107 [US5] Write H3 "Skills Portfolio for Physical AI Careers" in book-source/docs/chapter-02/lesson-05.md
- [x] T108 [US5] Write H3 "Internships and Industry Exposure" in book-source/docs/chapter-02/lesson-05.md
- [x] T109 [US5] Write H3 "Lifelong Learning and Adaptability Mindset" in book-source/docs/chapter-02/lesson-05.md
- [x] T110 [US5] Write Expert Insight #2 (4-5 lines) on career readiness in book-source/docs/chapter-02/lesson-05.md
- [x] T111 [US5] Write Key Takeaways section (4-6 bullet points) in book-source/docs/chapter-02/lesson-05.md
- [x] T112 [US5] Write chapter conclusion and call-to-action for next chapter in book-source/docs/chapter-02/lesson-05.md
- [x] T113 [US5] Validate lesson-05.md word count is 1200±100 words and has correct structure in book-source/docs/chapter-02/lesson-05.md

**Checkpoint**: Lesson 5 complete and independently readable

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and quality assurance

- [x] T114 [P] Run Docusaurus build to verify all MDX files render without errors
- [x] T115 [P] Verify sidebar navigation shows Chapter 2 with all 5 lessons
- [x] T116 [P] Verify breadcrumb navigation works (Home → Chapter 2 → Lesson X)
- [x] T117 [P] Verify Table of Contents renders correctly for each lesson
- [x] T118 [P] Test SummaryButton and PersonalizeButton components in all lessons
- [x] T119 Review all expert insights for applied, realistic Physical AI content
- [x] T120 Verify narrative flow and transitions between all lessons
- [x] T121 Final word count verification for all 6 files

**✅ Phase 9 Complete - All validation passed**

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - research must complete before content
- **User Stories (Phases 3-8)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (different lesson files)
  - Or sequentially by priority
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 6 (P2 - Index)**: Can start after Foundational - provides chapter overview
- **User Story 1 (P1 - Lesson 1)**: Can start after Foundational - no dependencies on other lessons
- **User Story 2 (P1 - Lesson 2)**: Can start after Foundational - references Lesson 1 concepts but independently testable
- **User Story 3 (P1 - Lesson 3)**: Can start after Foundational - builds on previous lessons conceptually
- **User Story 4 (P1 - Lesson 4)**: Can start after Foundational - independently testable
- **User Story 5 (P1 - Lesson 5)**: Can start after Foundational - conclusion requires awareness of all content

### Within Each User Story

- Frontmatter and imports before content
- H2 sections can be written in parallel within same file (but recommend sequential for narrative flow)
- Expert insights after main content of their section
- Key takeaways and transitions last
- Validation as final task

### Parallel Opportunities

- All Setup tasks (T001-T002) can run sequentially (same directory)
- All Foundational research tasks (T003-T007) can run in parallel (different sources)
- All User Story phases (3-8) can run in parallel (different .md files)
- All Polish validation tasks (T114-T118) can run in parallel

---

## Parallel Example: Research Phase

```bash
# Launch all research tasks together:
Task T003: "Fetch McKinsey report for Lesson 1"
Task T004: "Fetch WEF article for Lesson 2"
Task T005: "Fetch Brookings research for Lesson 3"
Task T006: "Fetch OECD report for Lesson 4"
Task T007: "Fetch UNESCO materials for Lesson 5"
```

## Parallel Example: Content Generation

```bash
# Once research complete, launch all lessons in parallel:
Task T019-T037: "Generate Lesson 1 (US1)"
Task T038-T056: "Generate Lesson 2 (US2)"
Task T057-T075: "Generate Lesson 3 (US3)"
Task T076-T094: "Generate Lesson 4 (US4)"
Task T095-T113: "Generate Lesson 5 (US5)"
```

---

## Implementation Strategy

### MVP First (Index + Lesson 1)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational Research
3. Complete Phase 3: User Story 6 (Index)
4. Complete Phase 4: User Story 1 (Lesson 1)
5. **STOP and VALIDATE**: Test index and Lesson 1 in Docusaurus
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Research → Foundation ready
2. Add Index → Deploy/Demo (Chapter overview available)
3. Add Lesson 1 → Deploy/Demo (MVP - partnership paradigm)
4. Add Lesson 2 → Deploy/Demo (Skills transformation)
5. Add Lesson 3 → Deploy/Demo (Hybrid roles)
6. Add Lesson 4 → Deploy/Demo (Societal impact)
7. Add Lesson 5 → Deploy/Demo (Workforce 2030)
8. Polish → Final validation

### Parallel Strategy

With research complete:
- Writer A: Index + Lesson 1 + Lesson 2
- Writer B: Lesson 3 + Lesson 4 + Lesson 5

Or with 6 parallel writers:
- Each writer handles one lesson independently
- Sync for transitions and narrative consistency

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total Tasks | 121 |
| Setup Tasks | 2 |
| Foundational Tasks | 6 |
| User Story 6 (Index) Tasks | 10 |
| User Story 1 (Lesson 1) Tasks | 19 |
| User Story 2 (Lesson 2) Tasks | 19 |
| User Story 3 (Lesson 3) Tasks | 19 |
| User Story 4 (Lesson 4) Tasks | 19 |
| User Story 5 (Lesson 5) Tasks | 19 |
| Polish Tasks | 8 |
| Parallel Opportunities | 15+ task groups |

---

## Notes

- [P] tasks = different files/sources, no dependencies
- [Story] label maps task to specific user story for traceability
- Each lesson is independently completable and testable
- Content should be committed after each lesson completion
- Stop at any checkpoint to validate content in Docusaurus
- Avoid: placeholder text, inconsistent terminology, broken component imports
