import { type Page, type Locator } from '@playwright/test';

export class CartPage {
  readonly page: Page;
  readonly cartItems: Locator;
  readonly checkoutButton: Locator;
  readonly continueShoppingButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.cartItems = page.locator('.cart_item');
    this.checkoutButton = page.locator('[data-test="checkout"]');
    this.continueShoppingButton = page.locator('[data-test="continue-shopping"]');
  }

  async goto() {
    await this.page.goto('/cart.html');
  }

  removeButton(itemSlug: string): Locator {
    return this.page.locator(`[data-test="remove-${itemSlug}"]`);
  }

  async removeItem(itemSlug: string) {
    await this.removeButton(itemSlug).click();
  }

  async getItemCount(): Promise<number> {
    return this.cartItems.count();
  }

  async goToCheckout() {
    await this.checkoutButton.click();
  }
}
