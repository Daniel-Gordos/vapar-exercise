from fastapi import FastAPI, Depends, HTTPException

from vapar_exercise.dependencies import get_github_service
from vapar_exercise.service import GithubService, RateLimitExceeded, UserDoesNotExist
from vapar_exercise.models import ListGithubReposResponseItem

app = FastAPI(
    title="VAPAR API Exercise",
    docs_url="/",
)


@app.get(
    "/repositories/{user_name}",
    responses={
        200: {"model": ListGithubReposResponseItem},
        404: {"model": str},
        429: {"model": str},
    },
)
async def list_repositories_by_user(
    user_name: str, service: GithubService = Depends(get_github_service)
):
    try:
        return await service.list_repositories_by_user(user_name)
    except UserDoesNotExist:
        raise HTTPException(status_code=404, detail=f"User {user_name} does not exist")
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
