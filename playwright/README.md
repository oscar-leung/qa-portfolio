# QA Portfolio — Playwright + TypeScript

End-to-end and API test automation suite built with [Playwright](https://playwright.dev) and TypeScript, using the Page Object Model. Runs against [Sauce Demo](https://www.saucedemo.com) (UI) and [jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com) (API) — both free, publicly available services intended for test automation practice.

[![CI](https://github.com/oscar-leung/qa-portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/oscar-leung/qa-portfolio/actions/workflows/ci.yml)

Part of [oscar-leung/qa-portfolio](../README.md); the sibling Selenium + pytest suite lives in [`../selenium/`](../selenium/).

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

Every push and PR runs the `setup`, `login`, `authenticated`, and `api` projects on Chromium via the repo-level workflow (`../.github/workflows/ci.yml`) and uploads the HTML report as an artifact. The nightly workflow (`../.github/workflows/nightly.yml`) runs the same projects and publishes the report to [oscar-leung.github.io/qa-portfolio](https://oscar-leung.github.io/qa-portfolio/). Firefox is configured and verified locally but not run in CI, to keep runs fast.
