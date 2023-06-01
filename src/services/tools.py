from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_async_session


async def ping(session: AsyncSession = Depends(get_async_session)) -> bool:
    """Проверка доступности БД."""
    try:
        await session.connection()
        return True
    except Exception:
        return False
