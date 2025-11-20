from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.app.setup.app_startup import startup_event
from src.interface.fastapi.routes import cards, web_socket, bios



def create_fastapi_app():

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        startup_event()
        yield
    app = FastAPI(lifespan=lifespan)

    app.include_router(cards.router)
    app.include_router(web_socket.router)
    app.include_router(bios.router)

    return app


    