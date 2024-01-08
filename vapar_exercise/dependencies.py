from functools import cache

from fastapi import Depends

from vapar_exercise.config import EnvConfig, Config


@cache
def get_env_name() -> str:
    return EnvConfig().env_name


@cache
def get_config(env_name: str = Depends(get_env_name)) -> Config:
    env_file_name = f".env.{env_name}"
    return Config(_env_file=env_file_name)  # type:ignore - Loaded from env file
