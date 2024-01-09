from pathlib import Path
import pytest
from httpx import Response

from vapar_exercise.service import GithubService, RateLimitExceeded, UserDoesNotExist
from vapar_exercise.models import ListGithubReposResponseItem


_example_github_response = Path(
    "vapar_exercise/tests/github_api_example_response.json"
).read_text()


@pytest.mark.asyncio(scope="module")
async def test_list_repositories_by_user(mock_http_client_factory):
    def handler(req):
        return Response(200, text=_example_github_response)

    http_client = mock_http_client_factory(handler)

    service = GithubService(http_client, api_token="dummy-token")
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
async def test_nonexistent_user(mock_http_client_factory):
    def handler(req):
        return Response(404)

    http_client = mock_http_client_factory(handler)

    service = GithubService(http_client, api_token="dummy-token")
    with pytest.raises(UserDoesNotExist):
        await service.list_repositories_by_user("Nonexistent-User")


async def test_rate_limited(mock_http_client_factory):
    def handler(req):
        return Response(429, text="Rate limit exceeded")

    http_client = mock_http_client_factory(handler)

    service = GithubService(http_client, api_token="dummy-token")
    with pytest.raises(RateLimitExceeded):
        await service.list_repositories_by_user("Dummy-User")
