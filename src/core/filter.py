from typing import Type, Dict, Any, Optional
from pydantic import create_model
from fastapi_filter.contrib.sqlalchemy import Filter
from sqlmodel import SQLModel

from sqlalchemy.dialects.postgresql import UUID as PGUUID
from datetime import datetime
from uuid import UUID as PyUUID


# Columnas que sólo tendrán búsqueda exacta (sin sufijos)
EXCLUDE_COLUMNS = {"id", "uuid", "created_at", "updated_at"}

# Para mapear tipos SQL→Python
PYTHON_TYPE_OVERRIDES = {
    PGUUID:   PyUUID,
}


def resolve_python_type(col) -> Type:
    try:
        return col.type.python_type
    except NotImplementedError:
        # Usa tu override si lo tienes, o str por defecto
        for sa_type, py_type in PYTHON_TYPE_OVERRIDES.items():
            if isinstance(col.type, sa_type):
                return py_type
        return str


def make_filter_for_model(model: Type[SQLModel]) -> Type[Filter]:
    annotations: Dict[str, Any] = {}
    defaults:    Dict[str, Any] = {}

    for col in model.__table__.columns:
        name = col.name
        py_type = resolve_python_type(col)

        # 1) siempre = búsqueda exacta
        annotations[name] = Optional[py_type]
        defaults[name] = None

        # 2) si no está excluido, decidimos sufijos basados en el tipo Python
        if name not in EXCLUDE_COLUMNS:
            if py_type is str:
                ops = ["ilike"]
            elif py_type in (int, float, datetime):
                ops = ["lt", "le", "gt", "ge"]
            else:
                ops = []

            for op in ops:
                key = f"{name}__{op}"
                annotations[key] = Optional[py_type]
                defaults[key] = None

    # 3) construye el Filter dinámico
    AutoFilter = create_model(
        f"{model.__name__}AutoFilter",
        __base__=Filter,
        **{k: (annotations[k], defaults[k]) for k in annotations}
    )
    AutoFilter.Constants.model = model
    return AutoFilter





# ----------------
from typing import Callable
from sqlalchemy.sql import Select

ModelSelect = Select
FilterHook = Callable[[ModelSelect], ModelSelect]

