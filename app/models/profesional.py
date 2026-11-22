
import sqlite3


class ProfesionalModel:

    @staticmethod
    def get_all(conn: sqlite3.Connection):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM profesionales
            ORDER BY apellido, nombre
        """)

        return cursor.fetchall()

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, profesional_id: int):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM profesionales
            WHERE id = ?
        """, (profesional_id,))

        return cursor.fetchone()

    @staticmethod
    def get_activos(conn: sqlite3.Connection):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM profesionales
            WHERE estado = 'Activo'
            ORDER BY apellido, nombre
        """)

        return cursor.fetchall()

    @staticmethod
    def create(conn: sqlite3.Connection, profesional_data: dict):
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO profesionales (
                matricula, nombre, apellido, email, estado
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            profesional_data["matricula"],
            profesional_data["nombre"],
            profesional_data["apellido"],
            profesional_data.get("email"),
            profesional_data.get("estado", "Activo")
        ))

        conn.commit()

        return cursor.lastrowid

    @staticmethod
    def update(conn: sqlite3.Connection, profesional_id: int, profesional_data: dict):
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE profesionales
            SET matricula = ?, nombre = ?, apellido = ?,
                email = ?, estado = ?
            WHERE id = ?
        """, (
            profesional_data["matricula"],
            profesional_data["nombre"],
            profesional_data["apellido"],
            profesional_data.get("email"),
            profesional_data.get("estado", "Activo"),
            profesional_id
        ))

        conn.commit()

        return cursor.rowcount > 0

    @staticmethod
    def delete(conn: sqlite3.Connection, profesional_id: int):
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM profesionales
            WHERE id = ?
        """, (profesional_id,))

        conn.commit()

        return cursor.rowcount > 0
