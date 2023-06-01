from typing import Any

from fastapi import APIRouter, Response, status

from services.tools import ping

router = APIRouter()


@router.get('/ping')
async def ping_db() -> Any:
    """Проверка доступности БД."""
    if await ping():
        return Response(
            'DB is available',
            status.HTTP_200_OK
        )
    return Response(
        'Connection to DB has some problem',
        status.HTTP_503_SERVICE_UNAVAILABLE
    )
