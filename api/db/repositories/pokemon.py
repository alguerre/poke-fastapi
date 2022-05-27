from typing import Iterator

import httpx
import sqlalchemy.exc
from sqlalchemy.future import select

from ...db.repositories.exceptions import PokemonNotFound, PokemonTableNotFound
from ...models.pokemon import Pokemon


class PokemonRepository:

    def __init__(self, session_factory, database) -> None:
        self.session_factory = session_factory
        self.database = database

    async def get_by_name(self, name: str) -> Pokemon:
        with self.session_factory() as session:
            try:
                q = select(Pokemon).filter(Pokemon.name == name).limit(1)
                result = await session.execute(q)
                pokemon = result.scalar()
                if not pokemon:
                    raise PokemonNotFound
                return pokemon
            except sqlalchemy.exc.OperationalError as e:
                raise PokemonTableNotFound from e
    
    async def get_all(self) -> Iterator[Pokemon]:
        with self.session_factory() as session:
            q = select(Pokemon)
            try:
                result = await session.execute(q)
                return result.scalars()
            except sqlalchemy.exc.OperationalError as e:
                raise PokemonTableNotFound from e

    async def load(self, number: int = 50) -> None:
        self.database.drop_existing_tables()
        self.database.create_new_tables()

        async with httpx.AsyncClient() as client:
            with self.session_factory() as session:
                for i in range(1, number + 1):
                    r = await client.get(
                        f'https://pokeapi.co/api/v2/pokemon/{i}')
                    r_json = r.json()
                    pokemon = Pokemon(id=i,
                                      name=r_json["name"],
                                      weight=r_json["weight"])
                    session.add(pokemon)

                await session.commit()
