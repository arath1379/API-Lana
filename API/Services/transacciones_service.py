from DB.conexion import get_db
from sqlalchemy.orm import Session
from models.modelsDB import Transaccion
from modelsPyDantic import TransaccionCreate

def crear_transaccion(db: Session, transaccion: TransaccionCreate, usuario_id: int):
    db_transaccion = Transaccion(**transaccion.dict(), usuario_id=usuario_id)
    db.add(db_transaccion)
    db.commit()
    db.refresh(db_transaccion)
    return db_transaccion

def obtener_transacciones(db: Session, usuario_id: int):
    return db.query(Transaccion).filter(Transaccion.usuario_id == usuario_id).all()

def obtener_transaccion(db: Session, transaccion_id: int):
    return db.query(Transaccion).filter(Transaccion.id == transaccion_id).first()

def actualizar_transaccion(db: Session, transaccion_id: int, transaccion: TransaccionCreate):
    db_transaccion = obtener_transaccion(db, transaccion_id)
    if not db_transaccion:
        return None
    
    for key, value in transaccion.dict().items():
        setattr(db_transaccion, key, value)
    
    db.commit()
    db.refresh(db_transaccion)
    return db_transaccion

def eliminar_transaccion(db: Session, transaccion_id: int):
    db_transaccion = obtener_transaccion(db, transaccion_id)
    if not db_transaccion:
        return False
    
    db.delete(db_transaccion)
    db.commit()
    return True