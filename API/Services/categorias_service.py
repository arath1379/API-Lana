from sqlalchemy.orm import Session
from models.modelsDB import Categoria
from modelsPyDantic import CategoriaBase

def crear_categoria(db: Session, categoria: CategoriaBase):
    db_categoria = Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def obtener_categorias(db: Session, tipo: str = None):
    query = db.query(Categoria)
    if tipo:
        query = query.filter(Categoria.tipo == tipo)
    return query.all()

def obtener_categoria(db: Session, categoria_id: int):
    return db.query(Categoria).filter(Categoria.id == categoria_id).first()