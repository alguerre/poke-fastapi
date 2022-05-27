from typing import Callable

from fastapi import FastAPI

from .containers import Container


def create_pokemon_service(app: FastAPI) -> None:
    app.state.pokemon_service = Container.pokemon_service.provider().provided()


def create_start_app_handler(app: FastAPI) -> Callable:
    def start_app() -> None:
        create_pokemon_service(app)

    return start_app
