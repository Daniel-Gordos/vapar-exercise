import pytest
from httpx import AsyncClient

from vapar_exercise.service import GithubService, UserDoesNotExist
from vapar_exercise.models import ListGithubReposResponseItem


@pytest.mark.asyncio(scope="module")
async def test_list_repositories_by_user(mock_http_client: AsyncClient):
    service = GithubService(mock_http_client, api_token="dummy-token")
    res = await service.list_repositories_by_user("Dummy-User")

    assert res == [
        ListGithubReposResponseItem(
            name="Hello-World",
            description="This your first repo!",
            stars=80,
            language=None,
        )
    ]


@pytest.mark.asyncio(scope="module")
async def test_nonexistent_user(mock_http_client_no_user: AsyncClient):
    service = GithubService(mock_http_client_no_user, api_token="dummy-token")
    with pytest.raises(UserDoesNotExist):
        await service.list_repositories_by_user("Nonexistent-User")
