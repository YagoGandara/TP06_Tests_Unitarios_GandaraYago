import { vi, it, expect, beforeEach } from 'vitest'
import { getTodos, createTodo, patchTodo, toggleTodo } from '../services/api'

beforeEach(() => {
  // @ts-ignore
  global.fetch = vi.fn()
})

it('GET /todos with params', async () => {
  // @ts-ignore
  fetch.mockResolvedValueOnce(new Response(JSON.stringify([{id:1,title:'a',status:'pending',priority:2,version:1}]), {status:200}))
  const data = await getTodos({ q: 'a', limit: 5 })
  expect(fetch).toHaveBeenCalledWith('/todos?q=a&limit=5', expect.any(Object))
  expect(data[0].title).toBe('a')
})

it('POST /todos create', async () => {
  // @ts-ignore
  fetch.mockResolvedValueOnce(new Response(JSON.stringify({id:1,title:'a',status:'pending',priority:2,version:1}), {status:200}))
  const created = await createTodo({ title: 'a' })
  expect(created.id).toBe(1)
})

it('PATCH /todos update', async () => {
  // @ts-ignore
  fetch.mockResolvedValueOnce(new Response(JSON.stringify({id:1,title:'b',status:'pending',priority:2,version:2}), {status:200}))
  const updated = await patchTodo(1, { title: 'b', version: 1 })
  expect(fetch).toHaveBeenCalledWith('/todos/1', expect.objectContaining({ method: 'PATCH' }))
  expect(updated.title).toBe('b')
})

it('POST /todos/{id}/toggle', async () => {
  // @ts-ignore
  fetch.mockResolvedValueOnce(new Response(JSON.stringify({id:1,title:'a',status:'done',priority:2,version:2}), {status:200}))
  const toggled = await toggleTodo(1)
  expect(fetch).toHaveBeenCalledWith('/todos/1/toggle', expect.objectContaining({ method: 'POST' }))
  expect(toggled.status).toBe('done')
})

it('request lanza si la respuesta no es ok (p.ej. 500)', async () => {
  // @ts-ignore
  fetch.mockResolvedValueOnce(new Response('boom', { status: 500 }))
  await expect(getTodos()).rejects.toThrow(/boom|Network/)
})