from fastapi import APIRouter, Depends, status, Query, Path
from typing import List
from app.invoices.schemas import InvoiceCreate, InvoiceResponse
from app.invoices.service import InvoiceService
from app.core.dependencies import get_invoice_service, get_current_user

router = APIRouter(prefix="/invoice", tags=["invoices"])

@router.post("/", 
             response_model=InvoiceResponse, 
             status_code=status.HTTP_201_CREATED,
             summary="Registrar Factura",
             description="Crea un nuevo registro de factura en la base de datos utilizando procedimientos almacenados.")
def create_invoice(
    invoice_in: InvoiceCreate,
    service: InvoiceService = Depends(get_invoice_service),
    current_user: str = Depends(get_current_user)
):
    return service.create_invoice(invoice_in)

@router.get("/search", 
            response_model=List[InvoiceResponse],
            summary="Buscar por Cliente",
            description="Retorna una lista de facturas cuyo nombre de cliente coincide parcialmente con el termino de búsqueda.")
def search_invoices_by_client(
    client: str = Query(..., description="Nombre o parte del nombre del cliente", example="Acme"),
    service: InvoiceService = Depends(get_invoice_service),
    current_user: str = Depends(get_current_user)
):
    return service.search_invoices(client)

@router.get("/{id}", 
            response_model=InvoiceResponse,
            summary="Consultar por ID",
            description="Obtiene el detalle completo de una factura especifica mediante su identificador numérico.")
def get_invoice_by_id(
    id: int = Path(..., description="ID unico de la factura", example=1),
    service: InvoiceService = Depends(get_invoice_service),
    current_user: str = Depends(get_current_user)
):
    return service.get_invoice(id)
