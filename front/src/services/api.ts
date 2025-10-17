export async function getTodos() {
  const res = await fetch('/todos', { headers: { 'Accept': 'application/json' }})
  if (!res.ok) throw new Error('Network')
  return await res.json()
}
