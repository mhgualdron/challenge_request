import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.dependencies import get_invoice_service
from app.invoices.repository import InvoiceRepositoryBase
from typing import List, Optional

class MockInvoiceRepository(InvoiceRepositoryBase):
    def __init__(self):
        self.invoices = [
            {
                "id": 1,
                "invoice_number": "INV-001",
                "client_name": "Test Client",
                "client_id": "C-001",
                "total_amount": 100.0,
                "currency": "COP",
                "issue_date": "2023-01-01",
                "status": "PAID",
                "created_at": "2023-01-01T00:00:00"
            }
        ]

    def create(self, invoice_data: dict) -> dict:
        new_id = len(self.invoices) + 1
        invoice_data["id"] = new_id
        invoice_data["created_at"] = "2023-01-01T10:00:00"
        self.invoices.append(invoice_data)
        return invoice_data

    def get_by_id(self, invoice_id: int) -> Optional[dict]:
        return next((inv for inv in self.invoices if inv["id"] == invoice_id), None)

    def search_by_client(self, client_name: str) -> List[dict]:
        return [inv for inv in self.invoices if client_name.lower() in inv["client_name"].lower()]

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_repo():
    return MockInvoiceRepository()
