import { test, expect } from '@playwright/test';

/**
 * API-only tests using Playwright's built-in `request` fixture - no browser
 * involved at all, just HTTP calls. Runs against jsonplaceholder.typicode.com,
 * a free fake REST API with no auth required.
 *
 * Note: this project originally targeted reqres.in, a similarly well-known
 * practice API - but reqres.in now requires a signed-up API key, discovered
 * while building this. Swapped to jsonplaceholder.typicode.com instead of
 * signing up for a key, since the point of this suite is to demonstrate API
 * testing patterns, not to depend on a specific provider.
 */
test.describe('Posts API', () => {
  test('GET a single post returns the expected shape', async ({ request }) => {
    const response = await request.get('/posts/1');
    expect(response.status()).toBe(200);

    const body = await response.json();
    expect(body).toMatchObject({
      id: 1,
      userId: expect.any(Number),
      title: expect.any(String),
      body: expect.any(String),
    });
  });

  test('GET the posts collection returns a non-empty array', async ({ request }) => {
    const response = await request.get('/posts');
    expect(response.status()).toBe(200);

    const body = await response.json();
    expect(Array.isArray(body)).toBe(true);
    expect(body.length).toBeGreaterThan(0);
  });

  test('GET a non-existent post returns 404', async ({ request }) => {
    const response = await request.get('/posts/999999');
    expect(response.status()).toBe(404);
  });

  test('POST creates a new post and echoes the payload back', async ({ request }) => {
    const payload = { title: 'QA portfolio test post', body: 'created via Playwright', userId: 1 };
    const response = await request.post('/posts', { data: payload });
    expect(response.status()).toBe(201);

    const body = await response.json();
    expect(body).toMatchObject(payload);
    expect(body.id).toBeDefined();
  });

  test('PUT updates an existing post', async ({ request }) => {
    const response = await request.put('/posts/1', {
      data: { id: 1, title: 'updated title', body: 'updated body', userId: 1 },
    });
    expect(response.status()).toBe(200);

    const body = await response.json();
    expect(body.title).toBe('updated title');
  });

  test('DELETE removes a post', async ({ request }) => {
    const response = await request.delete('/posts/1');
    expect(response.status()).toBe(200);
  });
});
