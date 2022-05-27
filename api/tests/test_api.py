from unittest import TestCase
from unittest.mock import patch

from fastapi.testclient import TestClient

from ..application import create_app
from ..startup_handler import create_pokemon_service
from ..errors import ResponseError

class ApiCompleteTest(TestCase):
    def setUp(self) -> None:
        app = create_app()
        create_pokemon_service(app)
        self.client = TestClient(app)

    def test_pokemon(self):
        response = self.client.get("/pokemon")
        self.assertEqual(response.status_code, 200)
        assert len(response.json()) >= 10

    def test_pokemon_by_name(self):
        response = self.client.get("/pokemon/bulbasaur")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(),
                             {"1": {"name": "bulbasaur", "weight": 69}})

    def test_pokemon_by_name__not_existing_pokemon(self):
        response = self.client.get("/pokemon/wrong-pokemon")
        self.assertEqual(response.status_code,
                         ResponseError.POKEMON_NOT_FOUND.value)
