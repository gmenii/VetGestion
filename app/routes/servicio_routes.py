
from fastapi import APIRouter, Depends, Query
import sqlite3

from app.database import get_db_connection
from app.controllers.servicio_controller import ServicioController
from app.views.servicio_view import (
    ServicioCreate,
    ServicioUpdate,
    ServicioResponse
)


router = APIRouter(
    prefix="/servicios",
    tags=["Servicios"]
)


@router.get("/", response_model=list[ServicioResponse])
def listar_servicios(
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    servicios = ServicioController.get_all(conn)
    return [dict(servicio) for servicio in servicios]


@router.get("/activos", response_model=list[ServicioResponse])
def listar_servicios_activos(
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    servicios = ServicioController.get_activos(conn)
    return [dict(servicio) for servicio in servicios]


@router.get("/buscar", response_model=list[ServicioResponse])
def buscar_servicios(
    nombre: str = Query(..., min_length=1),
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    return ServicioController.buscar_por_nombre(
        conn,
        nombre
    )


@router.get("/{servicio_id}", response_model=ServicioResponse)
def obtener_servicio(
    servicio_id: int,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    servicio = ServicioController.get_by_id(conn, servicio_id)
    return dict(servicio)


@router.post("/", status_code=201)
def crear_servicio(
    datos: ServicioCreate,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    respuesta = ServicioController.create(
        conn,
        datos.model_dump()
    )

    return respuesta


@router.put("/{servicio_id}")
def actualizar_servicio(
    servicio_id: int,
    datos: ServicioUpdate,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    ServicioController.update(
        conn,
        servicio_id,
        datos.model_dump()
    )

    return {
        "mensaje": "Servicio actualizado correctamente"
    }


@router.delete("/{servicio_id}")
def eliminar_servicio(
    servicio_id: int,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    ServicioController.delete(conn, servicio_id)

    return {
        "mensaje": "Servicio eliminado correctamente"
    }
