from fastapi import APIRouter

from .links import router as links_router
from .tools import router as tools_router
from .user import router as user_router

router = APIRouter()

router.include_router(user_router)
router.include_router(tools_router, tags=['tools'])
router.include_router(links_router, tags=['links'])
