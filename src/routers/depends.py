from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from src.routers.auth.schemas import TokenData
from src.settings import settings

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/v1/api/auth/token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    """
    Retrieve and validate the current user based on the provided token.

    Args:
        token (str): JWT token extracted from the request Authorization header.

    Returns:
        TokenData: An instance of TokenData containing the username.

    Raises:
        HTTPException: If the token is invalid or credentials cannot be validated.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(
            token,
            settings.AUTH_SECRET_KEY,
            algorithms=[settings.AUTH_ALGORITHM]
        )
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        return TokenData(username=username)
    except JWTError:
        raise credentials_exception
