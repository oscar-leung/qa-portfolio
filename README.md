<div align="center">

<h1>📊 QA Automation Portfolio — SauceDemo E2E Suite</h1>

<p><strong>Professional end-to-end test suite for a real e-commerce app — login, inventory, cart, and checkout flows covered with pytest, Selenium, and Page Object Model.</strong></p>

[![Tests](https://github.com/oscar-leung/qa-portfolio/actions/workflows/tests.yml/badge.svg)](https://github.com/oscar-leung/qa-portfolio/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Selenium](https://img.shields.io/badge/Selenium-4.x-43B02A?style=flat-square&logo=selenium&logoColor=white)](https://selenium.dev)
[![pytest](https://img.shields.io/badge/pytest-8.x-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](https://pytest.org)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

<br/>

**[Portfolio](https://oscar-leung.github.io) · [LinkedIn](https://linkedin.com/in/oscar-leung)**

</div>

---

## 🎯 What This Tests

Full end-to-end coverage of [saucedemo.com](https://saucedemo.com) — a production-like e-commerce demo site:

| Flow | Tests |
|------|-------|
| **Login** | Valid login, invalid credentials, locked-out user, empty fields |
| **Inventory** | Product listing, sorting (A→Z, Z→A, price), add to cart |
| **Cart** | Add/remove items, item count badge, cart persistence |
| **Checkout** | Full purchase flow, form validation, order confirmation |

---

## 🏗️ Architecture — Page Object Model

```
qa-portfolio/
├── pages/
│   ├── base_page.py        # Shared wait helpers, element actions
│   ├── login_page.py       # Login form interactions
│   ├── inventory_page.py   # Product grid, sort, add-to-cart
│   ├── cart_page.py        # Cart sidebar, item management
│   └── checkout_page.py    # Multi-step checkout flow
├── tests/
│   ├── conftest.py         # Fixtures: driver setup/teardown, base URL
│   ├── test_login.py       # 6 login scenario tests
│   ├── test_inventory.py   # Product and sort tests
│   └── test_checkout.py    # Full checkout E2E tests
├── pytest.ini              # HTML report config, markers
└── requirements.txt
```

**Why POM?** Each page is its own class — tests never touch raw selectors. When the UI changes, you update one file, not every test.

---

## 🚀 Quick Start

```bash
git clone https://github.com/oscar-leung/qa-portfolio.git
cd qa-portfolio
pip install -r requirements.txt
```

### Run all tests
```bash
pytest
```

### Run with HTML report
```bash
pytest --html=report.html --self-contained-html
open report.html
```

### Run a specific flow
```bash
pytest tests/test_login.py -v
pytest tests/test_checkout.py -v
```

### Run headless (CI mode)
```bash
pytest --headless
```

---

## 📋 Sample Test

```python
class TestLogin:

    def test_valid_login_redirects_to_inventory(self, driver):
        """Standard user can log in and reaches inventory page."""
        lp = LoginPage(driver)
        lp.open()
        lp.login("standard_user", "secret_sauce")
        assert "inventory" in driver.current_url

    def test_locked_out_user_shows_error(self, driver):
        """Locked-out user sees appropriate error."""
        lp = LoginPage(driver)
        lp.open()
        lp.login("locked_out_user", "secret_sauce")
        assert lp.is_error_displayed()
        assert "locked out" in lp.get_error_message().lower()
```

---

## 🔁 CI / GitHub Actions

Tests run automatically on every push and pull request via GitHub Actions:

```yaml
# .github/workflows/tests.yml
- Headless Chrome on ubuntu-latest
- Full pytest suite with HTML report upload
- Badge auto-updates on each run
```

[![Tests](https://github.com/oscar-leung/qa-portfolio/actions/workflows/tests.yml/badge.svg)](https://github.com/oscar-leung/qa-portfolio/actions/workflows/tests.yml)

### Headless-only failures, and how they were found

The four checkout tests passed on a laptop and failed only in CI. Three
attempts to fix that by tuning timeouts, adding retries, and warming the site
all failed, because the premise was wrong: nothing was slow.

Adding failure artifacts (`conftest.py` dumps the URL, a screenshot, and the
page source on failure; CI uploads them) settled it in one run. The artifacts
showed a fully rendered cart page, Checkout button visible and unobscured,
`.click()` having raised nothing, and the page simply not navigated.

**Headless Chrome silently drops some native clicks and keystrokes** on this
app — the call succeeds and nothing happens. `pages/inventory_page.py` already
documented the click half in `logout()`.

Both interactions now try the real user action first and escalate only if the
expected outcome does not appear:

- `click_until` falls back to a JS click.
- `type_text` falls back to React's native value setter plus a bubbling `input`
  event. Assigning `.value` alone is not enough — React tracks its own value on
  the node and ignores it, which would leave the field looking filled while the
  form still refused to submit.

Native-first ordering is deliberate. JS-clicking everything would be more
reliable and would test less.

Result: **17/17 in CI with no reruns consumed, 2m26s** — down from 23m51s, since
a dropped interaction is dropped instantly and no longer burns the full timeout
before escalating.

### CI timeouts and reruns

The system under test is a live third-party site, so the suite is only as fast
as the network to it. `SELENIUM_TIMEOUT=45` and `--reruns 1` are CI-only
concessions for that latency; neither is used locally, and neither is what makes
the suite pass.

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `selenium` | 4.x | WebDriver browser automation |
| `pytest` | 8.x | Test runner + fixtures |
| `pytest-html` | 4.x | HTML failure reports with screenshots |

---

## 👤 About

**Oscar Leung** — 5+ years QA Automation · Selenium · pytest · Playwright · Bay Area

> This suite demonstrates the same Page Object Model architecture I've used in production — at Maxar Technologies (spacecraft systems), State of Illinois (Salesforce automation), and Location Labs/Avast (AT&T carrier apps).

[![Portfolio](https://img.shields.io/badge/Portfolio-oscar--leung.github.io-38bdf8?style=flat-square)](https://oscar-leung.github.io)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/oscar-leung)
