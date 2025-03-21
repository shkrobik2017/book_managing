from datetime import datetime
from typing import List, Annotated
from fastapi import HTTPException, status

from pydantic import BaseModel, field_validator, Field, BeforeValidator

from src.db.models.author.model import AuthorModel
from src.db.models.models import BookModel_Pydantic, AuthorModel_Pydantic


def parse_date(value: str) -> datetime:
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in format YYYY-MM-DD.")

class AuthorCreate(BaseModel):
    name: str = Field(
        ...,
        description="Author's name."
    )
    surname: str = Field(
        ...,
        description="Author's surname."
    )
    birth_date: Annotated[datetime, BeforeValidator(parse_date)] = Field(
        ...,
        description="Author's birth date. Must be in format YYYY-MM-DD. Must be between 1700 and current year."
    )
    biography: str | None = Field(
        default=None,
        description="Author's biography."
    )

    @field_validator("birth_date")
    def validate_birth_date(cls, value):
        current_year = datetime.now().year
        birth_year = value.year
        if not (1700 <= birth_year <= current_year):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Author's birth date must be between 1700 and {current_year}."
            )
        return value


class AuthorsList(BaseModel):
    authors: List[AuthorModel_Pydantic]

class AuthorSchema(BaseModel):
    id: int
    full_name: str
    birth_date: datetime
    biography: str | None

class AuthorUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        description="Book title."
    )
    surname: str | None = Field(
        default=None,
        description="Author's surname."
    )
    birth_date: Annotated[datetime, BeforeValidator(parse_date)] | None= Field(
        default=None,
        description="Author's birth date. Must be in format YYYY-MM-DD. Must be between 1700 and current year."
    )
    biography: str | None = Field(
        default=None,
        description="Author's biography."
    )

    @field_validator("birth_date")
    def validate_birth_date(cls, value):
        if value is not None:
            current_year = datetime.now().year
            birth_year = value.year
            if not (1700 <= birth_year <= current_year):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Author's birth date must be between 1700 and {current_year}."
                )
            return value
        return value