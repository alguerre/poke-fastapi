from typing import Iterator

from ..db.repositories.pokemon import PokemonRepository
from ..models.pokemon import Pokemon


class PokemonService:
    def __init__(self, pokemon_repository: PokemonRepository) -> None:
        self._repository = pokemon_repository

    async def get_pokemons(self) -> Iterator[Pokemon]:
        return await self._repository.get_all()

    async def get_pokemon_by_name(self, name: str) -> Pokemon:
        return await self._repository.get_by_name(name)

    async def load_pokemons(self, number: int) -> None:
        return await self._repository.load(number)
