from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from src.core.database import get_session

router = APIRouter()


@router.get("/health", summary="Health Check")
async def health_check(session=Depends(get_session)):
    try:
        await session.execute(select(1))
        return {"status": "ok", "db": "connected"}
    except Exception:
        raise HTTPException(status_code=503, detail="DB connection failed")
