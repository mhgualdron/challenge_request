from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.engine import Connection
from app.core.database import get_connection
from app.core import security
from app.core.exceptions import AuthenticationError
from app.invoices.repository_impl import InvoiceRepositoryImpl
from app.invoices.service import InvoiceService

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_db():
    """Dependency to get a DB connection."""
    yield from get_connection()

def get_current_user(token: str = Depends(reusable_oauth2)):
    payload = security.decode_access_token(token)
    if not payload:
        raise AuthenticationError("Could not validate credentials")
    return payload.get("sub")

def get_invoice_service(conn: Connection = Depends(get_db)):
    """Point of wiring: Inject the concrete repository implementation."""
    repo = InvoiceRepositoryImpl(conn)
    return InvoiceService(repo)
