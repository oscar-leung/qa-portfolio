"""Inventory (products) page POM for saucedemo.com."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .base_page import BasePage


class InventoryPage(BasePage):
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    INVENTORY_ITEMS     = (By.CLASS_NAME, "inventory_item")
    ITEM_NAMES          = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES         = (By.CLASS_NAME, "inventory_item_price")
    SORT_DROPDOWN       = (By.CLASS_NAME, "product_sort_container")
    CART_BADGE          = (By.CLASS_NAME, "shopping_cart_badge")
    CART_ICON           = (By.CLASS_NAME, "shopping_cart_link")
    BURGER_MENU         = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK         = (By.ID, "logout_sidebar_link")

    def open(self):
        super().open("/inventory.html")
        self.wait_until_loaded()

    def wait_until_loaded(self):
        """Block until the product grid is present."""
        self.find(*self.INVENTORY_CONTAINER)
        return self

    def get_item_names(self) -> list[str]:
        return [el.text for el in self.driver.find_elements(*self.ITEM_NAMES)]

    def get_item_prices(self) -> list[float]:
        return [
            float(el.text.replace("$", ""))
            for el in self.driver.find_elements(*self.ITEM_PRICES)
        ]

    @staticmethod
    def _slug(item_name: str) -> str:
        """'Sauce Labs Bolt T-Shirt' -> 'sauce-labs-bolt-t-shirt'."""
        return item_name.strip().lower().replace(" ", "-")

    def add_item_to_cart(self, item_name: str):
        """Add a product to the cart and wait until the add has registered.

        Targets the app's own data-test hooks (add-to-cart-<slug> flips to
        remove-<slug>) rather than scanning the grid and matching button
        text. The grid re-renders on every click, so a text/DOM scan raced
        the render and intermittently timed out.
        """
        self.wait_until_loaded()
        slug = self._slug(item_name)
        self.click_until(
            (By.CSS_SELECTOR, f"[data-test='add-to-cart-{slug}']"),
            (By.CSS_SELECTOR, f"[data-test='remove-{slug}']"),
        )

    def get_cart_count(self) -> int:
        if not self.is_visible(*self.CART_BADGE):
            return 0
        return int(self.get_text(*self.CART_BADGE))

    def sort_by(self, option: str):
        """option: 'az', 'za', 'lohi', 'hilo'"""
        Select(self.find(*self.SORT_DROPDOWN)).select_by_value(option)

    def go_to_cart(self):
        """Open the cart and wait for it to render."""
        self.click_until(self.CART_ICON, (By.ID, "cart_contents_container"))

    def logout(self):
        import time
        self.click(*self.BURGER_MENU)
        time.sleep(0.5)  # Wait for sidebar animation
        # JS click bypasses headless animation timing issue
        logout_el = self.find(*self.LOGOUT_LINK)
        self.driver.execute_script("arguments[0].click();", logout_el)
