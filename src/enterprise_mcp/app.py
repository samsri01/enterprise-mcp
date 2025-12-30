from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount

from enterprise_mcp.config import settings
from enterprise_mcp.mcp_server import mcp

async def heatlth(request):
    return PlainTextResponse("OK", status_code=200)

routes = [
    Route("/health", heatlth, methods=["GET"]),
    Mount("/mcp", app=mcp.streamable_http_app())
]

app = Starlette(debug=settings.debug_mode, routes=routes)