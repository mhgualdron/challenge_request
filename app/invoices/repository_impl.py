from sqlalchemy import text, Connection
from typing import List, Optional
from app.invoices.repository import InvoiceRepositoryBase

class InvoiceRepositoryImpl(InvoiceRepositoryBase):
    def __init__(self, connection: Connection):
        self.connection = connection

    def create(self, invoice_data: dict) -> dict:
        """Call sp_CreateInvoice and return the created record."""
        query = text("""
            EXEC sp_CreateInvoice 
                @InvoiceNumber = :invoice_number,
                @ClientName = :client_name,
                @ClientID = :client_id,
                @TotalAmount = :total_amount,
                @Currency = :currency,
                @IssueDate = :issue_date,
                @DueDate = :due_date,
                @Status = :status,
                @Description = :description
        """)
        
        # We use .mappings() to get a dictionary-like object from the cursor
        result = self.connection.execute(query, invoice_data).mappings().first()
        
        # Optional: commit here if not handled by a global transaction manager
        self.connection.commit()
        
        return dict(result) if result else {}

    def get_by_id(self, invoice_id: int) -> Optional[dict]:
        """Call sp_GetInvoiceById."""
        query = text("EXEC sp_GetInvoiceById @ID = :id")
        result = self.connection.execute(query, {"id": invoice_id}).mappings().first()
        return dict(result) if result else None

    def search_by_client(self, client_name: str) -> List[dict]:
        """Call sp_SearchInvoicesByClient."""
        query = text("EXEC sp_SearchInvoicesByClient @ClientName = :client_name")
        result = self.connection.execute(query, {"client_name": client_name}).mappings().all()
        return [dict(row) for row in result]
