from src.db.models.author.model import AuthorModel
from typing import Optional, List


async def get_author_by_id_from_db(author_id: int) -> AuthorModel | None:
    """
    Retrieve an author by their ID.
    
    Args:
        author_id (int): The ID of the author.
    
    Returns:
        Optional[AuthorModel]: The author instance if found, otherwise None.
    """
    return await AuthorModel.get_or_none(id=author_id)


async def get_author_by_full_name(name: str, surname: str) -> AuthorModel | None:
    """
    Retrieve an author by their full name.
    
    Args:
        name (str): The author's first name.
        surname (str): The author's last name.
    
    Returns:
        Optional[AuthorModel]: The author instance if found, otherwise None.
    """
    return await AuthorModel.get_or_none(full_name=f"{name} {surname}")


async def create_author_in_db(author: dict) -> AuthorModel:
    """
    Create a new author in the database.
    
    Args:
        author (dict): A dictionary with author data (name, surname, birth_date, biography).
    
    Returns:
        AuthorModel: The created author instance.
    """
    return await AuthorModel.create(
        full_name=f"{author.get('name')} {author.get('surname')}",
        birth_date=author.get("birth_date"),
        biography=author.get("biography"),
    )


async def get_authors_from_db() -> List[AuthorModel]:
    """
    Retrieve all authors from the database.
    
    Returns:
        List[AuthorModel]: A list of author instances.
    """
    return await AuthorModel.all()


async def update_author_in_db(author_id: int, author: dict) -> AuthorModel:
    """
    Update an author's details in the database.
    
    Args:
        author_id (int): The ID of the author to update.
        author (dict): A dictionary with updated author data.
    
    Returns:
        AuthorModel: The number of affected rows (0 if no rows were updated).
    """
    updated_author = await AuthorModel.filter(id=author_id).update(**author).model
    return updated_author


async def delete_author_from_db(author_id: int) -> None:
    """
    Delete an author from the database.
    
    Args:
        author_id (int): The ID of the author to delete.
    
    Returns:
        None
    """
    await AuthorModel.filter(id=author_id).delete()
