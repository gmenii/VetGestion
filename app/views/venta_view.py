
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class VentaItem(BaseModel):

    producto_id: Optional[int] = Field(
        default=None,
        gt=0
    )

    servicio_id: Optional[int] = Field(
        default=None,
        gt=0
    )

    cantidad: int = Field(gt=0)


class VentaCreate(BaseModel):

    cliente_id: int = Field(gt=0)

    items: list[VentaItem] = Field(min_length=1)


class VentaResponse(BaseModel):

    id: int
    cliente_id: int
    fecha: str
    total: float

    model_config = ConfigDict(from_attributes=True)


class VentaDetalleResponse(BaseModel):

    id: int
    venta_id: int
    producto_id: Optional[int] = None
    servicio_id: Optional[int] = None
    cantidad: int
    precio_unitario: float
    subtotal: float

    model_config = ConfigDict(from_attributes=True)
