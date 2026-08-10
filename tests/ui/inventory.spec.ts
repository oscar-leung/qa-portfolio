import { test, expect } from '@playwright/test';
import { InventoryPage } from '../../pages/InventoryPage';

// These run in the "authenticated" project, which reuses the storageState
// saved by auth.setup.ts - no login step needed in the test body itself.
test.describe('Inventory', () => {
  test.beforeEach(async ({ page }) => {
    await new InventoryPage(page).goto();
  });

  test('sorting by price low-to-high orders items correctly', async ({ page }) => {
    const inventory = new InventoryPage(page);
    await inventory.sortBy('lohi');

    const prices = await inventory.getItemPrices();
    const sorted = [...prices].sort((a, b) => a - b);
    expect(prices).toEqual(sorted);
  });

  test('sorting by name Z-to-A orders items correctly', async ({ page }) => {
    const inventory = new InventoryPage(page);
    await inventory.sortBy('za');

    const names = await inventory.getItemNames();
    const sorted = [...names].sort().reverse();
    expect(names).toEqual(sorted);
  });

  test('adding an item to the cart updates the cart badge', async ({ page }) => {
    const inventory = new InventoryPage(page);
    await inventory.addToCart('sauce-labs-backpack');

    await expect(inventory.cartBadge).toHaveText('1');
  });

  test('adding multiple items accumulates the cart badge count', async ({ page }) => {
    const inventory = new InventoryPage(page);
    await inventory.addToCart('sauce-labs-backpack');
    await inventory.addToCart('sauce-labs-bike-light');

    await expect(inventory.cartBadge).toHaveText('2');
  });
});
