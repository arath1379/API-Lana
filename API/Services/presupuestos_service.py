from sqlalchemy.orm import Session
from models.modelsDB import Presupuesto
from modelsPyDantic import PresupuestoCreate
from models.modelsDB import Presupuesto, Categoria, Transaccion

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
    """
    Verifica alertas de presupuestos basado en el gasto real vs presupuesto
    """
    try:
        # Obtener presupuestos del usuario con información de categoría
        presupuestos = db.query(
            Presupuesto,
            Categoria.nombre.label('categoria_nombre')
        ).join(
            Categoria, Presupuesto.categoria_id == Categoria.id
        ).filter(
            Presupuesto.usuario_id == usuario_id
        ).all()
        
        alertas = []
        
        for presupuesto_row in presupuestos:
            presupuesto = presupuesto_row[0]  # El objeto Presupuesto
            categoria_nombre = presupuesto_row[1]  # El nombre de la categoría
            
            # Calcular gasto real sumando transacciones de la misma categoría y período
            gasto_real = db.query(func.sum(Transaccion.monto)).filter(
                and_(
                    Transaccion.usuario_id == usuario_id,
                    Transaccion.categoria_id == presupuesto.categoria_id,
                    func.extract('month', Transaccion.fecha) == presupuesto.mes,
                    func.extract('year', Transaccion.fecha) == presupuesto.año,
                    Transaccion.tipo == 'gasto'  # Solo contar gastos, no ingresos
                )
            ).scalar() or 0.0
            
            # Calcular valores
            monto_limite = float(presupuesto.monto)
            monto_gastado = float(gasto_real)
            monto_disponible = monto_limite - monto_gastado
            porcentaje_usado = (monto_gastado / monto_limite * 100) if monto_limite > 0 else 0
            
            # Crear alerta si se ha usado más del 80% o se ha excedido
            if porcentaje_usado >= 80:
                tipo_alerta = "excedido" if monto_disponible < 0 else "advertencia"
                
                alertas.append({
                    "presupuesto_id": presupuesto.id,
                    "categoria": categoria_nombre,
                    "monto_limite": monto_limite,
                    "monto_gastado": monto_gastado,
                    "monto_disponible": monto_disponible,
                    "porcentaje_usado": round(porcentaje_usado, 2),
                    "tipo": tipo_alerta,
                    "mensaje": f"{'¡Presupuesto excedido!' if tipo_alerta == 'excedido' else '⚠️ Cerca del límite'} Has usado el {round(porcentaje_usado, 1)}% de tu presupuesto de {categoria_nombre}",
                    "mes": presupuesto.mes,
                    "año": presupuesto.año
                })
        
        return alertas
        
    except Exception as e:
        print(f"Error en verificar_alertas: {e}")
        return []

def obtener_presupuestos_con_gastos(db: Session, usuario_id: int):
    """
    Obtiene los presupuestos del usuario con el cálculo de gastos reales
    """
    try:
        # Obtener presupuestos con información de categoría
        presupuestos = db.query(
            Presupuesto,
            Categoria.nombre.label('categoria_nombre')
        ).join(
            Categoria, Presupuesto.categoria_id == Categoria.id
        ).filter(
            Presupuesto.usuario_id == usuario_id
        ).all()
        
        resultado = []
        
        for presupuesto_row in presupuestos:
            presupuesto = presupuesto_row[0]
            categoria_nombre = presupuesto_row[1]
            
            # Calcular gasto real
            gasto_real = db.query(func.sum(Transaccion.monto)).filter(
                and_(
                    Transaccion.usuario_id == usuario_id,
                    Transaccion.categoria_id == presupuesto.categoria_id,
                    func.extract('month', Transaccion.fecha) == presupuesto.mes,
                    func.extract('year', Transaccion.fecha) == presupuesto.año,
                    Transaccion.tipo == 'gasto'
                )
            ).scalar() or 0.0
            
            # Crear objeto resultado
            presupuesto_data = {
                "id": presupuesto.id,
                "monto": float(presupuesto.monto),
                "monto_usado": float(gasto_real),  # Este campo lo necesita el frontend
                "gastado": float(gasto_real),      # Campo alternativo
                "mes": presupuesto.mes,
                "año": presupuesto.año,
                "usuario_id": presupuesto.usuario_id,
                "categoria_id": presupuesto.categoria_id,
                "categoria_nombre": categoria_nombre
            }
            
            resultado.append(presupuesto_data)
        
        return resultado
        
    except Exception as e:
        print(f"Error en obtener_presupuestos_con_gastos: {e}")
        return []
