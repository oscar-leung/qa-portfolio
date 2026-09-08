# CLAUDE.md

## What this repo is

Oscar's public QA portfolio: two test suites (selenium/, playwright/) against
live demo sites, run nightly in CI with reports published to GitHub Pages.
Everything in here is meant to be read by a hiring manager. It is not a
sandbox; experiments go in the claude-code-workspace repo.

## How to work here

- Run the suite you touched before pushing. Targets are live third-party
  sites, so expect network variance; a failure is still a failure until you
  have read the trace or the failure artifact.
- `cd selenium && pytest --headless` and `cd playwright && npx tsc --noEmit && npx playwright test`.
- Branches: `claude/<topic>-<id>` for agent work. Draft PRs; Oscar merges.
- Never skip, quarantine, or delete a test to get green. A known product bug
  is recorded with `test.fail()` / `xfail` and a case study, never removed.
- Never commit credentials. The demo sites use public test accounts only.

## Layout

```
selenium/      Python: pages/, tests/, conftest.py, pytest.ini, requirements.txt
playwright/    TypeScript: pages/, tests/ui, tests/api, playwright.config.ts
case-studies/  one Markdown file per investigation, linked from README
.github/workflows/  ci.yml (push/PR), nightly.yml (schedule + Pages publish)
.github/scripts/    build-report-index.sh builds the Pages index
```

## Conventions

- Page Object Model in both suites; tests never touch raw selectors.
- Prefer the app's `data-test` hooks over class names or text.
- Native user actions first; escalate to JS only when the outcome does not
  appear, and say so in a comment (see case study 01).
- New investigation worth remembering: add `case-studies/NN-slug.md` and a
  README bullet in the same PR.
