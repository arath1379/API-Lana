from sqlalchemy.orm import Session
from models.modelsDB import PagoProgramado
from modelsPyDantic import PagoProgramadoCreate

def crear_pago(db: Session, pago: PagoProgramadoCreate, usuario_id: int):
    db_pago = PagoProgramado(**pago.dict(), usuario_id=usuario_id)
    db.add(db_pago)
    db.commit()
    db.refresh(db_pago)
    return db_pago

def obtener_pagos(db: Session, usuario_id: int):
    return db.query(PagoProgramado).filter(PagoProgramado.usuario_id == usuario_id).all()

def obtener_pago(db: Session, pago_id: int):
    return db.query(PagoProgramado).filter(PagoProgramado.id == pago_id).first()

def actualizar_pago(db: Session, pago_id: int, pago: PagoProgramadoCreate):
    db_pago = obtener_pago(db, pago_id)
    if not db_pago:
        return None
    
    for key, value in pago.dict().items():
        setattr(db_pago, key, value)
    
    db.commit()
    db.refresh(db_pago)
    return db_pago

def eliminar_pago(db: Session, pago_id: int):
    db_pago = obtener_pago(db, pago_id)
    if not db_pago:
        return False
    
    db.delete(db_pago)
    db.commit()
    return True

def verificar_saldo(db: Session, usuario_id: int):
    # Implementar lógica de verificación de saldo
    return {"disponible": True}