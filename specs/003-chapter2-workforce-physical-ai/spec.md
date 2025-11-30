# Feature Specification: Chapter 2 — Humans, Agents & Robots: The Emerging Workforce of Physical AI

**Feature Branch**: `003-chapter2-workforce-physical-ai`  
**Created**: 2025-11-28  
**Status**: Draft  
**Input**: User description: "Chapter 2 covering the central role of humans, AI agents, and humanoid robots as a unified collaborative workforce, drawing on McKinsey's 'Agents, Robots, and Us' report insights"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Reader Understands the New Partnership Paradigm (Priority: P1)

A reader completing Chapter 1 wants to understand how humans, AI agents, and robots work together as a collaborative workforce. They navigate to Lesson 1 and find a comprehensive explanation of the partnership paradigm with real-world examples from logistics, healthcare, home environments, and industrial settings.

**Why this priority**: This lesson establishes the foundational concept of human-AI-robot collaboration that underpins the entire chapter and course. Understanding augmentation vs. replacement is critical before exploring specific aspects.

**Independent Test**: Reader can open Lesson 1, read the complete content (~1200 words), understand the partnership paradigm, and identify at least 4 real examples of collaborative human-AI-robot systems.

**Acceptance Scenarios**:

1. **Given** a reader has completed Chapter 1, **When** they navigate to Chapter 2 Lesson 1, **Then** they find a fully-formatted MDX page with 3 main headings, each with 3 subheadings, and 2 expert insight blocks
2. **Given** a reader is learning about collaboration, **When** they read Lesson 1, **Then** they understand why augmentation rather than replacement is the core purpose of Physical AI
3. **Given** a reader wants examples, **When** they scan Lesson 1, **Then** they find concrete examples from logistics automation, healthcare robotics, home AI companions, and industrial embodied systems

---

### User Story 2 - Reader Understands Human Skills That Remain Essential (Priority: P1)

A reader wants to understand which human capabilities remain irreplaceable even in robotics-rich environments. They read Lesson 2 to learn about contextual judgment, problem-solving, empathy, creativity, and ethical oversight, with McKinsey insights on rising and falling skill categories.

**Why this priority**: Understanding the enduring value of human intelligence addresses common fears about automation and provides motivation for personal skill development.

**Independent Test**: Reader can identify at least 5 essential human capabilities that Physical AI enhances rather than replaces, and understand McKinsey's skill category predictions.

**Acceptance Scenarios**:

1. **Given** a reader opens Lesson 2, **When** they read the content, **Then** they find clear explanations of contextual judgment, empathy, creativity, and ethical oversight
2. **Given** a reader wants data-driven insights, **When** they study Lesson 2, **Then** they learn which skill categories McKinsey identifies as rising or falling
3. **Given** a reader completes Lesson 2, **When** they reflect on the content, **Then** they can explain why Physical AI enhances human value rather than diminishing it

---

### User Story 3 - Reader Learns About Hybrid Roles and Task-Sharing (Priority: P1)

A reader wants to understand the new hybrid job roles emerging from embodied intelligence. They read Lesson 3 to learn about robot supervisors, AI workflow designers, safety operators, and household robotics coordinators, plus how task-sharing works between robots, AI agents, and humans.

**Why this priority**: Understanding emerging roles helps readers prepare for career opportunities and understand how human-robot work divisions will evolve.

**Independent Test**: Reader can describe at least 4 new hybrid job roles and explain the task-sharing framework for what robots, AI agents, and humans each do best.

**Acceptance Scenarios**:

1. **Given** a reader opens Lesson 3, **When** they read about hybrid roles, **Then** they find detailed descriptions of at least 4 emerging job categories
2. **Given** a reader wants to understand task division, **When** they read Lesson 3, **Then** they learn what robots do best, what AI agents automate, and what humans must manage
3. **Given** a reader is career-planning, **When** they complete Lesson 3, **Then** they understand how to position themselves in the emerging workforce

---

### User Story 4 - Reader Understands Societal and Economic Impacts (Priority: P1)

A reader wants to understand the global effects of robotics-enabled work. They read Lesson 4 to learn about productivity acceleration, job displacement, job creation, inequality challenges, infrastructure demands, governance, and human-robot coexistence.

**Why this priority**: Understanding societal implications prepares readers to be informed citizens and professionals who can contribute to responsible Physical AI deployment.

**Independent Test**: Reader can discuss at least 5 major societal/economic impacts of Physical AI and identify key governance and ethical considerations.

**Acceptance Scenarios**:

1. **Given** a reader opens Lesson 4, **When** they read about economic shifts, **Then** they understand productivity acceleration, regional job displacement, and new job creation patterns
2. **Given** a reader is concerned about inequality, **When** they read Lesson 4, **Then** they learn about challenges and infrastructure demands (compute, energy, robotics deployment)
3. **Given** a reader completes Lesson 4, **When** they review the content, **Then** they can discuss governance, safety, ethical constraints, and workplace coexistence considerations

---

### User Story 5 - Reader Prepares for the 2030 Workforce (Priority: P1)

A reader wants actionable guidance on how to prepare for careers in Physical AI. They read Lesson 5 to learn about evolving education systems, robotics literacy, AI-agent fluency, ethical frameworks, safety design, and hands-on embodied robotics work.

**Why this priority**: Providing actionable preparation guidance makes the chapter directly valuable for students planning their education and careers.

**Independent Test**: Reader can identify at least 5 specific skills or competencies to develop and understand how education systems must evolve for Physical AI careers.

**Acceptance Scenarios**:

1. **Given** a reader opens Lesson 5, **When** they read about education evolution, **Then** they understand how training systems must adapt for robotics literacy and AI-agent fluency
2. **Given** a reader wants practical guidance, **When** they study Lesson 5, **Then** they find specific recommendations for hands-on embodied robotics experience
3. **Given** a reader completes Lesson 5, **When** they reflect, **Then** they have a clear understanding of ethical frameworks and safety design principles for Physical AI careers

---

### User Story 6 - Reader Accesses Chapter Index Overview (Priority: P2)

A reader wants an overview of the entire chapter before diving into individual lessons. They access the index.md file to find a high-level explanation of human-AI-robot collaboration, why the chapter matters, brief lesson introductions, and a concluding perspective on workforce transformation.

**Why this priority**: The index provides navigation and context that enhances the learning experience, though individual lessons can be consumed independently.

**Independent Test**: Reader can read the ~800-word index and understand the chapter's scope, each lesson's focus, and the overall narrative arc.

**Acceptance Scenarios**:

1. **Given** a reader opens the Chapter 2 index, **When** they read the introduction, **Then** they understand how human-AI-robot collaboration works at a high level
2. **Given** a reader wants lesson previews, **When** they scan the index, **Then** they find 1-2 paragraph introductions for each of the 5 lessons
3. **Given** a reader completes the index, **When** they finish reading, **Then** they understand the chapter's importance as a core building block for the Physical AI & Humanoid Robotics course

---

### Edge Cases

- What happens when a reader navigates directly to Lesson 5 without reading previous lessons? Content should be understandable independently while referencing prior concepts.
- How does the content handle readers with varying technical backgrounds? Expert insights provide depth without disrupting flow for beginners.
- What if readers want to compare lessons? Each lesson follows identical structure (3 main headings × 3 subheadings, 2 expert insights) for easy comparison and navigation.
- How does content reference the McKinsey report without becoming dated? Insights are presented as representative research findings with conceptual takeaways that remain relevant.

## Requirements *(mandatory)*

### Functional Requirements

#### Index File Requirements

- **FR-001**: index.md MUST contain approximately 800 words of substantive content
- **FR-002**: index.md MUST include a high-level explanation of human-AI-robot collaboration
- **FR-003**: index.md MUST explain why this chapter is a core building block for the Physical AI & Humanoid Robotics course
- **FR-004**: index.md MUST include 1-2 paragraph introductions for each of the 5 lessons
- **FR-005**: index.md MUST include a concluding perspective on how Physical AI will reshape the global workforce

#### Lesson Structure Requirements

- **FR-006**: Each lesson MUST contain approximately 1200 words of substantive content
- **FR-007**: Each lesson MUST have exactly 3 main headings (H2)
- **FR-008**: Each main heading MUST have exactly 3 subheadings (H3)
- **FR-009**: Each lesson MUST include exactly 2 expert insight blocks labeled "Expert Insight #1" and "Expert Insight #2"
- **FR-010**: Each expert insight MUST be 4-5 lines with applied, realistic content linked to Physical AI and humanoid robotics
- **FR-011**: Each lesson MUST include proper MDX frontmatter with sidebar_position, title, description, keywords, and slug
- **FR-012**: Each lesson MUST import and include SummaryButton and PersonalizeButton components matching Chapter 1 structure
- **FR-013**: Each lesson MUST end with a Key Takeaways section containing 4-6 bullet points
- **FR-014**: Each lesson MUST include a transition statement connecting to the next lesson

#### Content Quality Requirements

- **FR-015**: Writing style MUST be professional, educational, and forward-looking, suitable for university-level learners
- **FR-016**: Content MUST be conceptually rich but accessible, explaining why concepts matter
- **FR-017**: Content MUST maintain strong linkage to Physical AI and humanoid robotics throughout
- **FR-018**: Content MUST incorporate references to global workforce transitions, automation trends, and economic implications
- **FR-019**: Lessons MUST feel interconnected, supporting the chapter's overarching narrative
- **FR-020**: All content MUST be accurate, avoiding filler or placeholder text
- **FR-021**: Content MUST be formatted for dark-theme compatibility in Docusaurus

#### Lesson-Specific Content Requirements

- **FR-022**: Lesson 1 MUST explain the shift from human-only labor to collaborative ecosystems
- **FR-023**: Lesson 1 MUST include real examples from logistics automation, healthcare robotics, home AI companions, and industrial embodied systems
- **FR-024**: Lesson 1 MUST emphasize augmentation rather than replacement as the core purpose of Physical AI
- **FR-025**: Lesson 2 MUST describe essential human capabilities: contextual judgment, problem-solving, empathy, creativity, ethical oversight
- **FR-026**: Lesson 2 MUST use McKinsey insights to show which skill categories rise or fall
- **FR-027**: Lesson 2 MUST explain why Physical AI enhances rather than diminishes human intelligence value
- **FR-028**: Lesson 3 MUST define at least 4 new hybrid job roles (robot supervisors, AI workflow designers, safety operators, household robotics coordinators)
- **FR-029**: Lesson 3 MUST explain task-sharing: what robots do best, what AI agents automate, what humans must manage
- **FR-030**: Lesson 4 MUST analyze global effects: productivity acceleration, regional job displacement, new job creation, inequality challenges
- **FR-031**: Lesson 4 MUST discuss infrastructure demands (compute, energy, robotics deployment)
- **FR-032**: Lesson 4 MUST address governance, safety, ethical constraints, and human-robot workplace coexistence
- **FR-033**: Lesson 5 MUST explain how education and training systems must evolve
- **FR-034**: Lesson 5 MUST include robotics literacy, AI-agent fluency, hands-on embodied robotics work, ethical frameworks, and safety design
- **FR-035**: Lesson 5 MUST provide guidance for students preparing for Physical AI careers

### Research Sources by Lesson

Each lesson MUST be grounded in authoritative academic and industry research:

- **Lesson 1 Source**: McKinsey Global Institute - "Agents, Robots, and Us: Skill Partnerships in the Age of AI"
  - URL: https://www.mckinsey.com/mgi/our-research/agents-robots-and-us-skill-partnerships-in-the-age-of-ai
  - Focus: Human-agent-robot partnership model, collaborative workforce dynamics

- **Lesson 2 Source**: World Economic Forum - "Human Skills in the Age of AI"
  - URL: https://www.weforum.org/agenda/2023/08/ai-human-skills-future-of-work/
  - Focus: Essential human capabilities, skill transformation, future of work

- **Lesson 3 Source**: Brookings Institution - "Automation and Artificial Intelligence: How Machines Affect People and Places"
  - URL: https://www.brookings.edu/articles/automation-and-artificial-intelligence-how-machines-affect-people-and-places/
  - Focus: Hybrid job roles, regional automation impacts, human-AI task division

- **Lesson 4 Source**: OECD - "Robotics Impact on Economy"
  - URL: https://www.oecd.org/digital/robotics-impact-on-economy/
  - Focus: Global economic shifts, productivity, inequality, governance implications

- **Lesson 5 Source**: UNESCO - "AI Skills and the Future of Education"
  - URL: https://www.unesco.org/en/digital-education/ai-skills-future
  - Focus: Education system evolution, career preparation, ethical frameworks

### Key Entities

- **Chapter Index**: Overview document (~800 words) providing chapter introduction, lesson previews, and concluding perspective
- **Lesson**: Self-contained learning unit (~1200 words) with 3 main headings, 9 subheadings total, 2 expert insights, and key takeaways
- **Expert Insight Block**: 4-5 line highlighted callout providing applied, realistic perspectives on Physical AI and humanoid robotics
- **Key Takeaways**: Bulleted summary (4-6 points) of main learning concepts at lesson end
- **Hybrid Role**: Emerging job category that combines human judgment with AI/robot capabilities
- **Task-Sharing Framework**: Conceptual model describing what robots, AI agents, and humans each do best in collaborative work

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 6 files (index.md + 5 lessons) are complete and render correctly in Docusaurus without errors
- **SC-002**: index.md contains approximately 800 words (±50 words, verified by word count)
- **SC-003**: Each lesson contains approximately 1200 words (±100 words, verified by word count)
- **SC-004**: Each lesson passes structural validation: 3 H2 headings, 3 H3 subheadings per H2, 2 expert insight blocks
- **SC-005**: All expert insight blocks are 4-5 lines and provide applied, realistic content on Physical AI
- **SC-006**: Readers can navigate sequentially through lessons 1-5 with coherent flow and transitions between lessons
- **SC-007**: All MDX components (SummaryButton, PersonalizeButton, :::tip blocks) render correctly
- **SC-008**: Content accuracy: no factual errors about AI/robotics/workforce concepts when reviewed by subject matter expert
- **SC-009**: Reader comprehension: a university-level reader can summarize each lesson's main concept in one sentence after reading
- **SC-010**: McKinsey insights are accurately represented and properly contextualized without direct copyright-infringing quotations
- **SC-011**: Each lesson's key takeaways section contains 4-6 actionable bullet points

### Assumptions

- Chapter 1 structure and style serves as the authoritative template for Chapter 2 lessons
- The target audience is university-level learners with basic technical literacy but may not have AI/robotics background
- Dark theme is the default viewing mode in Docusaurus
- SummaryButton and PersonalizeButton components exist and function as shown in Chapter 1
- The :::tip MDX syntax for expert insights is supported by the Docusaurus configuration
- File paths follow the pattern: `/docs/part-01/chapter-02/` with index.md and lesson-XX.md files
- McKinsey "Agents, Robots, and Us" report insights can be paraphrased and cited without direct reproduction
- Expert insights should be labeled "Expert Insight #1" and "Expert Insight #2" consistently across lessons
