from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Dict, List
from models.modelsDB import Transaccion, Categoria

def resumen_financiero(db: Session, usuario_id: int) -> Dict:
    # Consulta para los últimos 30 días
    fecha_inicio = datetime.now() - timedelta(days=30)
    
    datos = db.query(
        func.sum(Transaccion.monto).filter(Transaccion.tipo == "ingreso"),
        func.sum(Transaccion.monto).filter(Transaccion.tipo == "egreso")
    ).filter(
        Transaccion.usuario_id == usuario_id,
        Transaccion.fecha >= fecha_inicio
    ).first()

    return {
        "saldo": float((datos[0] or 0) - (datos[1] or 0)),
        "ingresos": float(datos[0] or 0),
        "egresos": float(datos[1] or 0),
        "periodo": "Últimos 30 días"
    }

def gastos_por_categoria(db: Session, usuario_id: int) -> List[Dict]:
    # Consulta para el mes actual
    hoy = datetime.now()
    fecha_inicio = hoy.replace(day=1)  # Primer día del mes
    
    gastos = db.query(
        Categoria.nombre,
        func.sum(Transaccion.monto).label("total")
    ).join(Transaccion).filter(
        Transaccion.usuario_id == usuario_id,
        Transaccion.tipo == "egreso",
        Transaccion.fecha >= fecha_inicio,
        Transaccion.fecha <= hoy
    ).group_by(Categoria.nombre).all()
    
    return [{"categoria": g[0], "total": float(g[1])} for g in gastos]