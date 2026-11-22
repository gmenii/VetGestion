
from fastapi import APIRouter, Depends, HTTPException
import sqlite3

from app.database import get_db_connection
from app.controllers.venta_controller import VentaController
from app.views.venta_view import VentaCreate


router = APIRouter(
    prefix="/ventas",
    tags=["Ventas"]
)


@router.get("/")
def listar_ventas(
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    ventas = VentaController.get_all(conn)
    return [dict(venta) for venta in ventas]


@router.get("/{venta_id}")
def obtener_venta(
    venta_id: int,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    venta = VentaController.get_by_id(conn, venta_id)

    if not venta:
        raise HTTPException(
            status_code=404,
            detail="La venta no existe."
        )

    detalles = VentaController.get_detalles(conn, venta_id)

    resultado = dict(venta)
    resultado["detalles"] = [
        dict(detalle) for detalle in detalles
    ]

    return resultado


@router.get("/cliente/{cliente_id}")
def listar_ventas_cliente(
    cliente_id: int,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    ventas = VentaController.get_by_cliente(conn, cliente_id)
    return [dict(venta) for venta in ventas]


@router.get("/{venta_id}/detalles")
def obtener_detalles_venta(
    venta_id: int,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    detalles = VentaController.get_detalles(conn, venta_id)
    return [dict(detalle) for detalle in detalles]


@router.post("/", status_code=201)
def crear_venta(
    datos: VentaCreate,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    items = [
        item.model_dump()
        for item in datos.items
    ]

    respuesta = VentaController.create(
        conn,
        datos.cliente_id,
        items
    )

    return respuesta
