from __future__ import annotations
from enum import Enum
from typing import Optional
from datetime import date
from pydantic import BaseModel, field_validator

class Status(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

class Priority(int, Enum):
    low = 1
    medium = 2
    high = 3

class TodoIn(BaseModel):
    title: str
    priority: Priority = Priority.medium
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def not_empty(cls, v: str):
        if not v or not v.strip():
            raise ValueError("title is required")
        v = v.strip()
        if len(v) > 100:
            raise ValueError("title too long (max 100)")
        return v

    @field_validator("due_date")
    @classmethod
    def valid_due_date(cls, v: Optional[date]):
        if v is not None and v < date.today():
            raise ValueError("due_date cannot be in the past")
        return v

class TodoOut(BaseModel):
    id: int
    title: str
    status: Status
    priority: Priority
    due_date: Optional[date] = None
    completed_at: Optional[date] = None
    version: int

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[Status] = None
    priority: Optional[Priority] = None
    due_date: Optional[date] = None
    version: int

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: Optional[str]):
        if v is None:
            return v
        if not v.strip():
            raise ValueError("title cannot be blank")
        if len(v.strip()) > 100:
            raise ValueError("title too long (max 100)")
        return v.strip()

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, v: Optional[date]):
        if v is not None and v < date.today():
            raise ValueError("due_date cannot be in the past")
        return v
