from src.db.models.author.model import AuthorModel
from src.db.models.book.model import BookModel
from typing import Optional, List, Dict


async def get_book_by_title(title: str) -> BookModel | None:
    """
    Retrieve a book by its title.

    Args:
        title (str): The title of the book.

    Returns:
        BookModel | None: The book if found, else None.
    """
    return await BookModel.get_or_none(title=title)


async def create_book_in_db(book: Dict, author: AuthorModel) -> BookModel:
    """
    Create a new book in the database.

    Args:
        book (Dict): A dictionary containing book details.
        author (AuthorModel): The author of the book.

    Returns:
        BookModel: The created book instance.
    """
    return await BookModel.create(
        title=book["title"],
        author=author,
        genre=book["genre"],
        published_year=book["published_year"],
    )

async def bulk_create_books_in_db(valid_books: List[BookModel]):
    await BookModel.bulk_create(valid_books)


async def get_books_from_db() -> List[BookModel]:
    """
    Retrieve all books from the database.

    Returns:
        List[BookModel]: A list of all book instances.
    """
    return await BookModel.all()


async def get_book_by_id_from_db(book_id: int) -> Optional[BookModel]:
    """
    Retrieve a book by its ID.

    Args:
        book_id (int): The ID of the book.

    Returns:
        Optional[BookModel]: The book if found, else None.
    """
    return await BookModel.get_or_none(id=book_id).prefetch_related("author")


async def get_books_by_filter_from_db(filters: Dict) -> List[BookModel]:
    """
    Retrieve books that match the given filters.

    Args:
        filters (Dict): A dictionary of filter criteria.

    Returns:
        List[BookModel]: A list of books matching the filters.
    """
    return await BookModel.filter(**filters)


async def update_book_in_db(book_id: int, book: Dict) -> BookModel:
    """
    Update a book's details in the database.

    Args:
        book_id (int): The ID of the book to update.
        book (Dict): A dictionary containing the updated book details.

    Returns:
        BookModel: The number of rows updated (0 if no update was performed).
    """
    return await BookModel.filter(id=book_id).update(**book).model


async def delete_book_from_db(book_id: int) -> None:
    """
    Delete a book by its ID.

    Args:
        book_id (int): The ID of the book to delete.

    Returns:
        None
    """
    await BookModel.filter(id=book_id).delete()
