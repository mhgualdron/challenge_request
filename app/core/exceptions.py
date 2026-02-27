from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Any, Dict

class DomainException(Exception):
    """Base category for domain-related errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class InvoiceNotFoundError(DomainException):
    def __init__(self, invoice_id: Any):
        super().__init__(f"Invoice with ID {invoice_id} not found")

class InvalidInvoiceDataError(DomainException):
    def __init__(self, message: str):
        super().__init__(message)

class AuthenticationError(DomainException):
    def __init__(self, message: str = "Could not validate credentials"):
        super().__init__(message)

async def domain_exception_handler(request: Request, exc: DomainException):
    status_code = status.HTTP_400_BAD_REQUEST
    
    if isinstance(exc, InvoiceNotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, AuthenticationError):
        status_code = status.HTTP_401_UNAUTHORIZED
        
    return JSONResponse(
        status_code=status_code,
        content={"detail": exc.message},
    )

async def global_exception_handler(request: Request, exc: Exception):
    # Log the exception here in a real scenario
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred."},
    )
