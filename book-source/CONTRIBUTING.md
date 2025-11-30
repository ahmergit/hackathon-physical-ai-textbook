# Contributing to Physical AI & Humanoid Robotics

Thank you for your interest in contributing to this book! This guide explains the structure and conventions for adding content.

## Content Structure

The book follows a hierarchical structure:

```
docs/
├── preface.md
└── part-{N}-{slug}/
    ├── _category_.json
    └── chapter-{N}-{slug}/
        ├── _category_.json
        ├── lesson-{N}-{slug}.md
        ├── lesson-{N}-{slug}.md
        └── lesson-{N}-{slug}.md
```

## Naming Conventions

### Parts (Top Level)

- **Directory**: `part-{N}-{slug}/` (e.g., `part-1-foundations/`)
- **Category file**: `_category_.json` with:
  ```json
  {"label": "Part {Roman}: {Title}", "position": {N}}
  ```
- Example: `part-1-foundations/` → `{"label": "Part I: Foundations", "position": 1}`

### Chapters (Second Level)

- **Directory**: `chapter-{N}-{slug}/` (e.g., `chapter-1-introduction/`)
- **Category file**: `_category_.json` with:
  ```json
  {"label": "Chapter {N}: {Title}", "position": {N}}
  ```
- Example: `chapter-1-introduction/` → `{"label": "Chapter 1: Introduction", "position": 1}`

### Lessons (Third Level - Content Files)

- **Filename**: `lesson-{N}-{slug}.md` (e.g., `lesson-1-what-is-physical-ai.md`)
- **Frontmatter** (required):
  ```yaml
  ---
  sidebar_position: {N}
  title: "Lesson {Chapter}-{N}: {Title}"
  description: "{150-160 character description}"
  keywords: [keyword1, keyword2, keyword3, keyword4, keyword5]
  ---
  ```

**Important**: Each chapter should contain **exactly 3 lessons** for consistency.

## Content Guidelines

### Lesson Structure

Each lesson should follow this structure:

```markdown
# Lesson {X}-{Y}: {Title}

## Overview
{Brief introduction paragraph}

## {Main Section 1}

### {Subsection 1}
{Content}

### {Subsection 2}
{Content}

## {Main Section 2}
... (repeat structure)

## Key Takeaways
- {Takeaway 1}
- {Takeaway 2}
- {Takeaway 3}

---

**Next**: [Lesson X-Y: Title](./lesson-{N}-{slug}.md)
```

### Style Guidelines

- **Clarity**: Write for learners with varying backgrounds
- **Depth**: Balance accessibility with technical accuracy
- **Examples**: Include real-world applications and case studies
- **Visuals**: Add diagrams, code blocks, or tables where helpful
- **Length**: Aim for 800-1200 words per lesson

### Markdown Features

You can use:

- **Headings**: H1 (title), H2 (sections), H3 (subsections)
- **Lists**: Bulleted and numbered lists
- **Code blocks**: With syntax highlighting
- **Admonitions**: For notes, tips, warnings (Docusaurus-specific)
- **Links**: Internal (to other lessons) and external
- **Images**: Place in `/static/img/` directory

## Adding New Content

### Adding a New Part

1. Create directory: `docs/part-{N}-{slug}/`
2. Add `_category_.json` with label and position
3. Create chapter directories within it

### Adding a New Chapter

1. Create directory: `docs/part-{N}-{slug}/chapter-{M}-{slug}/`
2. Add `_category_.json` with label and position
3. Create **exactly 3 lesson files** (lesson-1, lesson-2, lesson-3)

### Adding a New Lesson

1. Create file: `lesson-{N}-{slug}.md`
2. Add required frontmatter (sidebar_position, title, description, keywords)
3. Follow the lesson structure template
4. Ensure proper linking (previous/next lessons)

## Testing Your Contribution

Before submitting:

1. **Build the site**:
   ```bash
   cd book-source
   npm run build
   ```
   Ensure no errors.

2. **Test locally**:
   ```bash
   npm run start
   ```
   Navigate to your new content and verify:
   - Sidebar shows correct hierarchy
   - Content renders properly
   - Links work
   - TOC (Table of Contents) generates correctly

3. **Check formatting**:
   - Verify frontmatter is valid YAML
   - Ensure consistent heading hierarchy
   - Check for broken links

## Workflow

1. **Fork** the repository
2. **Create a branch**: `git checkout -b add-part-X-chapter-Y`
3. **Add content** following conventions
4. **Test** locally (build + serve)
5. **Commit** with clear message: `Add Part X, Chapter Y: Title`
6. **Push** and create a **Pull Request**

## Questions?

If you have questions about:
- Content scope or topics
- Technical accuracy
- Structural organization

Open an issue or reach out to the maintainers.

---

Thank you for contributing to making Physical AI education accessible to everyone!
