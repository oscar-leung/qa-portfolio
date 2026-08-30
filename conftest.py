"""
pytest fixtures — driver setup and teardown for all tests.
Uses Page Object Model (POM) pattern.

Site under test: https://www.saucedemo.com
(Built specifically for QA automation practice)
"""

import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption(
        "--headless", action="store_true", default=False,
        help="Run tests in headless Chrome"
    )


def _headless_requested(config):
    """Headless if --headless is passed or HEADLESS is set truthy.

    CI sets the HEADLESS env var rather than the flag, and a Linux runner
    has no display: without this, Chrome starts headed and immediately
    exits with SessionNotCreatedException.
    """
    if config.getoption("--headless"):
        return True
    return os.environ.get("HEADLESS", "").strip().lower() in {"1", "true", "yes", "on"}


@pytest.fixture(scope="function")
def driver(request):
    """Provide a configured Chrome WebDriver, quit after each test."""
    opts = Options()
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    if _headless_requested(request.config):
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")

    d = webdriver.Chrome(options=opts)
    d.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"},
    )
    d.set_window_size(1440, 900)
    # No implicit wait on purpose. Mixing it with WebDriverWait makes every
    # negative lookup inside an explicit wait block for the implicit timeout,
    # so a single poll can consume the whole explicit budget and raise
    # TimeoutException on a page that is actually fine. Page objects gate on
    # explicit waits instead.
    yield d
    d.quit()


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """Driver already logged in as standard_user, on a ready inventory page."""
    from pages.inventory_page import InventoryPage
    from pages.login_page import LoginPage
    lp = LoginPage(driver)
    lp.open()
    lp.login("standard_user", "secret_sauce")
    # login() only clicks; it does not wait for the redirect. Hand back a
    # driver that is actually on a rendered inventory page, so tests do not
    # race the navigation on a cold/slow runner.
    InventoryPage(driver).wait_until_loaded()
    yield driver
