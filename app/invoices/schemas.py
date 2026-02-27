from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import date, datetime
from typing import Optional, List
from decimal import Decimal

class InvoiceBase(BaseModel):
    invoice_number: str = Field(..., min_length=1, max_length=50)
    client_name: str = Field(..., min_length=1, max_length=150)
    client_id: str = Field(..., min_length=1, max_length=50)
    total_amount: Decimal = Field(..., gt=0)
    currency: str = Field(default="COP", min_length=3, max_length=3)
    issue_date: date
    due_date: Optional[date] = None
    status: str = Field(default="PENDING", pattern="^(PENDING|PAID|CANCELLED)$")
    description: Optional[str] = None

    @field_validator('total_amount')
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError('Total amount must be greater than zero')
        return v

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceResponse(InvoiceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class InvoiceListResponse(BaseModel):
    items: List[InvoiceResponse]
    total: int
