import random
import string
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import func, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import SHORTEN_URL_LEN
from models.link import Link, RequestsHistory, PrivacyStatusEnum
from models.user import User

from schemas.link import RequestsHistoryDB, FullInfoLinks


async def create_link(
        new_link: Link,
        user: User,
        session: AsyncSession
):
    """Create new link in DB"""
    new_link_dict = new_link.dict()
    new_link_dict['created_by'] = user
    new_link_dict['shorten_url'] = await make_shorten_url(session)
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
) -> Link:
    """Получение записи из БД по короткой ссылке."""
    statement = select(Link).where(Link.shorten_url == shorten_url)
    results = await session.execute(statement=statement)
    try:
        original_link = results.scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if original_link.status == PrivacyStatusEnum.private and user != original_link.created_by:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return original_link


async def make_shorten_url(session: AsyncSession) -> str:
    """Генерация короткой ссылки и проверка, что ее нет в БД"""
    def generate_short_name():
        """Генерация тела короткой ссылки."""
        return ''.join(
            random.choice(
                string.ascii_lowercase + string.digits
            )
            for _ in range(SHORTEN_URL_LEN)
        )

    while True:
        shorten_url = generate_short_name()
        statement = select(Link).where(Link.shorten_url == shorten_url)
        is_short_url_exists = (await session.execute(statement)).scalars().all()
        if not is_short_url_exists:
            break

    return shorten_url


async def get_all_links_by_user(user: User, session: AsyncSession) -> List[Link]:
    """Получение всех ссылок, созданных пользователем."""
    statement = select(Link).where(Link.created_by == user)
    results = await session.execute(statement)
    return results


async def get_jumps_count_by_link(shorten_url: str, session: AsyncSession) -> int:
    """Получение количества переходов по ссылке."""
    statement = select(func.count("*")).select_from(
        RequestsHistory
    ).where(RequestsHistory.link == shorten_url)

    result = await session.execute(statement)
    return result.scalar_one()


async def get_full_info_about_link(
        shorten_url: str,
        user: User,
        session: AsyncSession,
        fullinfo: Optional[str],
        limit: int, offset: int
) -> FullInfoLinks:
    """Получение полной информации о ссылке: сколько раз был сделан переход по ней и информация по каждому переходу"""
    current_link = await get_original_link_by_shorten(shorten_url, user, session)

    if current_link.status == PrivacyStatusEnum.private and current_link.created_by != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    count = await get_jumps_count_by_link(shorten_url, session)

    if not isinstance(fullinfo, str):
        return count
    statement = select(
        RequestsHistory
    ).where(RequestsHistory.link == shorten_url).limit(limit).offset(offset)

    full_links_info = await session.execute(statement)
    return full_links_info


async def delete_link(shorten_url: str, user: User, session: AsyncSession):
    """Удаление ссылки. Физическое удаление ссылки из БД не производится, только помечается удаленной."""
    current_link = await get_original_link_by_shorten(shorten_url, user, session)
    if current_link.created_by != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    statement = update(Link).where(Link.shorten_url == shorten_url).values(is_deleted=True)
    await session.execute(statement)
    await session.commit()


async def add_to_requests_history(
        shorten_url: str,
        client: str,
        session: AsyncSession
):
    """Создание информации о факте перехода по ссылке."""
    new_record_dict = RequestsHistoryDB(client=client, link=shorten_url).dict()
    db_record = RequestsHistory(**new_record_dict)
    session.add(db_record)

    await session.commit()


async def update_link(
        shorten_url: str,
        updated_link: Link,
        user: User,
        session: AsyncSession
):
    """Обновление статуса ссылки. Можно изменить только статус ссылки.
    Метод доступен только для зарегистрированных пользователей."""
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    current_link = await get_original_link_by_shorten(
        shorten_url,
        user,
        session
    )
    current_link.status = updated_link.status
    session.add(current_link)
    await session.commit()
    await session.refresh(current_link)
    return current_link
