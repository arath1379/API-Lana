from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from DB.conexion import get_db
from modelsPyDantic import Usuario, UsuarioCreate, Login
from Services.auth_service import crear_usuario, autenticar_usuario

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/registro", response_model=Usuario)
def registro(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crear_usuario(db, usuario)
    if not db_usuario:
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    return db_usuario

@router.post("/login", response_model=Usuario)
def login(credenciales: Login, db: Session = Depends(get_db)):
    usuario = autenticar_usuario(db, credenciales.correo, credenciales.contraseña)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return usuario

