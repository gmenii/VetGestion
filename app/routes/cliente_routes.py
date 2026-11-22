from fastapi import APIRouter, Depends
import sqlite3

from app.database import get_db_connection
from app.controllers.cliente_controller import ClienteController
from app.views.cliente_view import (
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse
)


router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


# ==========================================
# LISTAR CLIENTES
# ==========================================

@router.get("/", response_model=list[ClienteResponse])
def listar_clientes(
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    return ClienteController.get_all(conn)


# ==========================================
# BUSCAR CLIENTE POR DNI
# ==========================================

@router.get("/buscar/{dni}", response_model=ClienteResponse)
def buscar_cliente_por_dni(
    dni: str,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    return ClienteController.get_by_dni(conn, dni)


# ==========================================
# BUSCAR CLIENTE POR ID
# ==========================================

@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(
    cliente_id: int,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    return ClienteController.get_by_id(conn, cliente_id)


# ==========================================
# CREAR CLIENTE
# ==========================================

@router.post("/", status_code=201)
def crear_cliente(
    datos: ClienteCreate,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    return ClienteController.create(
        conn,
        datos.model_dump()
    )


# ==========================================
# ACTUALIZAR CLIENTE
# ==========================================

@router.put("/{cliente_id}")
def actualizar_cliente(
    cliente_id: int,
    datos: ClienteUpdate,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    return ClienteController.update(
        conn,
        cliente_id,
        datos.model_dump()
    )


# ==========================================
# ELIMINAR CLIENTE
# ==========================================

@router.delete("/{cliente_id}")
def eliminar_cliente(
    cliente_id: int,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    return ClienteController.delete(conn, cliente_id)
