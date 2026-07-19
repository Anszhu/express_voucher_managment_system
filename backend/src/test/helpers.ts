import request from 'supertest';
import app from '../app.js';

export const login = async (email: string, password: string) => {
  const res = await request(app).post('/api/v1/auth/login').send({ email, password });
  return res;
};

export const authHeader = async (email: string, password: string) => {
  const res = await login(email, password);
  if (res.status !== 200) throw new Error(`Login failed for ${email}: ${res.status} ${JSON.stringify(res.body)}`);
  return { Authorization: `Bearer ${res.body.accessToken}` };
};

export const createVoucher = async (
  token: string,
  payload: {
    expenseTitle: string;
    category: string;
    department: string;
    amount: number;
    expenseDate: string;
    description?: string;
  }
) => {
  const res = await request(app).post('/api/v1/vouchers').set('Authorization', `Bearer ${token}`).send(payload);
  return res;
};

export const parseAccessTokenFromLogin = (loginResponseBody: any): string => {
  if (!loginResponseBody?.accessToken) throw new Error('Missing accessToken in login response');
  return String(loginResponseBody.accessToken);
};
