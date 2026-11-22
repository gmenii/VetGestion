
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal


class ServicioCreate(BaseModel):

    nombre: str = Field(
        min_length=2,
        max_length=100
    )

    descripcion: Optional[str] = None

    precio: float = Field(ge=0)

    estado: Literal["Activo", "Inactivo"] = "Activo"


class ServicioUpdate(BaseModel):

    nombre: str = Field(
        min_length=2,
        max_length=100
    )

    descripcion: Optional[str] = None

    precio: float = Field(ge=0)

    estado: Literal["Activo", "Inactivo"] = "Activo"


class ServicioResponse(BaseModel):

    id: int
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    estado: str

    model_config = ConfigDict(from_attributes=True)
