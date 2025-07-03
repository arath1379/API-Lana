from sqlalchemy.orm import Session
from models.modelsDB import Presupuesto
from modelsPyDantic import PresupuestoCreate

def crear_presupuesto(db: Session, presupuesto: PresupuestoCreate, usuario_id: int):
    db_presupuesto = Presupuesto(**presupuesto.dict(), usuario_id=usuario_id)
    db.add(db_presupuesto)
    db.commit()
    db.refresh(db_presupuesto)
    return db_presupuesto

def obtener_presupuestos(db: Session, usuario_id: int):
    return db.query(Presupuesto).filter(Presupuesto.usuario_id == usuario_id).all()

def obtener_presupuesto(db: Session, presupuesto_id: int):
    return db.query(Presupuesto).filter(Presupuesto.id == presupuesto_id).first()

def actualizar_presupuesto(db: Session, presupuesto_id: int, presupuesto: PresupuestoCreate):
    db_presupuesto = obtener_presupuesto(db, presupuesto_id)
    if not db_presupuesto:
        return None
    
    for key, value in presupuesto.dict().items():
        setattr(db_presupuesto, key, value)
    
    db.commit()
    db.refresh(db_presupuesto)
    return db_presupuesto

def eliminar_presupuesto(db: Session, presupuesto_id: int):
    db_presupuesto = obtener_presupuesto(db, presupuesto_id)
    if not db_presupuesto:
        return False
    
    db.delete(db_presupuesto)
    db.commit()
    return True

def verificar_alertas(db: Session, usuario_id: int):
    # Implementar lógica de alertas de presupuesto
    return []