from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.app.setup.app_startup import startup_event
from src.features.bios.interface.fastapi import bios_routes
from src.features.cards.interface.fastapi import cards_routes
from src.features.websocket.interface.fastapi import web_socket_routes

def create_fastapi_app():

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        startup_event()
        yield
    app = FastAPI(lifespan=lifespan)

    app.include_router(cards_routes.router)
    app.include_router(web_socket_routes.router)
    app.include_router(bios_routes.router)

    return app


    