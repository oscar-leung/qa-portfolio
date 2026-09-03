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

from pages.base_page import BasePage


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


@pytest.fixture(scope="session", autouse=True)
def _warm_up_site():
    """Prime DNS/TLS/CDN for the site under test before any test runs.

    test_checkout.py sorts first, so its four navigation-heavy tests were
    the ones hitting a completely cold GitHub runner — unresolved DNS, no
    TLS session, nothing cached — and they were the only tests failing in
    CI while the 13 single-page tests passed. One cheap request up front
    moves that cost out of the first test.
    """
    import urllib.request
    for url in (f"{BasePage.BASE_URL}/", f"{BasePage.BASE_URL}/inventory.html"):
        try:
            urllib.request.urlopen(url, timeout=30).read(2048)
        except Exception:
            pass  # Warm-up is best-effort; never fail the suite on it.


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
