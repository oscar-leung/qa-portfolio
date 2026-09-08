"""Base page — shared driver helpers used by all page objects."""

import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    BASE_URL = "https://www.saucedemo.com"
    # The app under test is a live third-party site, so page loads are only
    # as fast as the network. A CI runner is materially slower than a laptop
    # (the same suite takes ~35s locally and ~150s on GitHub Actions), and
    # every navigation-heavy test was timing out there while single-page
    # tests passed. Let the environment raise the ceiling.
    DEFAULT_TIMEOUT = int(os.environ.get("SELENIUM_TIMEOUT", "10"))

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    def open(self, path=""):
        self.driver.get(self.BASE_URL + path)

    def find(self, by, value):
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def click(self, by, value):
        el = self.wait.until(EC.element_to_be_clickable((by, value)))
        el.click()
        return el

    def click_until(self, click_locator, expect_locator, attempts=3, per_attempt=None):
        """Click, then wait for the expected element; escalate if it was dropped.

        Headless Chrome silently swallows some native clicks: the element is
        found, enabled, visible and unobscured, .click() raises nothing, and
        the page simply does not navigate. CI artifacts showed exactly this —
        a fully rendered cart page with the Checkout button plainly visible,
        still sitting there after the click. logout() already worked around
        the same thing with a JS click.

        So: try a real click first, because that is what a user does and it
        works everywhere except headless. If the expected outcome does not
        appear, escalate to a JS click, which dispatches the handler directly.

        The first attempt waits briefly rather than the full timeout — when a
        click is dropped it is dropped immediately, and burning 45s before
        escalating is what turned CI runs into 20-minute jobs.
        """
        per_attempt = per_attempt or self.DEFAULT_TIMEOUT
        last_error = None
        for attempt in range(attempts):
            # Never re-fire something that already took effect.
            if attempt and self.driver.find_elements(*expect_locator):
                return self.driver.find_element(*expect_locator)
            try:
                el = self.wait.until(EC.element_to_be_clickable(click_locator))
                if attempt == 0:
                    el.click()
                else:
                    self.driver.execute_script("arguments[0].click();", el)
            except TimeoutException as exc:
                # Already navigated away: the click landed; verify below.
                last_error = exc
            timeout = min(8, per_attempt) if attempt == 0 else per_attempt
            try:
                return WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(expect_locator)
                )
            except TimeoutException as exc:
                last_error = exc
        raise last_error

    # Setting .value directly does not update a React controlled input — React
    # tracks its own value on the node. Go through the native setter and fire a
    # bubbling input event so React's onChange actually runs.
    _REACT_SET_VALUE = """
        var el = arguments[0], v = arguments[1];
        var setter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value').set;
        setter.call(el, v);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    """

    def type_text(self, by, value, text, attempts=3):
        """Type into a field and confirm the value actually landed.

        Same failure mode as the dropped clicks: headless Chrome will accept a
        clear()/send_keys() pair, raise nothing, and leave the field empty.
        CI caught it as "Could not set id='first-name' to 'Oscar'".

        Real keystrokes first, because that is what a user does and it exercises
        the app's own input handling. If the value does not stick, escalate to
        setting it through React's native setter.
        """
        for attempt in range(attempts):
            el = self.find(by, value)
            if attempt == 0:
                el.clear()
                if text:
                    el.send_keys(text)
            else:
                self.driver.execute_script(self._REACT_SET_VALUE, el, text)
            if self.find(by, value).get_attribute("value") == text:
                return
        raise AssertionError(
            f"Could not set {by}={value!r} to {text!r} after {attempts} attempts; "
            f"field still reads {self.find(by, value).get_attribute('value')!r}"
        )

    def get_text(self, by, value) -> str:
        return self.find(by, value).text.strip()

    def is_visible(self, by, value, timeout=3) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except Exception:
            return False

    @property
    def current_url(self) -> str:
        return self.driver.current_url
