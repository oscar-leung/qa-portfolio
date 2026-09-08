# Case study 02: A known bug as an expected failure, not a skipped test

**Suite:** `playwright/` · **File:** `playwright/tests/ui/known-bug.spec.ts`

## The bug

SauceDemo seeds a `problem_user` account with deliberate defects. One of them:
the inventory grid renders the same broken image source for all six products.
`standard_user` shows six distinct image sources; `problem_user` shows one,
repeated.

## The three ways to handle a known product bug in a suite

| Option | What the report shows | What happens when the bug is fixed |
|---|---|---|
| Delete the test | Nothing | Nobody notices |
| `test.skip()` | A grey skip that nobody reads | Nobody notices |
| `test.fail()` with the correct assertion | An expected failure, every run, with the reason | The test starts passing, and Playwright reports an unexpected pass as a failure |

The test asserts the **correct** behavior, that each product has its own image,
and is wrapped in `test.fail(true, reason)`. Today it fails as expected and the
report says why. The day SauceDemo fixes the seeded bug, the suite goes red and
someone has to look, which is exactly the point.

## Why it runs in the `login` project

The `authenticated` project reuses a saved `standard_user` session via
`storageState` so that thirty tests do not each log in through the UI. This
test needs a different user, so it lives in the unauthenticated project and
logs in itself. Auth reuse and "login is still tested" are not in tension when
the projects are split this way.

## What I would say in an interview

A test suite is documentation of what the product does and what it should do.
A skipped test documents neither. An expected failure documents both, and it
carries a tripwire for the fix.
