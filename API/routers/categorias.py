from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from DB.conexion import get_db
from modelsPyDantic import CategoriaBase
from Services.categorias_service import (
    crear_categoria,
    obtener_categorias,
    obtener_categoria
)

router = APIRouter(prefix="/categorias", tags=["categorias"])

@router.post("/", response_model=CategoriaBase)
def crear_categoria_endpoint(categoria: CategoriaBase, db: Session = Depends(get_db)):
    return crear_categoria(db, categoria)

@router.get("/", response_model=list[CategoriaBase])
def listar_categorias(tipo: str = None, db: Session = Depends(get_db)):
    return obtener_categorias(db, tipo)

@router.get("/{categoria_id}", response_model=CategoriaBase)
def obtener_categoria_endpoint(categoria_id: int, db: Session = Depends(get_db)):
    categoria = obtener_categoria(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria