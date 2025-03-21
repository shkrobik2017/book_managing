from src.settings import settings
from src.db.singleton_tortoise.db_singleton_creator import PostgresDB

DB = PostgresDB(
    dsn=f"postgres://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)
