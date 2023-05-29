from typing import Optional

from pydantic import BaseModel, HttpUrl

from models.link import StatusEnum
from models.user import User

class DBLink(BaseModel):
    """Представление ссылки при запросе из БД"""
    original_url: HttpUrl
    shorten_url: str
    created_by: Optional[User]
    status: StatusEnum
    is_deleted: bool

class CreateLink(BaseModel):
    """Схема ссылки при создании"""
    original_url: HttpUrl
    status: StatusEnum

class UpdateLink(BaseModel):
    """Схема обновления ссылки. Обновить можно только поле со статусом"""
    status: StatusEnum
