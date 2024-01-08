import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(scope="module")
async def test_successful_api_call(test_app_client: AsyncClient):
    resp = await test_app_client.get(
        "/repositories/Daniel-Gordos",
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    repo = data[0]
    assert repo["name"] == "vapar-exercise"
    assert repo["language"] == "Python"


@pytest.mark.asyncio(scope="module")
async def test_query_user_with_many_repos(test_app_client: AsyncClient):
    resp = await test_app_client.get(
        "/repositories/tiangolo",  # The creator of FastAPI
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "fastapi" in (repo["name"] for repo in data)


@pytest.mark.asyncio(scope="module")
async def test_non_existent_user(test_app_client: AsyncClient):
    resp = await test_app_client.get(
        "/repositories/this-user-does-not-exist-1234567890",
    )
    assert resp.status_code == 404
