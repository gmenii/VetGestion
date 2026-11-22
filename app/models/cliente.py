import sqlite3


class ClienteModel:

    @staticmethod
    def get_all(conn: sqlite3.Connection):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM clientes
            ORDER BY apellido, nombre
        """)

        return cursor.fetchall()

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, cliente_id: int):
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM clientes WHERE id = ?",
            (cliente_id,)
        )

        return cursor.fetchone()

    @staticmethod
    def get_by_dni(conn: sqlite3.Connection, dni: str):
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM clientes WHERE dni = ?",
            (dni,)
        )

        return cursor.fetchone()

    @staticmethod
    def create(conn: sqlite3.Connection, cliente_data: dict):
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO clientes (
                dni, nombre, apellido, email, telefono, direccion, estado
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            cliente_data["dni"],
            cliente_data["nombre"],
            cliente_data["apellido"],
            cliente_data.get("email"),
            cliente_data.get("telefono"),
            cliente_data.get("direccion"),
            cliente_data.get("estado", "Activo")
        ))

        conn.commit()

        return cursor.lastrowid

    @staticmethod
    def update(conn: sqlite3.Connection, cliente_id: int, cliente_data: dict):
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE clientes
            SET dni = ?, nombre = ?, apellido = ?,
                email = ?, telefono = ?, direccion = ?, estado = ?
            WHERE id = ?
        """, (
            cliente_data["dni"],
            cliente_data["nombre"],
            cliente_data["apellido"],
            cliente_data.get("email"),
            cliente_data.get("telefono"),
            cliente_data.get("direccion"),
            cliente_data.get("estado", "Activo"),
            cliente_id
        ))

        conn.commit()

        return cursor.rowcount > 0

    @staticmethod
    def delete(conn: sqlite3.Connection, cliente_id: int):
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM clientes WHERE id = ?",
            (cliente_id,)
        )

        conn.commit()

        return cursor.rowcount > 0
