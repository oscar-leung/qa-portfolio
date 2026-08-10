# QA Portfolio — Playwright + TypeScript

End-to-end and API test automation suite built with [Playwright](https://playwright.dev) and TypeScript, using the Page Object Model. Runs against [Sauce Demo](https://www.saucedemo.com) (UI) and [jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com) (API) — both free, publicly available services intended for test automation practice.

![Playwright Tests](https://github.com/oscar-leung/qa-portfolio/actions/workflows/playwright.yml/badge.svg)

## What's covered

- **Login** — valid credentials, locked-out user, wrong password, empty-field validation
- **Inventory** — sorting (price and name), add-to-cart, cart badge state
- **Cart & checkout** — item removal, form validation, full happy-path purchase
- **A documented UI defect** — `problem_user` renders a duplicate broken image for every product; captured as an expected-failure test via `test.fail()` rather than skipped or silently ignored
- **API** — GET/POST/PUT/DELETE against a REST API, including a 404 case

26 tests total across 4 Playwright projects (`setup`, `login`, `authenticated`, `api`), plus a `firefox` project configured for cross-browser coverage on demand.

## Why it's structured this way

- **Page Object Model** (`/pages`) — one class per page/flow, so a selector change only needs updating in one place, and tests read like plain English steps instead of raw locator calls.
- **Auth reuse via `storageState`** (`tests/auth.setup.ts`) — logs in once, saves the session, and every test in the `authenticated` project starts already logged in. Login itself still gets fully tested — it just runs in its own project (`login`) that intentionally has no stored session.
- **Separate `api` project** — pure HTTP checks via Playwright's `request` fixture, no browser involved, pointed at a different `baseURL` than the UI projects.

Full reasoning behind these decisions — and the interview questions they map to — is in [`STUDY_GUIDE.md`](./STUDY_GUIDE.md).

## Running it locally

```bash
npm install
npx playwright install --with-deps chromium   # add "firefox" too if you want that project
npx playwright test
npx playwright show-report                     # view the HTML report
```

Run a single project:

```bash
npx playwright test --project=login
```

## CI

Every push/PR to `main` runs the `setup`, `login`, `authenticated`, and `api` projects on Chromium via GitHub Actions (`.github/workflows/playwright.yml`) and uploads the HTML report as a build artifact. Firefox is configured and verified locally but not run on every push, to keep CI fast — see the workflow file for the exact command to add it.
