import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(scope="module")
async def test_successful_api_call(test_app_client: AsyncClient):
    resp = await test_app_client.get(
        "/repositories/Daniel-Gordos",
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0
    assert "vapar-exercise" in [item["name"] for item in data]


@pytest.mark.asyncio(scope="module")
async def test_non_existent_user(test_app_client: AsyncClient):
    resp = await test_app_client.get(
        "/repositories/this-user-does-not-exist-1234567890",
    )
    assert resp.status_code == 404
