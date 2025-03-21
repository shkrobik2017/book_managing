from datetime import datetime

from tortoise import fields, models

class BaseCommonModel(models.Model):
    """
    Abstract base model that includes common fields for all models.
    """
    id: int = fields.IntField(pk=True)
    created_at: datetime = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True