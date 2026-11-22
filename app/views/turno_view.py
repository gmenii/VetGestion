
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal


class TurnoCreate(BaseModel):

    mascota_id: int = Field(gt=0)

    profesional_id: int = Field(gt=0)

    servicio_id: int = Field(gt=0)

    fecha: str = Field(
        pattern=r"^\d{4}-\d{2}-\d{2}$"
    )

    hora: str = Field(
        pattern=r"^([01]\d|2[0-3]):[0-5]\d$"
    )

    motivo: Optional[str] = None


class TurnoUpdate(BaseModel):

    mascota_id: int = Field(gt=0)

    profesional_id: int = Field(gt=0)

    servicio_id: int = Field(gt=0)

    fecha: str = Field(
        pattern=r"^\d{4}-\d{2}-\d{2}$"
    )

    hora: str = Field(
        pattern=r"^([01]\d|2[0-3]):[0-5]\d$"
    )

    motivo: Optional[str] = None


class TurnoEstadoUpdate(BaseModel):

    estado: Literal[
        "Confirmado",
        "En curso",
        "Completado",
        "Cancelado"
    ]


class TurnoResponse(BaseModel):

    id: int
    mascota_id: int
    profesional_id: int
    servicio_id: int
    fecha: str
    hora: str
    estado: str
    motivo: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
