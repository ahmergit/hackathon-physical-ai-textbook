# Data Model: Chapter 1 Lessons 2-5

**Feature**: 002-chapter1-lessons-2-5  
**Date**: 2025-11-28  
**Purpose**: Define content structure and entities for lesson generation

## Entity Definitions

### Lesson

A self-contained learning unit within a chapter.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Unique identifier (e.g., "lesson-02") |
| title | string | Yes | Full lesson title for H1 heading |
| sidebar_position | integer | Yes | Order in sidebar navigation |
| description | string | Yes | SEO description (150-160 chars) |
| keywords | string[] | Yes | SEO keywords for the lesson |
| slug | string | Yes | URL path segment |
| word_count | integer | Yes | Target: 1100-1300 words |
| main_sections | MainSection[] | Yes | Array of 3 main H3 sections |
| key_takeaways | string[] | Yes | 4-6 bullet point summary |

### MainSection

A primary content division within a lesson (H3 level).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Section identifier |
| title | string | Yes | H3 heading text |
| introduction | string | No | Optional intro paragraph |
| subsections | Subsection[] | Yes | Array of 3 H4 subsections |

### Subsection

A detailed topic within a main section (H4 level).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Subsection identifier |
| title | string | Yes | H4 heading text |
| content | string | Yes | Main explanatory content (100-150 words) |
| expert_insight | ExpertInsight | Yes | Expert insight block |

### ExpertInsight

A highlighted callout providing expert perspective.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| topic | string | Yes | Insight topic for title |
| quote | string | No | Optional quote from expert |
| attribution | string | No | Quote attribution if present |
| context | string | Yes | Explanatory context (80-120 words) |
| references | string[] | No | Systems, papers, or organizations referenced |

## Content Structure Model

```
Lesson
├── frontmatter (MDX metadata)
├── imports (React components)
├── H1: Lesson Title
├── Component buttons (Summary, Personalize)
├── Overview paragraph
├── MainSection[0] (H3)
│   ├── Subsection[0] (H4)
│   │   ├── content
│   │   └── ExpertInsight
│   ├── Subsection[1] (H4)
│   │   ├── content
│   │   └── ExpertInsight
│   └── Subsection[2] (H4)
│       ├── content
│       └── ExpertInsight
├── MainSection[1] (H3)
│   └── [same structure]
├── MainSection[2] (H3)
│   └── [same structure]
├── Conclusion paragraph
└── Key Takeaways (bullet list)
```

## Validation Rules

### Lesson Validation
- `word_count` must be between 1100-1300
- `main_sections` must have exactly 3 items
- `key_takeaways` must have 4-6 items
- `sidebar_position` must be unique within chapter

### MainSection Validation
- `subsections` must have exactly 3 items
- `title` must not exceed 60 characters

### Subsection Validation
- `content` must be 100-150 words
- `expert_insight` must be present and valid

### ExpertInsight Validation
- `context` must be 80-120 words
- `topic` must not exceed 40 characters
- If `quote` present, `attribution` should be present

## State Transitions

Not applicable - content is static once generated.

## Relationships

```
Chapter 1
├── Lesson 1 (existing)
├── Lesson 2 ← NEW
├── Lesson 3 ← NEW
├── Lesson 4 ← NEW
└── Lesson 5 ← NEW

Each Lesson:
- belongs_to: Chapter
- has_many: MainSections (exactly 3)
- has_many: Subsections (exactly 9, via MainSections)
- has_many: ExpertInsights (exactly 9, via Subsections)
```

## Content Inventory

| Lesson | Main Sections | Subsections | Expert Insights | Est. Words |
|--------|---------------|-------------|-----------------|------------|
| 2 | 3 | 9 | 9 | 1200 |
| 3 | 3 | 9 | 9 | 1200 |
| 4 | 3 | 9 | 9 | 1200 |
| 5 | 3 | 9 | 9 | 1200 |
| **Total** | **12** | **36** | **36** | **4800** |
