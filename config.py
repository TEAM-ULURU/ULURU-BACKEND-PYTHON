import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_USERNAME: str = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_DATABASE: str = os.getenv("DB_DATABASE")
    DB_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

    JWT_ACCESS_SECRET: str = os.getenv("JWT_ACCESS_SECRET")
    JWT_REFRESH_SECRET: str = os.getenv("JWT_REFRESH_SECRET")
    ALGORITHM: str = os.getenv("ALGORITHM")


settings = Settings()
