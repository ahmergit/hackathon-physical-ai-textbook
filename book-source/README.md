# Book Source - Docusaurus Site

This directory contains the Docusaurus 3.9.2 static site for the **Physical AI & Humanoid Robotics** book.

## Structure

```
book-source/
├── docs/               # Documentation content (MDX files)
├── src/
│   ├── components/     # Custom React components
│   ├── css/            # Custom CSS and theming
│   ├── pages/          # Custom pages (homepage, etc.)
│   └── theme/          # Theme overrides
├── static/             # Static assets (images, files)
├── docusaurus.config.ts  # Main configuration
├── sidebars.ts         # Sidebar configuration
└── package.json        # Dependencies and scripts
```

## Quick Start

### Install Dependencies

```bash
cd book-source
npm install
```

### Development Server

```bash
npm run start
```

Opens the site at `http://localhost:3000` with hot reload.

### Build for Production

```bash
npm run build
```

Generates static files in `build/` directory.

### Serve Production Build Locally

```bash
npm run serve
```

### Deploy to GitHub Pages

```bash
npm run deploy
```

## Features Implemented

✅ **Phase 1-3 Complete:**
- Dark theme optimized for technical documentation
- Responsive homepage with hero section and CTA
- Custom components: Header, HomepageHero, TagBlock
- Auto-generated sidebar navigation
- TypeScript throughout with strict typing

## Tech Stack

- **Docusaurus**: 3.9.2
- **React**: 18.x
- **TypeScript**: 5.2.x
- **Node**: 18+ required

## Development Notes

- All components use TypeScript with strict typing
- CSS Modules for component styling
- Dark mode enabled by default
- Mobile-first responsive design
