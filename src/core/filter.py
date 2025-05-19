from typing import Optional, Type, Dict, Any
from pydantic import create_model
from fastapi_filter.contrib.sqlalchemy import Filter
from sqlmodel import SQLModel
from sqlalchemy import String, Integer, Float, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from datetime import datetime
from uuid import UUID as PyUUID


def resolve_python_type(col) -> Type:
    try:
        return col.type.python_type
    except NotImplementedError:
        impl = col.type.__class__
        if issubclass(impl, (String,)):
            return str
        if issubclass(impl, (Integer,)):
            return int
        if issubclass(impl, (Float,)):
            return float
        if issubclass(impl, (Boolean,)):
            return bool
        if issubclass(impl, (DateTime,)):
            return datetime
        if issubclass(impl, (PGUUID,)):
            return PyUUID
        return str


def make_filter_for_model(model: Type[SQLModel]) -> Type[Filter]:
    # Solo ilike + eq por defecto (sin sufijo)
    ops = ["ilike"]

    annotations: Dict[str, Any] = {}
    defaults:    Dict[str, Any] = {}

    for col in model.__table__.columns:
        py_type = resolve_python_type(col)

        # 1) Campo sin sufijo → eq por defecto
        annotations[col.name] = Optional[py_type]
        defaults[col.name] = None

        # 2) Campos con sufijo para otros operadores
        for op in ops:
            key = f"{col.name}__{op}"
            annotations[key] = Optional[py_type]
            defaults[key] = None

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
