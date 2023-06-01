from typing import Any, Optional

from fastapi import APIRouter, Depends, Response, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.user import current_user
from db.db import get_async_session
from models.user import User
from schemas.link import CreateLink, DBLink, UpdateLink
from services.link import (
    add_to_requests_history,
    create_link,
    delete_link,
    get_full_info_about_link,
    get_original_link_by_shorten,
    update_link
)

router = APIRouter()


@router.post(
    '/',
    response_model=DBLink,
    status_code=status.HTTP_201_CREATED
)
async def create(
        new_link: CreateLink,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
) -> Any:
    """Создание короткой ссылки"""
    link = await create_link(new_link=new_link, session=session, user=user)
    return link


@router.get(
    '/{shorten_url}'
)
async def get_link(
        shorten_url: str,
        request: Request,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> Any:
    """Получение полной ссылки по короткой и отражение получения в статистике"""
    original_link = await get_original_link_by_shorten(shorten_url, user, session)

    # если ссылка удалена -> 410 Gone
    if original_link.is_deleted:
        return Response(status_code=status.HTTP_410_GONE)

    # добавить в статистику
    await add_to_requests_history(shorten_url, request.client.host, session)

    # вернуть 307 статус-код
    return RedirectResponse(original_link.original_url)


@router.get('/{shorten_url}/status')
async def status_link(
        shorten_url: str,
        full_info: Optional[str] = None,
        offset: int = 0,
        limit: int = 10,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> Any:
    """Получение статуса ссылки. Если присутствует параметр full_info, то получить статистику по переходам."""
    status = await get_full_info_about_link(
        shorten_url, user, session, full_info, limit, offset)
    return status


@router.delete('/{shorten_url}')
async def delete(
        shorten_url: str,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> Any:
    """Удаление ссылки. Полностью ссылка не удаляется - лишь помечается удаленной."""
    await delete_link(shorten_url, user, session)
    return Response(status_code=status.HTTP_410_GONE)


@router.patch(
    '/{shorten_url}',
    response_model=DBLink
)
async def update(
        shorten_url: str,
        updated_link: UpdateLink,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> Any:
    """Обновление статуса ссылки. Доступно только зарегистрированным пользователям."""
    link = await update_link(shorten_url, updated_link, user, session)
    return link
