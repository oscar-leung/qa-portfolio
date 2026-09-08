import { test, expect } from '@playwright/test';
import { InventoryPage } from '../../pages/InventoryPage';
import { CartPage } from '../../pages/CartPage';
import { CheckoutPage } from '../../pages/CheckoutPage';

test.describe('Cart', () => {
  test('removing an item from the cart empties it', async ({ page }) => {
    const inventory = new InventoryPage(page);
    await inventory.goto();
    await inventory.addToCart('sauce-labs-backpack');
    await inventory.goToCart();

    const cart = new CartPage(page);
    await expect(cart.cartItems).toHaveCount(1);

    await cart.removeItem('sauce-labs-backpack');
    await expect(cart.cartItems).toHaveCount(0);
  });
});

test.describe('Checkout', () => {
  test('submitting the info form with a missing field is rejected', async ({ page }) => {
    const inventory = new InventoryPage(page);
    await inventory.goto();
    await inventory.addToCart('sauce-labs-backpack');
    await inventory.goToCart();
    await new CartPage(page).goToCheckout();

    const checkout = new CheckoutPage(page);
    // First/last name filled, postal code deliberately left blank.
    await checkout.fillInfo('Oscar', 'Leung', '');
    await checkout.continueToOverview();

    await expect(checkout.errorMessage).toHaveText('Error: Postal Code is required');
  });

  test('a full checkout completes and shows the confirmation screen', async ({ page }) => {
    const inventory = new InventoryPage(page);
    await inventory.goto();
    await inventory.addToCart('sauce-labs-backpack');
    await inventory.goToCart();
    await new CartPage(page).goToCheckout();

    const checkout = new CheckoutPage(page);
    await checkout.fillInfo('Oscar', 'Leung', '95618');
    await checkout.continueToOverview();

    await expect(checkout.totalLabel).toContainText('Total: $');

    await checkout.finish();
    await expect(checkout.completeHeader).toHaveText('Thank you for your order!');
  });
});
