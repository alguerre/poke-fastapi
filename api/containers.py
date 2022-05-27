from os import path
from typing import Tuple

from dependency_injector import containers, providers

from .db import Database
from .db.repositories.pokemon import PokemonRepository
from .services.pokemon import PokemonService


def get_url_db() -> Tuple[str, str]:
    api_directory = path.dirname(path.dirname(path.abspath(__file__)))
    db_path = path.join(api_directory, "pokemon.sqlite")
    return f"sqlite+aiosqlite:///{db_path}", f"sqlite:///{db_path}"


class Container(containers.DeclarativeContainer):
    db_url_async, db_url_sync = get_url_db()
    db = providers.Singleton(Database,
                             db_url_async=db_url_async,
                             db_url_sync=db_url_sync)

    pokemon_repository = providers.Factory(
        PokemonRepository,
        session_factory=db.provided.session,
        database=db
    )

    pokemon_service = providers.Factory(
        PokemonService,
        pokemon_repository=pokemon_repository
    )
