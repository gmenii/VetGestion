
import sqlite3
from datetime import datetime


class TurnoModel:

    # ==========================================
    # CONSULTAS
    # ==========================================

    @staticmethod
    def get_all(conn: sqlite3.Connection):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                turnos.*,
                mascotas.nombre AS nombre_mascota,
                profesionales.nombre AS nombre_profesional,
                profesionales.apellido AS apellido_profesional,
                servicios.nombre AS nombre_servicio
            FROM turnos
            INNER JOIN mascotas
                ON turnos.mascota_id = mascotas.id
            INNER JOIN profesionales
                ON turnos.profesional_id = profesionales.id
            INNER JOIN servicios
                ON turnos.servicio_id = servicios.id
            ORDER BY turnos.fecha, turnos.hora
        """)

        return cursor.fetchall()

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, turno_id: int):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                turnos.*,
                mascotas.nombre AS nombre_mascota,
                profesionales.nombre AS nombre_profesional,
                profesionales.apellido AS apellido_profesional,
                servicios.nombre AS nombre_servicio
            FROM turnos
            INNER JOIN mascotas
                ON turnos.mascota_id = mascotas.id
            INNER JOIN profesionales
                ON turnos.profesional_id = profesionales.id
            INNER JOIN servicios
                ON turnos.servicio_id = servicios.id
            WHERE turnos.id = ?
        """, (turno_id,))

        return cursor.fetchone()

    # ==========================================
    # VALIDACIONES
    # ==========================================

    @staticmethod
    def mascota_existe(conn: sqlite3.Connection, mascota_id: int):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id FROM mascotas
            WHERE id = ?
        """, (mascota_id,))

        return cursor.fetchone() is not None

    @staticmethod
    def profesional_activo(conn: sqlite3.Connection, profesional_id: int):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id FROM profesionales
            WHERE id = ? AND estado = 'Activo'
        """, (profesional_id,))

        return cursor.fetchone() is not None

    @staticmethod
    def servicio_activo(conn: sqlite3.Connection, servicio_id: int):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id FROM servicios
            WHERE id = ? AND estado = 'Activo'
        """, (servicio_id,))

        return cursor.fetchone() is not None

    @staticmethod
    def validar_horario(fecha: str, hora: str):
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
            hora_obj = datetime.strptime(hora, "%H:%M")
        except ValueError:
            return False

        dia_semana = fecha_obj.weekday()
        minutos = hora_obj.hour * 60 + hora_obj.minute

        # Domingo: cerrado
        if dia_semana == 6:
            return False

        # Los turnos comienzan cada 30 minutos
        if hora_obj.minute not in (0, 30):
            return False

        # Lunes a viernes: 10:00 a 18:00
        if dia_semana <= 4:
            return 600 <= minutos <= 1050

        # Sábados: 10:00 a 14:00
        if dia_semana == 5:
            return 600 <= minutos <= 810

        return False

    @staticmethod
    def disponibilidad(
        conn: sqlite3.Connection,
        mascota_id: int,
        profesional_id: int,
        fecha: str,
        hora: str,
        turno_id: int = None
    ):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM turnos
            WHERE fecha = ?
              AND hora = ?
              AND estado IN ('Confirmado', 'En curso')
              AND (
                    mascota_id = ?
                    OR profesional_id = ?
                  )
              AND id != ?
        """, (
            fecha,
            hora,
            mascota_id,
            profesional_id,
            turno_id if turno_id is not None else -1
        ))

        return cursor.fetchone() is None

    # ==========================================
    # CREAR TURNO
    # ==========================================

    @staticmethod
    def create(conn: sqlite3.Connection, turno_data: dict):
        cursor = conn.cursor()

        try:
            mascota_id = turno_data["mascota_id"]
            profesional_id = turno_data["profesional_id"]
            servicio_id = turno_data["servicio_id"]
            fecha = turno_data["fecha"]
            hora = turno_data["hora"]

            if not TurnoModel.mascota_existe(conn, mascota_id):
                raise ValueError("La mascota no existe.")

            if not TurnoModel.profesional_activo(conn, profesional_id):
                raise ValueError("El profesional no existe o está inactivo.")

            if not TurnoModel.servicio_activo(conn, servicio_id):
                raise ValueError("El servicio no existe o está inactivo.")

            if not TurnoModel.validar_horario(fecha, hora):
                raise ValueError("El día o el horario no están habilitados.")

            if not TurnoModel.disponibilidad(
                conn, mascota_id, profesional_id, fecha, hora
            ):
                raise ValueError(
                    "La mascota o el profesional ya tienen un turno en ese horario."
                )

            cursor.execute("""
                INSERT INTO turnos (
                    mascota_id, profesional_id, servicio_id,
                    fecha, hora, estado, motivo
                )
                VALUES (?, ?, ?, ?, ?, 'Confirmado', ?)
            """, (
                mascota_id,
                profesional_id,
                servicio_id,
                fecha,
                hora,
                turno_data.get("motivo")
            ))

            conn.commit()
            return cursor.lastrowid

        except Exception:
            conn.rollback()
            raise

    # ==========================================
    # REPROGRAMAR / MODIFICAR TURNO
    # ==========================================

    @staticmethod
    def update(
        conn: sqlite3.Connection,
        turno_id: int,
        turno_data: dict
    ):
        cursor = conn.cursor()

        try:
            turno_actual = TurnoModel.get_by_id(conn, turno_id)

            if turno_actual is None:
                raise ValueError("El turno no existe.")

            if turno_actual["estado"] != "Confirmado":
                raise ValueError(
                    "Solo se pueden modificar turnos confirmados."
                )

            mascota_id = turno_data["mascota_id"]
            profesional_id = turno_data["profesional_id"]
            servicio_id = turno_data["servicio_id"]
            fecha = turno_data["fecha"]
            hora = turno_data["hora"]

            if not TurnoModel.mascota_existe(conn, mascota_id):
                raise ValueError("La mascota no existe.")

            if not TurnoModel.profesional_activo(conn, profesional_id):
                raise ValueError("El profesional no existe o está inactivo.")

            if not TurnoModel.servicio_activo(conn, servicio_id):
                raise ValueError("El servicio no existe o está inactivo.")

            if not TurnoModel.validar_horario(fecha, hora):
                raise ValueError("El día o el horario no están habilitados.")

            if not TurnoModel.disponibilidad(
                conn,
                mascota_id,
                profesional_id,
                fecha,
                hora,
                turno_id
            ):
                raise ValueError(
                    "La mascota o el profesional ya tienen un turno en ese horario."
                )

            cursor.execute("""
                UPDATE turnos
                SET mascota_id = ?,
                    profesional_id = ?,
                    servicio_id = ?,
                    fecha = ?,
                    hora = ?,
                    motivo = ?
                WHERE id = ?
            """, (
                mascota_id,
                profesional_id,
                servicio_id,
                fecha,
                hora,
                turno_data.get("motivo"),
                turno_id
            ))

            conn.commit()
            return cursor.rowcount > 0

        except Exception:
            conn.rollback()
            raise

    # ==========================================
    # CAMBIAR ESTADO
    # ==========================================

    @staticmethod
    def cambiar_estado(
        conn: sqlite3.Connection,
        turno_id: int,
        nuevo_estado: str
    ):
        cursor = conn.cursor()

        estados_validos = {
            "Confirmado",
            "En curso",
            "Completado",
            "Cancelado"
        }

        if nuevo_estado not in estados_validos:
            raise ValueError("El estado indicado no es válido.")

        try:
            turno = TurnoModel.get_by_id(conn, turno_id)

            if turno is None:
                raise ValueError("El turno no existe.")

            estado_actual = turno["estado"]

            transiciones = {
                "Confirmado": ["En curso", "Cancelado"],
                "En curso": ["Completado", "Cancelado"],
                "Completado": [],
                "Cancelado": []
            }

            if nuevo_estado not in transiciones[estado_actual]:
                raise ValueError(
                    f"No se puede cambiar de {estado_actual} a {nuevo_estado}."
                )

            cursor.execute("""
                UPDATE turnos
                SET estado = ?
                WHERE id = ?
            """, (nuevo_estado, turno_id))

            conn.commit()
            return cursor.rowcount > 0

        except Exception:
            conn.rollback()
            raise

    # ==========================================
    # CANCELAR TURNO
    # ==========================================

    @staticmethod
    def delete(conn: sqlite3.Connection, turno_id: int):
        # No eliminamos físicamente el turno:
        # lo marcamos como cancelado para conservar su historial.
        return TurnoModel.cambiar_estado(
            conn,
            turno_id,
            "Cancelado"
        )
