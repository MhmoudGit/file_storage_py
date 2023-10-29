from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Any, Callable
from fastapi.responses import ORJSONResponse
import orjson
from pydantic import BaseModel


# env configs:
load_dotenv()


class Settings(BaseSettings):
    db_username: str
    db_password: str
    db_hostname: str
    db_name: str


settings = Settings()


def orjson_dumps(v: Any, *, default: Callable[[Any], Any] | None) -> str:
    return orjson.dumps(v, default=default).decode()


class ORJSONModel(BaseModel):
    class Config:
        from_attributes = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


app_configs: dict[str, Any] = {
    "title": "File Storage",
    "debug": True,
    "default_response_class": ORJSONResponse,
    "description": "API for a File Storage",
}
