from enum import Enum, auto


class ResponseError(Enum):
    POKEMON_NOT_FOUND = 450
    POKEMON_TABLE_NOT_FOUND = auto()
