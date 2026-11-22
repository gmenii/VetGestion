
from fastapi import APIRouter, Depends, Query
import sqlite3

from app.database import get_db_connection
from app.controllers.producto_controller import ProductoController
from app.views.producto_view import (
    ProductoCreate,
    ProductoUpdate,
    ProductoStockUpdate,
    ProductoResponse
)


router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)


@router.get("/", response_model=list[ProductoResponse])
def listar_productos(
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    productos = ProductoController.get_all(conn)
    return [dict(producto) for producto in productos]


@router.get("/activos", response_model=list[ProductoResponse])
def listar_productos_activos(
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    productos = ProductoController.get_activos(conn)
    return [dict(producto) for producto in productos]


@router.get("/buscar", response_model=list[ProductoResponse])
def buscar_productos(
    nombre: str = Query(..., min_length=1),
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    return ProductoController.buscar_por_nombre(
        conn,
        nombre
    )


@router.get("/stock-bajo", response_model=list[ProductoResponse])
def listar_stock_bajo(
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    productos = ProductoController.get_stock_bajo(conn)
    return [dict(producto) for producto in productos]


@router.get("/categoria/{categoria}", response_model=list[ProductoResponse])
def listar_por_categoria(
    categoria: str,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    productos = ProductoController.get_by_categoria(
        conn,
        categoria
    )

    return [dict(producto) for producto in productos]


@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(
    producto_id: int,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    producto = ProductoController.get_by_id(conn, producto_id)
    return dict(producto)


@router.post("/", status_code=201)
def crear_producto(
    datos: ProductoCreate,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    respuesta = ProductoController.create(
        conn,
        datos.model_dump()
    )

    return respuesta


@router.put("/{producto_id}")
def actualizar_producto(
    producto_id: int,
    datos: ProductoUpdate,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    ProductoController.update(
        conn,
        producto_id,
        datos.model_dump()
    )

    return {
        "mensaje": "Producto actualizado correctamente"
    }


@router.patch("/{producto_id}/stock")
def actualizar_stock(
    producto_id: int,
    datos: ProductoStockUpdate,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    ProductoController.actualizar_stock(
        conn,
        producto_id,
        datos.cantidad
    )

    return {
        "mensaje": "Stock actualizado correctamente"
    }


@router.delete("/{producto_id}")
def eliminar_producto(
    producto_id: int,
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    ProductoController.delete(conn, producto_id)

    return {
        "mensaje": "Producto eliminado correctamente"
    }
