from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from DB.conexion import get_db
from modelsPyDantic import Presupuesto, PresupuestoCreate
from Services.presupuestos_service import (
    crear_presupuesto,
    obtener_presupuestos,
    obtener_presupuesto,
    actualizar_presupuesto,
    eliminar_presupuesto,
    verificar_alertas
)
from Services.auth_service import obtener_usuario

router = APIRouter(prefix="/presupuestos", tags=["Presupuestos"])

@router.post("/", response_model=Presupuesto)
def crear_presupuesto_endpoint(
    presupuesto: PresupuestoCreate,
    usuario_id: int,
    db: Session = Depends(get_db)
):
    usuario = obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return crear_presupuesto(db, presupuesto, usuario_id)

@router.get("/", response_model=list[Presupuesto])
def listar_presupuestos(usuario_id: int, db: Session = Depends(get_db)):
    return obtener_presupuestos(db, usuario_id)

@router.get("/{presupuesto_id}", response_model=Presupuesto)
def obtener_presupuesto_endpoint(presupuesto_id: int, db: Session = Depends(get_db)):
    presupuesto = obtener_presupuesto(db, presupuesto_id)
    if not presupuesto:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    return presupuesto

@router.put("/{presupuesto_id}", response_model=Presupuesto)
def actualizar_presupuesto_endpoint(
    presupuesto_id: int,
    presupuesto: PresupuestoCreate,
    db: Session = Depends(get_db)
):
    db_presupuesto = actualizar_presupuesto(db, presupuesto_id, presupuesto)
    if not db_presupuesto:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    return db_presupuesto

@router.delete("/{presupuesto_id}")
def eliminar_presupuesto_endpoint(presupuesto_id: int, db: Session = Depends(get_db)):
    if not eliminar_presupuesto(db, presupuesto_id):
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    return {"mensaje": "Presupuesto eliminado"}

@router.get("/alertas/")
def obtener_alertas(usuario_id: int, db: Session = Depends(get_db)):
    return verificar_alertas(db, usuario_id)