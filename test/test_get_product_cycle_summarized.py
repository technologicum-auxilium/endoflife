import unittest
from fastapi.testclient import TestClient
from src.app.main import app
from unittest.mock import patch

client = TestClient(app)


class TestGetProductCycleSummarized(unittest.TestCase):
    @patch("src.app.controllers.product_controller.run_blocking_task")
    def test_get_product_cycle_summarized(self, mock_run_blocking_task):
        product = "python"
        cycle = "3.11"
        mock_data = {"eol": "2027-10-31"}

        mock_run_blocking_task.return_value = {
            "releaseDate": "2022-10-24",
            "eol": "2027-10-31",
            "latest": "3.11.10",
            "latestReleaseDate": "2024-09-07",
            "lts": False,
            "support": "2024-04-01",
        }

        response = client.get(f"/products/{product}/{cycle}/summarized")

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), mock_data)
