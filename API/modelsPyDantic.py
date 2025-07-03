from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Literal
from datetime import date

# Modelos para Usuario
class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    correo: EmailStr

class UsuarioCreate(UsuarioBase):
    contraseña: str = Field(..., min_length=6)

class Usuario(UsuarioBase):
    id: int
    
    class Config:
        from_attributes = True  # Reemplaza orm_mode en Pydantic v2

# Modelos para Categoría (NUEVO)
class CategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50)
    tipo: Literal['ingreso', 'egreso']  # Solo permite estos valores

class Categoria(CategoriaBase):
    id: int
    
    class Config:
        from_attributes = True

# Modelos para Transacción
class TransaccionBase(BaseModel):
    monto: float = Field(..., gt=0)  # Mayor que 0
    tipo: Literal['ingreso', 'egreso']
    fecha: date
    descripcion: Optional[str] = Field(None, max_length=200)
    categoria_id: int

    @field_validator('fecha')
    def fecha_no_futura(cls, v):
        if v > date.today():
            raise ValueError("La fecha no puede ser futura")
        return v

class Transaccion(TransaccionBase):
    id: int
    usuario_id: int
    
    class Config:
        from_attributes = True

class TransaccionCreate(TransaccionBase):
    pass

# Modelos para Presupuesto
class PresupuestoBase(BaseModel):
    monto: float = Field(..., gt=0)
    mes: int = Field(..., ge=1, le=12)  # Entre 1 y 12
    año: int = Field(..., ge=2000)      # Año >= 2000
    categoria_id: int

class Presupuesto(PresupuestoBase):
    id: int
    usuario_id: int
    
    class Config:
        from_attributes = True

class PresupuestoCreate(PresupuestoBase):
    pass

# Modelos para Pagos Programados
class PagoProgramadoBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    monto: float = Field(..., gt=0)
    fecha: date
    estado: Literal['pendiente', 'pagado', 'cancelado'] = "pendiente"
    categoria_id: int

class PagoProgramado(PagoProgramadoBase):
    id: int
    usuario_id: int
    
    class Config:
        from_attributes = True

class PagoProgramadoCreate(PagoProgramadoBase):
    pass

# Modelo para Login
class Login(BaseModel):
    correo: EmailStr
    contraseña: str = Field(..., min_length=6)