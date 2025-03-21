from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from src.db.models.user.model import UserModel
from src.routers.author.schemas import AuthorCreate, AuthorsList, AuthorUpdate
from src.routers.author.services import check_exist_author_and_create, get_authors, get_author_by_id, \
    check_exist_author_and_update, delete_author_by_id
from src.routers.depends import get_current_user

router = APIRouter(
    prefix="/authors",
    tags=["Authors"],
)


@router.post("/create", response_model=dict)
async def create_author(
        author: AuthorCreate,
        current_user: Annotated[UserModel, Depends(get_current_user)]
) -> dict:
    """
    Create a new author.

    Args:
        author (AuthorCreate): Data required to create a new author.
        current_user (UserModel): The current authenticated user.

    Returns:
        dict: A success message along with the created author's data.
    """
    created_author = await check_exist_author_and_create(author=author.model_dump())
    return {
        "success": True,
        "message": "Author created successfully",
        "data": created_author,
    }


@router.get("/all", response_model=dict)
async def get_all_authors(
        current_user: Annotated[UserModel, Depends(get_current_user)]
) -> dict:
    """
    Fetch all authors.

    Args:
        current_user (UserModel): The current authenticated user.

    Returns:
        dict: A success message along with the list of authors.
    """
    authors = await get_authors()
    return {
        "success": True,
        "message": "Authors fetched successfully",
        "data": AuthorsList(authors=authors),
    }


@router.get("/{author_id}", response_model=dict)
async def get_author(
        author_id: int,
        current_user: Annotated[UserModel, Depends(get_current_user)]
) -> dict:
    """
    Fetch an author by ID.

    Args:
        author_id (int): The ID of the author to fetch.
        current_user (UserModel): The current authenticated user.

    Returns:
        dict: A success message along with the author's data.
    """
    author = await get_author_by_id(author_id=author_id)
    return {
        "success": True,
        "message": "Author fetched successfully",
        "data": author,
    }


@router.put("/{author_id}", response_model=dict)
async def update_author(
        author_id: int,
        current_user: Annotated[UserModel, Depends(get_current_user)],
        author_name: str | None = None,
        author_surname: str | None = None,
        author_birth_date: str | None = None,
        author_biography: str | None = None,
) -> dict:
    """
    Update an author's details.

    Args:
        author_id (int): The ID of the author to update.
        author_name (str | None): Author's first name'.
        author_surname (str | None): Author's last name.'
        author_birth_date (datetime | None): Author's birthdate.'
        author_biography (str | None): Author's biography.'
        current_user (UserModel): The current authenticated user.

    Returns:
        dict: A success message along with the updated author's data.
    """
    try:
        author = AuthorUpdate(
            name=author_name,
            surname=author_surname,
            birth_date=author_birth_date,
            biography=author_biography,
        )
    except ValueError as ex:
        raise ex
    updated_author = await check_exist_author_and_update(author_id=author_id, author_update=author)
    return {
        "success": True,
        "message": "Author updated successfully",
        "data": updated_author,
    }


@router.delete("/{author_id}", response_model=dict)
async def delete_author(
        author_id: int,
        current_user: Annotated[UserModel, Depends(get_current_user)]
) -> dict:
    """
    Delete an author by ID.

    Args:
        author_id (int): The ID of the author to delete.
        current_user (UserModel): The current authenticated user.

    Returns:
        dict: A success message indicating the author was deleted.
    """
    await delete_author_by_id(author_id=author_id)
    return {
        "success": True,
        "message": "Author deleted successfully",
    }
