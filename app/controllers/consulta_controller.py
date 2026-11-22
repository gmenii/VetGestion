
import sqlite3

from fastapi import HTTPException

from app.models.consulta import ConsultaModel


class ConsultaController:

    # ==========================================
    # LISTAR TODAS LAS CONSULTAS
    # ==========================================

    @staticmethod
    def get_all(conn: sqlite3.Connection):
        consultas = ConsultaModel.get_all(conn)

        return [dict(consulta) for consulta in consultas]

    # ==========================================
    # BUSCAR CONSULTA POR ID
    # ==========================================

    @staticmethod
    def get_by_id(
        conn: sqlite3.Connection,
        consulta_id: int
    ):
        consulta = ConsultaModel.get_by_id(conn, consulta_id)

        if not consulta:
            raise HTTPException(
                status_code=404,
                detail="Consulta no encontrada."
            )

        return dict(consulta)

    # ==========================================
    # HISTORIAL CLINICO DE UNA MASCOTA
    # ==========================================

    @staticmethod
    def get_by_mascota(
        conn: sqlite3.Connection,
        mascota_id: int
    ):
        consultas = ConsultaModel.get_by_mascota(
            conn,
            mascota_id
        )

        return [dict(consulta) for consulta in consultas]

    # ==========================================
    # CREAR CONSULTA
    # ==========================================

    @staticmethod
    def create(
        conn: sqlite3.Connection,
        consulta_data: dict
    ):
        try:
            consulta_id = ConsultaModel.create(
                conn,
                consulta_data
            )

            return {
                "mensaje": "Consulta registrada correctamente.",
                "consulta_id": consulta_id
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
                detail="No se pudo registrar la consulta. Verifique los datos ingresados."
            )

    # ==========================================
    # ACTUALIZAR CONSULTA
    # ==========================================

    @staticmethod
    def update(
        conn: sqlite3.Connection,
        consulta_id: int,
        consulta_data: dict
    ):
        consulta = ConsultaModel.get_by_id(conn, consulta_id)

        if not consulta:
            raise HTTPException(
                status_code=404,
                detail="Consulta no encontrada."
            )

        try:
            actualizado = ConsultaModel.update(
                conn,
                consulta_id,
                consulta_data
            )

            if not actualizado:
                raise HTTPException(
                    status_code=404,
                    detail="No se pudo actualizar la consulta."
                )

            return {
                "mensaje": "Consulta actualizada correctamente."
            }

        except sqlite3.IntegrityError:
            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail="No se pudo actualizar la consulta."
            )

    # ==========================================
    # ELIMINAR CONSULTA
    # ==========================================

    @staticmethod
    def delete(
        conn: sqlite3.Connection,
        consulta_id: int
    ):
        consulta = ConsultaModel.get_by_id(conn, consulta_id)

        if not consulta:
            raise HTTPException(
                status_code=404,
                detail="Consulta no encontrada."
            )

        try:
            eliminado = ConsultaModel.delete(conn, consulta_id)

            if not eliminado:
                raise HTTPException(
                    status_code=404,
                    detail="No se pudo eliminar la consulta."
                )

            return {
                "mensaje": "Consulta eliminada correctamente."
            }

        except sqlite3.IntegrityError:
            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail="No se pudo eliminar la consulta."
            )
