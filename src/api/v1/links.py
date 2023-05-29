from typing import Any

from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.user import current_user
from db.db import get_session
from models.user import User
from schemas.link import CreateLink, DBLink
from services.link import create_link, get_original_link_by_shorten

router = APIRouter()

@router.post(
    '/',
    response_model=DBLink,
    status_code=status.HTTP_201_CREATED
)
async def create_link(
    new_link: CreateLink,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_session),
) -> Any:
    link = await create_link(new_link=new_link, session=session, user=user)
    return link

@router.get(
    '/{shorten_url}'
)
async def get_link(
    shorten_url: str,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_session)
) -> Any:
    
    original_link = await get_original_link_by_shorten(shorten_url, user, session)
    # если ссылка удалена -> 410 Gone
    if original_link.is_deleted:
        return Response(status_code=status.HTTP_410_GONE)
    # добавить в статистику


    # вернуть 307
    return RedirectResponse(original_link)

    

@router.get('{shorten_url}/status')
async def get_status(
    shorten_url: str,
) -> Any:
    status = await get_status(shorten_url)
    return status

@router.delete('/{shorten_url}')
async def delete_link(shorten_url: str) -> Any:
    await delete_link(shorten_url)
    return Response(status_code=status.HTTP_410_GONE)
