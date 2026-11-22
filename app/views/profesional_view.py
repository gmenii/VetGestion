
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal


class ProfesionalCreate(BaseModel):

    matricula: str = Field(
        min_length=3,
        max_length=20
    )

    nombre: str = Field(
        min_length=2,
        max_length=50
    )

    apellido: str = Field(
        min_length=2,
        max_length=50
    )

    email: Optional[str] = None

    estado: Literal["Activo", "Inactivo"] = "Activo"


class ProfesionalUpdate(BaseModel):

    matricula: str = Field(
        min_length=3,
        max_length=20
    )

    nombre: str = Field(
        min_length=2,
        max_length=50
    )

    apellido: str = Field(
        min_length=2,
        max_length=50
    )

    email: Optional[str] = None

    estado: Literal["Activo", "Inactivo"] = "Activo"


class ProfesionalResponse(BaseModel):

    id: int
    matricula: str
    nombre: str
    apellido: str
    email: Optional[str] = None
    estado: str

    model_config = ConfigDict(from_attributes=True)
