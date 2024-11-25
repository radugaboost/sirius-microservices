from pydantic_settings import BaseSettings, SettingsConfigDict

from .jobs import Job


class BaseConfig(BaseSettings):
    SERVICE_NAME: str

class DefaultSettings(BaseConfig):
    DO_JOB: Job

    model_config = SettingsConfigDict(env_file=".env")

class RpcSettings(BaseConfig):
    TO_SQUARE_URL: str = "http://to-square:8000/api/v1/do"
    TO_SQRT_URL: str = "http://to-sqrt:8000/api/v1/do"

    model_config = SettingsConfigDict(env_file=".env")
