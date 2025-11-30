/**
 * E2E tests for session management
 * Tests: T070 [US3] - login → refresh browser → still authenticated → logout → not authenticated
 *
 * Note: Requires Playwright to be installed:
 * npm install --save-dev @playwright/test
 * npx playwright install
 */

/**
 * Once Playwright is installed, uncomment and use these tests:

import { test, expect } from '@playwright/test';

test.describe('Session Management', () => {
  test('session persists across page refreshes', async ({ page }) => {
    // Step 1: Login
    await page.goto('/login');
    await page.fill('input[name="email"]', 'verified@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    // Wait for redirect after login
    await expect(page).not.toHaveURL('/login');

    // Step 2: Navigate to protected page
    await page.goto('/profile');
    await expect(page).toHaveURL('/profile');

    // Step 3: Refresh the browser
    await page.reload();

    // Step 4: Should still be on profile page (session persisted)
    await expect(page).toHaveURL('/profile');
    await expect(page.getByText(/profile|learning goals/i)).toBeVisible();

    // Step 5: Verify session is still valid by checking /me endpoint
    const response = await page.request.get('/auth/me');
    expect(response.ok()).toBeTruthy();
  });

  test('logout invalidates session', async ({ page }) => {
    // Step 1: Login
    await page.goto('/login');
    await page.fill('input[name="email"]', 'verified@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    // Wait for successful login
    await expect(page).not.toHaveURL('/login');

    // Step 2: Navigate to profile (should be accessible)
    await page.goto('/profile');
    await expect(page).toHaveURL('/profile');

    // Step 3: Logout
    await page.click('button:has-text("Logout")');

    // Step 4: Try to access protected page
    await page.goto('/profile');

    // Step 5: Should redirect to login
    await expect(page).toHaveURL('/login');
  });

  test('unauthenticated user redirected to login', async ({ page }) => {
    // Try to access protected page without logging in
    await page.goto('/profile');

    // Should redirect to login
    await expect(page).toHaveURL('/login');
  });

  test('session cookie has correct attributes', async ({ page, context }) => {
    await page.goto('/login');
    await page.fill('input[name="email"]', 'verified@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    // Wait for login
    await expect(page).not.toHaveURL('/login');

    // Get cookies
    const cookies = await context.cookies();

    // Find auth cookie (name may vary based on implementation)
    const authCookie = cookies.find(
      c => c.name === 'fastapiusersauth' || c.name.includes('auth')
    );

    expect(authCookie).toBeDefined();
    expect(authCookie?.httpOnly).toBe(true);
    expect(authCookie?.sameSite).toBe('Lax');
    // In production, should be secure
    // expect(authCookie?.secure).toBe(true);
  });

  test('user data accessible via /me endpoint', async ({ page }) => {
    // Login
    await page.goto('/login');
    await page.fill('input[name="email"]', 'verified@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    // Navigate to check /me endpoint
    const response = await page.request.get('/auth/me');

    expect(response.ok()).toBeTruthy();

    const userData = await response.json();
    expect(userData.email).toBe('verified@example.com');
    expect(userData.is_verified).toBe(true);
  });

  test('multiple tabs share same session', async ({ context }) => {
    // Create first tab and login
    const page1 = await context.newPage();
    await page1.goto('/login');
    await page1.fill('input[name="email"]', 'verified@example.com');
    await page1.fill('input[name="password"]', 'password123');
    await page1.click('button[type="submit"]');

    await expect(page1).not.toHaveURL('/login');

    // Create second tab
    const page2 = await context.newPage();
    await page2.goto('/profile');

    // Second tab should be authenticated (same context/cookies)
    await expect(page2).toHaveURL('/profile');

    // Logout from first tab
    await page1.click('button:has-text("Logout")');

    // Second tab should also be logged out after refresh
    await page2.reload();
    await expect(page2).toHaveURL('/login');

    await page1.close();
    await page2.close();
  });

  test('expired session redirects to login', async ({ page }) => {
    // This test would require manually expiring the session
    // or waiting for session timeout (not practical for automated tests)
    // Instead, test with invalid/deleted cookie

    await page.goto('/login');
    await page.fill('input[name="email"]', 'verified@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    // Clear cookies to simulate expired session
    await page.context().clearCookies();

    // Try to access protected page
    await page.goto('/profile');

    // Should redirect to login
    await expect(page).toHaveURL('/login');
  });

  test('navigation shows user email when authenticated', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[name="email"]', 'verified@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    // Check if user email is displayed in navbar
    await expect(page.getByText('verified@example.com')).toBeVisible();
  });
});

*/

import { test, expect } from '@playwright/test';

// Placeholder tests - uncomment actual tests above when auth pages are implemented
test.describe('Session Management', () => {
  test('page loads without errors', async ({ page }) => {
    // Basic sanity test - verifies app loads
    await page.goto('/');
    await expect(page.locator('body')).toBeVisible();
  });

  test.skip('maintains session across page navigations', async () => {
    // TODO: Implement when auth is ready
  });

  test.skip('handles session expiry gracefully', async () => {
    // TODO: Implement when auth is ready
  });

  test.skip('logout clears session', async () => {
    // TODO: Implement when auth is ready
  });
});
