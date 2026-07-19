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
      thresholds: {
        statements: 90,
        functions: 90,
        lines: 90,
        branches: 85
      }
    }
  }
});
