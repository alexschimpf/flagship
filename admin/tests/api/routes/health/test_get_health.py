from fastapi.testclient import TestClient

from app.main import app
from tests.api.base_test_case import BaseTestCase

client = TestClient(app)


class TestGetHealth(BaseTestCase):

    def test_get_health__200(self) -> None:
        response = client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '"Ok"')
