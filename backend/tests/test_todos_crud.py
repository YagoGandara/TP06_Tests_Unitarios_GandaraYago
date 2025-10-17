import pytest

@pytest.mark.anyio
async def test_create_get_list_update_delete(client):
    r = await client.post("/todos", json={"title": "persisto"})
    assert r.status_code == 201
    tid = r.json()["id"]

    r = await client.get(f"/todos/{tid}")
    assert r.status_code == 200
    assert r.json()["title"] == "persisto"

    r = await client.get("/todos")
    assert any(x["id"] == tid for x in r.json())

    r = await client.put(f"/todos/{tid}", json={"title": "nuevo"})
    assert r.status_code == 200
    assert r.json()["title"] == "nuevo"

    r = await client.delete(f"/todos/{tid}")
    assert r.status_code == 204

    r = await client.get(f"/todos/{tid}")
    assert r.status_code == 404
