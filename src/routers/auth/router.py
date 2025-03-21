from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from src.db.models.user.model import UserModel
from src.routers.auth.schemas import UserCreate, Token
from src.routers.auth.services import check_exist_and_create_user, validate_user_and_login
from src.routers.depends import get_current_user
from src.settings import settings

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register", summary="Register a new user", response_model=dict)
async def register(user: UserCreate) -> dict:
    """
    Handles user registration.

    Args:
        user (UserCreate): User registration data including username and password.

    Returns:
        dict: Success status and registered user data.
    """
    created_user = await check_exist_and_create_user(
        username=user.username,
        password=user.password
    )
    return {
        "success": True,
        "message": "User registered successfully",
        "data": created_user,
    }


@router.post("/token", response_model=Token, summary="User login and token generation")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    Handles user login and returns a token for authentication.

    Args:
        form_data (OAuth2PasswordRequestForm): User login credentials.

    Returns:
        Token: Generated access token and its type.
    """
    access_token = await validate_user_and_login(
        username=form_data.username,
        password=form_data.password,
    )
    return Token(
        access_token=access_token,
        token_type=settings.AUTH_TOKEN_TYPE
    )
