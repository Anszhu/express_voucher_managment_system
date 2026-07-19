import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'node',
    setupFiles: ['./src/test/vitest.setup.ts'],
    passWithNoTests: false,
    testTimeout: 30000,
    coverage: {
      all: true,
      reporter: ['text', 'html', 'lcov'],
      provider: 'v8',
      exclude: ['prisma.config.ts'],
      thresholds: {
        statements: 60,
        functions: 20,
        lines: 60,
        branches: 40
      }
    }
  }
});
