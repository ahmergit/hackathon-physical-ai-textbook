# Quickstart: Writing Chapter 3 Content

**Feature**: 004-chapter3-ai-humanoid-robots  
**Date**: 2025-11-29

## Overview

This guide helps writers create Chapter 3 content about AI-driven humanoid robots for O-Level students (ages 14-16). Follow these guidelines to ensure consistent, engaging, and educational content.

---

## Before You Start

### Required Reading
1. **spec.md** — Feature requirements and success criteria
2. **research.md** — Key insights from 2025 sources
3. **data-model.md** — Content structure and lesson templates
4. **contracts/\*** — Detailed contracts for each file

### Target Audience
- **Age**: 14-16 years old (O-Level students)
- **Background**: Basic science literacy, no robotics knowledge
- **Goals**: Understand AI + robots, feel excited about future opportunities

---

## Writing Style Guide

### Tone
- **Friendly**: Like a teacher explaining to a curious student
- **Simple**: Avoid jargon; explain technical terms when first used
- **Engaging**: Use stories, examples, and analogies
- **Encouraging**: Make students feel capable and excited

### Language Rules
| Do | Don't |
|----|-------|
| Use short sentences | Write long, complex sentences |
| Explain terms simply | Assume prior knowledge |
| Give concrete examples | Stay abstract |
| Use "you" and "we" | Use passive voice |
| Include analogies | Use heavy math |

### Example Transformations

**Too Technical:**
> "Humanoid robots utilize reinforcement learning algorithms to optimize their locomotion patterns through iterative feedback loops."

**O-Level Friendly:**
> "Humanoid robots learn to walk better each time they try, just like how you learned to ride a bike — by practicing and adjusting until you got it right."

---

## Content Structure

### Index Page (~1100 words)

```markdown
---
sidebar_position: 1
---

# Chapter 3: AI & Humanoid Robots

[Opening hook - why this matters - 150 words]

## What You'll Learn in This Chapter

[Brief intro to each lesson - 500 words total, ~100 per lesson]

## Why 2025 Is a Turning Point

[Recent advances making robots powerful - 250 words]

## Your Future with Robots

[Career opportunities, hopeful message - 200 words]
```

### Lesson Pages (~1300 words each)

```markdown
---
sidebar_position: [2-6]
---

# Lesson [N]: [Title]

[Opening paragraph setting context - 100 words]

## [H2 Section 1 Title]

### [H3 Subsection 1.1]
[Content - ~130 words]

### [H3 Subsection 1.2]
[Content - ~130 words]

### [H3 Subsection 1.3]
[Content - ~130 words]

:::info Expert Insight: [Title]
[4-5 lines of professional perspective]
:::

## [H2 Section 2 Title]
[Same pattern...]

## [H2 Section 3 Title]
[Same pattern...]

## Summary
[Key takeaways - 50 words]
```

---

## Expert Insight Blocks

### Format
Use Docusaurus admonition syntax:

```markdown
:::info Expert Insight: Why Human-Like Form Helps Adaptation
Robots shaped like humans can use the same tools we use, walk through the same doors, and climb the same stairs. This makes them more useful in places designed for people — homes, offices, and hospitals were all built with human bodies in mind.
:::
```

### Placement Rules
- One in first half of lesson, one in second half
- Never two consecutive insights
- Place after related content block
- Keep to 4-5 lines (not paragraphs)

### Content Guidelines
- Provide deeper perspective without being too technical
- Connect to real-world applications
- Can reference expert opinions from research

---

## Integrating Research Sources

### Do's
- Weave insights naturally into explanations
- Use phrases like "Recent reports show..." or "Industry experts explain..."
- Cite specific statistics when impactful
- Reference real companies and robots as examples

### Don'ts
- Don't add citation headers at top of lessons
- Don't use academic reference style [1] [2]
- Don't quote extensively — paraphrase for simplicity
- Don't overwhelm with too many statistics

### Example Integration

**Research Finding:**
> Morgan Stanley estimates ~1 billion humanoid robots by 2050

**In Lesson:**
> Imagine a world where there's one robot for every ten people on Earth. That's what some experts predict could happen by 2050! These robots won't just be in factories — they'll be in homes, hospitals, and schools, helping with everyday tasks.

---

## Examples and Analogies

### Good Examples for O-Level Students
- Robot lifting boxes in a warehouse (relatable action)
- Robot helping grandma with medicine (family connection)
- Robot greeting customers at a shop (everyday experience)
- Tesla's Optimus robot (known brand)
- Robots running a marathon (recent 2025 news)

### Effective Analogies
- Robot learning = student learning to ride a bike
- Robot sensors = human senses (eyes, ears, touch)
- AI decision-making = brain thinking through options
- Cobot = helpful teammate, not replacement
- Digital twin = practice mode in a video game

---

## Checklist Before Submitting

### Structure Check
- [ ] Word count within ±10% of target
- [ ] Exactly 3 H2 sections (lessons only)
- [ ] Exactly 9 H3 subsections (lessons only)
- [ ] Exactly 2 Expert Insight blocks (lessons only)

### Content Check
- [ ] No jargon without explanation
- [ ] At least 3 concrete examples per lesson
- [ ] At least 2 analogies per lesson
- [ ] Reference sources integrated naturally
- [ ] Opening hook engages curiosity

### Tone Check
- [ ] Friendly and encouraging throughout
- [ ] "You" and "we" used (not just "students")
- [ ] No condescending language
- [ ] Ends on positive/hopeful note

### Technical Check
- [ ] Frontmatter includes sidebar_position
- [ ] Expert Insight uses correct admonition syntax
- [ ] No broken markdown formatting
- [ ] File named correctly (lesson-N.md)

---

## File Naming and Location

```
book-source/docs/part-XX/chapter-03/
├── index.md           # sidebar_position: 1
├── lesson-1.md        # sidebar_position: 2
├── lesson-2.md        # sidebar_position: 3
├── lesson-3.md        # sidebar_position: 4
├── lesson-4.md        # sidebar_position: 5
└── lesson-5.md        # sidebar_position: 6
```

---

## Quick Reference: Lesson Summaries

| Lesson | Focus | Key Examples | Sources |
|--------|-------|--------------|---------|
| 1 | What makes humanoids special | Tesla Optimus, Boston Dynamics Atlas | Bankinter, AA News |
| 2 | Factory automation & flexibility | BMW robots, Amazon warehouses | GlobeNewswire, WEF |
| 3 | Healthcare, homes, daily life | Elder care robots, Aria reception bot | Bankinter, AA News |
| 4 | Jobs, privacy, ethics, rules | Job concerns, safety questions | WEF, AA News |
| 5 | Skills, learning, careers | Programming, robotics clubs, jobs | Bankinter, GlobeNewswire |

---

## Need Help?

- **Spec questions**: Review `spec.md` for requirements
- **Research details**: Check `research.md` for source insights
- **Structure issues**: Consult `data-model.md` for templates
- **Specific contracts**: See `contracts/` directory for per-file details
