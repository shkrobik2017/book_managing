from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Dict

from src.db.models.user.model import UserModel
from src.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a password against its hashed version.

    Args:
        plain_password (str): The plaintext password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashes a plaintext password using bcrypt.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


async def create_access_token(
        data: Dict[str, str],
        expires_delta: Optional[timedelta] = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
) -> str:
    """
    Creates a JSON Web Token (JWT) for authentication.

    Args:
        data (Dict[str, str]): The data to encode in the token.
        expires_delta (Optional[timedelta]): The token's expiration time. Defaults to settings' value.

    Returns:
        str: The encoded JWT.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.AUTH_SECRET_KEY, algorithm=settings.AUTH_ALGORITHM)
    return encoded_jwt
