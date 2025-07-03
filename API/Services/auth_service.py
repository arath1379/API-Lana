from DB.conexion import get_db
from sqlalchemy.orm import Session
from models.modelsDB import Usuario
from modelsPyDantic import UsuarioCreate

def crear_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = db.query(Usuario).filter(Usuario.correo == usuario.correo).first()
    if db_usuario:
        return None
    
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        contraseña=usuario.contraseña
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def autenticar_usuario(db: Session, correo: str, contraseña: str):
    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if not usuario or usuario.contraseña != contraseña:
        return None
    return usuario

def obtener_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()
