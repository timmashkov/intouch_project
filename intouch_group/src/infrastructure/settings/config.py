from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class GroupConfig(BaseSettings):
    # Postgres config
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Kafka config
    KAFKA_HOST: str
    KAFKA_PORT: int
    TOPIC_REG: str

    @property
    def kafka_url(self) -> str:
        return f"{self.KAFKA_HOST}:{self.KAFKA_PORT}"

    @property
    def topics(self) -> list:
        return [self.TOPIC_REG]

    # Rabbit config
    RABBIT_NAME: str
    RABBIT_PASS: str
    RABBIT_HOST: str
    RABBIT_PORT: int

    @property
    def rabbit_url(self) -> str:
        return f"amqp://{self.RABBIT_NAME}:{self.RABBIT_PASS}@{self.RABBIT_HOST}:{self.RABBIT_PORT}/"

    class Config:
        env_file = ".env"


group_config = GroupConfig()
