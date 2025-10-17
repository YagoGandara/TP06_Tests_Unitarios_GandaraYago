import { render, screen, waitFor } from '@testing-library/react'
import { vi } from 'vitest'
import { TodoList } from '../components/TodoList'

it('muestra items recibidos', async () => {
  // @ts-ignore
  global.fetch = vi.fn().mockResolvedValueOnce(new Response(JSON.stringify([{id:1,title:'a'}]), {status:200}))

  render(<TodoList />)
  await waitFor(() => expect(screen.getByText('a')).toBeInTheDocument())
})
