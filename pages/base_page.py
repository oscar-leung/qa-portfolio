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
        """Click, then wait for the expected element; retry a swallowed click.

        This app re-renders on interaction and will occasionally drop a click
        entirely — the call returns cleanly and nothing happened. Retrying
        against an observable outcome is what makes these steps reliable
        instead of intermittently timing out.
        """
        per_attempt = per_attempt or self.DEFAULT_TIMEOUT
        last_error = None
        for attempt in range(attempts):
            # Never re-submit something that already took effect: a second
            # click on a completed checkout would be a new interaction, not
            # a retry.
            if attempt and self.driver.find_elements(*expect_locator):
                return self.driver.find_element(*expect_locator)
            try:
                self.click(*click_locator)
            except TimeoutException as exc:
                # Already navigated away: the click landed, just verify below.
                last_error = exc
            try:
                return WebDriverWait(self.driver, per_attempt).until(
                    EC.presence_of_element_located(expect_locator)
                )
            except TimeoutException as exc:
                last_error = exc
        raise last_error

    def type_text(self, by, value, text, attempts=3):
        """Type into a field and confirm the value actually landed.

        These are React-controlled inputs: a clear()/send_keys() pair can be
        swallowed by a re-render, leaving the field empty while the call
        still appears to succeed. Verify and retry rather than trusting it.
        """
        for attempt in range(attempts):
            el = self.find(by, value)
            el.clear()
            if text:
                el.send_keys(text)
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
