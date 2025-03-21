from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration class for application settings, loaded from environment variables.

    Attributes:
        POSTGRES_HOST (str): The hostname of the PostgreSQL database.
        POSTGRES_PORT (int): The port number for connecting to the PostgreSQL database.
        POSTGRES_USER (str): The username for authenticating to the PostgreSQL database.
        POSTGRES_PASSWORD (str): The password for authenticating to the PostgreSQL database.
        POSTGRES_DB (str): The name of the PostgreSQL database to connect to.
        DATABASE_URL (str): The full connection URL for the PostgreSQL database.

        ACCESS_TOKEN_EXPIRE_MINUTES (int): Expiration time for access tokens in minutes.
        AUTH_SECRET_KEY (str): The secret key used for signing authentication tokens.
        AUTH_ALGORITHM (str): The algorithm used for signing authentication tokens.
        AUTH_TOKEN_TYPE (str): The type of authentication token.
    """

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
        frozen = True

    POSTGRES_HOST: str = Field(
        ...,
        description="The hostname of the PostgreSQL database."
    )

    POSTGRES_PORT: int = Field(
        ...,
        description="The port number for connecting to the PostgreSQL database."
    )

    POSTGRES_USER: str = Field(
        ...,
        description="The username for authenticating to the PostgreSQL database."
    )

    POSTGRES_PASSWORD: str = Field(
        ...,
        description="The password for authenticating to the PostgreSQL database."
    )

    POSTGRES_DB: str = Field(
        ...,
        description="The name of the PostgreSQL database to connect to."
    )

    DATABASE_URL: str = Field(
        ...,
        description="The full connection URL for the PostgreSQL database."
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        ...,
        description="Expiration time for access tokens in minutes."
    )

    AUTH_SECRET_KEY: str = Field(
        ...,
        description="The secret key used for signing authentication tokens."
    )

    AUTH_ALGORITHM: str = Field(
        ...,
        description="The algorithm used for signing authentication tokens."
    )

    AUTH_TOKEN_TYPE: str = Field(
        ...,
        description="The type of authentication token."
    )

settings: Settings = Settings()
