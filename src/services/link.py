import random
import string

from fastapi import HTTPException, status
from pydantic import HttpUrl
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import SHORTEN_URL_LEN
from models.link import Link, RequestsHistory, PrivacyStatusEnum
from models.user import User

from schemas.link import DBLink

async def create_link(
    new_link: Link,
    user: User,
    session: AsyncSession
):
    """Create new link in DB"""
    new_link_dict = new_link.dict()
    new_link_dict['created_by'] = user
    new_link_dict['shorten_url'] = make_shorten_url(session)
    if not user:
        new_link_dict['status'] = PrivacyStatusEnum.public
    db_link = Link(**new_link_dict)
    session.add(db_link)

    await session.commit()
    await session.refresh(db_link)

    return db_link

async def get_original_link_by_shorten(
        shorten_url: str,
        user: User,
        session: AsyncSession
):
    """Get original link by shorten link"""
    statement = select(Link.original_url).where(Link.shorten_url==shorten_url)
    results = await session.execute(statement=statement)
    original_link = results.scalar_one()
    if original_link.status == PrivacyStatusEnum.private and user != original_link.created_by:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return original_link


async def make_shorten_url(session: AsyncSession) -> str:
    def generate_short_name():
        return ''.join(
            random.choice(
                string.ascii_lowercase + string.digits
                for _ in range(SHORTEN_URL_LEN)
            )
        )
    
    while True:
        shorten_url = generate_short_name()
        if not select(Link).where(Link.shorten_url==shorten_url).exists():
            break

    return shorten_url


async def get_all_links_by_user(user: User, session: AsyncSession):
    """Get all links created by user"""
    statement = select(Link).where(Link.created_by==user)
    results = await session.execute(statement)
    return results


async def get_jumps_count_by_link(shorten_url: str, session: AsyncSession):
    # вернуть количество переходов по ссылке
    statement = select(RequestsHistory).where(RequestsHistory.link==shorten_url).count()
    result = await session.execute(statement)
    return result


async def get_full_info_about_link(shorten_url: str, session: AsyncSession, limit: int, offset: int):
    # вернуть полную информацию о переходах по ссылке
    statement = select(RequestsHistory).where(RequestsHistory.link==shorten_url).limit(limit).offset(offset)
    results = await session.execute(statement)
    return results
