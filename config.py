from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os


load_dotenv('.env')


class Config(BaseSettings):

    LOG_LEVEL: str = os.getenv('LOG_LEVEL')

    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = os.getenv('DB_PORT')
    DB_USER: str = os.getenv('DB_USER')
    DB_PASS: str = os.getenv('DB_PASS')
    DB_NAME: str = os.getenv('DB_NAME')

    SECRET_KEY: str = os.getenv('SECRET_KEY')
    SECRET_ALGORITHM: str = os.getenv('SECRET_ALGORITHM')

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"




env_config: Config = Config()