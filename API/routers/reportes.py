from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Services.reportes_service import *
from DB.conexion import get_db

router = APIRouter(tags=["Reportes"])

@router.get("/resumen-financiero/{usuario_id}")
async def get_resumen(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    try:
        data = resumen_financiero(db, usuario_id)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/gastos-categoria/{usuario_id}")
async def get_gastos_categoria(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    try:
        data = gastos_por_categoria(db, usuario_id)
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))