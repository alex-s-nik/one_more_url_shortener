import enum
import uuid

from sqlalchemy.dialects.postgresql import UUID

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text
)

from core.config import SHORTEN_URL_LEN
from db.db import BaseModel
from .user import User


class PrivacyStatusEnum(enum.Enum):
    """Тип приватности ссылок."""
    public = 'public'
    private = 'private'


class Link(BaseModel):
    __tablename__ = 'links'

    original_url = Column(Text, nullable=False)
    shorten_url = Column(String(SHORTEN_URL_LEN), primary_key=True)
    created_by = Column(Integer, ForeignKey(User.id))
    status = Column(Enum(PrivacyStatusEnum), nullable=False, default=PrivacyStatusEnum.public)
    is_deleted = Column(Boolean, nullable=False, default=False)


class RequestsHistory(BaseModel):
    __tablename__ = 'requests_history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_date = Column(DateTime, nullable=False, default=datetime.now)
    client = Column(Text)
    link = Column(String(SHORTEN_URL_LEN), ForeignKey(Link.shorten_url, ondelete="CASCADE"))
