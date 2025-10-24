import pytest
from datetime import date, timedelta

@pytest.mark.anyio
async def test_title_blank_returns_400(client):
    r = await client.post("/todos", json={"title": "   ", "priority": 2})
    assert r.status_code in (400, 422)

@pytest.mark.anyio
async def test_due_date_in_past_rejected(client):
    past = (date.today() - timedelta(days=1)).isoformat()
    r = await client.post("/todos", json={"title": "x", "due_date": past})
    assert r.status_code in (400, 422)

@pytest.mark.anyio
async def test_high_priority_requires_due_date(client):
    r = await client.post("/todos", json={"title": "critico", "priority": 3})
    assert r.status_code == 400
    assert "due_date" in r.json()["detail"]
