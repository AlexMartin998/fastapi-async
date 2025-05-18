from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.core.database import init_db


from src.core.routes import router as health_router
from src.inventory_settings.routers.category_router import (
    router as inventory_settings_router,
)
from src.core.error import register_all_errors
from src.core.middleware import register_middleware


# constants -------------
version = "v1"
version_prefix = f"/api/{version}"
description = """
A REST API for a awesome application.

This REST API can:
- Create, Read, Update, Delete entities
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


# init app -------------
app = FastAPI(
    title="My API",
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
    docs_url=f"{version_prefix}/swagger",
    redoc_url=f"{version_prefix}/redoc",
    # Aquí pasamos el context manager en lugar de on_event :contentReference[oaicite:7]{index=7}
    lifespan=lifespan
)


# handlers and middleware -------------
register_all_errors(app)
register_middleware(app)


# routers --------------------------------
app.include_router(health_router, prefix=version_prefix)
app.include_router(
    inventory_settings_router,
    prefix=version_prefix,  # /api/v1
)
