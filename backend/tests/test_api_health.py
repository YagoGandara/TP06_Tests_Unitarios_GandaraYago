import pytest

@pytest.mark.anyio
async def test_touch(client):
    r = await client.get("/admin/touch")
    assert r.status_code == 200
    assert r.json() == {"ok": True}
