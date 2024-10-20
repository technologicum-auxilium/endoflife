import pytest
from fastapi.testclient import TestClient
from app.controllers.product_controller import router as product_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(product_router)

client = TestClient(app)

def test_get_product_cycle_summarized():
    response = client.get("/products/python/3.11/summarized")
    assert response.status_code == 200
    data = response.json()
    assert "eol" in data
    # Atualize a data esperada com a data correta
    assert data["eol"] == "2027-10-31"
