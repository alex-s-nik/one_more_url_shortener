from fastapi import Request, Response, status


from core.config import BLACKLIST


class BlacklistMiddleware:
    """Middleware для ограничения доступа из запрещенных подсетей.
    Сами подсети задаются в файле core.config."""
    def __init__(self):
        self.blacklist = BLACKLIST

    async def __call__(self, request: Request, call_next):
        if request.client.host in self.blacklist:
            return Response(
                'Your network is in blacklist',
                status_code=status.HTTP_403_FORBIDDEN
            )

        response = await call_next(request)
        return response
