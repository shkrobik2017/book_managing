from src.settings import settings

TORTOISE_ORM_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": settings.POSTGRES_HOST,
                "port": settings.POSTGRES_PORT,
                "user": settings.POSTGRES_USER,
                "password": settings.POSTGRES_PASSWORD,
                "database": settings.POSTGRES_DB,
            }
        },
    },
    "apps": {
        "models": {
            "models": ["src.db.models.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}