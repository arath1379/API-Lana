from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from DB.conexion import get_db
from Services.reportes_service import (
    resumen_financiero,
    gastos_por_categoria,
    historico_mensual
)
from Services.auth_service import obtener_usuario

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("/resumen/{usuario_id}/{mes}/{año}")
def obtener_resumen(
    usuario_id: int,
    mes: int,
    año: int,
    db: Session = Depends(get_db)
):
    usuario = obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return resumen_financiero(db, usuario_id, mes, año)

@router.get("/categorias/{usuario_id}/{mes}/{año}")
def obtener_gastos_categoria(
    usuario_id: int,
    mes: int,
    año: int,
    db: Session = Depends(get_db)
):
    usuario = obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return gastos_por_categoria(db, usuario_id, mes, año)

@router.get("/historico/{usuario_id}/{año}")
def obtener_historico(
    usuario_id: int,
    año: int,
    db: Session = Depends(get_db)
):
    usuario = obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return historico_mensual(db, usuario_id, año)