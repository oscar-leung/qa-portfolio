import { defineConfig, devices } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  reporter: [['html', { open: 'never' }], ['list']],

  use: {
    baseURL: 'https://www.saucedemo.com',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    // Runs first: logs in once, saves the session to disk.
    {
      name: 'setup',
      testMatch: /auth\.setup\.ts/,
    },

    // Login itself is the thing under test here, so this project runs
    // logged-out, with no dependency on "setup" and no storageState.
    {
      name: 'login',
      testMatch: ['**/login.spec.ts', '**/known-bug.spec.ts'],
      use: { ...devices['Desktop Chrome'] },
    },

    // Everything that assumes an already-logged-in user. Depends on
    // "setup" so it always has a fresh session before it runs.
    {
      name: 'authenticated',
      testMatch: ['**/inventory.spec.ts', '**/cart-checkout.spec.ts'],
      use: { ...devices['Desktop Chrome'], storageState: authFile },
      dependencies: ['setup'],
    },

    // Pure HTTP tests - no browser, no storageState, different base URL,
    // so it gets its own project rather than reusing the UI ones above.
    {
      name: 'api',
      testMatch: ['**/api/**'],
      use: { baseURL: 'https://jsonplaceholder.typicode.com' },
    },

    // Configured but not run in CI by default (see the workflow file) -
    // available locally as proof that cross-browser coverage is one flag
    // away, without tripling every CI run's runtime.
    {
      name: 'firefox',
      testMatch: ['**/inventory.spec.ts', '**/cart-checkout.spec.ts'],
      use: { ...devices['Desktop Firefox'], storageState: authFile },
      dependencies: ['setup'],
    },
  ],
});
