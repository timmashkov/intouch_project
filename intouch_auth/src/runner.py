import asyncio
import sys

from fastapi import FastAPI

import uvicorn

from application.server import ApiServer


def start_app() -> FastAPI:

    app = ApiServer.app_profile

    return ApiServer(app).get_app()


if __name__ == "__main__":
    if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    uvicorn.run("runner:start_app", port=1222, reload=True)
