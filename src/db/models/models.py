from tortoise.contrib.pydantic import pydantic_model_creator

from src.db.models.author.model import AuthorModel
from src.db.models.book.model import BookModel
from src.db.models.user.model import UserModel

# Pydantic models
UserModel_Pydantic = pydantic_model_creator(UserModel, name="User")
BookModel_Pydantic = pydantic_model_creator(
    BookModel,
    name="Book",
    include=("id", "title", "published_year", "genre", "author")
)
AuthorModel_Pydantic = pydantic_model_creator(AuthorModel, name="Author")
