from httpx import AsyncClient
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


class GithubService:
    def __init__(self, http_client: AsyncClient, api_token: str):
        self._http_client = http_client
        self._api_token = api_token

    async def list_repositories_by_user(
        self,
        user_name: str,
    ) -> list[ListGithubReposResponseItem]:
        """
        List all public repositories for a given user.

        Throws:
        * UserDoesNotExist if the user does not exist
        * httpx.RequestError if the request fails for any other reason
        """
        url = f"https://api.github.com/users/{user_name}/repos"
        response = await self._http_client.get(
            url, headers={"Authorization": f"Bearer {self._api_token}"}
        )

        if response.status_code == 404:
            raise UserDoesNotExist(f"User {user_name} does not exist")
        elif not response.status_code == 200:
            response.raise_for_status()

        parser = TypeAdapter(list[GithubListReposResponseItem])
        parsed_response = parser.validate_json(response.text)

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
