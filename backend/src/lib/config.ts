import 'dotenv/config';
const required = (key: string, fallback?: string) => { const value = process.env[key] ?? fallback; if (!value) throw new Error(`Missing environment variable: ${key}`); return value; };
export const config = {
  env: process.env.NODE_ENV ?? 'development', port: Number(process.env.PORT ?? 4000),
  databaseUrl: required('DATABASE_URL'), accessSecret: required('JWT_ACCESS_SECRET'), refreshSecret: required('JWT_REFRESH_SECRET'),
  accessTtl: process.env.ACCESS_TOKEN_TTL ?? '15m', refreshTtl: process.env.REFRESH_TOKEN_TTL ?? '7d',
  corsOrigin: (process.env.CORS_ORIGIN ?? 'http://localhost:5173').split(','), maxUploadBytes: Number(process.env.MAX_UPLOAD_MB ?? 2) * 1024 * 1024
};
