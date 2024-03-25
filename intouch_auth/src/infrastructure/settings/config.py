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
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    SECRET: str
    X_API_TOKEN: str

    KAFKA_BOOTSTRAP_SERVERS: str
    TOPIC: str

    class Config:
        env_file = ".env"


base_config = AuthConfig()
