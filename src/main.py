import uvicorn
from fastapi import FastAPI

from api.v1.links import router
from core import config
from core.config import app_settings
from middlewares.blacklist import BlacklistMiddleware


app = FastAPI(
    title=app_settings.app_title,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json'
)

blacklist_middleware = BlacklistMiddleware()
app.include_router(router, prefix='/api/v1')

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=config.PROJECT_HOST,
        port=config.PROJECT_PORT,
        reload=True
    )
