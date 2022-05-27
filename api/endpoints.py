import time

from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from .db.repositories.exceptions import PokemonNotFound, PokemonTableNotFound
from .deps import get_pokemon_service
from .services.pokemon import PokemonService
from .errors import ResponseError

router = APIRouter()


@router.get("/")
def welcome():
    return {"msg": "Welcome to Pokemon API"}


@router.get("/pokemon")
@inject
async def pokemon_list(pokemon_service: PokemonService = Depends(get_pokemon_service)):
    try:
        pokemons = await pokemon_service.get_pokemons()
        return {p.id: {"name": p.name, "weight": p.weight} for p in pokemons}

    except PokemonTableNotFound:
        return JSONResponse(
            status_code=ResponseError.POKEMON_TABLE_NOT_FOUND.value,
            content="pokemons table does not exist, use 'load' first")


@router.get("/pokemon/{name}")
@inject
async def get_pokemon_by_name(name: str,
                       pokemon_service: PokemonService = Depends(get_pokemon_service)):
    try:
        pokemon = await pokemon_service.get_pokemon_by_name(name)
        return {pokemon.id: {"name": pokemon.name, "weight": pokemon.weight}}

    except PokemonNotFound:
        return JSONResponse(status_code=ResponseError.POKEMON_NOT_FOUND.value,
                            content=f"Requested pokemon ({name}) not in db.")
    except PokemonTableNotFound:
        return JSONResponse(
            status_code=ResponseError.POKEMON_TABLE_NOT_FOUND.value,
            content="pokemons table does not exist, use 'load' first")


@router.get("/load/{number}")
@inject
async def load_pokemons(number: int,
                       pokemon_service: PokemonService = Depends(get_pokemon_service)):
    start = time.time()
    await pokemon_service.load_pokemons(number)
    return {"msg": f"First {number} pokemons have been loaded in {time.time() - start}s"}
