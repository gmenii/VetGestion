from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional


EstadoCliente = Literal["Activo", "Inactivo"]


class ClienteCreate(BaseModel):
    dni: str = Field(min_length=7, max_length=15)
    nombre: str = Field(min_length=2, max_length=50)
    apellido: str = Field(min_length=2, max_length=50)
    email: Optional[str] = None
    telefono: Optional[str] = Field(default=None, max_length=20)
    direccion: Optional[str] = Field(default=None, max_length=150)
    estado: EstadoCliente = "Activo"


class ClienteUpdate(BaseModel):
    dni: str = Field(min_length=7, max_length=15)
    nombre: str = Field(min_length=2, max_length=50)
    apellido: str = Field(min_length=2, max_length=50)
    email: Optional[str] = None
    telefono: Optional[str] = Field(default=None, max_length=20)
    direccion: Optional[str] = Field(default=None, max_length=150)
    estado: EstadoCliente = "Activo"


class ClienteResponse(BaseModel):
    id: int
    dni: str
    nombre: str
    apellido: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    estado: EstadoCliente = "Activo"

    model_config = ConfigDict(from_attributes=True)
