from __future__ import annotations
import re
from typing import Any, Dict, List, Optional, Tuple
from src.core.settings import settings

# Regex reutilizables
_RE_KEY_PAIR = re.compile(
    r"Key \((?P<cols>.+?)\)=\((?P<vals>.+?)\)", re.IGNORECASE)
_RE_NOT_NULL = re.compile(
    r'null value in column\s+"(?P<column>[^"]+)"\s+violates not-null constraint', re.IGNORECASE)
_RE_FK = re.compile(
    r'foreign key constraint\s+"(?P<constraint>[^"]+)"', re.IGNORECASE)
_RE_STR_TRUNC = re.compile(
    r"value too long for type\s+(?P<dtype>.+)", re.IGNORECASE)
_RE_CHECK = re.compile(
    r'check constraint\s+"(?P<constraint>[^"]+)"', re.IGNORECASE)


def _split_csv(s: str) -> List[str]:
    return [x.strip() for x in s.split(",") if x.strip()]


def _pairs_from_text(text: str) -> List[Tuple[str, str]]:
    """
    Intenta extraer pares (col, val) desde el texto (DETAIL o str(e.orig)).
    """
    m = _RE_KEY_PAIR.search(text or "")
    if not m:
        return []
    cols = _split_csv(m.group("cols"))
    vals = _split_csv(m.group("vals"))
    # Empareja por posición, ignora sobrantes
    limit = min(len(cols), len(vals))
    return list(zip(cols[:limit], vals[:limit]))


def _build_message(error: str, pairs: List[Tuple[str, str]], fallback_field: Optional[str] = None) -> str:
    """
    Mensajes human-friendly, concisos y sin términos “de motor DB”.
    """
    if error == "unique_violation":
        if pairs:
            # Ej: "Ya existe un registro con (code='string2')."
            inside = ", ".join([f"{c}='{v}'" for c, v in pairs])
            return f"Ya existe un registro con ({inside})."
        # fallback por si no hay pairs
        field = fallback_field or "valores únicos"
        return f"Ya existe un registro con {field} duplicado."

    if error == "not_null_violation":
        field = fallback_field or "un campo requerido"
        return f"El campo {field} es obligatorio."

    if error == "foreign_key_violation":
        return "No se puede completar la operación por una relación no válida."

    if error == "check_violation":
        return "Los datos no cumplen una validación requerida."

    if error == "string_too_long":
        # No forzamos campo; el front no necesita el tipo exacto
        return "El valor excede la longitud permitida."

    return "Ocurrió un error al procesar la solicitud."


def format_db_error(exc: Exception) -> Dict[str, Any]:
    """
    Devuelve un payload **mínimo** para el front:
      - message: texto listo para mostrar
      - error: (opcional) código lógico: unique_violation, etc.

    Si settings.DEBUG=True añade 'debug' con sqlstate, detail, etc.
    """
    orig = getattr(exc, "orig", None)
    sqlstate = getattr(orig, "sqlstate", None)
    detail = getattr(orig, "detail", "") or ""
    full_text = str(orig) if orig is not None else str(exc)
    parse_text = detail or full_text

    # Clasifica por SQLSTATE
    error_code = "db_error"
    field_hint: Optional[str] = None
    pairs: List[Tuple[str, str]] = []

    if sqlstate == "23505":
        error_code = "unique_violation"
        pairs = _pairs_from_text(parse_text)

    elif sqlstate == "23502":
        error_code = "not_null_violation"
        m = _RE_NOT_NULL.search(parse_text)
        field_hint = m.group("column") if m else None

    elif sqlstate == "23503":
        error_code = "foreign_key_violation"

    elif sqlstate == "23514":
        error_code = "check_violation"

    elif sqlstate == "22001":
        error_code = "string_too_long"

    message = _build_message(error_code, pairs, fallback_field=field_hint)

    payload: Dict[str, Any] = {
        "message": message,
        "error": error_code,
    }

    if settings.DEBUG:
        payload["debug"] = {
            "sqlstate": sqlstate,
            "detail": detail or full_text,
        }
        if pairs:
            payload["debug"]["pairs"] = [
                {"field": c, "value": v} for c, v in pairs]
        if field_hint:
            payload["debug"]["field"] = field_hint

    return payload
