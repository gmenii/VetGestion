
import sqlite3


class ConsultaModel:

    # ==========================================
    # CONSULTAS
    # ==========================================

    @staticmethod
    def get_all(conn: sqlite3.Connection):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                consultas.*,
                mascotas.nombre AS nombre_mascota,
                clientes.nombre AS nombre_cliente,
                clientes.apellido AS apellido_cliente,
                profesionales.nombre AS nombre_profesional,
                profesionales.apellido AS apellido_profesional
            FROM consultas
            INNER JOIN turnos
                ON consultas.turno_id = turnos.id
            INNER JOIN mascotas
                ON turnos.mascota_id = mascotas.id
            INNER JOIN clientes
                ON mascotas.cliente_id = clientes.id
            INNER JOIN profesionales
                ON turnos.profesional_id = profesionales.id
            ORDER BY consultas.fecha DESC
        """)

        return cursor.fetchall()

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, consulta_id: int):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                consultas.*,
                mascotas.nombre AS nombre_mascota,
                clientes.nombre AS nombre_cliente,
                clientes.apellido AS apellido_cliente,
                profesionales.nombre AS nombre_profesional,
                profesionales.apellido AS apellido_profesional
            FROM consultas
            INNER JOIN turnos
                ON consultas.turno_id = turnos.id
            INNER JOIN mascotas
                ON turnos.mascota_id = mascotas.id
            INNER JOIN clientes
                ON mascotas.cliente_id = clientes.id
            INNER JOIN profesionales
                ON turnos.profesional_id = profesionales.id
            WHERE consultas.id = ?
        """, (consulta_id,))

        return cursor.fetchone()

    @staticmethod
    def get_by_mascota(conn: sqlite3.Connection, mascota_id: int):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                consultas.*,
                turnos.fecha AS fecha_turno,
                turnos.hora AS hora_turno,
                profesionales.nombre AS nombre_profesional,
                profesionales.apellido AS apellido_profesional
            FROM consultas
            INNER JOIN turnos
                ON consultas.turno_id = turnos.id
            INNER JOIN profesionales
                ON turnos.profesional_id = profesionales.id
            WHERE turnos.mascota_id = ?
            ORDER BY consultas.fecha DESC
        """, (mascota_id,))

        return cursor.fetchall()

    # ==========================================
    # VALIDACIONES
    # ==========================================

    @staticmethod
    def turno_en_curso(conn: sqlite3.Connection, turno_id: int):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM turnos
            WHERE id = ? AND estado = 'En curso'
        """, (turno_id,))

        return cursor.fetchone() is not None

    @staticmethod
    def turno_tiene_consulta(conn: sqlite3.Connection, turno_id: int):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM consultas
            WHERE turno_id = ?
        """, (turno_id,))

        return cursor.fetchone() is not None

    # ==========================================
    # CREAR CONSULTA
    # ==========================================

    @staticmethod
    def create(conn: sqlite3.Connection, consulta_data: dict):
        cursor = conn.cursor()

        try:
            turno_id = consulta_data["turno_id"]

            if not ConsultaModel.turno_en_curso(conn, turno_id):
                raise ValueError(
                    "No se puede registrar una consulta: "
                    "el turno no existe o no está en curso."
                )

            if ConsultaModel.turno_tiene_consulta(conn, turno_id):
                raise ValueError(
                    "Este turno ya tiene una consulta registrada."
                )

            cursor.execute("""
                INSERT INTO consultas (
                    turno_id,
                    fecha,
                    diagnostico,
                    observaciones
                )
                VALUES (?, ?, ?, ?)
            """, (
                turno_id,
                consulta_data["fecha"],
                consulta_data["diagnostico"],
                consulta_data.get("observaciones")
            ))

            conn.commit()

            return cursor.lastrowid

        except Exception:
            conn.rollback()
            raise

    # ==========================================
    # ACTUALIZAR CONSULTA
    # ==========================================

    @staticmethod
    def update(
        conn: sqlite3.Connection,
        consulta_id: int,
        consulta_data: dict
    ):
        cursor = conn.cursor()

        try:
            consulta = ConsultaModel.get_by_id(conn, consulta_id)

            if consulta is None:
                raise ValueError("La consulta no existe.")

            cursor.execute("""
                UPDATE consultas
                SET fecha = ?,
                    diagnostico = ?,
                    observaciones = ?
                WHERE id = ?
            """, (
                consulta_data["fecha"],
                consulta_data["diagnostico"],
                consulta_data.get("observaciones"),
                consulta_id
            ))

            conn.commit()

            return cursor.rowcount > 0

        except Exception:
            conn.rollback()
            raise

    # ==========================================
    # ELIMINAR CONSULTA
    # ==========================================

    @staticmethod
    def delete(conn: sqlite3.Connection, consulta_id: int):
        cursor = conn.cursor()

        try:
            cursor.execute("""
                DELETE FROM consultas
                WHERE id = ?
            """, (consulta_id,))

            conn.commit()

            return cursor.rowcount > 0

        except Exception:
            conn.rollback()
            raise
