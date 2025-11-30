/**
 * E2E tests for Google SSO
 * Tests: T081 [US2] - E2E test with Google test account
 *
 * Note: Requires Playwright to be installed and Google OAuth test mode setup:
 * npm install --save-dev @playwright/test
 * npx playwright install
 */

/**
 * Once Playwright and Google OAuth test mode are set up, uncomment and use these tests:
 *
 * IMPORTANT: These tests require:
 * 1. Google OAuth configured with test credentials
 * 2. A test Google account
 * 3. Environment variables for test account credentials
 *
 * Setup:
 * - Create a Google Cloud Project test environment
 * - Configure OAuth consent screen for testing
 * - Set GOOGLE_TEST_EMAIL and GOOGLE_TEST_PASSWORD environment variables

import { test, expect } from '@playwright/test';

test.describe('Google SSO Flow', () => {
  test.skip('complete Google OAuth flow for new user', async ({ page }) => {
    // Note: This test is skipped by default as it requires actual Google OAuth setup

    // Step 1: Navigate to signup/login page
    await page.goto('/signup');

    // Step 2: Click "Sign in with Google" button
    await page.click('button:has-text("Sign in with Google")');

    // Step 3: Google OAuth consent screen should appear
    await expect(page).toHaveURL(/accounts\.google\.com/);

    // Step 4: Enter Google test account credentials
    const testEmail = process.env.GOOGLE_TEST_EMAIL || 'test@example.com';
    const testPassword = process.env.GOOGLE_TEST_PASSWORD || 'password';

    await page.fill('input[type="email"]', testEmail);
    await page.click('button:has-text("Next")');

    await page.waitForSelector('input[type="password"]');
    await page.fill('input[type="password"]', testPassword);
    await page.click('button:has-text("Next")');

    // Step 5: Grant permissions (if first time)
    // await page.click('button:has-text("Allow")');

    // Step 6: Should redirect back to application
    await expect(page).toHaveURL(/localhost:3000|your-domain/);

    // Step 7: New OAuth users should go to onboarding
    if (page.url().includes('/onboarding')) {
      await page.selectOption('select[name="robotics_experience"]', 'beginner');
      await page.selectOption(
        'select[name="programming_experience"]',
        'intermediate'
      );
      await page.selectOption('select[name="ai_ml_experience"]', 'none');
      await page.fill(
        'textarea[name="learning_goals"]',
        'Learn with Google SSO'
      );
      await page.selectOption(
        'select[name="preferred_learning_style"]',
        'hands_on'
      );
      await page.fill('input[name="weekly_time_commitment"]', '10');
      await page.click('button[type="submit"]');
    }

    // Step 8: Should be authenticated and redirected to profile/dashboard
    await expect(page).toHaveURL(/\/profile|\/dashboard|\//);

    // Step 9: Verify user is authenticated
    const response = await page.request.get('/auth/me');
    expect(response.ok()).toBeTruthy();

    const userData = await response.json();
    expect(userData.email).toBe(testEmail);
    expect(userData.is_verified).toBe(true); // OAuth users pre-verified
  });

  test.skip('returning Google OAuth user skips onboarding', async ({
    page,
  }) => {
    // Note: This test is skipped by default as it requires actual Google OAuth setup

    await page.goto('/login');
    await page.click('button:has-text("Sign in with Google")');

    // Go through OAuth flow (same as above)
    const testEmail = process.env.GOOGLE_TEST_EMAIL || 'returning@example.com';

    // ... OAuth steps ...

    // Returning user should NOT see onboarding
    await expect(page).not.toHaveURL('/onboarding');
    await expect(page).toHaveURL(/\/profile|\/dashboard|\//);
  });

  test.skip('handles OAuth cancellation gracefully', async ({ page }) => {
    await page.goto('/signup');
    await page.click('button:has-text("Sign in with Google")');

    await expect(page).toHaveURL(/accounts\.google\.com/);

    // User cancels OAuth flow
    await page.click('button:has-text("Cancel")');

    // Should return to signup/login page
    await expect(page).toHaveURL(/\/signup|\/login/);
  });

  test.skip('OAuth user is marked as verified', async ({ page }) => {
    // Complete OAuth flow
    // ... (same as first test)

    // Check user data
    const response = await page.request.get('/auth/me');
    const userData = await response.json();

    // OAuth users should be automatically verified
    expect(userData.is_verified).toBe(true);
  });

  test('displays Google SSO button on signup and login pages', async ({
    page,
  }) => {
    // Check signup page
    await page.goto('/signup');
    await expect(
      page.getByRole('button', { name: /sign in with google/i })
    ).toBeVisible();

    // Check login page
    await page.goto('/login');
    await expect(
      page.getByRole('button', { name: /sign in with google/i })
    ).toBeVisible();
  });
});

test.describe('OAuth Security', () => {
  test.skip('OAuth flow uses PKCE for security', async ({ page }) => {
    // Monitor network requests
    const requests: any[] = [];

    page.on('request', request => {
      if (request.url().includes('google') && request.url().includes('oauth')) {
        requests.push({
          url: request.url(),
          method: request.method(),
        });
      }
    });

    await page.goto('/signup');
    await page.click('button:has-text("Sign in with Google")');

    // Verify PKCE parameters are included
    const authRequest = requests.find(r => r.url.includes('authorize'));
    expect(authRequest.url).toContain('code_challenge');
    expect(authRequest.url).toContain('code_challenge_method');
  });

  test.skip('OAuth callback validates state parameter', async ({ page }) => {
    // Test CSRF protection via state parameter
    // This would require intercepting and modifying the OAuth callback
    // Advanced security test
  });
});

*/

import { test, expect } from '@playwright/test';

// Placeholder tests - uncomment actual tests above when Google SSO is implemented
test.describe('Google SSO Flow', () => {
  test('homepage is accessible', async ({ page }) => {
    // Basic sanity test - verifies site is running
    await page.goto('/');
    await expect(page).toHaveURL('/');
  });

  test.skip('redirects to Google OAuth', async () => {
    // TODO: Implement when Google SSO is ready
  });

  test.skip('handles OAuth callback', async () => {
    // TODO: Implement when Google SSO is ready
  });

  test.skip('links Google account to existing user', async () => {
    // TODO: Implement when Google SSO is ready
  });
});
