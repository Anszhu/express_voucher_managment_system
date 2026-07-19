import { beforeAll, describe, expect, it } from 'vitest';
import request from 'supertest';

let app: typeof import('./app.js').default;

beforeAll(async () => {
  process.env.DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/voucher_test?schema=public';
  process.env.JWT_ACCESS_SECRET = 'test-access-secret-that-is-long-enough-for-tests';
  process.env.JWT_REFRESH_SECRET = 'test-refresh-secret-that-is-long-enough-for-tests';
  ({ default: app } = await import('./app.js'));
});

describe('health endpoint', () => {
  it('returns operational metadata and a request id', async () => {
    const response = await request(app).get('/health');
    expect(response.status).toBe(200);
    expect(response.body).toMatchObject({ status: 'ok', environment: expect.any(String), version: expect.any(String), requestId: expect.any(String) });
  });
});
