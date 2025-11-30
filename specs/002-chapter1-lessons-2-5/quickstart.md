# Quickstart: Chapter 1 Lessons 2-5 Implementation

**Feature**: 002-chapter1-lessons-2-5  
**Date**: 2025-11-28  
**Purpose**: Step-by-step guide for generating lesson content

## Prerequisites

- [x] Lesson 1 exists as template reference
- [x] Docusaurus site builds successfully
- [x] SummaryButton and PersonalizeButton components available
- [x] Spec and plan approved

## Implementation Steps

### Step 1: Create Lesson Files

Create four new MDX files in `book-source/docs/part-01/chapter-01/`:

```
lesson-02.md  # Why Embodied Intelligence Matters
lesson-03.md  # Evolution of AI: From LLMs to VLA
lesson-04.md  # The Embodied AI Pipeline
lesson-05.md  # Traditional Physical AI Falls Short
```

### Step 2: Add Frontmatter

Each lesson requires this frontmatter structure:

```yaml
---
sidebar_position: [2-5]
title: "Lesson [N]: [Title]"
description: "[150-160 char SEO description]"
keywords: [keyword1, keyword2, ...]
slug: /part-01/chapter-01/lesson-0[N]
---
```

### Step 3: Add Imports and Header

```mdx
import SummaryButton from '@site/src/components/SummaryButton';
import PersonalizeButton from '@site/src/components/PersonalizeButton';

# Lesson [N]: [Title]

<SummaryButton lessonId="lesson-0[N]" />
<PersonalizeButton lessonId="lesson-0[N]" defaultLevel="Beginner" />

## Overview

[Opening paragraph introducing the lesson topic]
```

### Step 4: Write Main Sections

For each lesson, create 3 main sections (H3) with 3 subsections (H4) each:

```mdx
## [Main Section Title]

### [Subsection Title]

[Content paragraph - 100-150 words]

:::tip Expert Insight: [Topic]

[Expert insight paragraph - 80-120 words with real-world reference]

:::

### [Next Subsection]
...
```

### Step 5: Add Conclusion and Takeaways

```mdx
## Conclusion

[Summary paragraph connecting to next lesson]

---

**Key Takeaways**:
- [Takeaway 1]
- [Takeaway 2]
- [Takeaway 3]
- [Takeaway 4]
- [Takeaway 5 (optional)]
- [Takeaway 6 (optional)]
```

### Step 6: Validate Content

For each lesson, verify:

| Check | Requirement |
|-------|-------------|
| Word count | 1100-1300 words |
| H3 sections | Exactly 3 |
| H4 subsections | Exactly 3 per H3 (9 total) |
| Expert insights | Exactly 9 (one per H4) |
| Key takeaways | 4-6 bullets |
| No placeholders | No [TODO], [TBD], etc. |
| Real examples | Systems/companies referenced |

### Step 7: Build and Preview

```bash
cd book-source
npm run build
npm run serve
```

Navigate to each lesson URL to verify rendering.

## Content Reference by Lesson

### Lesson 2: Why Embodied Intelligence Matters

**Main Sections**:
1. Importance of Physical Grounding
2. Interaction with the Environment
3. Real-World Learning Challenges

**Key Systems to Reference**: Boston Dynamics Spot/Atlas, Agility Robotics Digit, OpenAI domain randomization

### Lesson 3: Evolution of AI - From LLMs to VLA

**Main Sections**:
1. Digital-Only AI Systems
2. Multimodal Intelligence Integration
3. Action-Oriented Embodied AI

**Key Systems to Reference**: GPT, BERT, CLIP, GPT-4V, RT-1, RT-2, OpenVLA

### Lesson 4: Embodied AI Pipeline

**Main Sections**:
1. Perception Systems in Robotics
2. Planning and Decision-Making
3. Action Execution and Feedback

**Key Systems to Reference**: ORB-SLAM, MoveIt, OMPL, IsaacGym, Diffusion Policy

### Lesson 5: Traditional Physical AI Falls Short

**Main Sections**:
1. Limitations of Classical Robotics
2. Challenges in Unstructured Environments
3. Modern Embodied AI Solutions

**Key Systems to Reference**: Industrial arms, DARPA Challenge vehicles, Mobile ALOHA, PaLM-E

## File Checklist

| File | Status | Location |
|------|--------|----------|
| lesson-02.md | ⬜ To Create | `book-source/docs/part-01/chapter-01/` |
| lesson-03.md | ⬜ To Create | `book-source/docs/part-01/chapter-01/` |
| lesson-04.md | ⬜ To Create | `book-source/docs/part-01/chapter-01/` |
| lesson-05.md | ⬜ To Create | `book-source/docs/part-01/chapter-01/` |

## Estimated Effort

| Task | Time |
|------|------|
| Content generation (4 lessons) | 60-90 min |
| Review and validation | 15-20 min |
| Build and preview | 5 min |
| **Total** | **~2 hours** |
