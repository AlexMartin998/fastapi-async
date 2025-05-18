from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.core.config import settings
from src.core.database import init_db
from src.core.routes import router as health_router


version = "v1"
version_prefix = f"/api/{version}"
description = """
A REST API for a book review web service.

This REST API can:
- Create, Read, Update, Delete books
- Add reviews to books
- Add tags to books
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- Startup logic ----
    # 1. Inicializar base de datos
    # asegura crear tablas en DEV o conectar pool en PROD :contentReference[oaicite:5]{index=5}
    await init_db()
    # 2. Registrar manejadores de errores
    # register_all_errors(app)
    # 3. Registrar middleware
    # register_middleware(app)
    yield
    # ---- Shutdown logic ----
    # Aquí podrías cerrar conexiones o pools si fuera necesario :contentReference[oaicite:6]{index=6}


# Instancia de FastAPI con Lifespan
app = FastAPI(
    title="Bookly",
    description=description,
    version=version,
    license_info={"name": "MIT License",
                  "url": "https://opensource.org/license/mit"},
    contact={
        "name": "Ssali Jonathan",
        "url": "https://github.com/jod35",
        "email": "ssalijonathank@gmail.com",
    },
    terms_of_service="https://example.com/tos",
    openapi_url=f"{version_prefix}/openapi.json",
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc",
    # Aquí pasamos el context manager en lugar de on_event :contentReference[oaicite:7]{index=7}
    lifespan=lifespan
)

# Incluimos routers tras el lifespan
app.include_router(health_router, prefix=version_prefix)
