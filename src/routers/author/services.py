from fastapi import HTTPException, status
from typing import List, Union
from src.db.models.author.repository import (
    get_author_by_full_name, create_author_in_db,
    get_authors_from_db, get_author_by_id_from_db,
    update_author_in_db, delete_author_from_db
)
from src.db.models.models import AuthorModel_Pydantic
from src.routers.author.schemas import AuthorUpdate


async def check_exist_author_and_create(author: dict) -> AuthorModel_Pydantic:
    """
    Check if an author exists by full name, and create a new author if not.

    Args:
        author (dict): The author data to create.

    Returns:
        AuthorModel_Pydantic: The created author model.

    Raises:
        HTTPException: If the author already exists or an internal error occurs.
    """
    try:
        existing_author = await get_author_by_full_name(
            name=author.get("name"), surname=author.get("surname")
        )
        if existing_author is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Author already exists"
            )
        created_author = await create_author_in_db(author=author)
        return AuthorModel_Pydantic.model_validate(created_author)
    except HTTPException:
        raise
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"Internal Error": "Something went wrong during author creation!"}
        )


async def get_authors() -> List[AuthorModel_Pydantic]:
    """
    Fetch all authors from the database.

    Returns:
        List[AuthorModel_Pydantic]: A list of authors.

    Raises:
        HTTPException: If an internal error occurs during fetching.
    """
    try:
        authors = await get_authors_from_db()
        return [AuthorModel_Pydantic.from_orm(author) for author in authors]
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"Internal Error": "Something went wrong during all authors fetching!"}
        )


async def get_author_by_id(author_id: int) -> AuthorModel_Pydantic:
    """
    Fetch an author by their ID.

    Args:
        author_id (int): The ID of the author to fetch.

    Returns:
        AuthorModel_Pydantic: The author model.

    Raises:
        HTTPException: If the author is not found or an internal error occurs.
    """
    try:
        author = await get_author_by_id_from_db(author_id=author_id)
        if author is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author not found"
            )
        return AuthorModel_Pydantic.model_validate(author)
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"Internal Error": "Something went wrong during author fetching!"}
        )


async def check_exist_author_and_update(author_id: int, author_update: AuthorUpdate) -> AuthorModel_Pydantic:
    """
    Check if an author exists by ID, and update their details.

    Args:
        author_id (int): The ID of the author to update.
        author_update (AuthorUpdate): The updated author data.

    Returns:
        AuthorModel_Pydantic: The updated author model.

    Raises:
        HTTPException: If the author is not found or an internal error occurs.
    """
    try:
        existing_author = await get_author_by_id_from_db(author_id=author_id)
        if existing_author is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author not found"
            )
        if author_update.name is not None:
            existing_author.full_name = f"{author_update.name}+{existing_author.full_name.split('+')[1]}"
        if author_update.surname is not None:
            existing_author.full_name = f"{existing_author.full_name.split('+')[0]}+{author_update.surname}"
        if author_update.birth_date is not None:
            existing_author.birth_date = author_update.birth_date
        if author_update.biography is not None:
            existing_author.biography = author_update.biography

        await existing_author.save()
        return AuthorModel_Pydantic.model_validate(existing_author)
    except HTTPException:
        raise
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"Internal Error": "Something went wrong during author updating!"}
        )


async def delete_author_by_id(author_id: int) -> None:
    """
    Delete an author by their ID.

    Args:
        author_id (int): The ID of the author to delete.

    Raises:
        HTTPException: If the author is not found or an internal error occurs.
    """
    try:
        author = await get_author_by_id_from_db(author_id=author_id)
        if author is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author not found"
            )
        await delete_author_from_db(author_id=author_id)
    except HTTPException:
        raise
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"Internal Error": "Something went wrong during author deletion!"}
        )
