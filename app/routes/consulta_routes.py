
from fastapi import APIRouter, Depends
import sqlite3

from app.database import get_db_connection
from app.controllers.consulta_controller import ConsultaController
from app.views.consulta_view import (
    ConsultaCreate,
    ConsultaUpdate,
    ConsultaResponse
)


router = APIRouter(
    prefix="/consultas",
    tags=["Consultas"]
)


@router.get("/")
def listar_consultas(
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    consultas = ConsultaController.get_all(conn)
    return [dict(consulta) for consulta in consultas]


@router.get("/mascota/{mascota_id}")
def historial_mascota(
    mascota_id: int,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    consultas = ConsultaController.get_by_mascota(
        conn,
        mascota_id
    )

    return [dict(consulta) for consulta in consultas]


@router.get("/{consulta_id}", response_model=ConsultaResponse)
def obtener_consulta(
    consulta_id: int,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    consulta = ConsultaController.get_by_id(conn, consulta_id)
    return dict(consulta)


@router.post("/", status_code=201)
def crear_consulta(
    datos: ConsultaCreate,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    respuesta = ConsultaController.create(
        conn,
        datos.model_dump()
    )

    return respuesta

@router.put("/{consulta_id}")
def actualizar_consulta(
    consulta_id: int,
    datos: ConsultaUpdate,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    ConsultaController.update(
        conn,
        consulta_id,
        datos.model_dump()
    )

    return {
        "mensaje": "Consulta actualizada correctamente"
    }


@router.delete("/{consulta_id}")
def eliminar_consulta(
    consulta_id: int,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    ConsultaController.delete(conn, consulta_id)

    return {
        "mensaje": "Consulta eliminada correctamente"
    }
