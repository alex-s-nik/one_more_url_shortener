import asyncio

import pytest
from fastapi.testclient import TestClient

from main import app
from models.link import Link, PrivacyStatusEnum
from models.user import User
from core.user import current_user

user = User()

@pytest.fixture
def user_client():
    app.dependency_overrides = {}
    app.dependency_overrides[current_user] = lambda: user
    with TestClient(app) as client:
        yield client


@pytest.fixture
def link():
    return Link(
        original_url = 'https://python.org',
        shorten_url = 'abcd',
        created_by = None,
        status = PrivacyStatusEnum.public,
        is_deleted = False
    )

@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()