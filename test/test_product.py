import unittest
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)


class TestProduct(unittest.TestCase):
    def test_get_product(self):
        response = client.get("/products/python")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("error", response.json())

    def test_get_product_cycle(self):
        response = client.get("/products/python/3.11")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("error", response.json())
        self.assertIn("eol", response.json())
