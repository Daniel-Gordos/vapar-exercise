from httpx import AsyncClient
from httpx import codes as status_codes
from pydantic import TypeAdapter
from vapar_exercise.codegen.github_list_repos_response import (
    ModelItem as GithubListReposResponseItem,
)
from vapar_exercise.models import ListGithubReposResponseItem


class GithubServiceError(Exception):
    pass


class UserDoesNotExist(GithubServiceError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class RateLimitExceeded(GithubServiceError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class GithubService:
    _DEFAULT_BASE_URL = "https://api.github.com"

    def __init__(
        self,
        http_client: AsyncClient,
        api_token: str,
        base_url: str | None = None,
    ):
        self._http_client = http_client
        self._api_token = api_token
        self._base_url = self._DEFAULT_BASE_URL if base_url is None else base_url

    async def list_repositories_by_user(
        self,
        user_name: str,
    ) -> list[ListGithubReposResponseItem]:
        """
        List all public repositories for a given user.

        Throws:
        * UserDoesNotExist if the user does not exist
        * RateLimitExceeded if the github API call hit a rate limit
        * httpx.RequestError if the request fails for any other reason
        """
        url = f"{self._base_url}/users/{user_name}/repos"
        response = await self._http_client.get(
            url, headers={"Authorization": f"Bearer {self._api_token}"}
        )

        if response.status_code == status_codes.NOT_FOUND:
            raise UserDoesNotExist(f"User {user_name} does not exist")
        elif response.status_code == status_codes.TOO_MANY_REQUESTS:
            raise RateLimitExceeded("Rate limit exceeded")
        elif response.status_code != status_codes.OK:
            response.raise_for_status()

        return self._parse_response_body(response.text)

    def _parse_response_body(
        self, response_text: str
    ) -> list[ListGithubReposResponseItem]:
        parser = TypeAdapter(list[GithubListReposResponseItem])
        parsed_response = parser.validate_json(response_text)

        repositories = [
            ListGithubReposResponseItem(
                name=item.name,
                description=item.description,
                stars=item.stargazers_count if item.stargazers_count else 0,
                language=item.language,
            )
            for item in parsed_response
        ]

        return repositories
