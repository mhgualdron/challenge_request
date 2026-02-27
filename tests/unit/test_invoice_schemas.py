import pytest
from pydantic import ValidationError
from app.invoices.schemas import InvoiceCreate

def test_invoice_schema_valid():
    data = {
        "invoice_number": "INV-001",
        "client_name": "Client",
        "client_id": "C-001",
        "total_amount": 100.50,
        "issue_date": "2023-01-01"
    }
    invoice = InvoiceCreate(**data)
    assert invoice.total_amount == 100.50

def test_invoice_schema_invalid_amount():
    data = {
        "invoice_number": "INV-001",
        "client_name": "Client",
        "client_id": "C-001",
        "total_amount": -10.0,
        "issue_date": "2023-01-01"
    }
    with pytest.raises(ValidationError):
        InvoiceCreate(**data)

def test_invoice_schema_invalid_status():
    data = {
        "invoice_number": "INV-001",
        "client_name": "Client",
        "client_id": "C-001",
        "total_amount": 100.0,
        "issue_date": "2023-01-01",
        "status": "INVALID_STATUS"
    }
    with pytest.raises(ValidationError):
        InvoiceCreate(**data)
