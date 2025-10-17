import { vi, it, expect, beforeEach } from 'vitest'
import { getTodos } from '../services/api'

beforeEach(() => {
  // @ts-ignore
  global.fetch = vi.fn()
})

it('GET /todos devuelve data', async () => {
  // @ts-ignore
  fetch.mockResolvedValueOnce(new Response(JSON.stringify([{id:1,title:'a'}]), {status:200}))
  const data = await getTodos()
  expect(fetch).toHaveBeenCalledWith('/todos', expect.any(Object))
  expect(data[0].title).toBe('a')
})
