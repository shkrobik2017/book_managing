import logging
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, UploadFile, File

from src.db.models.user.model import UserModel
from src.routers.author.schemas import AuthorSchema
from src.routers.books.schemas import BookCreate, BookList, BookUpdate, BookSchema
from src.routers.books.services import (
    check_exist_book_and_create,
    get_books,
    get_book_by_id,
    get_book_by_filters,
    check_exist_book_and_update,
    delete_book_by_id, validate_and_save_books_to_db,
)
from src.routers.depends import get_current_user
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@router.post("/create", summary="Create a new book", response_description="Details of the newly created book")
async def create_book(
        book: BookCreate,
        current_user: Annotated[UserModel, Depends(get_current_user)]
) -> dict:
    """
    Create a new book in the database.

    Args:
        book (BookCreate): The details of the book to create.
        current_user (UserModel): The current authenticated user.

    Returns:
        dict: A dictionary containing success status, message, and created book data.
    """
    created_book, author = await check_exist_book_and_create(book=book.model_dump())
    return {
        "success": True,
        "message": "Book created successfully",
        "data": BookSchema(**created_book.model_dump(), author=AuthorSchema(**author.model_dump())),
    }


@router.post("/import")
async def import_books(file: UploadFile = File(...)):
    result = await validate_and_save_books_to_db(file=file)

    return {
        "success": True,
        "message": f"{result.get("Count of saved books")} books created successfully",
        "data": result
    }


@router.get("/all", summary="Get all books", response_description="List of all books")
async def get_all_books(
        current_user: Annotated[UserModel, Depends(get_current_user)]
) -> dict:
    """
    Fetch all books from the database.

    Args:
        current_user (UserModel): The current authenticated user.

    Returns:
        dict: A dictionary containing success status, message, and list of books.
    """
    books = await get_books()
    return {
        "success": True,
        "message": "Books fetched successfully",
        "data": BookList(books=books),
    }


@router.get("/{book_id}", summary="Get a book by ID", response_description="Details of the requested book")
async def get_book(
        book_id: int,
        current_user: Annotated[UserModel, Depends(get_current_user)]
) -> dict:
    """
    Fetch a specific book by its ID.

    Args:
        book_id (int): The ID of the book to fetch.
        current_user (UserModel): The current authenticated user.

    Returns:
        dict: A dictionary containing success status, message, and book data.
    """
    book, author = await get_book_by_id(book_id=book_id)
    return {
        "success": True,
        "message": "Book fetched successfully",
        "data": BookSchema(**book.model_dump(), author=AuthorSchema(**author.model_dump()))
    }


@router.get("/search/", summary="Search for books", response_description="List of books matching the search criteria")
async def search_books(
        current_user: Annotated[UserModel, Depends(get_current_user)],
        title: Optional[str] = None,
        author_id: Optional[str] = None,
        genre: Optional[str] = None,
        year: Optional[int] = None,
) -> dict:
    """
    Search for books based on various criteria.

    Args:
        current_user (UserModel): The current authenticated user.
        title (Optional[str]): Partial or complete book title to search for.
        author_id (Optional[str]): ID of the author to filter books by.
        genre (Optional[str]): Genre of the books to filter.
        year (Optional[int]): Published year to filter books by.

    Returns:
        dict: A dictionary containing success status, message, and list of filtered books.
    """
    filters = {}
    if title:
        filters["title__icontains"] = title
    if author_id:
        filters["author__id__icontains"] = author_id
    if genre:
        filters["genre__icontains"] = genre
    if year:
        filters["published_year"] = year

    books = await get_book_by_filters(filters=filters)
    return {
        "success": True,
        "message": "Books fetched successfully",
        "data": BookList(books=books),
    }


@router.put("/{book_id}", summary="Update a book", response_description="Details of the updated book")
async def update_book(
        book_id: int,
        current_user: Annotated[UserModel, Depends(get_current_user)],
        book_title: str | None = None,
        book_genre: str | None = None,
        book_published_year: int | None = None,
        book_author_id: int | None = None,

) -> dict:
    """
    Update the details of an existing book.
    
    This endpoint updates the details of a book in the database using the provided book ID
    and new book information such as title, genre, published year, and author ID.
    
    Args:
        book_id (int): The ID of the book to update.
        book_title (str | None): The new title of the book.
        book_genre (str | None): The new genre of the book.
        book_published_year (int | None): The new published year of the book.
        book_author_id (int | None): The new author ID of the book.
        current_user (UserModel): The current authenticated user making the request.
    
    Returns:
        dict: A dictionary containing:
            - success (bool): Status of the operation.
            - message (str): A success message.
            - data (dict): The updated book data.
    """
    try:
        book = BookUpdate(
            title=book_title,
            genre=book_genre,
            published_year=book_published_year,
            author_id=book_author_id,
        )
    except ValueError as ex:
        raise ex
    updated_book = await check_exist_book_and_update(book_id=book_id, book_update=book)
    return {
        "success": True,
        "message": "Book updated successfully",
        "data": updated_book,
    }


@router.delete("/{book_id}", summary="Delete a book", response_description="Confirmation of book deletion")
async def delete_book(
        book_id: int,
        current_user: Annotated[UserModel, Depends(get_current_user)]
) -> dict:
    """
    Delete a specific book from the database.

    Args:
        book_id (int): The ID of the book to delete.
        current_user (UserModel): The current authenticated user.

    Returns:
        dict: A dictionary containing success status and message.
    """
    await delete_book_by_id(book_id=book_id)
    return {
        "success": True,
        "message": "Book deleted successfully",
    }
