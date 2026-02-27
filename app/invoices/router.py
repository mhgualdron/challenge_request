from fastapi import APIRouter, Depends, status
from typing import List
from app.invoices.schemas import InvoiceCreate, InvoiceResponse
from app.invoices.service import InvoiceService
from app.core.dependencies import get_invoice_service

router = APIRouter(prefix="/invoice", tags=["invoices"])

@router.post("/", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_invoice(
    invoice_in: InvoiceCreate,
    service: InvoiceService = Depends(get_invoice_service)
):
    """
    Registrar una factura nueva.
    """
    return service.create_invoice(invoice_in)

@router.get("/{id}", response_model=InvoiceResponse)
def get_invoice_by_id(
    id: int,
    service: InvoiceService = Depends(get_invoice_service)
):
    """
    Obtener una factura por su ID.
    """
    return service.get_invoice(id)

@router.get("/search", response_model=List[InvoiceResponse])
def search_invoices_by_client(
    client: str,
    service: InvoiceService = Depends(get_invoice_service)
):
    """
    Buscar facturas por nombre de cliente.
    """
    return service.search_invoices(client)
