
import sqlite3

from fastapi import HTTPException

from app.models.venta import VentaModel


class VentaController:

    # ==========================================
    # LISTAR TODAS LAS VENTAS
    # ==========================================

    @staticmethod
    def get_all(conn: sqlite3.Connection):
        ventas = VentaModel.get_all(conn)

        return [dict(venta) for venta in ventas]

    # ==========================================
    # BUSCAR VENTA POR ID
    # ==========================================

    @staticmethod
    def get_by_id(
        conn: sqlite3.Connection,
        venta_id: int
    ):
        venta = VentaModel.get_by_id(conn, venta_id)

        if not venta:
            raise HTTPException(
                status_code=404,
                detail="Venta no encontrada."
            )

        return dict(venta)

    # ==========================================
    # LISTAR VENTAS DE UN CLIENTE
    # ==========================================

    @staticmethod
    def get_by_cliente(
        conn: sqlite3.Connection,
        cliente_id: int
    ):
        ventas = VentaModel.get_by_cliente(
            conn,
            cliente_id
        )

        return [dict(venta) for venta in ventas]

    # ==========================================
    # CONSULTAR DETALLES DE UNA VENTA
    # ==========================================

    @staticmethod
    def get_detalles(
        conn: sqlite3.Connection,
        venta_id: int
    ):
        venta = VentaModel.get_by_id(conn, venta_id)

        if not venta:
            raise HTTPException(
                status_code=404,
                detail="Venta no encontrada."
            )

        detalles = VentaModel.get_detalles(conn, venta_id)

        return [dict(detalle) for detalle in detalles]

    # ==========================================
    # CREAR VENTA
    # ==========================================

    @staticmethod
    def create(
        conn: sqlite3.Connection,
        cliente_id: int,
        items: list
    ):
        try:
            venta_id = VentaModel.create_transaction(
                conn,
                cliente_id,
                items
            )

            return {
                "mensaje": "Venta registrada correctamente.",
                "venta_id": venta_id
            }

        except ValueError as error:
            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail=str(error)
            )

        except sqlite3.IntegrityError:
            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail="No se pudo registrar la venta. Verifique los datos ingresados."
            )

