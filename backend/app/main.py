from __future__ import annotations
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, Query
from app.repositories.memory import InMemoryTodoRepo
from app.repositories.base import TodoRepo
from app.schemas.todo import TodoIn, TodoOut, TodoUpdate, Status, Priority

app = FastAPI(title="TP06 API (Advanced)")

_repo = InMemoryTodoRepo()
def get_repo() -> TodoRepo:
    return _repo

@app.get("/admin/touch")
def touch():
    return {"ok": True}

@app.get("/todos", response_model=List[TodoOut])
async def list_todos(
    status: Optional[Status] = Query(None),
    priority: Optional[Priority] = Query(None),
    q: Optional[str] = Query(None),
    overdue: Optional[bool] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    repo: TodoRepo = Depends(get_repo),
):
    return await repo.list(status=status.value if status else None,
                           priority=int(priority) if priority else None,
                           q=q, overdue=overdue, limit=limit, offset=offset)

@app.get("/todos/{todo_id}", response_model=TodoOut)
async def get_todo(todo_id: int, repo: TodoRepo = Depends(get_repo)):
    item = await repo.get(todo_id)
    if not item:
        raise HTTPException(status_code=404, detail="not found")
    return item

@app.post("/todos", status_code=201, response_model=TodoOut)
async def create_todo(inp: TodoIn, repo: TodoRepo = Depends(get_repo)):
    try:
        created = await repo.create(inp.model_dump())
        return created
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.patch("/todos/{todo_id}", response_model=TodoOut)
async def patch_todo(todo_id: int, changes: TodoUpdate, repo: TodoRepo = Depends(get_repo)):
    try:
        item = await repo.update(todo_id, changes.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=409 if "version" in str(e) else 400, detail=str(e))
    if not item:
        raise HTTPException(status_code=404, detail="not found")
    return item

@app.post("/todos/{todo_id}/toggle", response_model=TodoOut)
async def toggle_todo(todo_id: int, repo: TodoRepo = Depends(get_repo)):
    try:
        item = await repo.toggle(todo_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not item:
        raise HTTPException(status_code=404, detail="not found")
    return item

@app.post("/todos/bulk", response_model=List[TodoOut])
async def bulk_create(items: List[TodoIn], repo: TodoRepo = Depends(get_repo)):
    try:
        data = [i.model_dump() for i in items]
        created = await repo.bulk_create(data)
        return created
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int, repo: TodoRepo = Depends(get_repo)):
    ok = await repo.delete(todo_id)
    if not ok:
        raise HTTPException(status_code=404, detail="not found")
