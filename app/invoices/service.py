from typing import List, Optional
from app.invoices.repository import InvoiceRepositoryBase
from app.invoices.schemas import InvoiceCreate, InvoiceResponse
from app.core.exceptions import InvoiceNotFoundError

class InvoiceService:
    def __init__(self, repository: InvoiceRepositoryBase):
        self.repository = repository

    def create_invoice(self, invoice_in: InvoiceCreate) -> InvoiceResponse:
        """Logic for creating an invoice."""
        # Convert Pydantic model to dict for the repository
        data = invoice_in.model_dump()
        result = self.repository.create(data)
        return InvoiceResponse.model_validate(result)

    def get_invoice(self, invoice_id: int) -> InvoiceResponse:
        """Retrieve an invoice or raise not found."""
        result = self.repository.get_by_id(invoice_id)
        if not result:
            raise InvoiceNotFoundError(invoice_id)
        return InvoiceResponse.model_validate(result)

    def search_invoices(self, client_name: str) -> List[InvoiceResponse]:
        """Search invoices by client name."""
        results = self.repository.search_by_client(client_name)
        return [InvoiceResponse.model_validate(row) for row in results]
