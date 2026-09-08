import { test, expect } from '@playwright/test';
import { LoginPage } from '../../pages/LoginPage';
import { InventoryPage } from '../../pages/InventoryPage';

/**
 * DEFECT: problem_user's product grid renders every item with the same
 * broken image asset instead of each product's own image. Confirmed
 * manually: standard_user shows 6 unique image sources; problem_user
 * shows the same single source repeated 6 times.
 *
 * This uses test.fail() to mark the test as a *known, expected* failure
 * rather than silently skipping it or leaving the suite red. Two benefits
 * over just deleting/skipping the test: the CI report still shows the test
 * ran, and if Sauce Demo ever fixes the bug, this test starts unexpectedly
 * PASSING - which Playwright flags as its own kind of failure, so the fix
 * doesn't go unnoticed.
 *
 * Runs in the "login" (unauthenticated) project since it needs to log in
 * as problem_user rather than reuse the standard_user session from
 * auth.setup.ts.
 */
test('problem_user sees a duplicate product image defect', async ({ page }) => {
  test.fail(true, 'Known Sauce Demo seeded bug: problem_user renders a duplicate image for every product');

  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('problem_user', 'secret_sauce');

  const inventory = new InventoryPage(page);
  const imageSrcs = await inventory.getItemImageSrcs();
  const uniqueSrcs = new Set(imageSrcs);

  // Asserts the CORRECT behavior (each product should have its own image).
  // Combined with test.fail() above, this is expected to fail today.
  expect(uniqueSrcs.size, 'expected each product to have a distinct image').toBeGreaterThan(1);
});
