from fastapi import FastAPI

from .containers import Container
from .endpoints import router
from .startup_handler import create_start_app_handler


def create_app() -> FastAPI:
    container = Container()

    api = FastAPI()
    api.container = container
    api.add_event_handler("startup", create_start_app_handler(api))
    api.include_router(router)
    return api


if __name__ == "__main__":
    app = create_app()
