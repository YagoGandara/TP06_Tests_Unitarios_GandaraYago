export type Todo = {
  id: number
  title: string
  status: 'pending' | 'in_progress' | 'done'
  priority: 1 | 2 | 3
  due_date?: string | null
  completed_at?: string | null
  version: number
}

async function request(input: RequestInfo, init?: RequestInit) {
  const res = await fetch(input, { headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' }, ...init })
  if (!res.ok) throw new Error(await res.text() || 'Network')
  return res
}

export async function getTodos(params?: { q?: string; status?: string; priority?: number; overdue?: boolean; limit?: number; offset?: number }): Promise<Todo[]> {
  const q = new URLSearchParams()
  if (params) Object.entries(params).forEach(([k,v]) => v!==undefined && q.append(k, String(v)))
  const res = await request(`/todos${q.toString() ? `?${q.toString()}` : ''}`)
  return res.json()
}

export async function createTodo(data: { title: string; priority?: number; due_date?: string }) {
  const res = await request(`/todos`, { method: 'POST', body: JSON.stringify(data) })
  return res.json() as Promise<Todo>
}

export async function patchTodo(id: number, changes: Partial<Pick<Todo,'title'|'status'|'priority'|'due_date'>> & { version: number }) {
  const res = await request(`/todos/${id}`, { method: 'PATCH', body: JSON.stringify(changes) })
  return res.json() as Promise<Todo>
}

export async function toggleTodo(id: number) {
  const res = await request(`/todos/${id}/toggle`, { method: 'POST' })
  return res.json() as Promise<Todo>
}
