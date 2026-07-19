import { beforeAll, afterAll } from 'vitest';
import { execSync } from 'node:child_process';
import { prisma } from '../lib/prisma.js';

const TEST_DB_NAME = process.env.TEST_DB_NAME ?? 'voucher_test';
const TEST_DB_USER = process.env.TEST_DB_USER ?? 'postgres';
const TEST_DB_PASSWORD = process.env.TEST_DB_PASSWORD ?? 'postgres';
const TEST_DB_SCHEMA = process.env.TEST_DB_SCHEMA ?? 'public';
const TEST_DB_PORT = Number(process.env.TEST_DB_PORT ?? 5432);

// Ensure secrets exist so JWT verification in middleware/tests works.
process.env.JWT_ACCESS_SECRET =
  process.env.JWT_ACCESS_SECRET ?? 'test-access-secret-that-is-long-enough-for-tests';
process.env.JWT_REFRESH_SECRET =
  process.env.JWT_REFRESH_SECRET ?? 'test-refresh-secret-that-is-long-enough-for-tests';

// Use local Postgres by default. For thorough testing, the DB must be running.
const localDbUrl =
  process.env.DATABASE_URL ??
  `postgresql://${TEST_DB_USER}:${TEST_DB_PASSWORD}@localhost:${TEST_DB_PORT}/${TEST_DB_NAME}?schema=${TEST_DB_SCHEMA}`;

process.env.DATABASE_URL = localDbUrl;

const ensureDbIsReachable = async () => {
  try {
    await prisma.$queryRaw`SELECT 1`;
  } catch (err) {
    throw new Error(
      `Test database is not reachable at DATABASE_URL.\n` +
        `DATABASE_URL=${process.env.DATABASE_URL}\n` +
        `Please start a local PostgreSQL instance before running tests.`
    );
  }
};

beforeAll(async () => {
  await ensureDbIsReachable();

  // Ensure schema exists for the test DB (uses Prisma schema).
  execSync('npx prisma db push --force-reset', { stdio: 'inherit', env: process.env });

  // Seed baseline users.
  execSync('npx tsx prisma/seed.ts', { stdio: 'inherit', env: process.env });
});

afterAll(async () => {
  await prisma.$disconnect();
});
