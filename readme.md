# Pokemon async API exercise
This is a toy exercise in which we download some data from [pokeapi.co](https://pokeapi.co/) to later expose them with an async API.

## Learning goals
- Asynchronous requests and API
- Use the repository pattern and dependency injection

## Requirements
- Create an API rest with [FastAPI](https://fastapi.tiangolo.com/)
- Use repository pattern
- Use [dependency injection](https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html)
- Deploy it with uvicorn in a Docker container
- Pokemon data can be stored in any SQL or CSV file

### Endpoints
- One to load the _n_ first pokemon in our DB/CSV
- One to list all loaded pokemon
- One to get pokemon data from its name


## Usage
Launch API through the 8001 port.
```
docker build -t pokemon_image:latest .
docker-compose up -d
```

Check documentation
```
http://127.0.0.1:8001/docs
```
