"""Cart page POM for saucedemo.com."""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class CartPage(BasePage):
    CART_ITEMS      = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES      = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_BUTTON = (By.ID, "continue-shopping")
    REMOVE_BUTTONS  = (By.CSS_SELECTOR, "button[data-test^='remove']")
    CART_CONTAINER  = (By.ID, "cart_contents_container")

    def open(self):
        super().open("/cart.html")
        self.wait_until_loaded()

    def wait_until_loaded(self):
        """Block until the cart container is present (it renders even empty)."""
        self.find(*self.CART_CONTAINER)
        return self

    def get_cart_item_names(self) -> list[str]:
        self.wait_until_loaded()
        return [el.text for el in self.driver.find_elements(*self.ITEM_NAMES)]

    def get_cart_item_count(self) -> int:
        self.wait_until_loaded()
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def go_to_checkout(self):
        """Open checkout step one and wait for the form to render."""
        self.click_until(self.CHECKOUT_BUTTON, (By.ID, "first-name"))

    def continue_shopping(self):
        self.click(*self.CONTINUE_BUTTON)


class CheckoutPage(BasePage):
    FIRST_NAME   = (By.ID, "first-name")
    LAST_NAME    = (By.ID, "last-name")
    POSTAL_CODE  = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")
    FINISH_BTN   = (By.ID, "finish")
    SUCCESS_MSG  = (By.CLASS_NAME, "complete-header")
    ERROR_MSG    = (By.CSS_SELECTOR, "[data-test='error']")
    # Either outcome of submitting step one, in ONE lookup. Two separate
    # find_elements calls would each burn the driver's implicit wait when
    # absent, blowing the explicit timeout before the page could settle.
    STEP_ONE_SETTLED = (By.CSS_SELECTOR, "#finish, [data-test='error']")

    def fill_info(self, first: str, last: str, zip_code: str):
        self.type_text(*self.FIRST_NAME, first)
        self.type_text(*self.LAST_NAME, last)
        self.type_text(*self.POSTAL_CODE, zip_code)

    def continue_checkout(self):
        """Submit checkout step one and wait for the outcome to settle.

        Valid info advances to the overview page (the finish button);
        missing info keeps us on the form with an error. Waiting for
        whichever appears means callers never act on a half-rendered page —
        the positive flow was reaching finish_checkout() before the
        overview existed.
        """
        self.click_until(self.CONTINUE_BTN, self.STEP_ONE_SETTLED)

    def finish_checkout(self):
        """Submit the order and wait for the confirmation page.

        The click is what commits the order and clears the cart. Returning
        before the confirmation renders lets a test navigate away
        mid-commit, leaving the cart still populated.
        """
        self.click_until(self.FINISH_BTN, self.SUCCESS_MSG)

    def get_success_message(self) -> str:
        return self.get_text(*self.SUCCESS_MSG)

    def is_error_shown(self) -> bool:
        return self.is_visible(*self.ERROR_MSG)
