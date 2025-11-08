import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./setupTests.ts'],
    reporters: ['default', ['junit', { outputFile: './test-results/test-results.xml' }]],
    coverage: { reporter: ['text', 'lcov', 'cobertura'], lines: 80, functions: 80, branches: 70 }
  }
})
