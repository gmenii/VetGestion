
import sqlite3

from fastapi import HTTPException

from app.models.mascota import MascotaModel
from app.models.cliente import ClienteModel


class MascotaController:

    # ==========================================
    # LISTAR MASCOTAS
    # ==========================================

    @staticmethod
    def get_all(conn: sqlite3.Connection):
        mascotas = MascotaModel.get_all(conn)

        return [dict(mascota) for mascota in mascotas]

    # ==========================================
    # BUSCAR MASCOTA POR ID
    # ==========================================

    @staticmethod
    def get_by_id(
        conn: sqlite3.Connection,
        mascota_id: int
    ):
        mascota = MascotaModel.get_by_id(conn, mascota_id)

        if not mascota:
            raise HTTPException(
                status_code=404,
                detail="Mascota no encontrada."
            )

        return dict(mascota)

    # ==========================================
    # VALIDAR CLIENTE
    # ==========================================

    @staticmethod
    def validar_cliente(
        conn: sqlite3.Connection,
        cliente_id: int
    ):
        cliente = ClienteModel.get_by_id(conn, cliente_id)

        if not cliente:
            raise HTTPException(
                status_code=404,
                detail="El cliente indicado no existe."
            )

    # ==========================================
    # CREAR MASCOTA
    # ==========================================

    @staticmethod
    def create(
        conn: sqlite3.Connection,
        mascota_data: dict
    ):
        MascotaController.validar_cliente(
            conn,
            mascota_data["cliente_id"]
        )

        try:
            mascota_id = MascotaModel.create(conn, mascota_data)

            return {
                "mensaje": "Mascota registrada correctamente.",
                "mascota_id": mascota_id
            }

        except sqlite3.IntegrityError:
            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail="No se pudo registrar la mascota. Verifique los datos ingresados."
            )

    # ==========================================
    # ACTUALIZAR MASCOTA
    # ==========================================

    @staticmethod
    def update(
        conn: sqlite3.Connection,
        mascota_id: int,
        mascota_data: dict
    ):
        mascota = MascotaModel.get_by_id(conn, mascota_id)

        if not mascota:
            raise HTTPException(
                status_code=404,
                detail="Mascota no encontrada."
            )

        MascotaController.validar_cliente(
            conn,
            mascota_data["cliente_id"]
        )

        try:
            actualizado = MascotaModel.update(
                conn,
                mascota_id,
                mascota_data
            )

            if not actualizado:
                raise HTTPException(
                    status_code=404,
                    detail="No se pudo actualizar la mascota."
                )

            return {
                "mensaje": "Mascota actualizada correctamente."
            }

        except sqlite3.IntegrityError:
            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail="No se pudo actualizar la mascota. Verifique los datos ingresados."
            )

    # ==========================================
    # ELIMINAR MASCOTA
    # ==========================================

    @staticmethod
    def delete(
        conn: sqlite3.Connection,
        mascota_id: int
    ):
        mascota = MascotaModel.get_by_id(conn, mascota_id)

        if not mascota:
            raise HTTPException(
                status_code=404,
                detail="Mascota no encontrada."
            )

        try:
            eliminado = MascotaModel.delete(conn, mascota_id)

            if not eliminado:
                raise HTTPException(
                    status_code=404,
                    detail="No se pudo eliminar la mascota."
                )

            return {
                "mensaje": "Mascota eliminada correctamente."
            }

        except sqlite3.IntegrityError:
            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail="No se puede eliminar la mascota porque tiene turnos asociados."
            )
