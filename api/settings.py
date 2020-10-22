from pydantic import BaseSettings


class Settings(BaseSettings):
    HANDICAP_QUEUE_URL: str
    SEARCH_SERVICE_API_BASE_URL: str


settings = Settings(_env_file='./api/.env', _env_file_encoding='utf-8')
