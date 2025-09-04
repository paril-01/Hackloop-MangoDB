import { test, expect } from '@playwright/test';

test('user lockout after failed login attempts', async ({ page }) => {
  await page.goto('/');

  const username = `lockout_user_${Date.now()}`;
  const password = 'correct_pass';
  const wrongPassword = 'wrong_pass';

  // First signup with correct password
  await page.fill('input[name="username"]', username);
  await page.fill('input[name="password"]', password);
  await page.click('button:has-text("Sign Up")');
  
  // Wait for success and logout
  await expect(page.locator('text=Welcome')).toBeVisible();
  await page.click('button:has-text("Logout")');

  // Attempt login with wrong password multiple times (should trigger lockout)
  for (let i = 0; i < 6; i++) {
    await page.fill('input[name="username"]', username);
    await page.fill('input[name="password"]', wrongPassword);
    await page.click('button:has-text("Login")');
    
    if (i < 5) {
      await expect(page.locator('text=Invalid credentials')).toBeVisible();
    } else {
      // 6th attempt should show lockout message
      await expect(page.locator('text=Account locked')).toBeVisible();
    }
  }

  // Try login with correct password - should still be locked
  await page.fill('input[name="username"]', username);
  await page.fill('input[name="password"]', password);
  await page.click('button:has-text("Login")');
  await expect(page.locator('text=Account locked')).toBeVisible();
});

test('session expiry and forced logout', async ({ page }) => {
  await page.goto('/');

  const username = `session_user_${Date.now()}`;
  const password = 'session_pass';

  // Signup and login
  await page.fill('input[name="username"]', username);
  await page.fill('input[name="password"]', password);
  await page.click('button:has-text("Sign Up")');
  
  await expect(page.locator('text=Welcome')).toBeVisible();

  // Simulate session expiry by manipulating session cookie
  // Delete session cookie to simulate expiry
  const context = page.context();
  await context.clearCookies();

  // Try to access protected functionality - should redirect to login
  await page.click('button:has-text("Create Activity")');
  
  // Should be redirected to login state
  await expect(page.locator('button:has-text("Login")')).toBeVisible();
  await expect(page.locator('text=Please log in')).toBeVisible();
});

test('concurrent session handling', async ({ browser }) => {
  // Test multiple browser contexts (simulating multiple tabs/windows)
  const context1 = await browser.newContext();
  const context2 = await browser.newContext();
  
  const page1 = await context1.newPage();
  const page2 = await context2.newPage();

  const username = `concurrent_user_${Date.now()}`;
  const password = 'concurrent_pass';

  // Login in first context
  await page1.goto('/');
  await page1.fill('input[name="username"]', username);
  await page1.fill('input[name="password"]', password);
  await page1.click('button:has-text("Sign Up")');
  await expect(page1.locator('text=Welcome')).toBeVisible();

  // Try to login with same user in second context
  await page2.goto('/');
  await page2.fill('input[name="username"]', username);
  await page2.fill('input[name="password"]', password);
  await page2.click('button:has-text("Login")');
  
  // Second session should work (concurrent sessions allowed)
  await expect(page2.locator('text=Welcome')).toBeVisible();

  // Both sessions should be able to create activities
  await page1.click('button:has-text("Create Activity")');
  await page1.fill('input[name="activity_type"]', 'coding');
  await page1.click('button:has-text("Save")');

  await page2.click('button:has-text("Create Activity")');
  await page2.fill('input[name="activity_type"]', 'reading');
  await page2.click('button:has-text("Save")');

  await context1.close();
  await context2.close();
});
