from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):

    MONGO_INITDB_HOST: str
    MONGO_INITDB_PORT: str
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_INITDB_DATABASE: str
    @property
    def get_url_mg(self) -> str:
        return f"mongodb://{self.MONGO_INITDB_ROOT_USERNAME}:{self.MONGO_INITDB_ROOT_PASSWORD}@{self.MONGO_INITDB_HOST}:{self.MONGO_INITDB_PORT}"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
    )

settings = Settings()
print(settings)