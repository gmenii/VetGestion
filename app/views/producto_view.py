
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal


class ProductoCreate(BaseModel):

    nombre: str = Field(
        min_length=2,
        max_length=100
    )

    categoria: Optional[Literal["Medicamentos", "Vacunas"]] = None

    descripcion: Optional[str] = None

    precio: float = Field(ge=0)

    stock: int = Field(ge=0)

    stock_minimo: int = Field(
        default=5,
        ge=0
    )

    estado: Literal["Activo", "Inactivo"] = "Activo"


class ProductoUpdate(BaseModel):

    nombre: str = Field(
        min_length=2,
        max_length=100
    )

    categoria: Optional[Literal["Medicamentos", "Vacunas"]] = None

    descripcion: Optional[str] = None

    precio: float = Field(ge=0)

    stock: int = Field(ge=0)

    stock_minimo: int = Field(ge=0)

    estado: Literal["Activo", "Inactivo"] = "Activo"


class ProductoStockUpdate(BaseModel):

    cantidad: int


class ProductoResponse(BaseModel):

    id: int
    nombre: str
    categoria: Optional[str] = None
    descripcion: Optional[str] = None
    precio: float
    stock: int
    stock_minimo: int
    estado: str

    model_config = ConfigDict(from_attributes=True)
