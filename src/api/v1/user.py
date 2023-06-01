from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.user import auth_backend, current_user, fastapi_users
from db.db import get_async_session
from models.user import User
from schemas.user import UserCreate, UserRead, UserUpdate
from services.link import get_all_links_by_user


router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)


@router.get(
    '/user/status',
)
async def all_user_links(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Получение всех ссылок пользователя."""
    links = await get_all_links_by_user(user, session)
    return links
