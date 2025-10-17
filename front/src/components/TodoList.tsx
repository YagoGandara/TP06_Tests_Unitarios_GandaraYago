import React, { useEffect, useState } from 'react'
import { getTodos } from '../services/api'

export function TodoList() {
  const [todos, setTodos] = useState<{id:number,title:string}[]>([])
  useEffect(() => {
    getTodos().then(setTodos).catch(() => setTodos([]))
  }, [])
  return (
    <ul>
      {todos.map(t => <li key={t.id}>{t.title}</li>)}
    </ul>
  )
}
