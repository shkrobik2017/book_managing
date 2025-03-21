from datetime import datetime

from tortoise import fields

from src.db.common.model import BaseCommonModel


class AuthorModel(BaseCommonModel):
    full_name: str = fields.CharField(max_length=100)
    birth_date: datetime = fields.DateField(default=None, null=True)
    biography: str = fields.TextField(default=None, null=True)