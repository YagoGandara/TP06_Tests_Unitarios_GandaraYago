import pytest

@pytest.mark.anyio
async def test_status_transitions_and_version_conflict(client):
    r = await client.post("/todos", json={"title":"t1"})
    assert r.status_code == 201
    item = r.json()
    tid, ver = item["id"], item["version"]

    r = await client.patch(f"/todos/{tid}", json={"status":"in_progress", "version": ver})
    assert r.status_code == 200
    ver = r.json()["version"]

    r = await client.patch(f"/todos/{tid}", json={"status":"pending", "version": ver})
    assert r.status_code == 200
    ver = r.json()["version"]

    r = await client.patch(f"/todos/{tid}", json={"status":"done", "version": ver})
    assert r.status_code == 200
    done_item = r.json()
    assert done_item["status"] == "done"

    r = await client.patch(f"/todos/{tid}", json={"status":"pending", "version": done_item["version"]})
    assert r.status_code == 400

    r = await client.patch(f"/todos/{tid}", json={"title":"new", "version": 1})
    assert r.status_code == 409

@pytest.mark.anyio
async def test_toggle_and_uniqueness(client):
    r = await client.post("/todos", json={"title":"u1"}); assert r.status_code==201
    r = await client.post("/todos", json={"title":"u2"}); assert r.status_code==201
    t1 = (await client.get("/todos?q=u1")).json()[0]

    r = await client.post(f"/todos/{t1['id']}/toggle")
    assert r.status_code == 200
    assert r.json()["status"] == "done"

    r = await client.post(f"/todos/{t1['id']}/toggle")
    assert r.status_code == 400

    r = await client.post("/todos", json={"title":"u2"})
    assert r.status_code == 400
