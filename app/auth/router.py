from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.schemas import TokenResponse
from app.core import security
from app.core.exceptions import AuthenticationError

router = APIRouter(prefix="/auth", tags=["auth"])

# Mock user for the challenge
MOCK_USER = {"username": "admin", "password": "password123"}

@router.post("/token", response_model=TokenResponse)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != MOCK_USER["username"] or form_data.password != MOCK_USER["password"]:
        raise AuthenticationError("Invalid username or password")
    
    access_token = security.create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}
