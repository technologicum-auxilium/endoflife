import pytest
from fastapi.testclient import TestClient
from app.main import app  # Ajuste conforme o caminho real

client = TestClient(app)

@pytest.fixture
def mock_run_blocking_task(mocker):
    return mocker.patch("app.routes.product.run_blocking_task")

class TestGetProductCycleSummarized:
    def test_get_product_cycle_summarized(self, mock_run_blocking_task):
        product = "python"
        cycle = "3.11"
        mock_data = {
            "eol": "2027-10-31"
        }
        
        mock_run_blocking_task.return_value = {"releaseDate": "2022-10-24", "eol": "2027-10-31"}
        
        response = client.get(f"/products/{product}/{cycle}/summarized")
        
        assert response.status_code == 200
        assert response.json() == mock_data
