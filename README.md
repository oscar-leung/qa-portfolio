<div align="center">

<h1>QA Automation Portfolio</h1>

<p><strong>Two end-to-end suites against a live e-commerce demo, one in Selenium + pytest and one in Playwright + TypeScript, run every night in CI with the reports published for anyone to open.</strong></p>

[![CI](https://github.com/oscar-leung/qa-portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/oscar-leung/qa-portfolio/actions/workflows/ci.yml)
[![Nightly](https://github.com/oscar-leung/qa-portfolio/actions/workflows/nightly.yml/badge.svg)](https://github.com/oscar-leung/qa-portfolio/actions/workflows/nightly.yml)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

**[Last night's reports](https://oscar-leung.github.io/qa-portfolio/) · [Portfolio](https://oscar-leung.github.io) · [LinkedIn](https://linkedin.com/in/oscar-leung)**

</div>

---

## What is here

| Suite | Stack | Targets | Tests | Docs |
|---|---|---|---|---|
| [`selenium/`](selenium/) | Python 3.11, Selenium 4, pytest 8, Page Object Model | [saucedemo.com](https://www.saucedemo.com) | 17 (login, inventory, cart, checkout) | [selenium/README.md](selenium/README.md) |
| [`playwright/`](playwright/) | TypeScript, Playwright, Page Object Model, storageState auth reuse | saucedemo.com + [jsonplaceholder](https://jsonplaceholder.typicode.com) | 19 in CI across 4 projects (login, authenticated, api, setup); 26 with the optional firefox project | [playwright/README.md](playwright/README.md) |

Same application, two stacks on purpose. The Selenium suite is the architecture
I used in production at Maxar, the State of Illinois, and Location Labs/Avast.
The Playwright suite is the same coverage rebuilt with the tool most teams are
hiring for now, so the two can be compared line for line.

## Case studies

Things that went wrong and what fixing them taught. Each one links to the code.

1. **[Headless Chrome silently drops clicks](case-studies/01-headless-dropped-clicks.md)**. Four checkout tests passed locally and failed only in CI. Three timing "fixes" failed because nothing was slow. Failure artifacts settled it in one run; CI time dropped from 23m51s to 2m26s.
2. **[A known bug as an expected failure](case-studies/02-known-bug-as-expected-failure.md)**. SauceDemo's `problem_user` renders one broken image for every product. The test asserts the correct behavior and is marked `test.fail()`, so it shows up in every report and flips to a real failure the day the bug is fixed.

## How it runs

- **CI** (`.github/workflows/ci.yml`): both suites on every push and pull request, Chromium only, reports as build artifacts.
- **Nightly** (`.github/workflows/nightly.yml`): both suites at 06:00 UTC, then the two HTML reports and a generated index page are pushed to the `gh-pages` branch, which GitHub Pages serves. A red night publishes a red report; a stale green one would be worse.
- **One-time setup**: Settings, Pages, Build and deployment, Source: Deploy from a branch, branch `gh-pages`, folder `/ (root)`, Save. The branch exists after the first nightly run.
- The system under test is a live third-party site, so CI runs use one retry and a longer Selenium timeout. Neither is used locally, and neither is what makes the suites pass.

## Run locally

```bash
# Selenium + pytest
cd selenium && pip install -r requirements.txt && pytest            # add --headless for CI mode

# Playwright + TypeScript
cd playwright && npm ci && npx playwright install --with-deps chromium && npx playwright test
```

## About

**Oscar Leung**, QA / SDET, 5+ years. Selenium, Playwright, pytest, CI/CD, and
LLM output evaluation. Davis, CA. Open to remote roles in the US.
