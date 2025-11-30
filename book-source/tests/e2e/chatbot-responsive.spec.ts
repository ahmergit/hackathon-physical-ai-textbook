/**
 * E2E tests for responsive chatbot UI.
 */

import { test, expect } from '@playwright/test';

test.describe('Chatbot Responsive UI', () => {
  test('should display chatbot on desktop viewport', async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto('/docs/chapter-01/intro');

    // Check if chatbot is visible
    const chatbot = page.locator('.chatbot-container');
    await expect(chatbot).toBeVisible();

    // Verify desktop sizing
    const box = await chatbot.boundingBox();
    expect(box?.width).toBeGreaterThanOrEqual(380);
  });

  test('should adapt layout on tablet viewport', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/docs/chapter-01/intro');

    const chatbot = page.locator('.chatbot-container');
    await expect(chatbot).toBeVisible();

    // Verify tablet sizing
    const box = await chatbot.boundingBox();
    expect(box?.width).toBeLessThanOrEqual(400);
  });

  test('should adapt layout on mobile viewport (320px)', async ({ page }) => {
    await page.setViewportSize({ width: 320, height: 568 });
    await page.goto('/docs/chapter-01/intro');

    const chatbot = page.locator('.chatbot-container');
    await expect(chatbot).toBeVisible();

    // Verify mobile takes most of the width
    const box = await chatbot.boundingBox();
    const viewportWidth = 320;
    expect(box?.width).toBeGreaterThan(viewportWidth * 0.9);
  });

  test('should have touch-friendly button sizes on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/docs/chapter-01/intro');

    // Check send button minimum touch target
    const sendButton = page.locator('button[type="submit"]');
    const box = await sendButton.boundingBox();

    // Minimum 44px for touch targets
    expect(box?.height).toBeGreaterThanOrEqual(44);
  });

  test('should maintain functionality across breakpoints', async ({ page }) => {
    const viewports = [
      { width: 320, height: 568 },   // Mobile
      { width: 768, height: 1024 },  // Tablet
      { width: 1920, height: 1080 }, // Desktop
      { width: 2560, height: 1440 }, // Large desktop
    ];

    for (const viewport of viewports) {
      await page.setViewportSize(viewport);
      await page.goto('/docs/chapter-01/intro');

      // Verify input is accessible
      const input = page.locator('input[type="text"]');
      await expect(input).toBeVisible();

      // Verify send button is accessible
      const sendButton = page.locator('button[type="submit"]');
      await expect(sendButton).toBeVisible();
    }
  });
});
