
from fastapi import APIRouter, Depends
import sqlite3

from app.database import get_db_connection
from app.controllers.mascota_controller import MascotaController
from app.views.mascota_view import (
    MascotaCreate,
    MascotaUpdate,
    MascotaResponse
)


router = APIRouter(
    prefix="/mascotas",
    tags=["Mascotas"]
)


@router.get("/", response_model=list[MascotaResponse])
def listar_mascotas(
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    mascotas = MascotaController.get_all(conn)
    return [dict(mascota) for mascota in mascotas]


@router.get("/{mascota_id}", response_model=MascotaResponse)
def obtener_mascota(
    mascota_id: int,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    mascota = MascotaController.get_by_id(conn, mascota_id)
    return dict(mascota)


@router.post("/", status_code=201)
def crear_mascota(
    datos: MascotaCreate,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    respuesta = MascotaController.create(
        conn,
        datos.model_dump()
    )

    return respuesta


@router.put("/{mascota_id}")
def actualizar_mascota(
    mascota_id: int,
    datos: MascotaUpdate,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    MascotaController.update(
        conn,
        mascota_id,
        datos.model_dump()
    )

    return {
        "mensaje": "Mascota actualizada correctamente"
    }


@router.delete("/{mascota_id}")
def eliminar_mascota(
    mascota_id: int,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    MascotaController.delete(conn, mascota_id)

    return {
        "mensaje": "Mascota eliminada correctamente"
    }
