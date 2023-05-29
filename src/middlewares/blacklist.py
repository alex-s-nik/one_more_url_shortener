from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

from core.config import BLACKLIST

class BlacklistMiddleware(BaseHTTPMiddleware):
    def __init__(self, app) -> None:
        self.blacklist = BLACKLIST
    
    async def dispatch(self, request: Request, call_next: callable):
        if request.client.host in self.blacklist:
            return Response(
                'You are in blacklist',
                status_code=status.HTTP_403_FORBIDDEN
            )

        response = await call_next(request)
        return response
