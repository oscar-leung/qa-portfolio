import { type Page, type Locator } from '@playwright/test';

export class InventoryPage {
  readonly page: Page;
  readonly items: Locator;
  readonly sortDropdown: Locator;
  readonly cartBadge: Locator;
  readonly cartLink: Locator;
  readonly itemImages: Locator;

  constructor(page: Page) {
    this.page = page;
    this.items = page.locator('.inventory_item');
    this.sortDropdown = page.locator('[data-test="product-sort-container"]');
    this.cartBadge = page.locator('[data-test="shopping-cart-badge"]');
    this.cartLink = page.locator('[data-test="shopping-cart-link"]');
    this.itemImages = page.locator('.inventory_item_img img');
  }

  async goto() {
    await this.page.goto('/inventory.html');
  }

  /** Sauce Demo builds each add-to-cart button's data-test id from the product name. */
  addToCartButton(itemSlug: string): Locator {
    return this.page.locator(`[data-test="add-to-cart-${itemSlug}"]`);
  }

  async addToCart(itemSlug: string) {
    await this.addToCartButton(itemSlug).click();
  }

  async sortBy(value: 'az' | 'za' | 'lohi' | 'hilo') {
    await this.sortDropdown.selectOption(value);
  }

  async getItemNames(): Promise<string[]> {
    return this.page.locator('.inventory_item_name').allTextContents();
  }

  async getItemPrices(): Promise<number[]> {
    const texts = await this.page.locator('.inventory_item_price').allTextContents();
    return texts.map((t) => parseFloat(t.replace('$', '')));
  }

  async getItemImageSrcs(): Promise<string[]> {
    return this.itemImages.evaluateAll((imgs) =>
      imgs.map((img) => (img as HTMLImageElement).getAttribute('src') ?? '')
    );
  }

  async goToCart() {
    await this.cartLink.click();
  }
}
