
import sqlite3

from fastapi import HTTPException

from app.models.servicio import ServicioModel


class ServicioController:

    # ==========================================
    # LISTAR TODOS LOS SERVICIOS
    # ==========================================

    @staticmethod
    def get_all(conn: sqlite3.Connection):
        servicios = ServicioModel.get_all(conn)

        return [dict(servicio) for servicio in servicios]

    # ==========================================
    # LISTAR SERVICIOS ACTIVOS
    # ==========================================

    @staticmethod
    def get_activos(conn: sqlite3.Connection):
        servicios = ServicioModel.get_activos(conn)

        return [dict(servicio) for servicio in servicios]

    # ==========================================
    # BUSCAR SERVICIO POR NOMBRE
    # ==========================================

    @staticmethod
    def buscar_por_nombre(
        conn: sqlite3.Connection,
        nombre: str
    ):
        servicios = ServicioModel.buscar_por_nombre(
            conn,
            nombre
        )

        return [dict(servicio) for servicio in servicios]

    # ==========================================
    # BUSCAR SERVICIO POR ID
    # ==========================================

    @staticmethod
    def get_by_id(
        conn: sqlite3.Connection,
        servicio_id: int
    ):
        servicio = ServicioModel.get_by_id(conn, servicio_id)

        if not servicio:
            raise HTTPException(
                status_code=404,
                detail="Servicio no encontrado."
            )

        return dict(servicio)

    # ==========================================
    # CREAR SERVICIO
    # ==========================================

    @staticmethod
    def create(
        conn: sqlite3.Connection,
        servicio_data: dict
    ):
        try:
            servicio_id = ServicioModel.create(
                conn,
                servicio_data
            )

            return {
                "mensaje": "Servicio registrado correctamente.",
                "servicio_id": servicio_id
            }

        except sqlite3.IntegrityError:
            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail="No se pudo registrar el servicio. Verifique los datos ingresados y el precio."
            )

    # ==========================================
    # ACTUALIZAR SERVICIO
    # ==========================================

    @staticmethod
    def update(
        conn: sqlite3.Connection,
        servicio_id: int,
        servicio_data: dict
    ):
        servicio = ServicioModel.get_by_id(conn, servicio_id)

        if not servicio:
            raise HTTPException(
                status_code=404,
                detail="Servicio no encontrado."
            )

        try:
            actualizado = ServicioModel.update(
                conn,
                servicio_id,
                servicio_data
            )

            if not actualizado:
                raise HTTPException(
                    status_code=404,
                    detail="No se pudo actualizar el servicio."
                )

            return {
                "mensaje": "Servicio actualizado correctamente."
            }

        except sqlite3.IntegrityError:
            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail="No se pudo actualizar el servicio. Verifique los datos ingresados y el precio."
            )

    # ==========================================
    # ELIMINAR SERVICIO
    # ==========================================

    @staticmethod
    def delete(
        conn: sqlite3.Connection,
        servicio_id: int
    ):
        servicio = ServicioModel.get_by_id(conn, servicio_id)

        if not servicio:
            raise HTTPException(
                status_code=404,
                detail="Servicio no encontrado."
            )

        try:
            eliminado = ServicioModel.delete(conn, servicio_id)

            if not eliminado:
                raise HTTPException(
                    status_code=404,
                    detail="No se pudo eliminar el servicio."
                )

            return {
                "mensaje": "Servicio eliminado correctamente."
            }

        except sqlite3.IntegrityError:
            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail="No se puede eliminar el servicio porque tiene turnos o ventas asociados."
            )
