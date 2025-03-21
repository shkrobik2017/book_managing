from datetime import datetime

from tortoise import fields

from src.db.common.model import BaseCommonModel
from src.db.models.author.model import AuthorModel


class BookModel(BaseCommonModel):
    title: str = fields.CharField(max_length=100, unique=True)
    author: AuthorModel = fields.ForeignKeyField(
        "models.AuthorModel",
        related_name="books"
    )
    published_year: int = fields.IntField()
    genre: str = fields.CharField(max_length=100)