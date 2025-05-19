from typing import Type, Dict, Any, Optional
from pydantic import create_model
from fastapi_filter.contrib.sqlalchemy import Filter
from sqlmodel import SQLModel
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from datetime import datetime
from uuid import UUID as PyUUID

# 1) Campos que NUNCA tendrán sufijos de texto __ilike
TEXT_EXCLUDE = {"id", "uuid"}

# 2) Campos que tendrán siempre rangos (datetime)
DATE_RANGE = {"created_at", "updated_at"}

# 3) Campos numéricos a los que NO queremos rangos (aunque sean int/float)
RANGE_EXCLUDE = {"id", "uuid"}

# Para mapear tipos SQL→Python
PYTHON_TYPE_OVERRIDES = {
    PGUUID: PyUUID,
}


def resolve_python_type(col) -> Type:
    try:
        return col.type.python_type
    except NotImplementedError:
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

        # — 1) igualdad exacta SIEMPRE
        annotations[name] = Optional[py_type]
        defaults[name] = None

        # — 2) __ilike para textos no excluidos
        if py_type is str and name not in TEXT_EXCLUDE:
            annotations[f"{name}__ilike"] = Optional[str]
            defaults[f"{name}__ilike"] = None

        # — 3) rangos para datetimes siempre, y para números si no están en RANGE_EXCLUDE
        want_range = False
        if name in DATE_RANGE and py_type is datetime:
            want_range = True
        elif py_type in (int, float) and name not in RANGE_EXCLUDE:
            want_range = True

        if want_range:
            # for op in ("lt", "lte", "gt", "gte"):
            for op in ("lte", "gte"):
                annotations[f"{name}__{op}"] = Optional[py_type]
                defaults[f"{name}__{op}"] = None

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