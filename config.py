from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_PASS: str
    WEATHER_API_KEY: str
    WEATHER_API_URL: str
    API_PATH: str = ""
    ROOT_USER: str
    ROOT_PASS: str
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
