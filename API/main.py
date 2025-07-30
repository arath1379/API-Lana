from fastapi import FastAPI
from DB.conexion import engine
from models.modelsDB import Base
from routers import auth, transacciones, presupuestos, pagos, reportes, categorias
from fastapi.middleware.cors import CORSMiddleware

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API LanaApp",
    description="Sistema de Gestión Financiera",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

# Incluir todos los routers
app.include_router(auth.router)
app.include_router(transacciones.router)
app.include_router(presupuestos.router)
app.include_router(pagos.router)
app.include_router(reportes.router)
app.include_router(categorias.router)

@app.get("/")
def inicio():
    return {"mensaje": "API LanaApp - Sistema de Gestión Financiera"}