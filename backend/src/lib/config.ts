import 'dotenv/config';
const required = (key: string, fallback?: string) => { const value = process.env[key] ?? fallback; if (!value) throw new Error(`Missing environment variable: ${key}`); return value; };
const validPort = (value: string) => { const port = Number(value); if (!Number.isInteger(port) || port < 1 || port > 65535) throw new Error('PORT must be a valid TCP port'); return port; };
const secret = (key: string) => { const value = required(key); if (value.length < 32) throw new Error(`${key} must be at least 32 characters`); return value; };
export const config = {
  env: process.env.NODE_ENV ?? 'development', port: validPort(process.env.PORT ?? '4000'), appVersion: process.env.APP_VERSION ?? '1.0.0',
  databaseUrl: required('DATABASE_URL'), accessSecret: secret('JWT_ACCESS_SECRET'), refreshSecret: secret('JWT_REFRESH_SECRET'),
  accessTtl: process.env.ACCESS_TOKEN_TTL ?? '15m', refreshTtl: process.env.REFRESH_TOKEN_TTL ?? '7d',
  corsOrigin: (process.env.CORS_ORIGIN ?? 'http://localhost:5173').split(',').map(origin => origin.trim()).filter(Boolean), maxUploadBytes: Number(process.env.MAX_UPLOAD_MB ?? 2) * 1024 * 1024
};
