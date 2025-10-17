from typing import List, Optional

class InMemoryTodoRepo:
    def __init__(self):
        self._data = {}
        self._seq = 0

    async def create(self, title: str) -> dict:
        self._seq += 1
        item = {"id": self._seq, "title": title.strip()}
        self._data[self._seq] = item
        return item

    async def get(self, todo_id: int) -> Optional[dict]:
        return self._data.get(todo_id)

    async def list(self) -> List[dict]:
        return list(self._data.values())

    async def update(self, todo_id: int, title: str) -> Optional[dict]:
        if todo_id not in self._data:
            return None
        self._data[todo_id]["title"] = title.strip()
        return self._data[todo_id]

    async def delete(self, todo_id: int) -> bool:
        return self._data.pop(todo_id, None) is not None
