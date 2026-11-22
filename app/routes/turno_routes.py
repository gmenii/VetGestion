
from fastapi import APIRouter, Depends
import sqlite3

from app.database import get_db_connection
from app.controllers.turno_controller import TurnoController
from app.views.turno_view import (
    TurnoCreate,
    TurnoUpdate,
    TurnoEstadoUpdate,
    TurnoResponse
)


router = APIRouter(
    prefix="/turnos",
    tags=["Turnos"]
)


@router.get("/")
def listar_turnos(
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    turnos = TurnoController.get_all(conn)
    return [dict(turno) for turno in turnos]


@router.get("/{turno_id}")
def obtener_turno(
    turno_id: int,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    turno = TurnoController.get_by_id(conn, turno_id)
    return dict(turno)


@router.post("/", status_code=201)
def crear_turno(
    datos: TurnoCreate,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    respuesta = TurnoController.create(
        conn,
        datos.model_dump()
    )

    return respuesta


@router.put("/{turno_id}")
def reprogramar_turno(
    turno_id: int,
    datos: TurnoUpdate,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    TurnoController.update(
        conn,
        turno_id,
        datos.model_dump()
    )

    return {
        "mensaje": "Turno reprogramado correctamente"
    }


@router.patch("/{turno_id}/estado")
def cambiar_estado_turno(
    turno_id: int,
    datos: TurnoEstadoUpdate,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    TurnoController.cambiar_estado(
        conn,
        turno_id,
        datos.estado
    )

    return {
        "mensaje": "Estado del turno actualizado correctamente"
    }


@router.delete("/{turno_id}")
def cancelar_turno(
    turno_id: int,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    TurnoController.delete(conn, turno_id)

    return {
        "mensaje": "Turno cancelado correctamente"
    }
