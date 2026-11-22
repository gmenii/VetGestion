
import sqlite3


class ServicioModel:

    @staticmethod
    def get_all(conn: sqlite3.Connection):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM servicios
            ORDER BY nombre
        """)

        return cursor.fetchall()

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, servicio_id: int):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM servicios
            WHERE id = ?
        """, (servicio_id,))

        return cursor.fetchone()

    @staticmethod
    def get_activos(conn: sqlite3.Connection):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM servicios
            WHERE estado = 'Activo'
            ORDER BY nombre
        """)

        return cursor.fetchall()

    @staticmethod
    def buscar_por_nombre(conn: sqlite3.Connection, nombre: str):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM servicios
            WHERE nombre LIKE ? COLLATE NOCASE
              AND estado = 'Activo'
            ORDER BY nombre
        """, (f"%{nombre.strip()}%",))

        return cursor.fetchall()

    @staticmethod
    def create(conn: sqlite3.Connection, servicio_data: dict):
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO servicios (
                nombre, descripcion, precio, estado
            )
            VALUES (?, ?, ?, ?)
        """, (
            servicio_data["nombre"],
            servicio_data.get("descripcion"),
            servicio_data["precio"],
            servicio_data.get("estado", "Activo")
        ))

        conn.commit()

        return cursor.lastrowid

    @staticmethod
    def update(conn: sqlite3.Connection, servicio_id: int, servicio_data: dict):
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE servicios
            SET nombre = ?, descripcion = ?,
                precio = ?, estado = ?
            WHERE id = ?
        """, (
            servicio_data["nombre"],
            servicio_data.get("descripcion"),
            servicio_data["precio"],
            servicio_data.get("estado", "Activo"),
            servicio_id
        ))

        conn.commit()

        return cursor.rowcount > 0

    @staticmethod
    def delete(conn: sqlite3.Connection, servicio_id: int):
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM servicios
            WHERE id = ?
        """, (servicio_id,))

        conn.commit()

        return cursor.rowcount > 0
