from enum import Enum
from functools import lru_cache
import os
from typing import Optional

from pydantic_settings import BaseSettings
from pydantic import ValidationError


# @lru_cache
# def get_env_filename():
#     runtime_env = os.getenv("ENV") #Recupera la variable de entorno env, definida en el launch.json y a partir de aqui recarga desde el fichero
#     return f".env.{runtime_env}" if runtime_env else ".env"

@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    env_filename = f".env.{runtime_env}" if runtime_env else ".env"
    print(f"Using environment file: {env_filename}")
    return env_filename


class EnvironmentSettings(BaseSettings):
    ENV: Optional [str] = None
    API_VERSION: Optional [str] = None
    APP_NAME: Optional [str] = None
    DATABASE_DIALECT: Optional [str] = None
    DATABASE_HOSTNAME: Optional [str] = None
    DATABASE_NAME: Optional [str] = None
    DATABASE_PASSWORD: Optional [str] = None
    DATABASE_PORT: Optional [int] = None
    DATABASE_USERNAME: Optional [str] = None
    DEBUG_MODE: Optional [bool] = None
    PODMAN_URL: Optional [str] = None

    class Config:
        env_file = get_env_filename()
        env_file_encoding = "utf-8"


@lru_cache
def get_environment_variables():
    try:
        return EnvironmentSettings()
    except ValidationError as e:
        print("Error loading environment variables:", e)
        raise


# @lru_cache
# def get_environment_variables():
#     try:
#         env_file = get_env_filename()
#         print(f"Loading environment variables from: {env_file}")
#         settings = EnvironmentSettings()
#         print("Environment variables loaded successfully.")
#         return settings
#     except ValidationError as e:
#         print("Error loading environment variables:", e)
#         raise


class Environment(Enum):
    local = "local"
    dev = "dev"
    pre = "pre"
    pro = "pro"


# # Script de prueba
# if __name__ == "__main__":
#     print("Loading settings...")
#     settings = get_settings()
#     print(f"ENV: {settings.ENV}")
#     print(f"API_VERSION: {settings.API_VERSION}")
#     print(f"APP_NAME: {settings.APP_NAME}")
#     print(f"DATABASE_DIALECT: {settings.DATABASE_DIALECT}")
#     print(f"DATABASE_HOSTNAME: {settings.DATABASE_HOSTNAME}")
#     print(f"DATABASE_NAME: {settings.DATABASE_NAME}")
#     print(f"DATABASE_PASSWORD: {settings.DATABASE_PASSWORD}")
#     print(f"DATABASE_PORT: {settings.DATABASE_PORT}")
#     print(f"DATABASE_USERNAME: {settings.DATABASE_USERNAME}")
#     print(f"DEBUG_MODE: {settings.DEBUG_MODE}")
#     print(f"PODMAN_URL: {settings.PODMAN_URL}")