import unittest
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)


class TestHealth(unittest.TestCase):
    def test_liveness(self):
        response = client.get("/health/liveness")
        self.assertEqual(response.status_code, 200)

    def test_readiness(self):
        response = client.get("/health/readiness")
        self.assertEqual(response.status_code, 200)
