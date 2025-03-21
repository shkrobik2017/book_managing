from src.db.models.models import UserModel_Pydantic
from src.db.models.user.model import UserModel


async def get_user_from_db(username: str) -> UserModel | None:
    """
    Retrieves a user from the database by their username.

    Args:
        username (str): The username to search for.

    Returns:
        Optional[UserModel]: The user object if found, otherwise None.
    """
    return await UserModel.get_or_none(username=username)


async def create_user_in_db(username: str, hashed_password: str) -> UserModel:
    """
    Creates a new user in the database with the given credentials.

    Args:
        username (str): The username for the new user.
        hashed_password (str): The hashed password for the new user.

    Returns:
        UserModel: The created user object.
    """
    return await UserModel.create(username=username, hashed_password=hashed_password)
