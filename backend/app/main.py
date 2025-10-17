from fastapi import FastAPI, Depends, HTTPException
from app.repositories.memory import InMemoryTodoRepo
from app.repositories.base import TodoRepo
from app.schemas.todo import TodoIn, TodoOut

app = FastAPI(title="TP06 API")

_repo = InMemoryTodoRepo()

def get_repo() -> TodoRepo:
    return _repo

@app.get("/admin/touch")
def touch():
    return {"ok": True}

@app.get("/todos", response_model=list[TodoOut])
async def list_todos(repo: TodoRepo = Depends(get_repo)):
    return await repo.list()

@app.get("/todos/{todo_id}", response_model=TodoOut)
async def get_todo(todo_id: int, repo: TodoRepo = Depends(get_repo)):
    item = await repo.get(todo_id)
    if not item:
        raise HTTPException(status_code=404, detail="not found")
    return item

@app.post("/todos", status_code=201, response_model=TodoOut)
async def create_todo(inp: TodoIn, repo: TodoRepo = Depends(get_repo)):
    created = await repo.create(inp.title)
    return created

@app.put("/todos/{todo_id}", response_model=TodoOut)
async def update_todo(todo_id: int, inp: TodoIn, repo: TodoRepo = Depends(get_repo)):
    item = await repo.update(todo_id, inp.title)
    if not item:
        raise HTTPException(status_code=404, detail="not found")
    return item

@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int, repo: TodoRepo = Depends(get_repo)):
    ok = await repo.delete(todo_id)
    if not ok:
        raise HTTPException(status_code=404, detail="not found")
