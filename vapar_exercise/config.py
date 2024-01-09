from typing import Literal
from pydantic_settings import BaseSettings


class EnvConfig(BaseSettings):
    model_config = {"extra": "ignore"}

    env_name: Literal["dev", "prod"] = "dev"


class Config(BaseSettings):
    model_config = {"extra": "ignore", "case_sensitive": False}

    github_api_token: str
