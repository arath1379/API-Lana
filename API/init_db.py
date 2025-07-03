from DB.conexion import engine, Base
from models.modelsDB import Categoria
from sqlalchemy.orm import sessionmaker

def init_db():
    Base.metadata.create_all(bind=engine)
    
    Session = sessionmaker(bind=engine)
    db = Session()
    
    # Categorías básicas
    categorias = [
        {"nombre": "Alimentos", "tipo": "egreso"},
        {"nombre": "Transporte", "tipo": "egreso"},
        {"nombre": "Vivienda", "tipo": "egreso"},
        {"nombre": "Entretenimiento", "tipo": "egreso"},
        {"nombre": "Salud", "tipo": "egreso"},
        {"nombre": "Educación", "tipo": "egreso"},
        {"nombre": "Salario", "tipo": "ingreso"},
        {"nombre": "Bonos", "tipo": "ingreso"},
        {"nombre": "Inversiones", "tipo": "ingreso"},
        {"nombre": "Otros ingresos", "tipo": "ingreso"}
    ]
    
    try:
        for cat in categorias:
            if not db.query(Categoria).filter_by(nombre=cat["nombre"]).first():
                db.add(Categoria(**cat))
        db.commit()
        print("✅ Base de datos inicializada con categorías básicas")
    except Exception as e:
        db.rollback()
        print(f"❌ Error al inicializar DB: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()