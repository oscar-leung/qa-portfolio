# Study Guide — QA Portfolio Project

Read this end to end once, then skim it again the morning of an interview. Everything here maps to an actual file in the repo — if a question stumps you, go open that file and look at it while you think.

---

## 1. The 30-second pitch (memorize this)

> "I built a Playwright/TypeScript test suite against Sauce Demo, a site built for automation practice — login, inventory, cart, and checkout flows, plus an API test suite against a REST API. It uses the Page Object Model, reuses login sessions across tests instead of logging in every time, and runs in GitHub Actions on every push. It's 26 tests across four test projects, and I also documented a real UI bug I found rather than just writing happy-path tests."

That's it. Everything below is ammunition for follow-up questions.

---

## 2. Why these choices were made

**Why Sauce Demo?** It's purpose-built for automation practice, so it has realistic complexity (multiple user types with different behaviors, form validation, multi-step checkout) without needing permission to automate against it the way a real production site would require.

**Why Playwright over Selenium?** You already have Selenium experience from Maxar and State of Illinois — this project is about being able to speak to *both*. The honest answer if asked "why did you learn Playwright": auto-waiting (Playwright waits for elements to be actionable before interacting, instead of you writing explicit waits/sleeps everywhere), built-in test runner and assertions (Selenium needs a separate framework like pytest/JUnit bolted on), and it's what more job postings are asking for now.

**Why TypeScript instead of JavaScript?** Type safety on page objects and fixtures — if you rename a method or change what a function returns, TypeScript flags every broken call site at compile time instead of you discovering it when a test fails at runtime. It also gives you autocomplete on locators and methods, which matters more as a suite grows.

**Why Page Object Model?** One class per page/flow (`LoginPage`, `InventoryPage`, `CartPage`, `CheckoutPage`), each owning its own locators and actions. If Sauce Demo changes a selector, you fix it in one file instead of hunting through every test. Tests end up reading like plain steps: `loginPage.login(...)`, `inventory.addToCart(...)`.

**Why did the API testing target change mid-project?** The original plan was reqres.in, a well-known practice API. While building, I found it now requires a signed-up API key — a real, current fact about that service, not something I assumed. Rather than sign up for a key for a portfolio project, I switched to jsonplaceholder.typicode.com, a comparable no-auth practice API. **This is worth mentioning in an interview unprompted** — it's a genuine example of verifying a dependency's current state instead of trusting stale docs, which is exactly the instinct QA work depends on.

---

## 3. Concepts you need to be able to explain

### Page Object Model (POM)
A design pattern that separates *how to interact with a page* (locators, low-level actions) from *what a test is verifying* (assertions, business logic). Look at `pages/LoginPage.ts` — it exposes `login(username, password)`, not raw `page.fill(...)` calls. The test file just calls that method and asserts on the outcome.

### `storageState` / auth reuse
Logging in through the UI before every single test is slow and repetitive. Playwright can save a browser's cookies + localStorage to a JSON file after logging in once (`tests/auth.setup.ts` does this), and every subsequent test can load that file instead of repeating the login flow. Look at `playwright.config.ts` — the `authenticated` project has `storageState: authFile` and `dependencies: ['setup']`, meaning "run the setup project first, then use what it saved."

**Likely follow-up: "But doesn't that mean you're not testing login?"** Good catch if they ask — that's *why* `login.spec.ts` deliberately runs in its own separate project with no stored state at all. Login itself is fully tested elsewhere; the `authenticated` project just doesn't re-test it on every single test.

### Playwright "projects"
A project is a named configuration — which browser, which base URL, which tests to run, what auth state to use. This suite has four: `setup` (logs in), `login` (unauthenticated tests), `authenticated` (everything that needs to already be logged in), and `api` (pure HTTP, no browser). `firefox` is a fifth, same tests as `authenticated` but a different browser engine — proof cross-browser coverage is one config entry away, not a rewrite.

### `test.fail()` — documenting a known bug without a red build
Sauce Demo's `problem_user` shows the same broken image for every product — a real, seeded bug. `tests/ui/known-bug.spec.ts` writes a test that asserts the *correct* behavior (each product has its own image), which fails today because of the bug. `test.fail()` marks that as an *expected* failure. Two things that gives you: the report still shows the test executed (instead of skipping it and losing visibility), and if the bug is ever fixed, the test starts unexpectedly *passing*, which Playwright flags — so a fix wouldn't go unnoticed.

**This is one of the strongest talking points in the whole project.** Most people asked to "find a bug" just write it up in a doc. Encoding it as a test that tracks its own status over time is a level up, and it's a natural thing to walk an interviewer through.

### API testing with Playwright's `request` fixture
Playwright isn't just a browser tool — `tests/api/posts.spec.ts` makes raw HTTP calls (GET/POST/PUT/DELETE) with no browser involved at all, using the same `expect()` assertions as the UI tests. Useful to know: this is *why* it's a separate project in the config — it needs a different `baseURL` than the UI tests, and there's no reason to spin up a browser for it.

### Why only Chromium runs in CI by default
Running every browser on every push/PR adds real minutes to every CI run for marginal extra confidence most of the time. The pattern here — fast browser on every push, full cross-browser matrix available on demand — is a genuine, common real-world tradeoff, not a shortcut. If asked "would you run Firefox and WebKit in CI too," a good answer is "yes, on a schedule or before a release, not on every single push."

### Why `playwright/.auth/` is gitignored
It contains real session data (cookies/localStorage). Even for a throwaway demo-site login, committing session/credential data to source control is a bad habit to practice — so it's excluded on principle, the same as you'd exclude it on a real project with real user data.

---

## 4. File-by-file map

| File | What it's for |
|---|---|
| `playwright.config.ts` | Defines the 5 projects and how they relate (dependencies, auth state, base URLs) |
| `tests/auth.setup.ts` | Logs in once, saves the session |
| `tests/ui/login.spec.ts` | Login flow — valid, invalid, locked-out, empty-field |
| `tests/ui/inventory.spec.ts` | Sorting, add-to-cart |
| `tests/ui/cart-checkout.spec.ts` | Cart removal, checkout validation, full purchase flow |
| `tests/ui/known-bug.spec.ts` | The documented `problem_user` image defect |
| `tests/api/posts.spec.ts` | API CRUD tests, no browser |
| `pages/*.ts` | Page Object classes — one per page/flow |
| `.github/workflows/playwright.yml` | CI: installs deps, runs tests, uploads the HTML report |

---

## 5. Likely interview questions, mapped to this project

- **"Walk me through a test automation project you've built."** → Use the 30-second pitch, then let them steer into whichever part they want more on.
- **"How do you handle authentication in your test suite?"** → `storageState` pattern, and *why* login itself still gets tested separately.
- **"How do you avoid flaky tests?"** → Playwright's auto-waiting (no manual sleeps), plus this config's `retries: 2` in CI specifically (not locally) to absorb network flakiness without masking a real bug on your own machine.
- **"Why TypeScript for test automation?"** → Compile-time safety on page objects, autocomplete, catches broken refactors before you run anything.
- **"Tell me about a bug you found."** → The `problem_user` image defect — what it was, how you noticed it (comparing image src uniqueness against `standard_user` as a baseline), and how you encoded it as a test instead of just a bug report.
- **"How would you scale this to a bigger suite?"** → More projects/tags for smoke vs. full regression, sharding tests across CI runners, visual regression testing, containerizing with Docker for environment consistency.
- **"What would you add if you had more time?"** → Visual regression snapshots, running Firefox/WebKit on a schedule, a Slack or email notification on CI failure, testing against a staging environment instead of a public demo site.

---

## 6. One honest note

If an interviewer asks how you built this and you want to mention AI assistance — plenty of engineers now build portfolio projects this way, and it's not something to hide. What actually matters is that you can explain *why* each piece exists, not just that you typed it. Everything in this guide is the "why." If you can answer the questions in section 5 in your own words without reading off this page, you're ready.
