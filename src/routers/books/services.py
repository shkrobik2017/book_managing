import csv
import json
import logging

from fastapi import HTTPException, status, File, UploadFile
from typing import List, Dict, Any, Tuple

from src.db.models.author.repository import get_author_by_id_from_db
from src.db.models.book.model import BookModel
from src.db.models.book.repository import get_book_by_title, create_book_in_db, get_books_from_db, \
    get_book_by_id_from_db, get_books_by_filter_from_db, update_book_in_db, delete_book_from_db, bulk_create_books_in_db
from src.db.models.models import BookModel_Pydantic, AuthorModel_Pydantic
from src.routers.books.schemas import BookUpdate, BookCreate

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


async def check_book_and_author_exist(book: Dict[str, Any]) -> AuthorModel_Pydantic:
    """
    Check if the author exists and retrieve it, and ensure that the book does not already exist.

    Args:
        book (Dict[str, Any]): A dictionary containing book details.

    Returns:
        AuthorModel_Pydantic: The author of the book.

    Raises:
        HTTPException: If the author is not found or the book already exists.
    """
    author = await get_author_by_id_from_db(author_id=book.get("author_id"))
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )
    if await get_book_by_title(title=book.get("title")) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book already exists"
        )
    return author


async def check_exist_book_and_create(book: Dict[str, Any]) -> Tuple[BookModel_Pydantic, AuthorModel_Pydantic]:
    """
    Check if the book exists, and if not, create a new book.

    Args:
        book (Dict[str, Any]): A dictionary containing book details.

    Returns:
        Dict[str, BookModel_Pydantic]: The created book and its author in Pydantic format.

    Raises:
        HTTPException: If any error occurs during the process.
    """
    try:
        author = await check_book_and_author_exist(book=book)
        created_book = await create_book_in_db(book=book, author=author)
        return BookModel_Pydantic.model_validate(created_book), AuthorModel_Pydantic.model_validate(author)

    except HTTPException:
        raise
    except Exception as ex:
        logger.error(f"Error during book creation: {ex}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"Internal Error": "Something went wrong during book creation!"}
        )


async def import_from_json(file: UploadFile) -> List[Dict[str, Any]]:
    """
    Parse JSON file content into a list of dictionaries.

    Args:
        file (UploadFile): The uploaded JSON file.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing book data.

    Raises:
        HTTPException: If the JSON format is invalid.
    """
    content = await file.read()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")


async def import_from_csv(file: UploadFile) -> List[Dict[str, str]]:
    """
    Parse CSV file content into a list of dictionaries.

    Args:
        file (UploadFile): The uploaded CSV file.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing book data.
    """
    content = (await file.read()).decode("utf-8")
    reader = csv.DictReader(content.splitlines())
    return [row for row in reader]


async def validate_and_save_books_to_db(file: UploadFile) -> Dict[str, Any]:
    """
    Validate and save books from a JSON or CSV file to the database.

    Args:
        file (UploadFile): The uploaded file containing book details.

    Returns:
        Dict[str, Any]: Dictionary containing details about the save operation.

    Raises:
        HTTPException: If the file format is unsupported or file processing fails.
    """

    if file.filename.endswith(".json"):
        books = await import_from_json(file)
    elif file.filename.endswith(".csv"):
        books = await import_from_csv(file)
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Please upload a JSON or CSV file."
        )

    valid_books = []
    exist_books = []
    not_found_authors = []

    for book in books:
        try:
            validated_book = BookCreate(**book)
            author = await check_book_and_author_exist(book=validated_book.model_dump())
            valid_books.append(BookModel(
                title=validated_book.title,
                author=author,
                published_year=validated_book.published_year,
                genre=validated_book.genre,
            ))
        except HTTPException as ex:
            logger.error(f"Validation error for book {book.get('title')}: {ex}")
            if ex.status_code == 400 and ex.detail == "Book already exists":
                exist_books.append(book)
            elif ex.status_code == 404 and ex.detail == "Author not found":
                not_found_authors.append(book)
            continue
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"Internal Error": f"Something went wrong during book import: {ex}"}
            )

    if valid_books:
        await bulk_create_books_in_db(valid_books=valid_books)

    return {
        "Count of saved books": len(valid_books),
        "Books already exist": exist_books,
        "Authors not found": not_found_authors
    }



async def get_books() -> List[BookModel_Pydantic]:
    """
    Fetch all books from the database.

    Returns:
        List[BookModel_Pydantic]: A list of books in Pydantic format.
    """
    try:
        books = await get_books_from_db()
        return [BookModel_Pydantic.from_orm(book) for book in books]
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"Internal Error": "Something went wrong during all books fetching!"}
        )


async def get_book_by_id(book_id: int) -> BookModel_Pydantic:
    """
    Fetch a book by its ID.

    Args:
        book_id (int): The ID of the book.

    Returns:
        BookModel_Pydantic: The book in Pydantic format.
    """
    try:
        book = await get_book_by_id_from_db(book_id=book_id)
        if book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        return BookModel_Pydantic.model_validate(book), AuthorModel_Pydantic.model_validate(book.author)
    except HTTPException as ex:
        raise ex
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"Internal Error": "Something went wrong during book fetching!"}
        )


async def get_book_by_filters(filters: Dict) -> List[BookModel_Pydantic]:
    """
    Fetch books based on filters.

    Args:
        filters (Dict): The filter criteria.

    Returns:
        List[BookModel_Pydantic]: A list of books in Pydantic format.
    """
    try:
        books = await get_books_by_filter_from_db(filters=filters)
        if len(books) > 0:
            return [BookModel_Pydantic.from_orm(book) for book in books]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No books found"
        )
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"Internal Error": "Something went wrong during book filtering!"}
        )


async def check_exist_book_and_update(book_id: int, book_update: BookUpdate) -> BookModel_Pydantic:
    """
    Check if a book exists, and update its details.

    Args:
        book_id (int): The ID of the book to update.
        book_update (Dict): A dictionary containing the updated book details.

    Returns:
        BookModel_Pydantic: The updated book in Pydantic format.
    """
    try:
        book = await get_book_by_id_from_db(book_id=book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )

        if book_update.title is not None:
            book.title = book_update.title
        if book_update.author_id is not None:
            author = await get_author_by_id_from_db(author_id=book_update.author_id)
            if author is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Author not found"
                )
            book.author = await get_author_by_id_from_db(author_id=book_update.author_id)
        if book_update.published_year is not None:
            book.published_year = book_update.published_year
        if book_update.genre is not None:
            book.genre = book_update.genre

        await book.save()
        return BookModel_Pydantic.model_validate(book)
    except HTTPException:
        raise
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"Internal Error": "Something went wrong during book updating!"}
        )


async def delete_book_by_id(book_id: int) -> Dict[str, str]:
    """
    Delete a book by its ID.

    Args:
        book_id (int): The ID of the book to delete.

    Returns:
        Dict[str, str]: A success message.
    """
    try:
        book = await get_book_by_id_from_db(book_id=book_id)
        if book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        await delete_book_from_db(book_id=book_id)
        return {"message": "Book deleted successfully"}
    except HTTPException:
        raise
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"Internal Error": "Something went wrong during book deletion!"}
        )
