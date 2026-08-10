import { type Page, type Locator } from '@playwright/test';

/**
 * Covers all three Sauce Demo checkout steps (info form -> overview -> complete).
 * They're one user journey, so one page object models the whole flow rather
 * than splitting into three classes for what's really a single logical task.
 */
export class CheckoutPage {
  readonly page: Page;
  // Step one: customer info
  readonly firstNameInput: Locator;
  readonly lastNameInput: Locator;
  readonly postalCodeInput: Locator;
  readonly continueButton: Locator;
  readonly errorMessage: Locator;
  // Step two: overview
  readonly totalLabel: Locator;
  readonly finishButton: Locator;
  // Step three: complete
  readonly completeHeader: Locator;

  constructor(page: Page) {
    this.page = page;
    this.firstNameInput = page.locator('[data-test="firstName"]');
    this.lastNameInput = page.locator('[data-test="lastName"]');
    this.postalCodeInput = page.locator('[data-test="postalCode"]');
    this.continueButton = page.locator('[data-test="continue"]');
    this.errorMessage = page.locator('[data-test="error"]');
    this.totalLabel = page.locator('[data-test="total-label"]');
    this.finishButton = page.locator('[data-test="finish"]');
    this.completeHeader = page.locator('[data-test="complete-header"]');
  }

  async fillInfo(firstName: string, lastName: string, postalCode: string) {
    await this.firstNameInput.fill(firstName);
    await this.lastNameInput.fill(lastName);
    await this.postalCodeInput.fill(postalCode);
  }

  async continueToOverview() {
    await this.continueButton.click();
  }

  async finish() {
    await this.finishButton.click();
  }

  async getTotal(): Promise<string> {
    return this.totalLabel.textContent().then((t) => t ?? '');
  }
}
