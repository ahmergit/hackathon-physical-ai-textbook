# Testing & Deployment Guide

This guide covers the remaining manual testing tasks for Phase 9 of the Docusaurus site implementation.

## Completed Automated Tasks ✅

- ✅ T082: Optimized image assets (logo SVG created, placeholders for book-cover and social-card)
- ✅ T083: Added logo file to `static/img/logo.svg`
- ✅ T084: Added comprehensive SEO meta tags (keywords, description, Open Graph, Twitter Card)
- ✅ T087: Full production build successful (`npm run build`)
- ✅ T088: Local serve test successful (`npm run serve`)
- ✅ T096: TypeScript compilation verified (`tsc --noEmit`)
- ✅ T097: GitHub Pages deployment configured (organizationName, projectName, deploymentBranch)

## Manual Testing Tasks (Require Browser)

### T085: Test Dark/Light Mode Toggle

**Steps:**
1. Start dev server: `npm run start` (from `book-source/` directory)
2. Open browser to `http://localhost:3000/physical-ai-humaniod-robotics/`
3. Locate the theme toggle button (moon/sun icon) in the navbar
4. Click toggle to switch between dark and light modes
5. Verify the mode changes persist across page navigations

**Expected:**
- Default mode: Dark
- Toggle switches modes smoothly
- Preference saved in localStorage

---

### T086: Verify Colors are Readable

**Steps:**
1. Test both dark and light modes
2. Check all UI elements:
   - Body text
   - Headings (H1-H6)
   - Links (normal, hover, active states)
   - Buttons (primary, secondary, disabled)
   - Sidebar items (normal, active, hover)
   - Breadcrumbs
   - Tags
   - AI Tools button

**Expected:**
- All text is readable with sufficient contrast
- Active states are clearly distinguishable
- No color-only indicators (accessibility)

---

### T089: Lighthouse Audit - Homepage

**Steps:**
1. Build the site: `npm run build`
2. Serve built site: `npm run serve`
3. Open Chrome DevTools (F12)
4. Navigate to "Lighthouse" tab
5. Select: Performance, Accessibility, Best Practices, SEO
6. Device: Desktop
7. Run audit on `http://localhost:3000/physical-ai-humaniod-robotics/`

**Expected Scores:**
- ✅ Performance: > 90
- ✅ Accessibility: > 90
- ✅ Best Practices: > 80
- ✅ SEO: > 90

**Common Issues & Fixes:**
- Low performance: Check for unoptimized images (book-cover should be WebP < 200KB)
- Accessibility: Verify ARIA labels, color contrast, tap targets (44px minimum)
- SEO: Ensure meta tags present (already added in T084)

---

### T090: Lighthouse Audit - Doc Page

**Steps:**
1. Run same Lighthouse audit on a documentation page
2. Test URL: `http://localhost:3000/physical-ai-humaniod-robotics/docs/intro`

**Expected Scores:**
- Same thresholds as homepage
- Check TOC navigation accessibility
- Verify breadcrumb navigation

---

### T091: Keyboard Navigation

**Steps:**
1. Open site in browser
2. Use only keyboard (Tab, Shift+Tab, Enter, Escape)
3. Test all interactive elements:
   - **Navbar**: Logo, Docs link, GitHub link, theme toggle
   - **Sidebar**: Navigation items, expand/collapse
   - **Main content**: All links
   - **TOC**: Right-side table of contents links
   - **Breadcrumbs**: Part/Chapter/Lesson links
   - **Buttons**: CTA buttons, AI Tools button

**Expected:**
- All elements are reachable via Tab
- Focus indicators are visible (outline or highlight)
- Logical tab order (top-to-bottom, left-to-right)
- Enter key activates links/buttons
- Escape closes mobile menu (if applicable)

---

### T092: Screen Reader Testing

**Tools:**
- **Windows**: NVDA (free, recommended) or Narrator
- **macOS**: VoiceOver (Cmd+F5)
- **Linux**: Orca

**Steps:**
1. Start screen reader
2. Navigate through the site
3. Verify announcements:
   - Page titles (e.g., "Getting Started | Physical AI & Humanoid Robotics")
   - Heading hierarchy (H1 → H2 → H3)
   - Link text (descriptive, not "click here")
   - ARIA labels (navbar, breadcrumbs, TOC)
   - Image alt text

**Expected:**
- All content is readable by screen reader
- Navigation landmarks are announced
- No "unlabeled" buttons or links
- Headings create logical outline

---

### T093: WCAG 2.1 AA Color Contrast

**Tools:**
- Chrome DevTools: Inspect element → Styles → Color picker shows contrast ratio
- Online: [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- Extension: [axe DevTools](https://www.deque.com/axe/devtools/)

**Steps:**
1. Test color combinations:
   - Body text on background (dark mode: #ffffff on #1e1e1e)
   - Body text on background (light mode: #000000 on #ffffff)
   - Primary color (#00D4AA) on backgrounds
   - Link colors (normal and hover states)
   - Button text on button backgrounds

**WCAG 2.1 AA Requirements:**
- ✅ Normal text (< 18px): Contrast ratio ≥ 4.5:1
- ✅ Large text (≥ 18px bold or 24px regular): Contrast ratio ≥ 3:1

**CSS Variables to Check:**
```css
/* Dark theme (default) */
--ifm-color-primary: #00D4AA;
--ifm-background-color: #1e1e1e;
--ifm-font-color-base: #ffffff;
```

---

### T094: Cross-Browser Compatibility

**Browsers to Test:**
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+ (macOS/iOS)
- ✅ Edge 90+

**Test Cases:**
1. Homepage renders correctly
2. Docs pages display with three-column layout
3. Sidebar navigation works
4. TOC is sticky and clickable
5. Breadcrumbs navigate correctly
6. Dark/light mode toggle works
7. Mobile responsive (< 768px): hamburger menu, no TOC, vertical stacking

**Common Issues:**
- CSS Grid/Flexbox support (should be fine for modern browsers)
- Sticky positioning (`position: sticky`) - supported in all listed browsers
- Custom scrollbar styles (WebKit only, degrades gracefully)

---

### T095: No Console Errors

**Steps:**
1. Open Chrome DevTools Console (F12 → Console tab)
2. Navigate through all pages:
   - Homepage: `/`
   - Intro doc: `/docs/intro`
   - Future doc pages (if added)
3. Check for errors (red text)

**Expected:**
- ✅ No errors
- ⚠️ Warnings are acceptable (e.g., deprecated API warnings from dependencies)
- 🔍 Common warnings to ignore:
  - Docusaurus deprecation warnings (non-breaking)
  - Third-party library warnings

**If errors appear:**
- Note the file and line number
- Check browser compatibility
- Verify all component imports are correct

---

## Deployment Tasks

### T098: Test Deployment to GitHub Pages

**Prerequisites:**
1. Create GitHub repository (if not exists)
2. Update `docusaurus.config.ts`:
   ```ts
   organizationName: 'your-github-username',
   projectName: 'physical-ai-humaniod-robotics',
   ```

**Steps:**
1. Install gh-pages (already done): `npm install --save-dev gh-pages`
2. Add deploy script to `package.json` (already done):
   ```json
   "scripts": {
     "deploy": "docusaurus deploy"
   }
   ```
3. Set up Git (if not done):
   ```bash
   git init
   git add .
   git commit -m "Initial Docusaurus site"
   git remote add origin https://github.com/your-username/physical-ai-humaniod-robotics.git
   git push -u origin master
   ```
4. Deploy to GitHub Pages:
   ```bash
   npm run deploy
   ```

**Expected:**
- Script builds the site
- Pushes to `gh-pages` branch
- No errors during deployment

**Troubleshooting:**
- **Error: "fatal: 'gh-pages' branch not found"**: Normal on first deploy, will be created
- **Error: "Permission denied"**: Check Git credentials and repository permissions
- **Error: "Build failed"**: Run `npm run build` first to verify no build errors

---

### T099: Verify Live Site Accessible

**Steps:**
1. Wait 1-5 minutes after deployment
2. Open browser to: `https://your-username.github.io/physical-ai-humaniod-robotics/`
3. Check that site loads correctly

**Expected:**
- Site loads with all assets
- Navigation works
- No 404 errors
- No broken links

**GitHub Pages Settings:**
1. Go to repository → Settings → Pages
2. Source: `gh-pages` branch, `/ (root)` folder
3. URL shown: `https://your-username.github.io/physical-ai-humaniod-robotics/`

---

### T100: Final Validation

**Checklist:**
- [ ] Homepage displays correctly on live site
- [ ] All navigation links work (sidebar, breadcrumbs, TOC)
- [ ] Dark/light mode toggle works
- [ ] Images load (logo, book-cover, social-card)
- [ ] Responsive on mobile (test on phone or Chrome DevTools device mode)
- [ ] SEO meta tags present (view page source, check `<head>`)
- [ ] No broken links (use [W3C Link Checker](https://validator.w3.org/checklink))

**Tools for Final Validation:**
- [W3C HTML Validator](https://validator.w3.org/)
- [W3C Link Checker](https://validator.w3.org/checklink)
- [Google Mobile-Friendly Test](https://search.google.com/test/mobile-friendly)
- [PageSpeed Insights](https://pagespeed.web.dev/)

---

## Summary

**Completed (7/19 tasks):**
- Image optimization and asset creation
- SEO meta tags
- TypeScript compilation
- Production build
- Local serve test
- GitHub Pages configuration

**Remaining Manual Tasks (12/19):**
- T085-T086: Dark/light mode testing (browser required)
- T089-T095: Lighthouse audits, keyboard navigation, screen reader, contrast, cross-browser, console errors (browser/manual testing)
- T098-T100: Deployment and live site validation (requires GitHub account and repository)

**To Complete Remaining Tasks:**
1. Run `npm run start` from `book-source/` directory
2. Open browser to `http://localhost:3000/physical-ai-humaniod-robotics/`
3. Follow each test section above
4. Update `organizationName` in `docusaurus.config.ts` with your GitHub username
5. Deploy using `npm run deploy`
6. Validate live site

---

## Quick Reference Commands

```bash
# Development
cd book-source
npm install                  # Install dependencies (if needed)
npm run start               # Start dev server (hot reload)

# Build & Test
npm run build               # Production build
npm run serve               # Serve built site locally
npx tsc --noEmit            # TypeScript check

# Deployment
npm run deploy              # Deploy to GitHub Pages (gh-pages branch)

# Troubleshooting
npm run clear               # Clear Docusaurus cache
npm run build -- --verbose  # Verbose build output
```

---

## Notes

- **Image Placeholders**: `book-cover.png` and `social-card.jpg` are currently text placeholders. Replace with actual images for production:
  - Book cover: 300×400px, WebP format, < 200KB
  - Social card: 1200×630px, JPG/PNG, optimized for social media previews

- **Logo**: `logo.svg` is a simple robot icon. Replace with your branding as needed.

- **GitHub Username**: Before deploying, update `organizationName` in `docusaurus.config.ts` to match your GitHub username.

- **Base URL**: If deploying to a different URL, update `baseUrl` in `docusaurus.config.ts`.

---

**Last Updated:** 2025-11-28
**Status:** 7/19 Phase 9 tasks completed, ready for manual testing and deployment
