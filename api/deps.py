from starlette.requests import Request


def get_pokemon_service(request: Request):
    return request.app.state.pokemon_service
