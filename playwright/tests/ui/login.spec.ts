import { test, expect } from '@playwright/test';
import { LoginPage } from '../../pages/LoginPage';

// These run in the "login" project (see playwright.config.ts), which has
// no stored auth state — every test here starts from a clean, logged-out
// browser, because that's the whole point of a login test.
test.describe('Login', () => {
  test('valid credentials reach the inventory page', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('standard_user', 'secret_sauce');

    await expect(page).toHaveURL(/inventory\.html/);
  });

  test('locked-out user is blocked with the expected message', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('locked_out_user', 'secret_sauce');

    await expect(page).toHaveURL(/saucedemo\.com\/$/);
    await expect(loginPage.errorMessage).toHaveText(
      'Epic sadface: Sorry, this user has been locked out.'
    );
  });

  test('wrong password is rejected with a generic error', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('standard_user', 'not_the_right_password');

    await expect(loginPage.errorMessage).toHaveText(
      'Epic sadface: Username and password do not match any user in this service'
    );
  });

  test('submitting with empty fields is rejected', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.loginButton.click();

    await expect(loginPage.errorMessage).toHaveText('Epic sadface: Username is required');
  });
});
