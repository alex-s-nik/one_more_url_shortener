from sqlalchemy import Column, Integer
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from db.db import BaseModel


class User(SQLAlchemyBaseUserTable[int], BaseModel):
    id = Column(Integer, primary_key=True)
