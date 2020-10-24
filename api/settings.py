from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    HANDICAP_QUEUE_URL: AnyHttpUrl
    SEARCH_SERVICE_API_BASE_URL: AnyHttpUrl
    FOOTWEDGE_DATABASE_URI: str
    REDIS_URI: str


settings = Settings(_env_file='./api/.env', _env_file_encoding='utf-8')
