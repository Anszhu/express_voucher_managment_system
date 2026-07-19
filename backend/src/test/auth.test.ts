import { describe, expect, it } from 'vitest';
import request from 'supertest';

import app from '../app.js';
import { prisma } from '../lib/prisma.js';

const login = async (email: string, password: string) => {
  const res = await request(app).post('/api/v1/auth/login').send({ email, password });
  return res;
};

describe('Auth API', () => {
  it('POST /api/v1/auth/login - returns tokens for valid credentials', async () => {
    const res = await login('employee@example.com', 'ChangeMe123!');
    expect(res.status).toBe(200);
    expect(res.body).toMatchObject({
      accessToken: expect.any(String),
      refreshToken: expect.any(String),
      user: expect.objectContaining({ email: 'employee@example.com' })
    });
  });

  it('POST /api/v1/auth/login - rejects invalid credentials', async () => {
    const res = await login('employee@example.com', 'wrong-password');
    expect(res.status).toBe(401);
    expect(res.body).toMatchObject({
      success: false,
      errorCode: 'UNAUTHENTICATED'
    });
  });

  it('GET /api/v1/auth/me - requires authentication', async () => {
    const res = await request(app).get('/api/v1/auth/me');
    expect(res.status).toBe(401);
    expect(res.body).toMatchObject({
      success: false,
      errorCode: 'UNAUTHENTICATED'
    });
  });

  it('GET /api/v1/auth/me - returns user for authenticated token', async () => {
    const loginRes = await login('employee@example.com', 'ChangeMe123!');
    const accessToken = loginRes.body.accessToken;

    const res = await request(app)
      .get('/api/v1/auth/me')
      .set('Authorization', `Bearer ${accessToken}`);

    expect(res.status).toBe(200);
    expect(res.body).toMatchObject({
      user: expect.objectContaining({
        email: 'employee@example.com',
        role: expect.any(String)
      })
    });
  });
});
