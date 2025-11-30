# Data Model: Chapter 3 — AI & Humanoid Robots

**Feature**: 004-chapter3-ai-humanoid-robots  
**Date**: 2025-11-29

## Overview

This document defines the content structure and entities for Chapter 3. The chapter follows a consistent pattern where each lesson has a defined structure, content flow, and integration points for research-based insights.

---

## Entity Definitions

### Chapter
The top-level container for all chapter content.

| Field | Type | Description |
|-------|------|-------------|
| title | string | "Chapter 3 — AI & Humanoid Robots: How Intelligence Powers Real-World Machines" |
| index | IndexPage | Chapter overview document |
| lessons | Lesson[5] | Array of 5 lessons |
| target_audience | string | "O-Level students (ages 14-16)" |
| tone | string | "Friendly, simple, accessible" |

---

### IndexPage
The chapter introduction that sets context and previews all lessons.

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| word_count | number | ~1100 (±10%) | Target 990-1210 words |
| sections | Section[] | Required | Overview, lesson previews, 2025 advances, career outlook |

**Required Content Blocks**:
1. **Opening Hook**: Why AI + humanoid robots matter now
2. **What You'll Learn**: Brief intro to each of 5 lessons
3. **2025 Breakthroughs**: Recent advances making robots powerful
4. **Future Outlook**: Hopeful note about careers and opportunities

---

### Lesson
A self-contained educational unit with consistent structure.

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| number | number | 1-5 | Lesson sequence number |
| title | string | Required | Lesson title |
| word_count | number | ~1300 (±10%) | Target 1170-1430 words |
| h2_sections | H2Section[3] | Exactly 3 | Major sections |
| expert_insights | ExpertInsight[2] | Exactly 2 | Callout blocks |
| references | Reference[] | 2 per lesson | Source articles |

---

### H2Section
A major section within a lesson (3 per lesson).

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| heading | string | H2 format | Section title |
| h3_subsections | H3Subsection[3] | Exactly 3 | Subsections within |
| approx_words | number | ~400 | Roughly 1/3 of lesson |

---

### H3Subsection
A subsection within an H2 section (9 total per lesson).

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| heading | string | H3 format | Subsection title |
| content | string | ~130 words | Explanation, examples, stories |

---

### ExpertInsight
A highlighted callout providing professional perspective.

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| title | string | Required | Brief topic label |
| content | string | 4-5 lines | Expert perspective or deeper insight |
| placement | string | After H2 or H3 | Where it appears in lesson flow |
| format | string | Blockquote/Admonition | Docusaurus styling |

**Template**:
```markdown
:::info Expert Insight: [Title]
[4-5 lines of content providing professional perspective, using simple language appropriate for O-Level students]
:::
```

---

### Reference
Source article integrated into lesson content.

| Field | Type | Description |
|-------|------|-------------|
| source | string | Publication name (e.g., "Fundación Bankinter") |
| url | string | Full URL to article |
| year | number | 2025 |
| key_insights | string[] | Main points to incorporate |

---

## Lesson Structure Templates

### Lesson 1: Why Humanoid Robots Matter Today & Tomorrow

```yaml
title: "Why Humanoid Robots Matter Today & Tomorrow"
word_count: 1300
references:
  - Fundación Bankinter (PAL Robotics)
  - AA News (Humanoid Revolution)

h2_sections:
  - heading: "What Makes Humanoid Robots Special"
    h3_subsections:
      - "The Human-Like Shape"
      - "Sensors and Balance"
      - "AI Thinking and Learning"
      
  - heading: "Why Humanoid Robots Are Rising Now"
    h3_subsections:
      - "Better Motors and Cheaper Parts"
      - "Powerful AI Breakthroughs"
      - "Growing Industry Interest"
      
  - heading: "Where Humanoid Robots Are Heading"
    h3_subsections:
      - "From Labs to Real Life"
      - "Companies Leading the Way"
      - "What the Future Holds"

expert_insights:
  - title: "Why the Human-Like Form Helps Adaptation"
    placement: After H2.1
  - title: "Recent Breakthroughs Changing Everything"
    placement: After H2.2
```

### Lesson 2: Automation & Flexibility

```yaml
title: "Automation & Flexibility: How AI-Driven Humanoid Robots Change Work"
word_count: 1300
references:
  - GlobeNewswire (Industrial Robots Report 2025)
  - World Economic Forum

h2_sections:
  - heading: "From Fixed Machines to Flexible Helpers"
    h3_subsections:
      - "How Old Robots Worked"
      - "Why Flexibility Matters Now"
      - "AI Makes the Difference"
      
  - heading: "Robots Working Alongside Humans"
    h3_subsections:
      - "Cobots: Collaborative Robots"
      - "Safe Human-Robot Teams"
      - "Real Factory Examples"
      
  - heading: "Learning and Adapting on the Job"
    h3_subsections:
      - "How Robots Learn Tasks"
      - "Switching Between Jobs"
      - "The Smart Factory of Tomorrow"

expert_insights:
  - title: "Robots Working Beside Humans"
    placement: After H2.2
  - title: "Why AI Gives Robots Flexibility"
    placement: After H2.3
```

### Lesson 3: Service & Care

```yaml
title: "Service & Care: Robots in Homes, Hospitals, and Everyday Life"
word_count: 1300
references:
  - Fundación Bankinter
  - AA News (Realbotix, elderly care)

h2_sections:
  - heading: "Robots in Healthcare"
    h3_subsections:
      - "Helping Doctors and Nurses"
      - "Caring for Elderly Patients"
      - "Medication and Monitoring"
      
  - heading: "Robots in Our Homes"
    h3_subsections:
      - "Household Chores and Tasks"
      - "Companionship and Communication"
      - "Safety and Emergency Help"
      
  - heading: "Robots in Public Spaces"
    h3_subsections:
      - "Shops and Customer Service"
      - "Hotels and Reception"
      - "Museums and Information"

expert_insights:
  - title: "Robots Helping Elderly Safely"
    placement: After H2.1
  - title: "Daily-Life Tasks Robots Can Learn"
    placement: After H2.2
```

### Lesson 4: Challenges & Ethics

```yaml
title: "Challenges & Ethics: What We Must Think About When Robots Join Society"
word_count: 1300
references:
  - World Economic Forum
  - AA News

h2_sections:
  - heading: "Jobs and Work in a Robot World"
    h3_subsections:
      - "Will Robots Take Our Jobs?"
      - "New Jobs Robots Create"
      - "Working Together, Not Replacing"
      
  - heading: "Privacy, Safety, and Trust"
    h3_subsections:
      - "Who Controls Robot Data?"
      - "What If Robots Make Mistakes?"
      - "Building Trust with Technology"
      
  - heading: "Rules and Responsibility"
    h3_subsections:
      - "Why We Need Robot Rules"
      - "Who Is Responsible?"
      - "Making Fair Decisions"

expert_insights:
  - title: "Balancing Progress and Safety"
    placement: After H2.2
  - title: "Why Ethics Matter in Robotics"
    placement: After H2.3
```

### Lesson 5: Future Skills

```yaml
title: "Future Skills: How You Can Be Ready for a Robot-AI Future"
word_count: 1300
references:
  - Fundación Bankinter
  - GlobeNewswire (workforce trends)

h2_sections:
  - heading: "Skills That Matter Most"
    h3_subsections:
      - "Creativity and Problem-Solving"
      - "Logical Thinking and Math Basics"
      - "Teamwork and Communication"
      
  - heading: "Getting Started with Technology"
    h3_subsections:
      - "Basic Programming Ideas"
      - "Understanding How AI Works"
      - "Hands-On Robotics Projects"
      
  - heading: "Your Path Forward"
    h3_subsections:
      - "School Subjects That Help"
      - "Activities and Clubs to Join"
      - "Careers in Robotics and AI"

expert_insights:
  - title: "Skills Employers Need in the Robot Era"
    placement: After H2.1
  - title: "Learning Path for Teens"
    placement: After H2.3
```

---

## Content Flow Rules

### Sequential Flow (Recommended Reading Order)
1. Index → Lesson 1 → Lesson 2 → Lesson 3 → Lesson 4 → Lesson 5

### Independent Accessibility
Each lesson must be understandable if read in isolation, with:
- Brief context at the start
- Self-contained explanations
- No forward references to unread lessons

### Reference Integration
- Integrate article insights **within** lesson content (not as header citations)
- Use natural phrasing: "Recent reports show..." or "Industry experts explain..."
- Avoid academic-style citations

### Expert Insight Placement
- One insight in first half of lesson
- One insight in second half of lesson
- Never two consecutive insights
- Always after a related content block

---

## Validation Rules

| Rule | Check |
|------|-------|
| Word count (index) | 990-1210 words |
| Word count (lessons) | 1170-1430 words each |
| H2 count | Exactly 3 per lesson |
| H3 count | Exactly 9 per lesson (3 per H2) |
| Expert Insight count | Exactly 2 per lesson |
| Expert Insight length | 4-5 lines each |
| Readability | Flesch-Kincaid Grade 8-10 |
| Tone | No jargon, analogies used, conversational |
