from functools import cache

from fastapi import Depends
from httpx import AsyncClient

from vapar_exercise.config import EnvConfig, Config
from vapar_exercise.service import GithubService


@cache
def get_env_name() -> str:
    return EnvConfig().env_name


@cache
def get_config(env_name: str = Depends(get_env_name)) -> Config:
    env_file_name = f".env.{env_name}"
    return Config(_env_file=env_file_name)  # type:ignore - Loaded from env file


@cache
def get_http_client() -> AsyncClient:
    return AsyncClient()


def get_github_service(
    http_client: AsyncClient = Depends(get_http_client),
    config: Config = Depends(get_config),
):
    return GithubService(http_client, config.github_api_token)
