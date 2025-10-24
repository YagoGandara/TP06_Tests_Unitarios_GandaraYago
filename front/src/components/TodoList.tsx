import React, { useEffect, useState } from 'react'
import { getTodos, createTodo, toggleTodo, type Todo } from '../services/api'

export function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([])
  const [title, setTitle] = useState('')
  const [error, setError] = useState<string | null>(null)

  async function refresh() {
    try {
      const data = await getTodos()
      setTodos(data)
    } catch (e:any) {
      setError('Error loading todos')
    }
  }

  useEffect(() => { refresh() }, [])

  async function onAdd() {
    setError(null)
    try {
      const created = await createTodo({ title })
      setTodos([...todos, created])
      setTitle('')
    } catch (e:any) {
      setError('Error creating todo')
    }
  }

  async function onToggle(id: number) {
    try {
      const updated = await toggleTodo(id)
      setTodos(todos.map(t => t.id === id ? updated : t))
    } catch (e:any) {
      setError('Error toggling')
    }
  }

  return (
    <div>
      {error && <div role="alert">{error}</div>}
      <input aria-label="title" value={title} onChange={e=>setTitle(e.target.value)} />
      <button onClick={onAdd}>Add</button>
      <ul>
        {todos.map(t => (
          <li key={t.id}>
            <span>{t.title} [{t.status}]</span>
            {t.status !== 'done' && <button onClick={()=>onToggle(t.id)}>Done</button>}
          </li>
        ))}
      </ul>
    </div>
  )
}
