# Selenium + pytest suite

End-to-end coverage of [saucedemo.com](https://www.saucedemo.com) with Selenium 4,
pytest 8, and the Page Object Model. 17 tests: login, inventory, cart, checkout.

```
selenium/
├── pages/
│   ├── base_page.py        shared waits, click_until, type_text (see case study 01)
│   ├── login_page.py
│   ├── inventory_page.py
│   └── cart_page.py        CartPage and CheckoutPage
├── tests/
│   ├── test_login.py       6 tests
│   ├── test_inventory.py   7 tests
│   └── test_checkout.py    4 tests
├── conftest.py             driver fixture, logged_in_driver, failure artifacts
├── pytest.ini
└── requirements.txt
```

## Run

```bash
pip install -r requirements.txt
pytest                      # headed, local Chrome
pytest --headless           # CI mode (or HEADLESS=true)
pytest --html=report.html --self-contained-html
pytest tests/test_login.py -v
```

`SELENIUM_TIMEOUT` (default 10) raises the explicit-wait ceiling; CI sets 45
because the target is a live site on a cold runner. There is no implicit wait
on purpose: mixing it with `WebDriverWait` makes every negative lookup block for
the implicit timeout and can burn the whole explicit budget on a healthy page.

## Failure artifacts

On any failure `conftest.py` writes the URL, a screenshot, and the page source
to `failure-artifacts/`, and CI uploads the folder. This is what turned a
three-attempt timing mystery into a one-run diagnosis; the full story is in
[case-studies/01-headless-dropped-clicks.md](../case-studies/01-headless-dropped-clicks.md).
