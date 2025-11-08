import { it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from '../App'

it('renderiza el título', () => {
  render(<App />)
  expect(screen.getByText(/TP06 Front/i)).toBeInTheDocument()
})
