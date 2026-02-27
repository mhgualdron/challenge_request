from abc import ABC, abstractmethod
from typing import List, Optional, Any

class InvoiceRepositoryBase(ABC):
    @abstractmethod
    def create(self, invoice_data: dict) -> dict:
        """Create a new invoice using sp_CreateInvoice."""
        pass

    @abstractmethod
    def get_by_id(self, invoice_id: int) -> Optional[dict]:
        """Get an invoice by ID using sp_GetInvoiceById."""
        pass

    @abstractmethod
    def search_by_client(self, client_name: str) -> List[dict]:
        """Search invoices by client name using sp_SearchInvoicesByClient."""
        pass
