import pytest
from app.invoices.service import InvoiceService
from app.invoices.schemas import InvoiceCreate
from app.core.exceptions import InvoiceNotFoundError

def test_create_invoice(mock_repo):
    service = InvoiceService(mock_repo)
    invoice_data = InvoiceCreate(
        invoice_number="INV-NEW",
        client_name="New Client",
        client_id="C-NEW",
        total_amount=500.0,
        issue_date="2023-01-01"
    )
    
    result = service.create_invoice(invoice_data)
    
    assert result.invoice_number == "INV-NEW"
    assert result.id is not None

def test_get_invoice_exists(mock_repo):
    service = InvoiceService(mock_repo)
    result = service.get_invoice(1)
    assert result.id == 1
    assert result.client_name == "Test Client"

def test_get_invoice_not_found(mock_repo):
    service = InvoiceService(mock_repo)
    with pytest.raises(InvoiceNotFoundError):
        service.get_invoice(999)

def test_search_invoices(mock_repo):
    service = InvoiceService(mock_repo)
    results = service.search_invoices("Test")
    assert len(results) == 1
    assert results[0].client_name == "Test Client"
