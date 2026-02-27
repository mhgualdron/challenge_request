import pytest
from app.main import app
from app.core.dependencies import get_invoice_service
from app.invoices.service import InvoiceService

def test_auth_token(client):
    response = client.post("/auth/token", data={"username": "admin", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_invoice_unauthorized(client):
    response = client.get("/invoice/1")
    assert response.status_code == 401

def test_get_invoice_with_mock_service(client, mock_repo):
    # Override dependency to use mock repository
    def get_mock_service():
        return InvoiceService(mock_repo)
    
    app.dependency_overrides[get_invoice_service] = get_mock_service
    
    # Get token
    token_resp = client.post("/auth/token", data={"username": "admin", "password": "password123"})
    token = token_resp.json()["access_token"]
    
    response = client.get("/invoice/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["client_name"] == "Test Client"
    
    # Clean up overrides
    app.dependency_overrides.clear()
