import { test, expect } from '@playwright/test';

const API = 'http://localhost:8000'

test('full signup, login, create activity flow', async ({ page }) => {
  await page.goto('/');

  const username = `e2e_user_${Date.now()}`;
  const password = 'e2e_pass';

  // fill create form
  await page.fill('input[placeholder="username"]', username);
  await page.fill('input[placeholder="password"]', password);
  await page.click('text=Create');

  // login
  await page.click('text=Login');

  // wait for username to appear as signed-in
  await expect(page.locator('text=Signed in as')).toContainText(username, {timeout: 5000});

  // create an activity
  await page.fill('input[placeholder="activity type"]', 'e2e_activity');
  await page.click('text=Create Activity');

  // check activities list updated
  await expect(page.locator('ul li').first()).toContainText('e2e_activity');
});
