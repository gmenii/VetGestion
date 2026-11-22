
import sqlite3

from fastapi import HTTPException

from app.models.producto import ProductoModel


class ProductoController:

    # ==========================================
    # LISTAR PRODUCTOS
    # ==========================================

    @staticmethod
    def get_all(conn: sqlite3.Connection):
        productos = ProductoModel.get_all(conn)

        return [dict(producto) for producto in productos]

    # ==========================================
    # LISTAR PRODUCTOS ACTIVOS
    # ==========================================

    @staticmethod
    def get_activos(conn: sqlite3.Connection):
        productos = ProductoModel.get_activos(conn)

        return [dict(producto) for producto in productos]

    # ==========================================
    # BUSCAR PRODUCTO POR NOMBRE
    # ==========================================

    @staticmethod
    def buscar_por_nombre(
        conn: sqlite3.Connection,
        nombre: str
    ):
        productos = ProductoModel.buscar_por_nombre(
            conn,
            nombre
        )

        return [dict(producto) for producto in productos]

    # ==========================================
    # BUSCAR PRODUCTO POR ID
    # ==========================================

    @staticmethod
    def get_by_id(
        conn: sqlite3.Connection,
        producto_id: int
    ):
        producto = ProductoModel.get_by_id(conn, producto_id)

        if not producto:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado."
            )

        return dict(producto)

    # ==========================================
    # BUSCAR POR CATEGORIA
    # ==========================================

    @staticmethod
    def get_by_categoria(
        conn: sqlite3.Connection,
        categoria: str
    ):
        productos = ProductoModel.get_by_categoria(
            conn,
            categoria
        )

        return [dict(producto) for producto in productos]

    # ==========================================
    # CONSULTAR STOCK BAJO
    # ==========================================

    @staticmethod
    def get_stock_bajo(conn: sqlite3.Connection):
        productos = ProductoModel.get_stock_bajo(conn)

        return [dict(producto) for producto in productos]

    # ==========================================
    # CREAR PRODUCTO
    # ==========================================

    @staticmethod
    def create(
        conn: sqlite3.Connection,
        producto_data: dict
    ):
        try:
            producto_id = ProductoModel.create(
                conn,
                producto_data
            )

            return {
                "mensaje": "Producto registrado correctamente.",
                "producto_id": producto_id
            }

        except sqlite3.IntegrityError:
            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail="No se pudo registrar el producto. Verifique el precio y las cantidades."
            )

    # ==========================================
    # ACTUALIZAR PRODUCTO
    # ==========================================

    @staticmethod
    def update(
        conn: sqlite3.Connection,
        producto_id: int,
        producto_data: dict
    ):
        producto = ProductoModel.get_by_id(conn, producto_id)

        if not producto:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado."
            )

        try:
            actualizado = ProductoModel.update(
                conn,
                producto_id,
                producto_data
            )

            if not actualizado:
                raise HTTPException(
                    status_code=404,
                    detail="No se pudo actualizar el producto."
                )

            return {
                "mensaje": "Producto actualizado correctamente."
            }

        except sqlite3.IntegrityError:
            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail="No se pudo actualizar el producto. Verifique el precio y las cantidades."
            )

    # ==========================================
    # ACTUALIZAR STOCK
    # ==========================================

    @staticmethod
    def actualizar_stock(
        conn: sqlite3.Connection,
        producto_id: int,
        cantidad: int
    ):
        producto = ProductoModel.get_by_id(conn, producto_id)

        if not producto:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado."
            )

        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad == 0:
            raise HTTPException(
                status_code=400,
                detail="La cantidad debe ser un número entero distinto de cero."
            )

        actualizado = ProductoModel.actualizar_stock(
            conn,
            producto_id,
            cantidad
        )

        if not actualizado:
            raise HTTPException(
                status_code=400,
                detail="No se pudo actualizar el stock. Verifique que no quede negativo."
            )

        return {
            "mensaje": "Stock actualizado correctamente."
        }

    # ==========================================
    # ELIMINAR PRODUCTO
    # ==========================================

    @staticmethod
    def delete(
        conn: sqlite3.Connection,
        producto_id: int
    ):
        producto = ProductoModel.get_by_id(conn, producto_id)

        if not producto:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado."
            )

        try:
            eliminado = ProductoModel.delete(conn, producto_id)

            if not eliminado:
                raise HTTPException(
                    status_code=404,
                    detail="No se pudo eliminar el producto."
                )

            return {
                "mensaje": "Producto eliminado correctamente."
            }

        except sqlite3.IntegrityError:
            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail="No se puede eliminar el producto porque tiene ventas asociadas."
            )
