
import sqlite3


class MascotaModel:

    @staticmethod
    def get_all(conn: sqlite3.Connection):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                mascotas.*,
                clientes.nombre AS nombre_cliente,
                clientes.apellido AS apellido_cliente
            FROM mascotas
            INNER JOIN clientes
                ON mascotas.cliente_id = clientes.id
            ORDER BY mascotas.nombre
        """)

        return cursor.fetchall()

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, mascota_id: int):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                mascotas.*,
                clientes.nombre AS nombre_cliente,
                clientes.apellido AS apellido_cliente
            FROM mascotas
            INNER JOIN clientes
                ON mascotas.cliente_id = clientes.id
            WHERE mascotas.id = ?
        """, (mascota_id,))

        return cursor.fetchone()

    @staticmethod
    def create(conn: sqlite3.Connection, mascota_data: dict):
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO mascotas (
                cliente_id, nombre, especie, raza,
                fecha_nacimiento, sexo, observaciones
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            mascota_data["cliente_id"],
            mascota_data["nombre"],
            mascota_data["especie"],
            mascota_data.get("raza"),
            mascota_data.get("fecha_nacimiento"),
            mascota_data.get("sexo"),
            mascota_data.get("observaciones")
        ))

        conn.commit()

        return cursor.lastrowid

    @staticmethod
    def update(conn: sqlite3.Connection, mascota_id: int, mascota_data: dict):
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE mascotas
            SET cliente_id = ?, nombre = ?, especie = ?,
                raza = ?, fecha_nacimiento = ?, sexo = ?,
                observaciones = ?
            WHERE id = ?
        """, (
            mascota_data["cliente_id"],
            mascota_data["nombre"],
            mascota_data["especie"],
            mascota_data.get("raza"),
            mascota_data.get("fecha_nacimiento"),
            mascota_data.get("sexo"),
            mascota_data.get("observaciones"),
            mascota_id
        ))

        conn.commit()

        return cursor.rowcount > 0

    @staticmethod
    def delete(conn: sqlite3.Connection, mascota_id: int):
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM mascotas WHERE id = ?",
            (mascota_id,)
        )

        conn.commit()

        return cursor.rowcount > 0
