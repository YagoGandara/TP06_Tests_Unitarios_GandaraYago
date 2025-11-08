import { expect, afterEach, vi } from 'vitest'
import * as matchers from '@testing-library/jest-dom/matchers'
import { cleanup } from '@testing-library/react'
import 'whatwg-fetch'

// Extiende los matchers de jest-dom sobre el expect de Vitest
expect.extend(matchers)

// Limpia el DOM entre tests
afterEach(() => {
  cleanup()
  vi.restoreAllMocks()
})
