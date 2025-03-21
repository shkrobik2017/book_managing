from datetime import datetime
from typing import List

from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator, Field

from src.db.models.author.model import AuthorModel
from src.db.models.models import BookModel_Pydantic
from src.routers.author.schemas import AuthorSchema


class BookCreate(BaseModel):
    title: str = Field(
        ...,
        description="Author's name."
    )
    published_year: int = Field(
        ...,
        description="Published year. It must be between 1800 and current year."
    )
    genre: str = Field(
        ...,
        description="Genre of the book. It can be one of those: Fiction, Non-Fiction, Science, History."
    )
    author_id: int = Field(
        ...,
        description="Author ID. You can get it from /authors endpoint."
    )

    @field_validator("published_year")
    def validate_published_year(cls, value):
        current_year = datetime.now().year
        if not (1800 <= value <= current_year):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Published year must be between 1800 and {current_year}."
            )
        return value

    @field_validator("genre")
    def validate_genre(cls, value):
        valid_genres = ["Fiction", "Non-Fiction", "Science", "History"]
        if value not in valid_genres:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Genre myst be one of those genres: {', '.join(valid_genres)}."
            )
        return value


class BookList(BaseModel):
    books: List[BookModel_Pydantic]


class BookSchema(BaseModel):
    id: int
    title: str
    published_year: int
    genre: str
    author: AuthorSchema



class BookUpdate(BaseModel):
    title: None | str = Field(
        default=None,
        description="Book title."
    )
    published_year: None | int = Field(
        default=None,
        description="Published year. It must be between 1800 and current year."
    )
    genre: None | str= Field(
        default=None,
        description="Genre of the book. It can be one of those: Fiction, Non-Fiction, Science, History."
    )
    author_id: None | int = Field(
        default=None,
        description="Author ID. You can get it from /authors endpoint."
    )

    @field_validator("published_year")
    def validate_published_year(cls, value):
        current_year = datetime.now().year
        if value is not None and not (1800 <= value <= current_year):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Published year must be between 1800 and {current_year}."
            )
        return value

    @field_validator("genre")
    def validate_genre(cls, value):
        valid_genres = ["Fiction", "Non-Fiction", "Science", "History"]
        if value is not None and value not in valid_genres:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Genre myst be one of those genres: {', '.join(valid_genres)}."
            )
        return value