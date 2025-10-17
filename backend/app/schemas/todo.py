from pydantic import BaseModel, field_validator

class TodoIn(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def not_empty(cls, v: str):
        if not v or not v.strip():
            raise ValueError("title is required")
        if len(v.strip()) > 100:
            raise ValueError("title too long (max 100)")
        return v

class TodoOut(BaseModel):
    id: int
    title: str
