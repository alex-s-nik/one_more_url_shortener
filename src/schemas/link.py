from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, HttpUrl

from models.link import PrivacyStatusEnum
from models.user import User

class DBLink(BaseModel):
    """Представление ссылки при запросе из БД"""
    original_url: HttpUrl
    shorten_url: str
    created_by: Optional[int]
    status: PrivacyStatusEnum
    is_deleted: bool

    class Config:
        orm_mode = True

class CreateLink(BaseModel):
    """Схема ссылки при создании"""
    original_url: HttpUrl
    status: Optional[PrivacyStatusEnum]

class UpdateLink(BaseModel):
    """Схема обновления ссылки. Обновить можно только поле со статусом"""
    status: PrivacyStatusEnum


class RequestsHistoryDB(BaseModel):
    client: str
    link: str

class LinkInfo(BaseModel):
    date: datetime
    client: str

class FullInfoLinks(BaseModel):
    count: int
    links_info: Optional[List[LinkInfo]]
