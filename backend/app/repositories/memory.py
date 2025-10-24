from __future__ import annotations
from datetime import date
from typing import List, Optional, Dict, Any

class InMemoryTodoRepo:
    def __init__(self):
        self._data: Dict[int, Dict[str, Any]] = {}
        self._seq = 0

    def _ensure_title_unique(self, title: str, skip_id: Optional[int]=None):
        for tid, item in self._data.items():
            if skip_id is not None and tid == skip_id:
                continue
            if item["title"].lower() == title.lower():
                raise ValueError("title already exists")

    async def create(self, data: Dict[str, Any]) -> dict:
        title = data["title"].strip()
        if data.get("priority") == 3 and not data.get("due_date"):
            raise ValueError("high priority items must have a due_date")
        self._ensure_title_unique(title)
        self._seq += 1
        item = {
            "id": self._seq,
            "title": title,
            "status": "pending",
            "priority": int(data.get("priority", 2)),
            "due_date": data.get("due_date"),
            "completed_at": None,
            "version": 1,
        }
        self._data[self._seq] = item
        return item.copy()

    async def get(self, todo_id: int) -> Optional[dict]:
        item = self._data.get(todo_id)
        return item.copy() if item else None

    async def list(self, *, status: Optional[str]=None, priority: Optional[int]=None,
                   q: Optional[str]=None, overdue: Optional[bool]=None,
                   limit: int = 50, offset: int = 0) -> List[dict]:
        items = list(self._data.values())
        if status:
            items = [x for x in items if x["status"] == status]
        if priority:
            items = [x for x in items if x["priority"] == int(priority)]
        if q:
            ql = q.lower()
            items = [x for x in items if ql in x["title"].lower()]
        if overdue is True:
            today = date.today()
            items = [x for x in items if x["due_date"] is not None and x["due_date"] < today and x["status"] != "done"]
        items = items[offset:offset+limit]
        return [x.copy() for x in items]

    async def update(self, todo_id: int, changes: Dict[str, Any]) -> Optional[dict]:
        current = self._data.get(todo_id)
        if not current:
            return None
        expected_version = changes.pop("version", None)
        if expected_version is None or expected_version != current["version"]:
            raise ValueError("version conflict")
        if "title" in changes and changes["title"] is not None:
            title = changes["title"].strip()
            self._ensure_title_unique(title, skip_id=todo_id)
            current["title"] = title
        if "priority" in changes and changes["priority"] is not None:
            pr = int(changes["priority"])
            if pr == 3 and not (changes.get("due_date") or current.get("due_date")):
                raise ValueError("high priority items must have a due_date")
            current["priority"] = pr
        if "due_date" in changes:
            current["due_date"] = changes["due_date"]
        if "status" in changes and changes["status"] is not None:
            st = changes["status"]
            allowed = {
                "pending": {"in_progress", "done"},
                "in_progress": {"pending", "done"},
                "done": set()
            }
            if st not in allowed[current["status"]]:
                raise ValueError("invalid status transition")
            current["status"] = st
            if st == "done":
                current["completed_at"] = date.today()
        current["version"] += 1
        return current.copy()

    async def delete(self, todo_id: int) -> bool:
        return self._data.pop(todo_id, None) is not None

    async def toggle(self, todo_id: int) -> Optional[dict]:
        current = self._data.get(todo_id)
        if not current:
            return None
        if current["status"] == "done":
            raise ValueError("cannot toggle a completed item")
        current["status"] = "done"
        current["completed_at"] = date.today()
        current["version"] += 1
        return current.copy()

    async def bulk_create(self, items: List[Dict[str, Any]]) -> List[dict]:
        created = []
        for d in items:
            created.append(await self.create(d))
        return created
