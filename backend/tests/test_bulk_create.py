import pytest

@pytest.mark.anyio
async def test_bulk_create(client):
    payload = [
      {"title":"b1","priority":1},
      {"title":"b2","priority":2},
      {"title":"b3"}
    ]
    r = await client.post("/todos/bulk", json=payload)
    assert r.status_code == 200
    assert len(r.json()) == 3
