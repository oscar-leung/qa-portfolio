# Case study 01: Headless Chrome silently drops clicks

**Suite:** `selenium/` · **Files:** `selenium/pages/base_page.py`, `selenium/conftest.py`, `.github/workflows/ci.yml`

## Symptom

The four checkout tests in `selenium/tests/test_checkout.py` passed on a laptop
every time and failed only in GitHub Actions. The thirteen single-page tests
passed everywhere.

## What did not work

Three fixes built on the assumption that the CI runner was slow:

1. Raising `SELENIUM_TIMEOUT` from 10s to 45s.
2. Adding `--reruns 1` with a delay.
3. A session-scoped warm-up fixture that primed DNS, TLS, and the CDN before the first test.

Each made the runs longer without making them pass. The suite went from about
four minutes to 23m51s because every dropped interaction burned the full
timeout before failing.

## What settled it

`conftest.py` gained a `pytest_runtest_makereport` hook that, on failure, writes
the current URL, a screenshot, and the page source to `failure-artifacts/`, and
the workflow uploads that folder. One CI run later the artifacts showed a fully
rendered cart page, the Checkout button visible and unobscured, `.click()` having
raised nothing, and the page simply not navigated.

Nothing was slow. **Headless Chrome was silently dropping some native clicks and
keystrokes on this app.** The call returned success and nothing happened. The
same thing had already been worked around once, by hand, with a JS click in
`InventoryPage.logout()`.

## The fix

Two helpers in `BasePage`, both native-first:

- `click_until(click_locator, expect_locator)` clicks, waits briefly for the
  expected element, and escalates to a JS click only if it does not appear.
  The first wait is capped at 8s because a dropped click is dropped instantly.
- `type_text(...)` types with `send_keys`, confirms the value landed, and
  escalates to React's native value setter plus a bubbling `input` event.
  Assigning `.value` alone is not enough; React tracks its own value on the
  node and ignores it, which leaves the field looking filled while the form
  still refuses to submit.

Native-first ordering is deliberate. JS-clicking everything would be more
reliable and would test less.

## Result

| | Before | After |
|---|---|---|
| Checkout tests in CI | 0/4 | 4/4 |
| Suite in CI | 13/17, 23m51s | 17/17, 2m26s, no reruns consumed |

## What I would say in an interview

Timeouts are a symptom, not a diagnosis. The cheapest fix was to make the
failure observable before changing anything. The three timing fixes were each
reasonable in isolation and each wrong, because the premise was wrong.
