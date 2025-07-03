from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from DB.conexion import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, index=True, nullable=False)
    contraseña = Column(String(100), nullable=False)
    
    transacciones = relationship("Transaccion", back_populates="usuario")
    presupuestos = relationship("Presupuesto", back_populates="usuario")
    pagos = relationship("PagoProgramado", back_populates="usuario")

class Categoria(Base):
    __tablename__ = "categorias"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    tipo = Column(String(10), nullable=False)

class Transaccion(Base):
    __tablename__ = "transacciones"
    
    id = Column(Integer, primary_key=True, index=True)
    monto = Column(Float, nullable=False)
    tipo = Column(String(10), nullable=False)
    fecha = Column(Date, nullable=False)
    descripcion = Column(String(200))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    
    usuario = relationship("Usuario", back_populates="transacciones")
    categoria = relationship("Categoria")

class Presupuesto(Base):
    __tablename__ = "presupuestos"
    
    id = Column(Integer, primary_key=True, index=True)
    monto = Column(Float, nullable=False)
    mes = Column(Integer, nullable=False)
    año = Column(Integer, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    
    usuario = relationship("Usuario", back_populates="presupuestos")
    categoria = relationship("Categoria")

class PagoProgramado(Base):
    __tablename__ = "pagos_programados"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    monto = Column(Float, nullable=False)
    fecha = Column(Date, nullable=False)
    estado = Column(String(20), default="pendiente")
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    
    usuario = relationship("Usuario", back_populates="pagos")
    categoria = relationship("Categoria")