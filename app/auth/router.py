from fastapi import APIRouter, Form
from app.auth.schemas import TokenResponse
from app.core import security
from app.core.exceptions import AuthenticationError

router = APIRouter(prefix="/auth", tags=["auth"])

# Mock user for the challenge
MOCK_USER = {"username": "admin", "password": "password123"}

@router.post("/token", 
             response_model=TokenResponse,
             summary="Autenticación (Obtener Token)",
             description="""
             1. Ingrese `admin` / `password123`.
             2. Copie el valor de **access_token** de la respuesta.
             3. Haga clic en el botón verde **Authorize** arriba y pegue el token en el campo **Value**.
             """)
def login_for_access_token(
    username: str = Form(..., description="Usuario administrador", example="admin"),
    password: str = Form(..., description="Contraseña de acceso", example="password123")
):
    if username != MOCK_USER["username"] or password != MOCK_USER["password"]:
        raise AuthenticationError("Invalid username or password")
    
    access_token = security.create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}
