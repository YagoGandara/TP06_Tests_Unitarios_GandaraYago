import pytest

@pytest.mark.anyio
async def test_filters_and_pagination(client):
    await client.post("/todos", json={"title":"a", "priority":1})
    await client.post("/todos", json={"title":"b", "priority":2})
    await client.post("/todos", json={"title":"c", "priority":2})

    r = await client.get("/todos?q=b")
    assert any(x["title"]=="b" for x in r.json())

    r = await client.get("/todos?limit=1&offset=1")
    assert r.status_code == 200
    assert len(r.json()) == 1
