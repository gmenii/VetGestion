
import sqlite3

from fastapi import HTTPException

from app.models.cliente import ClienteModel


class ClienteController:

    # ==========================================
    # LISTAR CLIENTES
    # ==========================================

    @staticmethod
    def get_all(conn: sqlite3.Connection):
        clientes = ClienteModel.get_all(conn)

        return [dict(cliente) for cliente in clientes]

    # ==========================================
    # BUSCAR CLIENTE POR ID
    # ==========================================

    @staticmethod
    def get_by_id(
        conn: sqlite3.Connection,
        cliente_id: int
    ):
        cliente = ClienteModel.get_by_id(conn, cliente_id)

        if not cliente:
            raise HTTPException(
                status_code=404,
                detail="Cliente no encontrado."
            )

        return dict(cliente)

    # ==========================================
    # BUSCAR CLIENTE POR DNI
    # ==========================================

    @staticmethod
    def get_by_dni(
        conn: sqlite3.Connection,
        dni: str
    ):
        cliente = ClienteModel.get_by_dni(conn, dni)

        if not cliente:
            raise HTTPException(
                status_code=404,
                detail="No se encontró ningún cliente con ese DNI."
            )

        return dict(cliente)

    # ==========================================
    # CREAR CLIENTE
    # ==========================================

    @staticmethod
    def create(
        conn: sqlite3.Connection,
        cliente_data: dict
    ):
        try:
            cliente_id = ClienteModel.create(conn, cliente_data)

            return {
                "mensaje": "Cliente creado correctamente.",
                "cliente_id": cliente_id
            }

        except sqlite3.IntegrityError:
            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail="No se pudo crear el cliente. Verifique que el DNI no esté registrado."
            )

    # ==========================================
    # ACTUALIZAR CLIENTE
    # ==========================================

    @staticmethod
    def update(
        conn: sqlite3.Connection,
        cliente_id: int,
        cliente_data: dict
    ):
        cliente = ClienteModel.get_by_id(conn, cliente_id)

        if not cliente:
            raise HTTPException(
                status_code=404,
                detail="Cliente no encontrado."
            )

        try:
            actualizado = ClienteModel.update(
                conn,
                cliente_id,
                cliente_data
            )

            if not actualizado:
                raise HTTPException(
                    status_code=404,
                    detail="No se pudo actualizar el cliente."
                )

            return {
                "mensaje": "Cliente actualizado correctamente."
            }

        except sqlite3.IntegrityError:
            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail="No se pudo actualizar el cliente. Verifique que el DNI no esté registrado."
            )

    # ==========================================
    # ELIMINAR CLIENTE
    # ==========================================

    @staticmethod
    def delete(
        conn: sqlite3.Connection,
        cliente_id: int
    ):
        cliente = ClienteModel.get_by_id(conn, cliente_id)

        if not cliente:
            raise HTTPException(
                status_code=404,
                detail="Cliente no encontrado."
            )

        try:
            eliminado = ClienteModel.delete(conn, cliente_id)

            if not eliminado:
                raise HTTPException(
                    status_code=404,
                    detail="No se pudo eliminar el cliente."
                )

            return {
                "mensaje": "Cliente eliminado correctamente."
            }

        except sqlite3.IntegrityError:
            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail="No se puede eliminar el cliente porque tiene mascotas o ventas asociadas."
            )
