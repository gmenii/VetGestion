
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal


class MascotaCreate(BaseModel):

    cliente_id: int = Field(gt=0)

    nombre: str = Field(
        min_length=2,
        max_length=50
    )

    especie: Literal["Perro", "Gato"]

    raza: Optional[str] = Field(
        default=None,
        max_length=50
    )

    fecha_nacimiento: Optional[str] = None

    sexo: Optional[Literal["Hembra", "Macho"]] = None

    observaciones: Optional[str] = None


class MascotaUpdate(BaseModel):

    cliente_id: int = Field(gt=0)

    nombre: str = Field(
        min_length=2,
        max_length=50
    )

    especie: Literal["Perro", "Gato"]

    raza: Optional[str] = Field(
        default=None,
        max_length=50
    )

    fecha_nacimiento: Optional[str] = None

    sexo: Optional[Literal["Hembra", "Macho"]] = None

    observaciones: Optional[str] = None


class MascotaResponse(BaseModel):

    id: int
    cliente_id: int
    nombre: str
    especie: str
    raza: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    sexo: Optional[str] = None
    observaciones: Optional[str] = None

    nombre_cliente: Optional[str] = None
    apellido_cliente: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
