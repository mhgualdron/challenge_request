from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.invoices.router import router as invoice_router
from app.auth.router import router as auth_router
from app.core.exceptions import DomainException, domain_exception_handler, global_exception_handler

def create_app() -> FastAPI:
    app = FastAPI(
        title="Invoice Management API",
        description="""
        ### Guía de Inicio Rápido
        Para probar los endpoints protegidos:
        1. Diríjase al endpoint **POST /auth/token** abajo y ejecútelo con `admin` / `password123`.
        2. Copie el valor de **access_token**.
        3. Haga clic en el botón **Authorize** arriba y pegue el token en el campo **Value**.
        """,
        version="1.0.0"
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register Domain Exception Handlers
    app.add_exception_handler(DomainException, domain_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)

    # Register Routers
    app.include_router(auth_router)
    app.include_router(invoice_router)

    return app

app = create_app()
