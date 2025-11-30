# Implementation Plan: Docusaurus Site Structure

**Feature**: Docusaurus-based Documentation Website Structure
**Version**: 1.0.0
**Status**: Draft
**Created**: 2025-11-28
**Last Updated**: 2025-11-28
**Related Spec**: `specs/docusaurus-site-structure/spec.md`

---

## Executive Summary

This plan defines the technical implementation strategy for building a production-ready Docusaurus 3.9.2 static site with a custom book layout, three-column reading interface, dark-themed homepage, and AI-powered assistance integration points. The site will serve as the foundation for an AI-generated technical book on Physical AI and Humanoid Robotics, with content organized hierarchically as Parts → Chapters → Lessons, rendered via MDX, and deployed as a static site to GitHub Pages.

**Core Implementation Principle**: Build the complete site structure and navigation framework first, with placeholder content, so that AI-generated book content can be plugged in without structural changes.

---

## 1. Scope and Dependencies

### 1.1 In Scope

**Core Infrastructure:**
- Docusaurus 3.9.2 installation with TypeScript and React 18 configuration
- Static site generation pipeline targeting GitHub Pages deployment
- TypeScript configuration with strict mode enabled
- NPM package management with locked dependencies

**Homepage Implementation:**
- Dark-themed sticky header with book title and GitHub link
- Centered hero section with book cover image, title, subtitle
- Call-to-action button linking to `/docs/preface`
- Tag block component displaying "Open Source" and "Embodied Intelligence"
- Responsive mobile layout with stacked elements

**Book Navigation Structure:**
- Three-tier hierarchy: Parts → Chapters → Lessons
- Auto-generated sidebar from folder structure via `sidebars.ts`
- Folder convention: `/docs/part-x/chapter-y/lesson-z.md`
- Each chapter contains exactly 3 lessons (enforced via documentation)

**Documentation Layout:**
- Three-column layout: left sidebar, center content, right TOC
- Custom theme override in `/src/theme/DocItem/` for layout control
- Breadcrumb navigation showing Part > Chapter > Lesson path
- Right-side sticky TOC auto-generated from H2/H3 headings
- AI tool buttons integrated into doc pages (placeholder for future RAG feature)

**Custom Components:**
- `Header`: Dark-themed navigation bar (reusable across pages)
- `HomepageHero`: Hero section with cover, title, subtitle, CTA
- `TagBlock`: Tag display component for homepage features
- `BookLayout`: Wrapper for three-column documentation layout
- `AITools`: Placeholder button component for future RAG assistant

**Responsive Behavior:**
- Mobile: Collapse left sidebar to hamburger, hide right TOC
- Tablet: Maintain sidebar, collapse TOC or make toggleable
- Desktop: Full three-column layout

**Configuration:**
- Dark mode enabled by default in `docusaurus.config.ts`
- Navbar items: book title (left), GitHub link (right)
- Custom component registration and plugin configuration
- Static export optimized for GitHub Pages

**Deliverables:**
- Fully functional Docusaurus site structure
- Polished homepage with hero and tags
- Three-column book reading interface
- Responsive mobile/tablet/desktop layouts
- Deployable static build ready for GitHub Pages

---

### 1.2 Out of Scope

**Content Generation:**
- AI-generated book content (separate feature with its own spec)
- Actual chapter and lesson writing (placeholder MDX files only)

**RAG Assistant Implementation:**
- Vector database setup (Qdrant)
- Embedding generation and ingestion pipeline
- Interactive chat interface
- Backend API for RAG queries

**Advanced Features:**
- Full-text search (will use Docusaurus default search if needed)
- Analytics and user tracking
- Comments or discussion features
- Multi-language support (i18n)
- Version switching (versioned docs)

**Custom Theming:**
- Advanced color schemes beyond dark mode default
- Custom fonts (will use Docusaurus defaults initially)
- Complex animations or transitions

---

### 1.3 External Dependencies

| Dependency | Version | Purpose | Ownership |
|------------|---------|---------|-----------|
| Node.js | 18+ (LTS) | JavaScript runtime | External (nodejs.org) |
| npm | 9+ | Package manager | External (npmjs.com) |
| Docusaurus | 3.9.2 | Static site generator | External (Meta/Facebook) |
| React | 18+ | UI framework | External (Meta/Facebook) |
| TypeScript | 5.x | Type safety | External (Microsoft) |
| MDX | 3.x | Markdown + JSX | External (MDX team) |
| GitHub Pages | N/A | Static hosting | External (GitHub) |

**Dependency Management:**
- All dependencies locked in `package-lock.json`
- Semantic versioning enforced (exact versions for Docusaurus)
- Security updates monitored via `npm audit`

---

### 1.4 Internal Dependencies

| Dependency | Location | Purpose |
|------------|----------|---------|
| Constitution | `.specify/memory/constitution.md` | Project principles and governance |
| Specification | `specs/docusaurus-site-structure/spec.md` | Feature requirements |
| Git Repository | Root directory | Version control |
| GitHub Repository | Remote | Deployment target |

---

## 2. Key Decisions and Rationale

### 2.1 Decision: Use Docusaurus 3.9.2 as Static Site Generator

**Options Considered:**
1. **Docusaurus 3.9.2** (chosen)
2. VuePress
3. Next.js with MDX
4. Gatsby
5. Custom React SPA

**Rationale:**
- **Pro**: Docusaurus is purpose-built for documentation sites with excellent defaults
- **Pro**: Built-in support for versioning, search, sidebar generation, and TOC
- **Pro**: React-based, allowing custom components and theme overrides
- **Pro**: MDX support for embedding interactive components in content
- **Pro**: Active development and large community (Meta-backed)
- **Pro**: Zero-config static export suitable for GitHub Pages
- **Con**: Less flexible than custom Next.js build, but flexibility not needed for this use case
- **Con**: Opinionated structure, but aligns with our requirements

**Trade-offs:**
- **Accept**: Opinionated folder structure and configuration patterns
- **Gain**: Rapid development, battle-tested navigation, automatic TOC/sidebar generation
- **Risk**: Locked into Docusaurus upgrade path (mitigated by version pinning)

**Principles Applied:**
- Constitution Principle III: Automation-First & Reproducible (Docusaurus provides automatic routing, TOC, sidebar)
- Constitution Principle IV: Code Quality & Type Safety (TypeScript support)
- Constitution Principle VI: Performance & UX Consistency (Lighthouse-optimized defaults)

---

### 2.2 Decision: MDX for All Book Content

**Options Considered:**
1. **MDX (Markdown + JSX)** (chosen)
2. Plain Markdown (.md)
3. AsciiDoc
4. reStructuredText

**Rationale:**
- **Pro**: MDX allows embedding React components in content (future-proofs for interactive diagrams, code playgrounds)
- **Pro**: Full Markdown compatibility (all existing Markdown is valid MDX)
- **Pro**: Native Docusaurus integration with frontmatter support
- **Pro**: Enables inline custom components (e.g., callouts, interactive widgets)
- **Con**: Slightly more complex than plain Markdown, but not significantly
- **Gain**: Flexibility for future interactive content without migration

**Trade-offs:**
- **Accept**: Learning curve for MDX syntax for content creators
- **Gain**: Future-proof content format, no migration needed for interactive elements

---

### 2.3 Decision: Three-Tier Hierarchy (Parts → Chapters → Lessons)

**Options Considered:**
1. **Parts → Chapters → Lessons** (chosen)
2. Chapters → Lessons (two-tier)
3. Sections → Subsections (generic naming)
4. Flat structure with tags

**Rationale:**
- **Pro**: Three-tier hierarchy matches typical technical book structure
- **Pro**: Allows grouping related chapters into logical parts (e.g., "Fundamentals", "Applications")
- **Pro**: Scales well for large books (50+ lessons)
- **Pro**: Clear mental model for readers and content creators
- **Con**: Slightly more nesting than two-tier, but manageable with auto-generated sidebar

**Folder Convention:**
```
/docs/
  preface.md
  part-1-foundations/
    _category_.json
    chapter-1-introduction/
      _category_.json
      lesson-1-what-is-physical-ai.md
      lesson-2-history-and-evolution.md
      lesson-3-core-challenges.md
    chapter-2-robotics-basics/
      _category_.json
      lesson-1-mechanical-systems.md
      lesson-2-sensors-and-actuators.md
      lesson-3-control-theory.md
  part-2-advanced-topics/
    ...
```

**Principles Applied:**
- Constitution Principle IX: Minimal & Sufficient Content (clear structure without over-nesting)
- Constitution Principle X: Modularity & Maintainability (clear naming convention)

---

### 2.4 Decision: Custom Theme Override for DocItem Layout

**Options Considered:**
1. **Theme override in `/src/theme/DocItem/`** (chosen)
2. Custom plugin to inject layout
3. Wrapper component via MDX provider
4. Fork and modify Docusaurus core

**Rationale:**
- **Pro**: Docusaurus "swizzling" (theme override) is the official way to customize layouts
- **Pro**: Clean separation: core Docusaurus unchanged, customizations isolated
- **Pro**: Survives Docusaurus upgrades (with compatibility checks)
- **Pro**: Allows injecting breadcrumbs, AI tool buttons, and custom layout elements
- **Con**: Requires understanding Docusaurus theme internals
- **Con**: May break on major Docusaurus version upgrades (mitigated by version pinning)

**Implementation Strategy:**
1. Run `npm run swizzle @docusaurus/theme-classic DocItem/Layout -- --wrap`
2. Modify wrapper to inject breadcrumbs, AI tools, and three-column layout
3. Test across multiple pages and screen sizes

**Trade-offs:**
- **Accept**: Maintenance burden for theme override on Docusaurus upgrades
- **Gain**: Full control over doc page layout without forking core

---

### 2.5 Decision: Auto-Generated Sidebar via sidebars.ts

**Options Considered:**
1. **Auto-generated from folder structure** (chosen)
2. Manually defined sidebar items in `sidebars.ts`
3. Hybrid: auto-generate with manual overrides

**Rationale:**
- **Pro**: Zero maintenance once folder convention is established
- **Pro**: Sidebar always reflects actual content structure (no drift)
- **Pro**: Content creators add chapters/lessons by creating folders and files (no config edits)
- **Con**: Less control over ordering (mitigated by `_category_.json` position field)
- **Gain**: Constitution Principle III compliance (automation-first)

**Configuration:**
```typescript
// sidebars.ts
const sidebars = {
  bookSidebar: [
    {
      type: 'autogenerated',
      dirName: '.',
    },
  ],
};
```

**Ordering Control:**
- Use `position` field in `_category_.json` for parts and chapters
- Use filename prefixes (e.g., `lesson-1-`, `lesson-2-`) for lessons

---

### 2.6 Decision: Dark Mode as Default

**Options Considered:**
1. **Dark mode as default** (chosen)
2. Light mode as default
3. System preference detection
4. User toggle with persistence

**Rationale:**
- **Pro**: Modern technical documentation trend favors dark mode
- **Pro**: Reduces eye strain for long reading sessions
- **Pro**: Aligns with "Physical AI" branding (tech-forward aesthetic)
- **Con**: Some users prefer light mode (mitigated by Docusaurus built-in toggle)
- **Implementation**: Set `colorMode.defaultMode: 'dark'` in `docusaurus.config.ts`

**Trade-offs:**
- **Accept**: Not all users prefer dark mode
- **Gain**: Modern aesthetic, reduced eye strain, user can toggle if preferred

---

### 2.7 Decision: Exactly 3 Lessons per Chapter (Enforced via Documentation)

**Options Considered:**
1. **Exactly 3 lessons per chapter** (chosen)
2. Variable lessons per chapter (1-5)
3. No constraint

**Rationale:**
- **Pro**: Consistent structure aids reader comprehension (predictable pattern)
- **Pro**: Prevents chapters from becoming too short (1 lesson) or too long (10+ lessons)
- **Pro**: Simplifies AI content generation (fixed template)
- **Con**: May force artificial splits if natural content doesn't fit 3 lessons
- **Enforcement**: Document convention in `CONTRIBUTING.md`, validate during content review

**Trade-offs:**
- **Accept**: Some flexibility lost (cannot have 2 or 4 lessons)
- **Gain**: Consistency, predictability, easier content planning

---

### 2.8 Decision: GitHub Pages for Deployment

**Options Considered:**
1. **GitHub Pages** (chosen)
2. Netlify
3. Vercel
4. AWS S3 + CloudFront
5. Self-hosted server

**Rationale:**
- **Pro**: Free hosting for public repositories
- **Pro**: Automatic deployment via GitHub Actions
- **Pro**: Custom domain support (if needed later)
- **Pro**: No additional accounts or services required
- **Con**: Limited to static sites (not a concern for Docusaurus)
- **Con**: No server-side rendering (not needed for this project)

**Deployment Strategy:**
- Use `gh-pages` branch for static build output
- Configure `docusaurus.config.ts` with correct `baseUrl`
- Set up GitHub Actions workflow for automatic deployment on push to `main`

---

## 3. Interfaces and API Contracts

### 3.1 Folder Structure Contract

**Purpose**: Define the contract between content creators and the Docusaurus build system.

**Contract:**
```
/docs/
  preface.md                              # Special: landing page at /docs/preface
  part-{N}-{slug}/                        # Part folder (N = 1, 2, 3, ...)
    _category_.json                       # Part metadata
    chapter-{M}-{slug}/                   # Chapter folder (M = 1, 2, 3, ...)
      _category_.json                     # Chapter metadata
      lesson-{K}-{slug}.md                # Lesson file (K = 1, 2, 3)
```

**Naming Rules:**
- `{N}`, `{M}`, `{K}`: Numbers without leading zeros (e.g., `1`, `2`, `10`)
- `{slug}`: Lowercase kebab-case (e.g., `introduction`, `core-concepts`)
- Lesson slugs should be descriptive (e.g., `what-is-physical-ai`, not `intro`)

**_category_.json Schema:**
```json
{
  "label": "string",          // Display name in sidebar (e.g., "Part I: Foundations")
  "position": "number",       // Sort order (1, 2, 3, ...)
  "link": {
    "type": "generated-index",
    "description": "string"   // Optional: description for part/chapter index page
  },
  "collapsed": "boolean"      // Optional: default collapsed state (default: false)
}
```

**Lesson Frontmatter Schema:**
```yaml
---
id: lesson-1-what-is-physical-ai
title: What is Physical AI?
sidebar_label: What is Physical AI?
sidebar_position: 1
description: Introduction to Physical AI and its applications
keywords: [physical ai, robotics, embodied intelligence]
---
```

**Outputs:**
- URL: `/docs/part-{N}-{slug}/chapter-{M}-{slug}/lesson-{K}-{slug}`
- Sidebar: Auto-generated tree structure
- Breadcrumbs: Part > Chapter > Lesson

**Validation:**
- Pre-commit hook (future): Validate folder structure and frontmatter
- Build-time: Docusaurus throws error on missing `_category_.json` or malformed frontmatter

---

### 3.2 Component Interface Contracts

#### 3.2.1 Header Component

**Location**: `/src/components/Header.tsx`

**Purpose**: Dark-themed sticky navigation bar for all pages.

**Props:**
```typescript
interface HeaderProps {
  title: string;           // Book title (e.g., "Physical AI & Humanoid Robotics")
  githubUrl: string;       // GitHub repository URL
}
```

**Outputs:**
- Sticky header (position: sticky, top: 0)
- Left: Book title (links to `/`)
- Right: GitHub icon button (opens in new tab)
- Background: Dark theme (e.g., `#1a1a1a`)
- Z-index: High (e.g., 1000) to overlay content on scroll

**Styling:**
- Responsive: Full width on all devices
- Mobile: Title may truncate with ellipsis if too long

---

#### 3.2.2 HomepageHero Component

**Location**: `/src/components/HomepageHero.tsx`

**Purpose**: Centered hero section with book cover, title, subtitle, CTA.

**Props:**
```typescript
interface HomepageHeroProps {
  coverImage: string;       // Path to book cover image (e.g., "/img/book-cover.png")
  title: string;            // Main title (e.g., "Physical AI & Humanoid Robotics")
  subtitle: string;         // Subtitle (e.g., "From Fundamentals to Advanced Applications")
  ctaText: string;          // CTA button text (e.g., "Start Reading")
  ctaLink: string;          // CTA button link (e.g., "/docs/preface")
}
```

**Outputs:**
- Centered layout (max-width: 900px)
- Book cover image (max-width: 300px, centered)
- Title: Large font (3rem), bold
- Subtitle: Medium font (1.5rem), lighter weight
- CTA button: Prominent (primary color, large padding)

**Responsive:**
- Mobile: Stack vertically, reduce font sizes
- Tablet/Desktop: Horizontal layout or centered stack

---

#### 3.2.3 TagBlock Component

**Location**: `/src/components/TagBlock.tsx`

**Purpose**: Display feature tags on homepage (e.g., "Open Source", "Embodied Intelligence").

**Props:**
```typescript
interface TagBlockProps {
  tags: string[];           // Array of tag labels (e.g., ["Open Source", "Embodied Intelligence"])
}
```

**Outputs:**
- Horizontal list of tags
- Each tag: Rounded border, padding, background color
- Responsive: Wrap to multiple lines on mobile

**Styling:**
- Tag background: Semi-transparent (e.g., `rgba(255, 255, 255, 0.1)`)
- Tag text: White or light color
- Spacing: Gap between tags (e.g., 1rem)

---

#### 3.2.4 BookLayout Component

**Location**: `/src/components/BookLayout.tsx`

**Purpose**: Wrapper for three-column documentation layout.

**Props:**
```typescript
interface BookLayoutProps {
  children: React.ReactNode;   // Main content (MDX)
  sidebar: React.ReactNode;    // Left sidebar (Docusaurus auto-generated)
  toc: React.ReactNode;        // Right TOC (Docusaurus auto-generated)
}
```

**Layout:**
```
+-------------------+-------------------------+-------------------+
| Sidebar (250px)   | Content (flex-grow)     | TOC (250px)       |
| - Auto-generated  | - MDX rendering         | - H2/H3 headings  |
| - Collapsible     | - Max-width: 900px      | - Sticky position |
+-------------------+-------------------------+-------------------+
```

**Responsive:**
- Desktop (1024px+): Full three-column layout
- Tablet (768px-1023px): Sidebar toggleable, TOC hidden or toggleable
- Mobile (< 768px): Sidebar hamburger menu, TOC hidden, full-width content

---

#### 3.2.5 AITools Component

**Location**: `/src/components/AITools.tsx`

**Purpose**: Placeholder button for future RAG assistant integration.

**Props:**
```typescript
interface AIToolsProps {
  variant?: 'button' | 'floating';   // Display variant (default: 'button')
}
```

**Outputs:**
- Button: "Ask AI Assistant" (icon + text)
- Position: Top-right of doc page (if `variant: 'floating'`)
- Behavior: Currently does nothing (placeholder for future feature)

**Future Integration:**
- Click opens chat modal with RAG assistant
- Sends current page context to assistant

---

### 3.3 Configuration Contracts

#### 3.3.1 docusaurus.config.ts

**Purpose**: Main configuration file for Docusaurus.

**Key Sections:**

```typescript
const config = {
  // Site metadata
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'From Fundamentals to Advanced Applications',
  url: 'https://yourusername.github.io',
  baseUrl: '/physical-ai-humaniod-robotics/',

  // Dark mode default
  themeConfig: {
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,
      respectPrefersColorScheme: false,
    },

    // Navbar
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      items: [
        {
          href: 'https://github.com/yourusername/physical-ai-humaniod-robotics',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },

    // Footer (minimal or removed for book site)
    footer: {
      style: 'dark',
      copyright: `© ${new Date().getFullYear()} Physical AI Robotics. Built with Docusaurus.`,
    },
  },

  // Presets
  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: 'docs',
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/yourusername/physical-ai-humaniod-robotics/tree/main/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      },
    ],
  ],
};
```

---

#### 3.3.2 sidebars.ts

**Purpose**: Configure sidebar generation strategy.

```typescript
const sidebars = {
  bookSidebar: [
    {
      type: 'autogenerated',
      dirName: '.',
    },
  ],
};
```

**Behavior:**
- Scans `/docs/` directory recursively
- Generates sidebar tree from folder structure
- Respects `_category_.json` for metadata and ordering
- Lesson order determined by `sidebar_position` frontmatter or filename

---

## 4. Non-Functional Requirements (NFRs) and Budgets

### 4.1 Performance

**Build Performance:**
- **Target**: Static build completes in < 60 seconds for ~50 pages
- **Budget**: < 10 seconds for initial Docusaurus build (empty site)
- **Budget**: < 1 second per page (50 pages × 1s = 50s total)
- **Measurement**: `npm run build` execution time
- **Mitigation**: Optimize images, minimize custom JavaScript, use code splitting

**Page Load Performance:**
- **Target**: First Contentful Paint (FCP) < 1.5 seconds
- **Target**: Time to Interactive (TTI) < 3 seconds
- **Target**: Lighthouse Performance score > 90
- **Measurement**: Lighthouse audit in Chrome DevTools
- **Mitigation**:
  - Lazy-load images
  - Minimize custom CSS/JS
  - Use Docusaurus default optimizations (code splitting, prefetching)
  - Optimize book cover image (WebP format, < 200KB)

**Asset Budgets:**
- JavaScript bundle (main): < 200KB (gzipped)
- CSS bundle: < 50KB (gzipped)
- Book cover image: < 200KB
- Total page size: < 500KB (per page)

---

### 4.2 Reliability

**Uptime (GitHub Pages):**
- **Target**: 99.9% uptime (managed by GitHub)
- **SLO**: Not applicable (no backend services)

**Build Reliability:**
- **Target**: 100% build success rate for valid content
- **Error Handling**:
  - Broken internal links: Fail build (Docusaurus default)
  - Missing images: Warn or fail (configurable)
  - Malformed frontmatter: Fail build with clear error message

**Degradation Strategy:**
- If JavaScript fails to load: Content still readable (progressive enhancement)
- If CSS fails to load: Basic HTML structure still usable
- If sidebar fails to render: Breadcrumbs provide navigation

---

### 4.3 Security

**Content Security:**
- **Threat Model**: Static site (no user input, no backend)
- **Attack Surface**: Minimal (read-only content)
- **XSS Prevention**: Docusaurus sanitizes Markdown by default
- **Dependency Security**:
  - Run `npm audit` before every deployment
  - Update dependencies monthly (or on critical CVEs)
  - No direct use of `dangerouslySetInnerHTML` in custom components

**Access Control:**
- GitHub repository: Public (open source book)
- No authentication required for site access

**Secrets Management:**
- No secrets required for static site
- GitHub Actions: Use secrets for deployment tokens (if needed)

---

### 4.4 Accessibility

**Compliance:**
- **Target**: WCAG 2.1 Level AA
- **Measurement**: Lighthouse Accessibility score > 90

**Requirements:**
- Semantic HTML5 structure (headers, nav, main, article)
- Keyboard navigation: All interactive elements accessible via Tab
- Screen reader support: Proper ARIA labels for custom components
- Color contrast:
  - Body text: 4.5:1 minimum
  - Large text (18pt+): 3:1 minimum
- Alt text: All images (book cover, diagrams) have descriptive alt text
- Focus indicators: Visible focus outlines on all interactive elements

**Testing:**
- Automated: Lighthouse, axe DevTools
- Manual: Keyboard-only navigation, screen reader testing (NVDA/VoiceOver)

---

### 4.5 SEO

**Meta Tags:**
- Title: Unique per page (from frontmatter `title`)
- Description: Unique per page (from frontmatter `description`)
- Open Graph tags: Image, title, description for social sharing
- Canonical URLs: Auto-generated by Docusaurus

**Sitemap:**
- Auto-generated by Docusaurus (`sitemap.xml`)
- Submitted to Google Search Console (post-deployment)

**Robots.txt:**
- Allow all crawlers (default Docusaurus behavior)

---

## 5. Data Management and Migration

### 5.1 Source of Truth

**Content:**
- **Source**: MDX files in `/docs/` directory (version-controlled in Git)
- **Generated Artifacts**: Static HTML in `/build/` directory (not version-controlled)

**Configuration:**
- **Source**: `docusaurus.config.ts`, `sidebars.ts`, `package.json` (version-controlled)

**Assets:**
- **Source**: Images, fonts in `/static/` directory (version-controlled)

---

### 5.2 Schema Evolution

**Frontmatter Schema Changes:**
- **Process**:
  1. Update schema documentation in this plan
  2. Add new fields to frontmatter template
  3. Update existing MDX files (manual or scripted)
  4. Test build

**_category_.json Schema Changes:**
- **Process**:
  1. Update schema documentation
  2. Update all `_category_.json` files
  3. Test sidebar rendering

**Backward Compatibility:**
- New fields: Always optional with sensible defaults
- Deprecated fields: Warn in build logs, continue to work for 1 minor version

---

### 5.3 Migration and Rollback

**Content Migration:**
- **Scenario**: Migrating from different static site generator
- **Process**: Not applicable (new site, no existing content)

**Rollback Strategy:**
- **Git-based**: Revert to previous commit if deployment breaks
- **Process**:
  1. Identify broken deployment
  2. `git revert <commit>` or `git reset --hard <previous-commit>`
  3. Rebuild and redeploy
  4. Investigate issue in separate branch

**Deployment Rollback:**
- GitHub Pages: Redeploy previous `gh-pages` branch commit
- Process:
  1. Checkout `gh-pages` branch
  2. `git reset --hard <previous-commit>`
  3. `git push --force`

---

### 5.4 Data Retention

**Build Artifacts:**
- Local builds (`/build/`): Not retained (regenerated on each build)
- GitHub Pages builds: Retained in `gh-pages` branch (Git history)

**Logs:**
- Build logs: Retained in CI/CD system (GitHub Actions: 90 days default)
- Access logs: Not applicable (GitHub Pages does not provide access logs)

---

## 6. Operational Readiness

### 6.1 Observability

**Build Monitoring:**
- **Logs**: `npm run build` output (stdout/stderr)
- **Metrics**: Build duration, file count, bundle sizes
- **Tool**: GitHub Actions logs (for CI/CD builds)

**Runtime Monitoring:**
- **Not Applicable**: Static site (no server-side runtime)
- **Client-Side Errors**: Can add Sentry or LogRocket (future enhancement)

**Synthetic Monitoring:**
- Use Lighthouse CI to track performance metrics over time (future enhancement)

---

### 6.2 Alerting

**Build Failures:**
- **Trigger**: `npm run build` exits with non-zero code
- **Notification**: GitHub Actions sends email/Slack notification (configurable)
- **Action**: Review build logs, fix errors, redeploy

**Deployment Failures:**
- **Trigger**: GitHub Pages deployment fails
- **Notification**: GitHub Actions notification
- **Action**: Check GitHub Pages settings, verify `gh-pages` branch

**Performance Degradation:**
- **Manual Monitoring**: Run Lighthouse audits periodically
- **Future**: Set up Lighthouse CI to alert on performance regression

---

### 6.3 Runbooks

#### Runbook: Build Failure

**Symptoms**: `npm run build` fails with error.

**Steps:**
1. Check build logs for error message
2. Common errors:
   - **Broken link**: Fix link in MDX file
   - **Missing image**: Add image to `/static/img/` or fix path
   - **Malformed frontmatter**: Fix YAML syntax in MDX file
   - **TypeScript error**: Fix type error in custom component
3. Run `npm run build` locally to reproduce
4. Fix error and commit
5. Redeploy

---

#### Runbook: Deployment Failure

**Symptoms**: GitHub Actions workflow succeeds, but site not updated.

**Steps:**
1. Check GitHub Pages settings: Source should be `gh-pages` branch
2. Verify `gh-pages` branch has new commit
3. Check `docusaurus.config.ts`: Verify `baseUrl` matches repository name
4. Wait 1-2 minutes for GitHub Pages to rebuild (caching delay)
5. Hard refresh browser (Ctrl+Shift+R) to bypass cache
6. If still failing, redeploy manually: `npm run deploy`

---

#### Runbook: Performance Regression

**Symptoms**: Lighthouse score drops below 90.

**Steps:**
1. Run Lighthouse audit to identify issue (Performance, Accessibility, etc.)
2. Common issues:
   - **Large images**: Optimize images (WebP, compression)
   - **Large JavaScript bundle**: Review custom components, remove unused code
   - **Blocking resources**: Use async/defer for non-critical scripts
3. Fix issue and rebuild
4. Re-run Lighthouse to verify improvement

---

### 6.4 Deployment

**Deployment Strategy:**
- **Type**: Blue-Green (GitHub Pages switches atomically to new build)
- **Frequency**: On-demand (manual trigger) or automatic (on push to `main`)

**Deployment Pipeline (GitHub Actions):**
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm ci
      - run: npm run build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build
```

**Rollback:**
- Revert commit in `main` branch and redeploy
- Or manually reset `gh-pages` branch to previous commit

---

### 6.5 Feature Flags

**Not Required**: Static site with no conditional features.

**Future Consideration**:
- Use environment variables to toggle features (e.g., `ENABLE_AI_TOOLS=true`)
- Inject at build time via `docusaurus.config.ts`

---

### 6.6 Backward Compatibility

**Docusaurus Version Compatibility:**
- Lock Docusaurus to `3.9.2` in `package.json`
- Test upgrades in separate branch before merging
- Review Docusaurus changelog for breaking changes

**Theme Override Compatibility:**
- Swizzled components may break on Docusaurus upgrades
- Test theme overrides after every upgrade
- Re-swizzle if necessary

**URL Stability:**
- Maintain stable URLs: `/docs/part-X/chapter-Y/lesson-Z`
- Avoid renaming files (breaks external links)
- If renaming, add redirects (Docusaurus plugin: `@docusaurus/plugin-client-redirects`)

---

## 7. Risk Analysis and Mitigation

### 7.1 Top Risks

#### Risk 1: Theme Override Breaks on Docusaurus Upgrade

**Impact**: HIGH
- Custom layout (`/src/theme/DocItem/`) may break on major Docusaurus upgrades
- Site may fail to build or render incorrectly

**Likelihood**: MEDIUM
- Docusaurus 3.x is stable, but breaking changes possible in 4.x

**Blast Radius**: All documentation pages (entire site)

**Mitigation:**
- **Preventive**: Pin Docusaurus to `3.9.2` in `package.json` (exact version)
- **Detective**: Test upgrades in separate branch before merging
- **Corrective**: Re-swizzle theme components if breakage occurs
- **Guardrails**: Version control allows rollback to previous commit

**Kill Switch**: Revert to previous commit if upgrade breaks site

---

#### Risk 2: Large Book Content Slows Build Time

**Impact**: MEDIUM
- Build time exceeds 60-second target as book grows (100+ pages)
- Slows down deployment pipeline

**Likelihood**: MEDIUM
- Likely if book reaches 100+ pages with large images

**Blast Radius**: CI/CD pipeline (delays deployments)

**Mitigation:**
- **Preventive**: Optimize images (WebP, compression, < 200KB each)
- **Preventive**: Use lazy-loading for images
- **Detective**: Monitor build times in GitHub Actions
- **Corrective**: Implement incremental builds (Docusaurus caching)
- **Guardrails**: Set CI timeout to 5 minutes (fail fast if stuck)

**Kill Switch**: Split book into multiple deployments (e.g., Part 1, Part 2) if necessary

---

#### Risk 3: Broken Links Accumulate as Content Grows

**Impact**: MEDIUM
- Internal links break as content is reorganized
- Degrades user experience

**Likelihood**: MEDIUM
- Likely as content evolves and files are renamed

**Blast Radius**: Affected pages (localized)

**Mitigation:**
- **Preventive**: Use Docusaurus link checking (enabled by default)
- **Preventive**: Prefer relative links over absolute paths
- **Detective**: Build fails on broken links (Docusaurus `onBrokenLinks: 'throw'`)
- **Corrective**: Fix links during build failure
- **Guardrails**: Pre-commit hook to validate links (future enhancement)

**Kill Switch**: Temporarily set `onBrokenLinks: 'warn'` to deploy despite warnings

---

### 7.2 Risk Matrix

| Risk | Impact | Likelihood | Priority | Mitigation Status |
|------|--------|------------|----------|-------------------|
| Theme override breaks on upgrade | HIGH | MEDIUM | 1 | Pinned version, test upgrades in branch |
| Build time exceeds 60s | MEDIUM | MEDIUM | 2 | Optimize images, monitor build times |
| Broken links accumulate | MEDIUM | MEDIUM | 3 | Docusaurus link checking enabled |

---

## 8. Evaluation and Validation

### 8.1 Definition of Done

**Checklist:**
- [ ] Docusaurus 3.9.2 installed with TypeScript and React 18
- [ ] Homepage implemented with Header, Hero, TagBlock components
- [ ] Dark mode enabled by default in configuration
- [ ] Three-column book layout (sidebar, content, TOC) rendering correctly
- [ ] Custom theme override in `/src/theme/DocItem/` injecting breadcrumbs
- [ ] Placeholder MDX files for Parts, Chapters, Lessons (at least 1 part, 2 chapters, 6 lessons)
- [ ] Sidebar auto-generated from folder structure
- [ ] Right-side TOC auto-generated from H2/H3 headings
- [ ] Responsive layout tested on mobile (375px), tablet (768px), desktop (1024px+)
- [ ] All pages build successfully (`npm run build` completes)
- [ ] Lighthouse Performance score > 90
- [ ] Lighthouse Accessibility score > 90
- [ ] Deployed to GitHub Pages and accessible at public URL
- [ ] No broken links (Docusaurus link checker passes)
- [ ] No console errors in browser DevTools
- [ ] TypeScript compiles without errors (`tsc --noEmit`)
- [ ] All custom components tested and rendering correctly

---

### 8.2 Test Plan

#### 8.2.1 Unit Tests

**Not Required**: Static site with minimal custom logic.

**Future**: Add Jest tests for complex custom components (if needed).

---

#### 8.2.2 Build Tests

**Objective**: Verify site builds successfully.

**Tests:**
1. `npm install` completes without errors
2. `npm run build` completes without errors
3. `/build/` directory contains static HTML files
4. All MDX files compiled to HTML
5. No broken links reported
6. No TypeScript errors

**Automation**: Run in GitHub Actions on every commit.

---

#### 8.2.3 Visual Regression Tests

**Objective**: Verify layout and styling across pages and devices.

**Manual Tests:**
1. Homepage:
   - [ ] Header displays with title and GitHub link
   - [ ] Hero section centered with cover, title, subtitle, CTA
   - [ ] TagBlock displays tags horizontally
   - [ ] Responsive: Mobile stacks vertically
2. Documentation pages:
   - [ ] Sidebar displays on left with Parts, Chapters, Lessons
   - [ ] Content displays in center (max-width 900px)
   - [ ] TOC displays on right with H2/H3 headings
   - [ ] Breadcrumbs display at top (Part > Chapter > Lesson)
   - [ ] Active page highlighted in sidebar
   - [ ] Responsive: Mobile collapses sidebar, hides TOC
3. Navigation:
   - [ ] Clicking sidebar item navigates to page
   - [ ] Clicking TOC item scrolls to section
   - [ ] Clicking breadcrumb navigates to parent
   - [ ] Clicking CTA button navigates to `/docs/preface`

**Tools**: Manual testing in Chrome, Firefox, Safari (desktop + mobile).

**Future**: Automate with Percy or Chromatic (visual regression testing).

---

#### 8.2.4 Performance Tests

**Objective**: Verify site meets performance targets.

**Tests:**
1. Run Lighthouse audit on homepage:
   - [ ] Performance score > 90
   - [ ] First Contentful Paint < 1.5s
   - [ ] Time to Interactive < 3s
2. Run Lighthouse audit on documentation page:
   - [ ] Performance score > 90
   - [ ] Total page size < 500KB
3. Measure build time:
   - [ ] `npm run build` completes in < 60s (for ~50 pages)

**Automation**: Lighthouse CI (future enhancement).

---

#### 8.2.5 Accessibility Tests

**Objective**: Verify site is accessible to all users.

**Tests:**
1. Run Lighthouse accessibility audit:
   - [ ] Accessibility score > 90
2. Manual keyboard navigation:
   - [ ] Tab through all interactive elements (links, buttons)
   - [ ] Focus indicators visible
   - [ ] Enter key activates links/buttons
3. Screen reader testing (NVDA or VoiceOver):
   - [ ] Page title announced correctly
   - [ ] Headings announced in order
   - [ ] Links have descriptive text
4. Color contrast:
   - [ ] Body text: 4.5:1 ratio
   - [ ] Large text: 3:1 ratio

**Tools**: Lighthouse, axe DevTools, NVDA/VoiceOver.

---

#### 8.2.6 Cross-Browser Tests

**Objective**: Verify site works on all supported browsers.

**Browsers:**
- Chrome 90+ (desktop + mobile)
- Firefox 88+ (desktop)
- Safari 14+ (desktop + mobile)
- Edge 90+ (desktop)

**Tests:**
1. Homepage renders correctly
2. Documentation page renders correctly
3. Sidebar and TOC functional
4. No JavaScript errors in console

**Tools**: BrowserStack or manual testing.

---

### 8.3 Acceptance Criteria

**User Acceptance:**
- [ ] User can navigate to homepage and see hero section
- [ ] User can click "Start Reading" and navigate to `/docs/preface`
- [ ] User can browse chapters from sidebar
- [ ] User can click lesson in sidebar and read content
- [ ] User can click TOC heading and jump to section
- [ ] User can toggle dark/light mode
- [ ] User can access site on mobile without horizontal scrolling

**Technical Acceptance:**
- [ ] All functional requirements (FR-1 to FR-9) met
- [ ] All non-functional requirements (NFRs) met
- [ ] All tests pass (build, visual, performance, accessibility)
- [ ] Deployed to GitHub Pages successfully

---

## 9. Implementation Roadmap

### Phase 1: Project Setup (Days 1-2)

**Tasks:**
1. Initialize Docusaurus 3.9.2 project with TypeScript
   - Run: `npx create-docusaurus@3.9.2 . classic --typescript`
   - Verify: `npm run start` launches dev server
2. Configure Git repository and commit initial structure
   - Initialize Git: `git init`
   - Add `.gitignore` for `node_modules/`, `build/`, `.docusaurus/`
   - Commit: "Initial Docusaurus setup"
3. Configure `docusaurus.config.ts`
   - Set title, tagline, URL, baseUrl
   - Enable dark mode: `colorMode.defaultMode: 'dark'`
   - Configure navbar: title, GitHub link
   - Remove unnecessary footer sections
4. Configure `package.json`
   - Lock Docusaurus version to `3.9.2`
   - Add deployment scripts (if using `gh-pages`)
5. Test build: `npm run build`
   - Verify: `/build/` directory created
   - Verify: No errors

**Acceptance:**
- [ ] Docusaurus installed and configured
- [ ] Dark mode enabled by default
- [ ] Dev server runs successfully
- [ ] Build completes successfully

---

### Phase 2: Homepage Implementation (Days 3-4)

**Tasks:**
1. Create `Header` component
   - File: `/src/components/Header.tsx`
   - Implement: Dark background, sticky position, title + GitHub link
   - Test: Renders on homepage and doc pages
2. Create `HomepageHero` component
   - File: `/src/components/HomepageHero.tsx`
   - Implement: Cover image, title, subtitle, CTA button
   - Add placeholder book cover image to `/static/img/book-cover.png`
   - Test: Centered layout, responsive on mobile
3. Create `TagBlock` component
   - File: `/src/components/TagBlock.tsx`
   - Implement: Horizontal tag list, rounded borders
   - Test: Displays "Open Source" and "Embodied Intelligence" tags
4. Update homepage (`/src/pages/index.tsx`)
   - Import and compose: Header, HomepageHero, TagBlock
   - Remove default Docusaurus homepage content
   - Test: Homepage renders correctly
5. Add custom CSS
   - File: `/src/css/custom.css`
   - Customize colors, fonts, hero styling
   - Test: Dark theme applied correctly

**Acceptance:**
- [ ] Homepage displays Header, Hero, and TagBlock
- [ ] "Start Reading" button links to `/docs/preface`
- [ ] Responsive layout on mobile
- [ ] Dark theme applied

---

### Phase 3: Documentation Structure (Days 5-7)

**Tasks:**
1. Create folder structure
   - Create: `/docs/preface.md` (landing page)
   - Create: `/docs/part-1-foundations/`
   - Create: `/docs/part-1-foundations/chapter-1-introduction/`
   - Create: `/docs/part-1-foundations/chapter-1-introduction/lesson-1-what-is-physical-ai.md`
   - Repeat for at least 1 part, 2 chapters, 6 lessons (placeholder content)
2. Add `_category_.json` files
   - Add to each part and chapter folder
   - Set labels, positions, descriptions
3. Add frontmatter to lesson MDX files
   - Add: `id`, `title`, `sidebar_label`, `sidebar_position`, `description`
   - Add placeholder content with H2/H3 headings (for TOC testing)
4. Configure `sidebars.ts`
   - Set: `type: 'autogenerated'`
   - Test: Sidebar reflects folder structure
5. Test navigation
   - Verify: Sidebar displays Parts, Chapters, Lessons
   - Verify: Clicking lesson navigates to page
   - Verify: Active page highlighted

**Acceptance:**
- [ ] Folder structure created with placeholder content
- [ ] Sidebar auto-generated and displays correctly
- [ ] All lesson pages accessible via sidebar
- [ ] Breadcrumbs display Part > Chapter > Lesson

---

### Phase 4: Custom Layout and Theme Override (Days 8-10)

**Tasks:**
1. Swizzle `DocItem/Layout` component
   - Run: `npm run swizzle @docusaurus/theme-classic DocItem/Layout -- --wrap`
   - File created: `/src/theme/DocItem/Layout/index.tsx`
2. Inject breadcrumbs into doc layout
   - Add breadcrumb component at top of doc content
   - Test: Breadcrumbs display Part > Chapter > Lesson
3. Create `BookLayout` component
   - File: `/src/components/BookLayout.tsx`
   - Implement: Three-column layout (sidebar, content, TOC)
   - Test: Layout renders correctly on desktop
4. Create `AITools` component (placeholder)
   - File: `/src/components/AITools.tsx`
   - Implement: Button with "Ask AI Assistant" text
   - Position: Top-right of doc page
   - Test: Button displays but does nothing (placeholder)
5. Integrate `BookLayout` and `AITools` into `DocItem/Layout`
   - Wrap doc content with `BookLayout`
   - Inject `AITools` button
   - Test: Three-column layout + AI button on all doc pages
6. Test responsive behavior
   - Mobile: Sidebar collapses, TOC hidden
   - Tablet: Sidebar toggleable, TOC hidden or toggleable
   - Desktop: Full three-column layout

**Acceptance:**
- [ ] Three-column layout renders on desktop
- [ ] Breadcrumbs display at top of doc pages
- [ ] AI Tools button displays (placeholder)
- [ ] Responsive: Sidebar/TOC collapse on mobile

---

### Phase 5: Styling and Polish (Days 11-12)

**Tasks:**
1. Customize colors and fonts
   - Update: `/src/css/custom.css`
   - Set: Primary/secondary colors, font family, sizes
   - Test: Consistent branding across pages
2. Optimize book cover image
   - Convert to WebP format
   - Compress to < 200KB
   - Test: Image loads quickly
3. Add favicon and logo
   - Add: `/static/img/favicon.ico`
   - Add: `/static/img/logo.svg` (if available)
   - Update: `docusaurus.config.ts` to reference logo
4. Test dark/light mode toggle
   - Verify: Toggle switches themes correctly
   - Verify: Colors readable in both modes
5. Polish typography
   - Adjust: Line height, paragraph spacing, heading sizes
   - Test: Content readable and pleasant to read

**Acceptance:**
- [ ] Custom colors and fonts applied
- [ ] Book cover optimized and loads quickly
- [ ] Favicon and logo display correctly
- [ ] Dark/light mode toggle works

---

### Phase 6: Testing and Deployment (Days 13-14)

**Tasks:**
1. Run build tests
   - Run: `npm run build`
   - Verify: No errors, `/build/` directory created
2. Run Lighthouse audits
   - Homepage: Performance > 90, Accessibility > 90
   - Doc page: Performance > 90, Accessibility > 90
3. Run accessibility tests
   - Keyboard navigation: Tab through all elements
   - Screen reader: Test with NVDA or VoiceOver
4. Test cross-browser compatibility
   - Chrome, Firefox, Safari, Edge
   - Mobile: Chrome Mobile, Safari Mobile
5. Configure GitHub Pages deployment
   - Update: `docusaurus.config.ts` with correct `baseUrl`
   - Add: `gh-pages` package if deploying via npm script
   - Configure: GitHub repository settings (Pages source)
6. Deploy to GitHub Pages
   - Run: `npm run deploy` or push to `main` branch (if using GitHub Actions)
   - Verify: Site accessible at public URL
7. Final validation
   - Visit live site, test all navigation
   - Verify: No console errors, no broken links

**Acceptance:**
- [ ] All tests pass (build, Lighthouse, accessibility)
- [ ] Site deployed to GitHub Pages successfully
- [ ] Live site accessible and functional

---

## 10. Architecture Decision Records (ADRs)

Based on the three-part test (Impact + Alternatives + Scope), the following decisions are architecturally significant and should be documented as ADRs:

### ADR Suggestions

1. **ADR: Static Site Generator Selection (Docusaurus vs Next.js vs Gatsby)**
   - **Impact**: Long-term framework lock-in, affects development workflow and deployment
   - **Alternatives**: Docusaurus, Next.js, Gatsby, VuePress, custom React SPA
   - **Scope**: Cross-cutting decision affecting entire site architecture

   📋 Architectural decision detected: **Static Site Generator Selection**
   - Document reasoning and tradeoffs? Run `/sp.adr static-site-generator-selection`

2. **ADR: Content Format (MDX vs Markdown vs AsciiDoc)**
   - **Impact**: Affects content authoring, migration, and future interactivity
   - **Alternatives**: MDX, plain Markdown, AsciiDoc, reStructuredText
   - **Scope**: All content files, impacts AI content generation pipeline

   📋 Architectural decision detected: **Content Format Selection**
   - Document reasoning and tradeoffs? Run `/sp.adr content-format-mdx`

3. **ADR: Theme Customization Strategy (Swizzling vs Custom Plugin vs Fork)**
   - **Impact**: Affects maintainability and upgrade path for Docusaurus
   - **Alternatives**: Swizzling, custom plugin, forking Docusaurus, wrapper components
   - **Scope**: Custom layout, breadcrumbs, AI tools integration

   📋 Architectural decision detected: **Theme Customization Strategy**
   - Document reasoning and tradeoffs? Run `/sp.adr theme-customization-swizzling`

4. **ADR: Deployment Platform (GitHub Pages vs Netlify vs Vercel)**
   - **Impact**: Affects hosting costs, deployment pipeline, and infrastructure management
   - **Alternatives**: GitHub Pages, Netlify, Vercel, AWS S3, self-hosted
   - **Scope**: Deployment and CI/CD pipeline

   📋 Architectural decision detected: **Deployment Platform Selection**
   - Document reasoning and tradeoffs? Run `/sp.adr deployment-platform-github-pages`

---

## 11. Open Questions and Assumptions

### 11.1 Open Questions

1. **Book Cover Image**: Do we have a finalized book cover design?
   - **Assumption**: Use placeholder image initially, replace when available
   - **Action**: Create placeholder in `/static/img/book-cover.png`

2. **GitHub Repository URL**: What is the final GitHub repository URL?
   - **Assumption**: `https://github.com/yourusername/physical-ai-humaniod-robotics`
   - **Action**: Update `docusaurus.config.ts` when confirmed

3. **Domain Name**: Will we use a custom domain or GitHub Pages default?
   - **Assumption**: GitHub Pages default initially (`yourusername.github.io/repo-name/`)
   - **Action**: Update `baseUrl` if custom domain is used

4. **Social Links**: Which social platforms to include in footer?
   - **Assumption**: GitHub only initially, expand later if needed
   - **Action**: Add placeholders in footer for Twitter, Discord (optional)

5. **AI Tools Button**: Should the placeholder button be visible or hidden initially?
   - **Assumption**: Visible as placeholder with tooltip "Coming Soon"
   - **Action**: Implement as disabled button with tooltip

---

### 11.2 Assumptions

1. **Content Volume**: Assuming ~10 parts, ~30 chapters, ~90 lessons (3 lessons per chapter)
   - **Implication**: Build time should remain < 60s with optimization

2. **Target Audience**: Technical readers comfortable with code examples and diagrams
   - **Implication**: No need for simplified language or interactive tutorials (initially)

3. **Browser Support**: Modern browsers only (Chrome 90+, Firefox 88+, Safari 14+)
   - **Implication**: Can use modern CSS features (flexbox, grid, CSS variables)

4. **Mobile Usage**: 30-40% of readers on mobile devices
   - **Implication**: Mobile-first design is critical

5. **Deployment Frequency**: Weekly or on-demand (not real-time updates)
   - **Implication**: Manual or GitHub Actions-triggered deployments are sufficient

---

## 12. Success Metrics and KPIs

### 12.1 Development Metrics

- **Time to First Build**: < 1 hour from project init to first successful build
- **Component Development Velocity**: 1-2 custom components per day
- **Theme Override Complexity**: < 100 lines of custom code in swizzled components

---

### 12.2 Technical Metrics

- **Build Time**: < 60 seconds for full site build
- **Lighthouse Performance Score**: > 90 (homepage and doc pages)
- **Lighthouse Accessibility Score**: > 90
- **Bundle Size**: JavaScript < 200KB (gzipped), CSS < 50KB (gzipped)
- **Page Load Time**: < 2 seconds (FCP < 1.5s, TTI < 3s)

---

### 12.3 User Experience Metrics

- **Navigation Success Rate**: 100% (all sidebar links work)
- **Mobile Usability**: No horizontal scrolling on 320px+ screens
- **Accessibility Compliance**: WCAG 2.1 AA (validated via Lighthouse + manual testing)

---

## 13. Appendix

### 13.1 Glossary

- **Docusaurus**: Open-source static site generator optimized for documentation sites
- **MDX**: Markdown with embedded JSX (React components)
- **Swizzling**: Docusaurus term for overriding theme components
- **TOC**: Table of Contents (auto-generated from headings)
- **Sidebar**: Left navigation panel showing Parts, Chapters, Lessons
- **Breadcrumbs**: Navigation trail showing current location (Part > Chapter > Lesson)
- **FCP**: First Contentful Paint (performance metric)
- **TTI**: Time to Interactive (performance metric)
- **WCAG**: Web Content Accessibility Guidelines

---

### 13.2 References

**External Documentation:**
- [Docusaurus 3.9.2 Documentation](https://docusaurus.io/docs)
- [MDX Documentation](https://mdxjs.com/)
- [React 18 Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

**Internal Documentation:**
- Constitution: `.specify/memory/constitution.md`
- Specification: `specs/docusaurus-site-structure/spec.md`
- PHR Template: `.specify/templates/phr-template.prompt.md`

---

### 13.3 Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-28 | Claude Code | Initial plan created |

---

**END OF PLAN**
