from tortoise import fields

from src.db.common.model import BaseCommonModel


class UserModel(BaseCommonModel):
    """
    Model representing a user with their credentials and contact details.
    """
    username: str = fields.CharField(max_length=50, unique=True)
    hashed_password: str = fields.CharField(max_length=128)