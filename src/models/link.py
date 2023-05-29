import enum

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.db import BaseModel
from .user import User

class PrivacyStatusEnum(enum.Enum):
    public = 0
    private = 1


class Link(BaseModel):
    __tablename__ = 'links'

    original_url = Column(String, nullable=False)
    shorten_url = Column(String, primary_key=True)
    created_by = Column(Integer, ForeignKey(User.id), nullable=False)
    status = Column(Enum(PrivacyStatusEnum), nullable=False, default=PrivacyStatusEnum.public)
    is_deleted = Column(Boolean, nullable=False, default=False)


class RequestsHistory(BaseModel):
    __tablename__ = 'requests_history'
    id = Column(Integer, primary_key=True)
    event_date = Column(DateTime, nullable=False, default=datetime.now)
    client = Column(String)
    link = Column(String, ForeignKey(Link.shorten_url))
