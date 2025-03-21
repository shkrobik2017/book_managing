from fastapi import HTTPException, status

from src.db.models.models import UserModel_Pydantic
from src.db.models.user.repository import get_user_from_db, create_user_in_db
from src.routers.auth.security import get_password_hash, verify_password, create_access_token


async def get_user(username: str) -> None:
    """
    Checks if a user with the given username exists in the database.

    Args:
        username (str): The username to search for.

    Raises:
        HTTPException: If the user already exists, raises a 400 error.
    """
    user = await get_user_from_db(username=username)
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")


async def check_exist_and_create_user(username: str, password: str) -> UserModel_Pydantic:
    """
    Checks if a user exists, hashes the password, and creates a new user.

    Args:
        username (str): The username to register.
        password (str): The password for the user.

    Returns:
        UserModel_Pydantic: The newly created user.

    Raises:
        HTTPException: If the user already exists or an internal error occurs.
    """
    try:
        await get_user(username=username)
        hashed_password = get_password_hash(password)
        user = await create_user_in_db(username=username, hashed_password=hashed_password)
        return UserModel_Pydantic.model_validate(user)
    except HTTPException as ex:
        raise ex
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"Internal Error": "Something went wrong during registration!"}
        )


async def validate_user_and_login(username: str, password: str) -> str:
    """
    Validates a user's credentials and generates an access token.

    Args:
        username (str): The username of the user.
        password (str): The plaintext password to validate.

    Returns:
        str: The generated access token.

    Raises:
        HTTPException: If credentials are incorrect or an internal error occurs.
    """
    try:
        user = await get_user_from_db(username=username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        return await create_access_token(data={"sub": user.username})
    except HTTPException as ex:
        raise ex
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"Internal Error": "Something went wrong during login!"}
        )
