
from fastapi import APIRouter, Depends
import sqlite3

from app.database import get_db_connection
from app.controllers.profesional_controller import ProfesionalController
from app.views.profesional_view import (
    ProfesionalCreate,
    ProfesionalUpdate,
    ProfesionalResponse
)


router = APIRouter(
    prefix="/profesionales",
    tags=["Profesionales"]
)


@router.get("/", response_model=list[ProfesionalResponse])
def listar_profesionales(
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    profesionales = ProfesionalController.get_all(conn)
    return [dict(profesional) for profesional in profesionales]


@router.get("/activos", response_model=list[ProfesionalResponse])
def listar_profesionales_activos(
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    profesionales = ProfesionalController.get_activos(conn)
    return [dict(profesional) for profesional in profesionales]


@router.get("/{profesional_id}", response_model=ProfesionalResponse)
def obtener_profesional(
    profesional_id: int,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    profesional = ProfesionalController.get_by_id(conn, profesional_id)
    return dict(profesional)


@router.post("/", status_code=201)
def crear_profesional(
    datos: ProfesionalCreate,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    respuesta = ProfesionalController.create(
        conn,
        datos.model_dump()
    )

    return respuesta


@router.put("/{profesional_id}")
def actualizar_profesional(
    profesional_id: int,
    datos: ProfesionalUpdate,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    ProfesionalController.update(
        conn,
        profesional_id,
        datos.model_dump()
    )

    return {
        "mensaje": "Profesional actualizado correctamente"
    }


@router.delete("/{profesional_id}")
def eliminar_profesional(
    profesional_id: int,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    ProfesionalController.delete(conn, profesional_id)

    return {
        "mensaje": "Profesional eliminado correctamente"
    }
