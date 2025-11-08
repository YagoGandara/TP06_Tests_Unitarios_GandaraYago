import { it, expect, vi } from 'vitest'
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import { TodoList } from '../components/TodoList'

it('adds and toggles items', async () => {
  // @ts-ignore
  global.fetch = vi.fn()
    .mockResolvedValueOnce(new Response(JSON.stringify([]), {status:200})) // getTodos
    .mockResolvedValueOnce(new Response(JSON.stringify({id:1,title:'a',status:'pending',priority:2,version:1}), {status:200})) // create
    .mockResolvedValueOnce(new Response(JSON.stringify({id:1,title:'a',status:'done',priority:2,version:2}), {status:200})) // toggle

  render(<TodoList />)

  await waitFor(() => expect(screen.queryByRole('alert')).toBeNull())

  const input = screen.getByLabelText('title')
  fireEvent.change(input, { target: { value: 'a' } })
  fireEvent.click(screen.getByText('Add'))
  await waitFor(() => screen.getByText(/a \[pending\]/))

  fireEvent.click(screen.getByText('Done'))
  await waitFor(() => screen.getByText(/a \[done\]/))
})

it('handles fetch error on load', async () => {
  // @ts-ignore
  global.fetch = vi.fn().mockResolvedValueOnce(new Response('boom', {status:500}))
  render(<TodoList />)
  await waitFor(() => screen.getByRole('alert'))
  expect(screen.getByRole('alert')).toHaveTextContent('Error loading todos')
})

it('muestra error si falla crear (POST /todos 400)', async () => {
  // GET inicial vacío
  // @ts-ignore
  global.fetch = vi.fn()
    .mockResolvedValueOnce(new Response(JSON.stringify([]), { status: 200 }))
    // create falla con 400
    .mockResolvedValueOnce(new Response('bad request', { status: 400 }))

  render(<TodoList />)

  // sin error al cargar
  await waitFor(() => expect(screen.queryByRole('alert')).toBeNull())

  // intento de crear -> 400
  const input = screen.getByLabelText('title')
  fireEvent.change(input, { target: { value: 'x' } })
  fireEvent.click(screen.getByText('Add'))

  // se muestra el error de creación (cubre setError en catch de onAdd)
  await waitFor(() => screen.getByRole('alert'))
  expect(screen.getByRole('alert')).toHaveTextContent('Error creating todo')
})

it('no muestra botón Done cuando el item ya está done', async () => {
  // GET devuelve un item ya "done"
  // @ts-ignore
  global.fetch = vi.fn()
    .mockResolvedValueOnce(new Response(JSON.stringify([
      { id: 1, title: 'hecha', status: 'done', priority: 2, version: 1 }
    ]), { status: 200 }))

  render(<TodoList />)

  // aparece la tarea con estado [done]
  await waitFor(() => screen.getByText(/hecha \[done\]/i))

  // NO debería estar el botón Done (cubre rama condicional del render)
  expect(screen.queryByText('Done')).toBeNull()
})

it('muestra error si falla el toggle (POST /todos/{id}/toggle 400)', async () => {
  // GET inicial con un item pendiente
  // @ts-ignore
  global.fetch = vi.fn()
    .mockResolvedValueOnce(new Response(JSON.stringify([
      { id: 1, title: 'fallará', status: 'pending', priority: 2, version: 1 }
    ]), { status: 200 }))
    // toggle falla con 400
    .mockResolvedValueOnce(new Response('toggle error', { status: 400 }))

  render(<TodoList />)

  // aparece el item pendiente
  await waitFor(() => screen.getByText(/fallará \[pending\]/i))

  // intento de marcar como done -> 400
  fireEvent.click(screen.getByText('Done'))

  // se muestra el error de toggle (cubre setError en catch de onToggle)
  await waitFor(() => screen.getByRole('alert'))
  expect(screen.getByRole('alert')).toHaveTextContent('Error toggling')
})