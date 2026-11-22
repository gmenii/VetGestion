
import sqlite3

from fastapi import HTTPException

from app.models.profesional import ProfesionalModel


class ProfesionalController:

    # ==========================================
    # LISTAR TODOS LOS PROFESIONALES
    # ==========================================

    @staticmethod
    def get_all(conn: sqlite3.Connection):
        profesionales = ProfesionalModel.get_all(conn)

        return [dict(profesional) for profesional in profesionales]

    # ==========================================
    # LISTAR PROFESIONALES ACTIVOS
    # ==========================================

    @staticmethod
    def get_activos(conn: sqlite3.Connection):
        profesionales = ProfesionalModel.get_activos(conn)

        return [dict(profesional) for profesional in profesionales]

    # ==========================================
    # BUSCAR PROFESIONAL POR ID
    # ==========================================

    @staticmethod
    def get_by_id(
        conn: sqlite3.Connection,
        profesional_id: int
    ):
        profesional = ProfesionalModel.get_by_id(
            conn,
            profesional_id
        )

        if not profesional:
            raise HTTPException(
                status_code=404,
                detail="Profesional no encontrado."
            )

        return dict(profesional)

    # ==========================================
    # CREAR PROFESIONAL
    # ==========================================

    @staticmethod
    def create(
        conn: sqlite3.Connection,
        profesional_data: dict
    ):
        try:
            profesional_id = ProfesionalModel.create(
                conn,
                profesional_data
            )

            return {
                "mensaje": "Profesional registrado correctamente.",
                "profesional_id": profesional_id
            }

        except sqlite3.IntegrityError:
            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail="No se pudo registrar el profesional. Verifique que la matrícula no esté registrada y que los datos sean válidos."
            )

    # ==========================================
    # ACTUALIZAR PROFESIONAL
    # ==========================================

    @staticmethod
    def update(
        conn: sqlite3.Connection,
        profesional_id: int,
        profesional_data: dict
    ):
        profesional = ProfesionalModel.get_by_id(
            conn,
            profesional_id
        )

        if not profesional:
            raise HTTPException(
                status_code=404,
                detail="Profesional no encontrado."
            )

        try:
            actualizado = ProfesionalModel.update(
                conn,
                profesional_id,
                profesional_data
            )

            if not actualizado:
                raise HTTPException(
                    status_code=404,
                    detail="No se pudo actualizar el profesional."
                )

            return {
                "mensaje": "Profesional actualizado correctamente."
            }

        except sqlite3.IntegrityError:
            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail="No se pudo actualizar el profesional. Verifique que la matrícula no esté registrada y que los datos sean válidos."
            )

    # ==========================================
    # ELIMINAR PROFESIONAL
    # ==========================================

    @staticmethod
    def delete(
        conn: sqlite3.Connection,
        profesional_id: int
    ):
        profesional = ProfesionalModel.get_by_id(
            conn,
            profesional_id
        )

        if not profesional:
            raise HTTPException(
                status_code=404,
                detail="Profesional no encontrado."
            )

        try:
            eliminado = ProfesionalModel.delete(
                conn,
                profesional_id
            )

            if not eliminado:
                raise HTTPException(
                    status_code=404,
                    detail="No se pudo eliminar el profesional."
                )

            return {
                "mensaje": "Profesional eliminado correctamente."
            }

        except sqlite3.IntegrityError:
            conn.rollback()

            raise HTTPException(
                status_code=400,
                detail="No se puede eliminar el profesional porque tiene turnos asociados."
            )
