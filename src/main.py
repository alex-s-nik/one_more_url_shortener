import logging

import uvicorn
from fastapi import FastAPI

from api.v1 import base
from core import config
from core.config import app_settings
from core.logger import LOGGING
from middlewares.blacklist import BlacklistMiddleware


app = FastAPI(
    title=app_settings.app_title,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json'
)

app.add_middleware(BlacklistMiddleware)
app.include_router(base.router, prefix='/api/v1')

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=config.PROJECT_HOST,
        port=config.PROJECT_PORT,
        reload=True
    ) 