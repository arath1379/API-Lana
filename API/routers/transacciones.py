from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from DB.conexion import get_db
from modelsPyDantic import Transaccion, TransaccionCreate
from Services.transacciones_service import (
    crear_transaccion,
    obtener_transacciones,
    obtener_transaccion,
    actualizar_transaccion,
    eliminar_transaccion
)
from Services.auth_service import obtener_usuario

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

@router.post("/", response_model=Transaccion)
def crear_transaccion_endpoint(
    transaccion: TransaccionCreate,
    usuario_id: int,
    db: Session = Depends(get_db)
):
    usuario = obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return crear_transaccion(db, transaccion, usuario_id)

@router.get("/", response_model=list[Transaccion])
def listar_transacciones(usuario_id: int, db: Session = Depends(get_db)):
    return obtener_transacciones(db, usuario_id)

@router.put("/{transaccion_id}", response_model=Transaccion)
def actualizar_transaccion_endpoint(
    transaccion_id: int,
    transaccion: TransaccionCreate,
    db: Session = Depends(get_db)
):
    db_transaccion = actualizar_transaccion(db, transaccion_id, transaccion)
    if not db_transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return db_transaccion

@router.delete("/{transaccion_id}")
def eliminar_transaccion_endpoint(transaccion_id: int, db: Session = Depends(get_db)):
    if not eliminar_transaccion(db, transaccion_id):
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return {"mensaje": "Transacción eliminada"}