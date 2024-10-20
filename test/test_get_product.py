import pytest
from fastapi.testclient import TestClient
from app.controllers import get_product

client = TestClient(get_product)

@pytest.fixture
def mock_run_blocking_task(mocker):
    return mocker.patch("app.routes.product.run_blocking_task")

class TestGetProduct:
    def test_get_product(self, mock_run_blocking_task):
        product = "python"
        mock_data = {
            "releaseDate": "2022-10-24",
            "eol": "2027-10-31",
            "latest": "3.11.10",
            "latestReleaseDate": "2024-09-07",
            "lts": False,
            "support": "2024-04-01"
        }
        
        mock_run_blocking_task.return_value = mock_data
        
        response = client.get(f"/products/{product}")
        
        assert response.status_code == 200
        assert response.json() == mock_data
