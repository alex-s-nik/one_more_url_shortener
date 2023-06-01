from fastapi import status
from httpx import AsyncClient

from main import app


async def test_create_link(event_loop):
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/api/v1") as ac:
        response = await ac.post(
            '/',
            json={
                'original_url': 'https://fastapi.tiangolo.com/'
            }
        )
    assert response.status_code == status.HTTP_201_CREATED
    response_keys = [
        'original_url',
        'shorten_url',
        'created_by',
        'status',
        'is_deleted'
    ]
    assert (
        sorted(response.json().keys()) == sorted(response_keys)
    ), "Не все поля возвращаются в ответе при создании ссылки"


async def test_get_link():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/api/v1") as ac:
        response = await ac.post(
            '/',
            json={
                'original_url': 'https://fastapi.tiangolo.com/'
            }
        )
    short_url = response.json()['shorten_url']
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/api/v1") as ac:
        response = await ac.get(
            f'/{short_url}'
        )

    assert (
        response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    ), "Статус код при переходе по короткой ссылке не соответствует требуемому"


async def test_get_link_status():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/api/v1") as ac:
        response = await ac.post(
            '/',
            json={
                'original_url': 'https://fastapi.tiangolo.com/'
            }
        )
    short_url = response.json()['shorten_url']
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/api/v1") as ac:
        response = await ac.get(
            f'/{short_url}'
        )
        response = await ac.get(f'/{short_url}/status')
    assert response.json() == 1


async def test_delete_link():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/api/v1") as ac:
        response = await ac.post(
            '/',
            json={
                'original_url': 'https://fastapi.tiangolo.com/'
            }
        )
    short_url = response.json()['shorten_url']

    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/api/v1") as ac:
        response = await ac.delete(f'/{short_url}')
    assert response.status_code == status.HTTP_410_GONE
