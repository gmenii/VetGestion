
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ConsultaCreate(BaseModel):

    turno_id: int = Field(gt=0)

    fecha: str = Field(
        pattern=r"^\d{4}-\d{2}-\d{2}$"
    )

    diagnostico: str = Field(
        min_length=2,
        max_length=500
    )

    observaciones: Optional[str] = None


class ConsultaUpdate(BaseModel):

    fecha: str = Field(
        pattern=r"^\d{4}-\d{2}-\d{2}$"
    )

    diagnostico: str = Field(
        min_length=2,
        max_length=500
    )

    observaciones: Optional[str] = None


class ConsultaResponse(BaseModel):

    id: int
    turno_id: int
    fecha: str
    diagnostico: str
    observaciones: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
