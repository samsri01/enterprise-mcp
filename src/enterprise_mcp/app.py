from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount

from enterprise_mcp.mcp_server import mcp
from enterprise_mcp.config import settings
from enterprise_mcp.container import build_auth_strategy
from enterprise_mcp.security.middleware import AuthMiddleware


async def health(request):
    return PlainTextResponse("OK", status_code=200)


routes = [
    Route("/health", health, methods=["GET"]),
    Mount("/mcp", app=mcp.streamable_http_app()),
]

app = Starlette(
    debug=settings.debug,
    routes=routes,
)

# Add auth middleware
app.add_middleware(
    AuthMiddleware,
    strategy=build_auth_strategy(),
    protected_prefixes=("/mcp",),     # protect MCP
    public_prefixes=("/health",),     # health open
)
