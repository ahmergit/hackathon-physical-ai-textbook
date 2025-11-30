# Testing Checklist for Physical AI & Humanoid Robotics Site

This document tracks all testing and validation tasks for the Docusaurus site.

## Automated Tests (Completed ✅)

- [x] **T087**: Build succeeds without errors (`npm run build`)
- [x] **T088**: Built site serves locally (`npm run serve`)
- [x] **T096**: TypeScript compiles without errors (`npx tsc --noEmit`)
- [x] **T097**: GitHub Pages deployment configured in `docusaurus.config.ts`

## Manual Tests (To Be Completed)

### Accessibility Tests

- [ ] **T085**: Test dark/light mode toggle functionality
  - Toggle between dark and light modes
  - Verify preference persists across sessions
  - Check that toggle button is visible and functional

- [ ] **T086**: Verify colors are readable in both dark and light modes
  - Check all text has sufficient contrast
  - Verify link colors are distinguishable
  - Ensure code blocks are readable

- [ ] **T089**: Run Lighthouse audit on homepage
  - Performance score > 90
  - Accessibility score > 90
  - Best Practices score > 90
  - SEO score > 90
  - Generate report and save

- [ ] **T090**: Run Lighthouse audit on doc page
  - Test representative lesson page
  - Performance score > 90
  - Accessibility score > 90
  - Best Practices score > 90
  - SEO score > 90

- [ ] **T091**: Test keyboard navigation
  - Tab through all interactive elements
  - Verify focus indicators are visible
  - Test sidebar navigation with keyboard only
  - Test TOC navigation with keyboard
  - Verify Skip to Content link works

- [ ] **T092**: Test screen reader (NVDA or VoiceOver)
  - Page titles announced correctly
  - Headings hierarchy is logical
  - Links have descriptive text
  - Images have alt text
  - Navigation landmarks are present

- [ ] **T093**: Verify color contrast meets WCAG 2.1 AA
  - Body text: 4.5:1 contrast ratio minimum
  - Large text: 3:1 contrast ratio minimum
  - Interactive elements meet requirements
  - Use contrast checker tool

### Cross-Browser Compatibility

- [ ] **T094**: Test on multiple browsers
  - Chrome 90+ (latest stable)
  - Firefox 88+ (latest stable)
  - Safari 14+ (macOS/iOS)
  - Edge 90+ (latest stable)
  - Verify layout, functionality, performance

- [ ] **T095**: Verify no console errors
  - Check browser DevTools console on homepage
  - Check console on documentation pages
  - Check console on lesson pages
  - Verify no JavaScript errors
  - Verify no resource loading errors

### Deployment Tests

- [ ] **T098**: Test GitHub Pages deployment
  - Run `npm run deploy`
  - Verify gh-pages branch created
  - Verify deployment completes successfully
  - Check deployment logs for errors

- [ ] **T099**: Verify live site accessible
  - Visit GitHub Pages URL
  - Verify site loads correctly
  - Test navigation works
  - Check all assets load (images, CSS, JS)

- [ ] **T100**: Final validation on live site
  - Navigate through all major sections
  - Verify no broken links
  - Test sidebar navigation
  - Test TOC navigation
  - Verify mobile responsiveness
  - Test search functionality (if enabled)
  - Verify all lessons load correctly

## Testing Instructions

### Running Lighthouse Audit

1. Open Chrome DevTools (F12)
2. Navigate to "Lighthouse" tab
3. Select "Desktop" or "Mobile" device
4. Check all categories
5. Click "Generate report"
6. Save report and verify scores

### Testing Keyboard Navigation

1. Open site in browser
2. Press Tab to navigate
3. Verify focus order is logical
4. Ensure all interactive elements reachable
5. Press Enter to activate links/buttons
6. Use arrow keys in navigation menus

### Testing Screen Reader

**Windows (NVDA)**:
1. Download NVDA (free)
2. Launch NVDA
3. Navigate site using screen reader
4. Verify all content is announced
5. Check heading hierarchy

**macOS (VoiceOver)**:
1. Press Cmd+F5 to enable VoiceOver
2. Use VoiceOver keyboard shortcuts
3. Navigate through content
4. Verify announcements are clear

### Testing Color Contrast

1. Use WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
2. Test foreground/background combinations
3. Verify meets WCAG 2.1 AA standards
4. Document any failures and fix

### Cross-Browser Testing

For each browser:
1. Open site in browser
2. Navigate through homepage
3. Browse documentation pages
4. Test sidebar collapse/expand
5. Test TOC navigation
6. Verify responsive design
7. Check DevTools console for errors

## Results Summary

### Build Status
- ✅ **Build**: Success
- ✅ **TypeScript**: No errors
- ✅ **Local Serve**: Works

### Accessibility (To Be Tested)
- ⏳ Dark/Light Mode
- ⏳ Color Readability
- ⏳ Lighthouse (Homepage)
- ⏳ Lighthouse (Doc Page)
- ⏳ Keyboard Navigation
- ⏳ Screen Reader
- ⏳ Color Contrast

### Compatibility (To Be Tested)
- ⏳ Chrome
- ⏳ Firefox
- ⏳ Safari
- ⏳ Edge
- ⏳ Console Errors

### Deployment (To Be Tested)
- ⏳ GitHub Pages Deploy
- ⏳ Live Site Access
- ⏳ Final Validation

## Notes

- All automated tests pass ✅
- Manual tests require human interaction
- Deployment tests require GitHub repository setup
- Record any issues found during testing
- Update this checklist as tests are completed

---

Last Updated: 2025-11-28
