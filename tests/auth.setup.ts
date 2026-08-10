import { test as setup } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

/**
 * Runs once before the "authenticated" project. Logs in as standard_user
 * and saves the resulting browser storage (cookies/localStorage) to disk.
 * Every test in the "authenticated" project then starts already logged in,
 * instead of repeating the login flow at the top of every single test.
 *
 * Login itself is still fully tested — see tests/ui/login.spec.ts, which
 * runs in a separate, non-authenticated project on purpose.
 */
const authFile = 'playwright/.auth/user.json';

setup('authenticate as standard_user', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('standard_user', 'secret_sauce');
  await page.waitForURL('**/inventory.html');
  await page.context().storageState({ path: authFile });
});
