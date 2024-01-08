from pydantic import BaseModel


class ListGithubReposResponseItem(BaseModel):
    name: str
    description: str | None
    stars: int
    language: str | None
