from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class AuthConfig(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    SECRET: str
    X_API_TOKEN: str

    KAFKA_HOST: str
    KAFKA_PORT: int
    TOPIC_REG: str

    @property
    def kafka_url(self) -> str:
        return f"{self.KAFKA_HOST}:{self.KAFKA_PORT}"

    @property
    def topics(self) -> list:
        return [self.TOPIC_REG]

    class Config:
        env_file = ".env"


base_config = AuthConfig()
