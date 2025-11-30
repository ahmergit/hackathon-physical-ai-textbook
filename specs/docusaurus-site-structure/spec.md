# Feature Specification: Docusaurus Site Structure

**Feature Name**: Docusaurus-based Documentation Website Structure
**Version**: 1.0.0
**Status**: Draft
**Created**: 2025-11-28
**Last Updated**: 2025-11-28

---

## 1. Overview

### 1.1 Purpose
Build a complete, production-ready Docusaurus 3.9.2 static site structure with professional navigation, layout, and information architecture—ready to receive AI-generated book content.

### 1.2 Scope

**In Scope:**
- Complete Docusaurus 3.9.2 installation and configuration
- Homepage with hero section, tagline, CTA buttons, and feature blocks
- Documentation sidebar with collapsible chapter/lesson tree navigation
- Main content layout with centered content and auto-generated right-side TOC
- Global navbar with links to Home, Docs, GitHub, and placeholder sections
- Footer with three columns: About, Resources, and Social links
- Responsive layout (mobile-first design for 320px+ screens)
- Automatic page routing based on folder structure
- Information architecture: `chapters → lessons → subpages` maps to folder hierarchy
- TypeScript configuration for site customization
- Build pipeline and static asset generation

**Out of Scope:**
- Actual book content generation (handled in future features)
- RAG assistant integration (separate feature)
- Custom search functionality (use Docusaurus defaults)
- Advanced theming beyond clean, professional defaults
- Backend services or APIs
- Analytics or tracking (can be added later)
- Custom MDX components beyond Docusaurus defaults

### 1.3 Dependencies

**External Dependencies:**
- Node.js 18+ (LTS version)
- npm or yarn package manager
- Docusaurus 3.9.2
- React 18+
- TypeScript 5.x

**Internal Dependencies:**
- Project constitution (`.specify/memory/constitution.md`)
- Git repository for version control
- GitHub repository for deployment target (GitHub Pages)

---

## 2. Requirements

### 2.1 Functional Requirements

#### FR-1: Docusaurus Installation & Configuration
**Priority**: CRITICAL
**Description**: Install Docusaurus 3.9.2 with TypeScript support and configure for static site generation.

**Acceptance Criteria:**
- [ ] Docusaurus 3.9.2 installed via npm/yarn
- [ ] TypeScript enabled and configured (tsconfig.json)
- [ ] `docusaurus.config.ts` created with project metadata
- [ ] Project builds successfully: `npm run build` completes without errors
- [ ] Development server runs: `npm run start` launches on localhost
- [ ] Static output generated in `build/` directory
- [ ] All dependencies locked in `package-lock.json` or `yarn.lock`

**Inputs:**
- Project name, tagline, GitHub repository URL
- Base URL and deployment path (e.g., `/` for root or `/docs/` for subpath)

**Outputs:**
- Fully configured Docusaurus project
- `package.json` with all dependencies
- `docusaurus.config.ts` with site metadata

---

#### FR-2: Homepage with Hero Section
**Priority**: HIGH
**Description**: Create a visually clean homepage with hero section, tagline, CTA buttons, and feature highlights.

**Acceptance Criteria:**
- [ ] Homepage displays project name and tagline prominently
- [ ] Hero section includes 1-2 CTA buttons (e.g., "Get Started", "View on GitHub")
- [ ] Feature blocks section highlights 3-4 key features (icons + text)
- [ ] Layout is centered and responsive
- [ ] No placeholder or "lorem ipsum" text
- [ ] Hero background color or gradient matches brand (configurable)
- [ ] All buttons link to correct pages (Docs intro, GitHub repo)

**Inputs:**
- Project name, tagline, description
- Feature highlights (titles and brief descriptions)
- CTA button labels and links

**Outputs:**
- `src/pages/index.tsx` or `src/pages/index.md`
- Custom CSS modules if needed for hero styling

---

#### FR-3: Documentation Sidebar Navigation
**Priority**: CRITICAL
**Description**: Configure a collapsible sidebar that reflects the folder hierarchy: chapters → lessons → subpages.

**Acceptance Criteria:**
- [ ] Sidebar automatically generated from `docs/` folder structure
- [ ] Chapters display as top-level collapsible categories
- [ ] Lessons display as second-level items under chapters
- [ ] Subpages (if any) display as third-level nested items
- [ ] Active page highlighted in sidebar
- [ ] Sidebar collapses on mobile, accessible via hamburger menu
- [ ] Sidebar order respects folder naming or `_category_.json` files
- [ ] No manual sidebar config required (auto-generated preferred)

**Inputs:**
- `docs/` folder structure with chapters as subdirectories
- Optional `_category_.json` files for custom labels and ordering

**Outputs:**
- `sidebars.ts` configuration (auto-generated or manual)
- `docs/` folder structure convention documented

**Example Structure:**
```
docs/
  intro.md
  chapter-01-basics/
    _category_.json
    lesson-01-introduction.md
    lesson-02-setup.md
  chapter-02-advanced/
    _category_.json
    lesson-01-concepts.md
    lesson-02-examples.md
```

---

#### FR-4: Main Content Layout with Auto-Generated TOC
**Priority**: HIGH
**Description**: Display main content in the center with auto-generated table of contents (TOC) on the right.

**Acceptance Criteria:**
- [ ] Main content area centered with appropriate max-width (e.g., 900px)
- [ ] Right-side TOC auto-generated from heading tags (h2, h3)
- [ ] TOC scrolls with page and highlights current section
- [ ] TOC collapses on tablets and mobile (hamburger or hidden)
- [ ] Markdown headings (`##`, `###`) map correctly to TOC entries
- [ ] TOC is visible on all documentation pages
- [ ] No manual TOC configuration required

**Inputs:**
- Markdown content with heading structure

**Outputs:**
- Docusaurus theme configuration (`themeConfig` in `docusaurus.config.ts`)
- CSS overrides if needed for TOC styling

---

#### FR-5: Global Navbar
**Priority**: HIGH
**Description**: Create a global navbar with links to Home, Docs, GitHub, and placeholder sections.

**Acceptance Criteria:**
- [ ] Navbar displays project logo/name on left
- [ ] Navbar includes links: Home, Docs, GitHub
- [ ] Navbar includes placeholders for future sections (e.g., Blog, Community)
- [ ] Navbar is sticky (remains visible on scroll)
- [ ] Navbar collapses to hamburger menu on mobile
- [ ] Active page highlighted in navbar
- [ ] GitHub link opens in new tab with icon

**Inputs:**
- Project name/logo
- Navigation links and labels
- GitHub repository URL

**Outputs:**
- `navbar` configuration in `docusaurus.config.ts`
- Optional logo file in `static/img/`

---

#### FR-6: Footer with Three Columns
**Priority**: MEDIUM
**Description**: Create a footer with three columns: About, Resources, and Social links.

**Acceptance Criteria:**
- [ ] Footer displayed on all pages
- [ ] Three columns: About, Resources, Social
- [ ] About column includes project description or tagline
- [ ] Resources column includes links (e.g., Docs, GitHub, Contributing)
- [ ] Social column includes icons for GitHub, Twitter, Discord (or placeholders)
- [ ] Footer is responsive: stacks vertically on mobile
- [ ] Footer background color distinct from main content
- [ ] All links functional or clearly marked as placeholders

**Inputs:**
- Project description
- Resource links (Docs, GitHub, etc.)
- Social media URLs (or placeholders)

**Outputs:**
- `footer` configuration in `docusaurus.config.ts`
- Social media icons (using Docusaurus defaults or custom)

---

#### FR-7: Responsive Layout
**Priority**: CRITICAL
**Description**: Ensure all pages and components are fully responsive and work on desktop, tablet, and mobile.

**Acceptance Criteria:**
- [ ] Mobile-first design: works on 320px+ screens
- [ ] Breakpoints for tablet (768px) and desktop (1024px)
- [ ] Sidebar collapses to hamburger on mobile
- [ ] TOC hidden or collapsible on mobile
- [ ] Hero section and feature blocks stack vertically on mobile
- [ ] Navbar collapses to hamburger on mobile
- [ ] Footer columns stack vertically on mobile
- [ ] No horizontal scrolling on any device
- [ ] Touch-friendly buttons and links (minimum 44px tap targets)
- [ ] Tested on Chrome, Firefox, Safari (mobile and desktop)

**Inputs:**
- Device sizes: mobile (320px-767px), tablet (768px-1023px), desktop (1024px+)

**Outputs:**
- Custom CSS modules or Docusaurus theme overrides
- Responsive testing checklist

---

#### FR-8: Automatic Page Routing
**Priority**: CRITICAL
**Description**: Automatic page routing based on folder structure, no manual route configuration required.

**Acceptance Criteria:**
- [ ] All `.md` and `.mdx` files in `docs/` automatically routed
- [ ] URL structure mirrors folder structure (e.g., `/docs/chapter-01/lesson-01`)
- [ ] `intro.md` serves as landing page for `/docs/`
- [ ] Folder names converted to URL slugs (lowercase, hyphens)
- [ ] Frontmatter `slug` overrides supported if needed
- [ ] 404 page displays for missing routes
- [ ] All routes work in both dev (`npm run start`) and prod (`npm run build`)

**Inputs:**
- `docs/` folder structure
- Optional frontmatter `slug` fields

**Outputs:**
- Docusaurus routing configuration (default behavior)
- Documentation of folder-to-URL mapping

---

#### FR-9: Clean Information Architecture
**Priority**: HIGH
**Description**: Establish folder and file naming conventions that map directly to book structure: chapters → lessons → subpages.

**Acceptance Criteria:**
- [ ] Folder naming convention documented (e.g., `chapter-##-name/`)
- [ ] File naming convention documented (e.g., `lesson-##-name.md`)
- [ ] `_category_.json` files define chapter metadata (label, position, description)
- [ ] Each chapter folder contains lessons as markdown files
- [ ] Subpages nested under lessons if needed (e.g., `lesson-01/subsection.md`)
- [ ] No orphaned files (all files belong to a chapter)
- [ ] README or docs guide explains structure for content creators

**Inputs:**
- Book structure outline (chapters and lessons)

**Outputs:**
- `docs/` folder structure convention
- `CONTRIBUTING.md` or `docs/README.md` with structure guide

**Example Convention:**
```
docs/
  intro.md                           # Landing page for /docs/
  chapter-01-getting-started/
    _category_.json                  # { label: "Getting Started", position: 1 }
    lesson-01-introduction.md
    lesson-02-installation.md
  chapter-02-core-concepts/
    _category_.json                  # { label: "Core Concepts", position: 2 }
    lesson-01-fundamentals.md
    lesson-02-architecture.md
```

---

### 2.2 Non-Functional Requirements

#### NFR-1: Performance
- Static site build time < 60 seconds (for typical book size: ~50 pages)
- Page load time < 2 seconds (Lighthouse Performance score > 90)
- First Contentful Paint (FCP) < 1.5 seconds
- Time to Interactive (TTI) < 3 seconds
- Minimal JavaScript bundle size (use code splitting)

#### NFR-2: Accessibility
- WCAG 2.1 Level AA compliance
- Semantic HTML5 structure
- Keyboard navigation support (tab through links, sidebar, TOC)
- Screen reader friendly (proper ARIA labels)
- Sufficient color contrast (4.5:1 for body text, 3:1 for large text)
- Alt text for all images

#### NFR-3: Browser Compatibility
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile Safari (iOS 14+)
- Chrome Mobile (Android 10+)

#### NFR-4: Maintainability
- TypeScript for all configuration files
- Clear folder structure with README documentation
- Docusaurus version locked in `package.json`
- All customizations documented in comments
- No hard-coded values (use config variables)

#### NFR-5: Deployment Readiness
- Static build output suitable for GitHub Pages, Netlify, Vercel
- Base URL configurable for subpath or root deployment
- No runtime dependencies (purely static HTML/CSS/JS)
- Asset optimization (images, fonts) via Docusaurus defaults
- SEO meta tags configured (title, description, Open Graph)

---

## 3. User Stories

### US-1: Reader Browses Chapters
**As a** reader
**I want to** browse chapters from the left sidebar
**So that** I can quickly navigate to the content I need

**Acceptance:**
- Sidebar displays all chapters in order
- Clicking a chapter expands lessons
- Active page is highlighted

---

### US-2: Reader Views Lesson Content
**As a** reader
**I want to** read a lesson with auto-generated headings navigation
**So that** I can jump to specific sections within the lesson

**Acceptance:**
- Lesson content displays in center
- Right-side TOC shows all headings
- Clicking TOC link scrolls to section

---

### US-3: Reader Discovers Project on Homepage
**As a** new visitor
**I want to** see a clear tagline and call-to-action on the homepage
**So that** I understand what the project offers and how to get started

**Acceptance:**
- Homepage displays project name and tagline
- CTA buttons link to Docs and GitHub
- Feature highlights explain key benefits

---

### US-4: Mobile Reader Navigates Easily
**As a** mobile user
**I want to** access navigation via hamburger menu
**So that** I can browse content on my phone without layout issues

**Acceptance:**
- Navbar collapses to hamburger on mobile
- Sidebar accessible via menu button
- Content readable without horizontal scrolling

---

### US-5: Content Creator Adds New Chapter
**As a** content creator
**I want to** add a new chapter by creating a folder and markdown files
**So that** the sidebar and routing update automatically

**Acceptance:**
- Create folder `docs/chapter-03-name/`
- Add `_category_.json` with metadata
- Add lesson markdown files
- Sidebar reflects new chapter without config changes

---

## 4. Technical Specification

### 4.1 Technology Stack

**Static Site Generator:**
- Docusaurus 3.9.2

**Frontend:**
- React 18+ (provided by Docusaurus)
- TypeScript 5.x
- CSS Modules for custom styling

**Build Tools:**
- Node.js 18+ (LTS)
- npm or yarn
- Webpack (bundled with Docusaurus)

**Deployment:**
- Static HTML/CSS/JS output
- Suitable for GitHub Pages, Netlify, Vercel, or any static host

---

### 4.2 Project Structure

```
physical-ai-humanoid-robotics/
├── .specify/                      # Spec-Driven Development files
│   ├── memory/
│   │   └── constitution.md
│   └── templates/
├── docs/                          # Documentation content
│   ├── intro.md                   # Landing page for /docs/
│   ├── chapter-01-*/              # Chapter folders
│   │   ├── _category_.json
│   │   └── lesson-*.md
│   └── chapter-02-*/
├── src/                           # Custom components and pages
│   ├── components/                # Reusable React components
│   ├── css/                       # Custom CSS modules
│   └── pages/                     # Custom pages (homepage, etc.)
│       └── index.tsx              # Homepage
├── static/                        # Static assets
│   ├── img/                       # Images, logos, icons
│   └── files/                     # Downloadable files
├── docusaurus.config.ts           # Main configuration
├── sidebars.ts                    # Sidebar configuration
├── tsconfig.json                  # TypeScript configuration
├── package.json                   # Dependencies
└── README.md                      # Project documentation
```

---

### 4.3 Configuration Files

#### 4.3.1 docusaurus.config.ts
**Purpose**: Main configuration for site metadata, navbar, footer, theme.

**Key Sections:**
- `title`: Project name
- `tagline`: Short description
- `url`: Production URL
- `baseUrl`: Base path (e.g., `/` or `/docs/`)
- `organizationName`: GitHub username/org
- `projectName`: GitHub repository name
- `themeConfig`:
  - `navbar`: Logo, links, GitHub button
  - `footer`: Columns with About, Resources, Social links
  - `colorMode`: Dark/light theme toggle
  - `prism`: Syntax highlighting themes
- `presets`: Docusaurus classic preset with docs and pages plugins

**Example:**
```typescript
import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Physical AI Humanoid Robotics',
  tagline: 'Learn humanoid robotics from fundamentals to advanced applications',
  favicon: 'img/favicon.ico',

  url: 'https://yourusername.github.io',
  baseUrl: '/physical-ai-humaniod-robotics/',

  organizationName: 'yourusername',
  projectName: 'physical-ai-humaniod-robotics',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/yourusername/physical-ai-humaniod-robotics/tree/main/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'Physical AI Robotics',
      logo: {
        alt: 'Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Docs',
        },
        {
          href: 'https://github.com/yourusername/physical-ai-humaniod-robotics',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'About',
          items: [
            {
              label: 'Introduction',
              to: '/docs/intro',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'Documentation',
              to: '/docs/intro',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/yourusername/physical-ai-humaniod-robotics',
            },
          ],
        },
        {
          title: 'Social',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/yourusername/physical-ai-humaniod-robotics',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI Robotics. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
```

---

#### 4.3.2 sidebars.ts
**Purpose**: Configure sidebar navigation (auto-generated or manual).

**Strategy**: Use auto-generated sidebars from folder structure.

**Example:**
```typescript
import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'autogenerated',
      dirName: '.',
    },
  ],
};

export default sidebars;
```

**Alternative (Manual):**
```typescript
const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Getting Started',
      items: ['chapter-01/lesson-01', 'chapter-01/lesson-02'],
    },
    {
      type: 'category',
      label: 'Core Concepts',
      items: ['chapter-02/lesson-01', 'chapter-02/lesson-02'],
    },
  ],
};
```

---

#### 4.3.3 _category_.json
**Purpose**: Define metadata for chapter folders.

**Location**: Inside each chapter folder (e.g., `docs/chapter-01-basics/_category_.json`)

**Example:**
```json
{
  "label": "Getting Started",
  "position": 1,
  "link": {
    "type": "generated-index",
    "description": "Learn the basics of humanoid robotics."
  }
}
```

**Fields:**
- `label`: Display name in sidebar
- `position`: Sort order (1, 2, 3, ...)
- `link`: Optional generated index page
- `collapsed`: Boolean to collapse category by default

---

### 4.4 Page Templates

#### 4.4.1 Homepage (src/pages/index.tsx)
**Purpose**: Landing page with hero section and feature highlights.

**Sections:**
1. Hero Section: Title, tagline, CTA buttons
2. Features Section: 3-4 feature blocks with icons and descriptions

**Example Structure:**
```tsx
import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Get Started
          </Link>
        </div>
      </div>
    </header>
  );
}

function HomepageFeatures() {
  const features = [
    {
      title: 'Comprehensive Coverage',
      description: 'From fundamentals to advanced topics in humanoid robotics.',
    },
    {
      title: 'Hands-On Examples',
      description: 'Practical code samples and real-world applications.',
    },
    {
      title: 'AI-Powered Assistance',
      description: 'Ask questions and get instant answers with our RAG assistant.',
    },
  ];

  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {features.map((feature, idx) => (
            <div key={idx} className={clsx('col col--4')}>
              <div className="text--center padding-horiz--md">
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Learn humanoid robotics from fundamentals to advanced applications">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
```

---

#### 4.4.2 Documentation Page Template
**Purpose**: Standard layout for all documentation pages.

**Provided by Docusaurus**: Automatic via `@theme/DocPage`

**Customization**: Override via swizzling if needed (not recommended for initial setup)

**Layout:**
- Left: Sidebar with chapter/lesson navigation
- Center: Main content area
- Right: Auto-generated TOC from headings

---

### 4.5 Styling and Theming

#### 4.5.1 Custom CSS (src/css/custom.css)
**Purpose**: Override Docusaurus default styles for branding.

**Key Customizations:**
- Primary and secondary colors
- Font family and sizes
- Hero section styling
- Feature block layout
- Footer styling

**Example:**
```css
:root {
  --ifm-color-primary: #2e8555;
  --ifm-color-primary-dark: #29784c;
  --ifm-color-primary-darker: #277148;
  --ifm-color-primary-darkest: #205d3b;
  --ifm-color-primary-light: #33925d;
  --ifm-color-primary-lighter: #359962;
  --ifm-color-primary-lightest: #3cad6e;
  --ifm-code-font-size: 95%;
  --ifm-font-family-base: 'Inter', system-ui, -apple-system, sans-serif;
}

.hero--primary {
  background: linear-gradient(135deg, var(--ifm-color-primary) 0%, var(--ifm-color-primary-dark) 100%);
  color: white;
}

.hero__title {
  font-size: 3rem;
  font-weight: 700;
}

.hero__subtitle {
  font-size: 1.5rem;
  margin-top: 1rem;
}
```

---

### 4.6 Routing and Navigation

#### 4.6.1 URL Structure
**Mapping:**
- `/` → Homepage (`src/pages/index.tsx`)
- `/docs/intro` → Introduction page (`docs/intro.md`)
- `/docs/chapter-01-basics/lesson-01` → Lesson 1 in Chapter 1
- `/docs/chapter-01-basics/` → Auto-generated category index

**Convention:**
- Folder names → URL slugs (lowercase, hyphens)
- File names → URL paths (without `.md` extension)
- `intro.md` serves as landing page for `/docs/`

---

#### 4.6.2 Sidebar Navigation Logic
**Auto-Generated:**
- Docusaurus scans `docs/` folder
- Each folder with `_category_.json` becomes a category
- Markdown files become sidebar items
- Order determined by `position` in `_category_.json` or alphabetically

**Manual Override:**
- Define custom sidebar structure in `sidebars.ts`
- Useful for complex hierarchies or custom grouping

---

### 4.7 Build and Deployment

#### 4.7.1 Development Workflow
**Commands:**
- `npm install` — Install dependencies
- `npm run start` — Start dev server (http://localhost:3000)
- `npm run build` — Build static site
- `npm run serve` — Serve built site locally
- `npm run clear` — Clear cache

**Development Server:**
- Hot reload enabled
- TypeScript type checking
- Fast refresh for React components

---

#### 4.7.2 Production Build
**Output:**
- `build/` directory with static HTML/CSS/JS
- Optimized assets (minified, code-split)
- SEO-friendly meta tags

**Deployment Targets:**
- GitHub Pages: `npm run deploy` (with `gh-pages` package)
- Netlify: Drag-and-drop `build/` folder
- Vercel: Connect GitHub repo
- Any static host: Upload `build/` contents

---

#### 4.7.3 GitHub Pages Deployment
**Steps:**
1. Install `gh-pages`: `npm install --save-dev gh-pages`
2. Add deploy script to `package.json`:
   ```json
   "scripts": {
     "deploy": "docusaurus deploy"
   }
   ```
3. Configure `docusaurus.config.ts`:
   ```typescript
   organizationName: 'yourusername',
   projectName: 'physical-ai-humaniod-robotics',
   deploymentBranch: 'gh-pages',
   trailingSlash: false,
   ```
4. Run: `npm run deploy`

---

## 5. Data Model

### 5.1 Content Structure

#### Chapter Metadata (_category_.json)
```json
{
  "label": "string",        // Display name
  "position": "number",     // Sort order
  "link": {
    "type": "generated-index" | "doc",
    "description": "string" // Optional description for index page
  },
  "collapsed": "boolean"    // Collapsed by default
}
```

#### Lesson Frontmatter (lesson-*.md)
```yaml
---
id: lesson-01-introduction         # Unique identifier
title: Introduction to Robotics    # Page title
sidebar_label: Introduction        # Sidebar display name
sidebar_position: 1                # Sort order within category
description: Learn the basics      # Meta description
keywords: [robotics, ai, basics]   # SEO keywords
---
```

---

### 5.2 Folder Naming Convention

**Chapters:**
- Format: `chapter-##-name/`
- Example: `chapter-01-getting-started/`

**Lessons:**
- Format: `lesson-##-name.md`
- Example: `lesson-01-introduction.md`

**Subpages (if needed):**
- Format: `lesson-##-name/subsection.md`
- Example: `lesson-01-introduction/prerequisites.md`

---

## 6. Interface Contracts

### 6.1 Public APIs
**Not Applicable**: This is a static site with no backend APIs.

### 6.2 Internal Interfaces

#### Configuration API (docusaurus.config.ts)
**Input:**
- Site metadata (title, tagline, URLs)
- Navbar items (links, labels)
- Footer columns (links, copyright)
- Theme settings (colors, fonts)

**Output:**
- Configured Docusaurus site

#### Sidebar API (sidebars.ts)
**Input:**
- Sidebar structure (auto-generated or manual)

**Output:**
- Rendered sidebar navigation

---

## 7. Error Handling

### 7.1 Build Errors
**Broken Links:**
- Docusaurus throws error on broken internal links
- Resolution: Fix link or add to ignore list

**Missing Files:**
- Error if referenced file doesn't exist
- Resolution: Create file or remove reference

**Invalid Frontmatter:**
- Error if frontmatter YAML is malformed
- Resolution: Validate YAML syntax

### 7.2 Runtime Errors
**404 Pages:**
- Custom 404 page provided by Docusaurus
- Displays when route not found

**JavaScript Errors:**
- Captured by React error boundaries
- Logged to browser console

---

## 8. Testing Strategy

### 8.1 Build Testing
**Objective**: Ensure site builds successfully without errors.

**Tests:**
- [ ] `npm run build` completes without errors
- [ ] All pages accessible in `build/` directory
- [ ] No broken links reported
- [ ] Assets (images, CSS, JS) load correctly

### 8.2 Visual Testing
**Objective**: Verify layout and styling across devices.

**Tests:**
- [ ] Homepage hero section displays correctly
- [ ] Sidebar navigation works on desktop
- [ ] Sidebar collapses on mobile
- [ ] TOC displays on right side (desktop)
- [ ] Footer displays three columns (desktop)
- [ ] Footer stacks vertically (mobile)

### 8.3 Accessibility Testing
**Objective**: Ensure site is accessible to all users.

**Tools:**
- Lighthouse (Chrome DevTools)
- axe DevTools extension

**Tests:**
- [ ] Lighthouse Accessibility score > 90
- [ ] Keyboard navigation works (Tab, Enter)
- [ ] Screen reader announces page titles
- [ ] Color contrast meets WCAG AA

### 8.4 Performance Testing
**Objective**: Verify site meets performance targets.

**Tools:**
- Lighthouse (Chrome DevTools)
- WebPageTest

**Tests:**
- [ ] Lighthouse Performance score > 90
- [ ] First Contentful Paint (FCP) < 1.5s
- [ ] Time to Interactive (TTI) < 3s
- [ ] Page load time < 2s

---

## 9. Migration and Rollout

### 9.1 Implementation Phases

#### Phase 1: Setup and Configuration
- Install Docusaurus 3.9.2
- Configure `docusaurus.config.ts`
- Set up TypeScript and linting
- Create initial folder structure

#### Phase 2: Homepage and Navigation
- Build homepage with hero and features
- Configure navbar
- Configure footer

#### Phase 3: Documentation Structure
- Set up `docs/` folder structure
- Create `_category_.json` files
- Configure sidebar
- Create placeholder intro page

#### Phase 4: Styling and Theming
- Customize CSS for branding
- Test responsive layout
- Optimize for mobile

#### Phase 5: Build and Deploy
- Run production build
- Test static site locally
- Deploy to GitHub Pages
- Verify live site

---

### 9.2 Rollback Plan
**Issue**: Build fails or site breaks after deployment.

**Steps:**
1. Revert to previous commit in Git
2. Rebuild and redeploy
3. Investigate issue in separate branch

---

## 10. Success Metrics

### 10.1 Functional Metrics
- [ ] Sidebar reflects folder hierarchy (chapters → lessons)
- [ ] Homepage displays hero, tagline, and features
- [ ] Right-side TOC updates based on headings
- [ ] Navbar and footer present on all pages
- [ ] All pages compile and load successfully

### 10.2 Performance Metrics
- [ ] Build time < 60 seconds
- [ ] Page load time < 2 seconds
- [ ] Lighthouse Performance score > 90

### 10.3 Usability Metrics
- [ ] Mobile navigation works smoothly
- [ ] No horizontal scrolling on any device
- [ ] Active page highlighted in sidebar
- [ ] TOC scrolls with page and highlights current section

---

## 11. Risks and Mitigations

### 11.1 Risk: Docusaurus Version Compatibility
**Impact**: Future Docusaurus updates break site.
**Likelihood**: Medium
**Mitigation**: Lock Docusaurus version in `package.json`; test upgrades in separate branch.

### 11.2 Risk: Complex Folder Structure
**Impact**: Auto-generated sidebar doesn't match expected hierarchy.
**Likelihood**: Low
**Mitigation**: Use `_category_.json` files for metadata; manual sidebar fallback.

### 11.3 Risk: Performance Degradation
**Impact**: Large book content slows down build/load times.
**Likelihood**: Medium
**Mitigation**: Monitor build times; use code splitting; optimize images.

### 11.4 Risk: Responsive Layout Issues
**Impact**: Site breaks on certain devices.
**Likelihood**: Low
**Mitigation**: Test on multiple devices/browsers; use Docusaurus responsive defaults.

---

## 12. Open Questions

1. **Branding**: Do we have a logo and color scheme finalized?
   - **Action**: Placeholder logo in `static/img/`; colors in `custom.css` (configurable)

2. **GitHub Repository**: What is the final GitHub URL?
   - **Action**: Update `docusaurus.config.ts` when available

3. **Deployment Path**: Root (`/`) or subpath (`/docs/`)?
   - **Action**: Configure `baseUrl` in `docusaurus.config.ts`

4. **Social Links**: Which social platforms to include in footer?
   - **Action**: GitHub required; Twitter/Discord optional (placeholders for now)

---

## 13. References

### 13.1 External Documentation
- [Docusaurus 3.9.2 Docs](https://docusaurus.io/docs)
- [Docusaurus Configuration](https://docusaurus.io/docs/configuration)
- [Docusaurus Markdown Features](https://docusaurus.io/docs/markdown-features)
- [Docusaurus Deployment](https://docusaurus.io/docs/deployment)

### 13.2 Internal References
- Constitution: `.specify/memory/constitution.md`
- Project README: `README.md`
- PHR template: `.specify/templates/phr-template.prompt.md`

---

## 14. Approval and Sign-Off

**Prepared By**: Claude Code (AI Assistant)
**Date**: 2025-11-28
**Status**: Draft — Awaiting User Approval

**Approval:**
- [ ] User approves specification
- [ ] Ready to proceed to planning phase

---

**END OF SPECIFICATION**
