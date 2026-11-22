
import sqlite3

from fastapi import HTTPException

from app.models.turno import TurnoModel


class TurnoController:

    # ==========================================
    # LISTAR TURNOS
    # ==========================================

    @staticmethod
    def get_all(conn: sqlite3.Connection):
        turnos = TurnoModel.get_all(conn)

        return [dict(turno) for turno in turnos]

    # ==========================================
    # BUSCAR TURNO POR ID
    # ==========================================

    @staticmethod
    def get_by_id(
        conn: sqlite3.Connection,
        turno_id: int
    ):
        turno = TurnoModel.get_by_id(conn, turno_id)

        if not turno:
            raise HTTPException(
                status_code=404,
                detail="Turno no encontrado."
            )

        return dict(turno)

    # ==========================================
    # CREAR TURNO
    # ==========================================

    @staticmethod
    def create(
        conn: sqlite3.Connection,
        turno_data: dict
    ):
        try:
            turno_id = TurnoModel.create(conn, turno_data)

            return {
                "mensaje": "Turno registrado correctamente.",
                "turno_id": turno_id
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
                detail="No se pudo registrar el turno. Verifique los datos ingresados."
            )

    # ==========================================
    # REPROGRAMAR TURNO
    # ==========================================

    @staticmethod
    def update(
        conn: sqlite3.Connection,
        turno_id: int,
        turno_data: dict
    ):
        turno = TurnoModel.get_by_id(conn, turno_id)

        if not turno:
            raise HTTPException(
                status_code=404,
                detail="Turno no encontrado."
            )

        try:
            actualizado = TurnoModel.update(
                conn,
                turno_id,
                turno_data
            )

            if not actualizado:
                raise HTTPException(
                    status_code=400,
                    detail="No se pudo reprogramar el turno."
                )

            return {
                "mensaje": "Turno reprogramado correctamente."
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
                detail="No se pudo reprogramar el turno. Verifique los datos ingresados."
            )

    # ==========================================
    # CAMBIAR ESTADO DEL TURNO
    # ==========================================

    @staticmethod
    def cambiar_estado(
        conn: sqlite3.Connection,
        turno_id: int,
        nuevo_estado: str
    ):
        turno = TurnoModel.get_by_id(conn, turno_id)

        if not turno:
            raise HTTPException(
                status_code=404,
                detail="Turno no encontrado."
            )

        try:
            actualizado = TurnoModel.cambiar_estado(
                conn,
                turno_id,
                nuevo_estado
            )

            if not actualizado:
                raise HTTPException(
                    status_code=400,
                    detail="No se pudo cambiar el estado del turno."
                )

            return {
                "mensaje": "Estado del turno actualizado correctamente.",
                "nuevo_estado": nuevo_estado
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
                detail="No se pudo actualizar el estado del turno."
            )

    # ==========================================
    # CANCELAR TURNO
    # ==========================================

    @staticmethod
    def delete(
        conn: sqlite3.Connection,
        turno_id: int
    ):
        turno = TurnoModel.get_by_id(conn, turno_id)

        if not turno:
            raise HTTPException(
                status_code=404,
                detail="Turno no encontrado."
            )

        try:
            cancelado = TurnoModel.delete(conn, turno_id)

            if not cancelado:
                raise HTTPException(
                    status_code=400,
                    detail="No se pudo cancelar el turno."
                )

            return {
                "mensaje": "Turno cancelado correctamente."
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
                detail="No se pudo cancelar el turno."
            )
