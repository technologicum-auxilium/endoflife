import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_product():
    response = client.get("/products/all")
    assert response.status_code == 200
    assert "error" not in response.json()

def test_get_product_cycle():
    response = client.get("/products/python/3.11")
    assert response.status_code == 200
    assert "error" not in response.json()
