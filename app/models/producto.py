
import sqlite3


class ProductoModel:

    # ==========================================
    # CONSULTAS
    # ==========================================

    @staticmethod
    def get_all(conn: sqlite3.Connection):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM productos
            ORDER BY categoria, nombre
        """)

        return cursor.fetchall()

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, producto_id: int):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM productos
            WHERE id = ?
        """, (producto_id,))

        return cursor.fetchone()

    @staticmethod
    def get_activos(conn: sqlite3.Connection):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM productos
            WHERE estado = 'Activo'
            ORDER BY nombre
        """)

        return cursor.fetchall()

    @staticmethod
    def buscar_por_nombre(conn: sqlite3.Connection, nombre: str):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM productos
            WHERE nombre LIKE ? COLLATE NOCASE
              AND estado = 'Activo'
            ORDER BY nombre
        """, (f"%{nombre.strip()}%",))

        return cursor.fetchall()

    @staticmethod
    def get_by_categoria(conn: sqlite3.Connection, categoria: str):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM productos
            WHERE categoria = ?
            ORDER BY nombre
        """, (categoria,))

        return cursor.fetchall()

    @staticmethod
    def get_stock_bajo(conn: sqlite3.Connection):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM productos
            WHERE stock <= stock_minimo
              AND estado = 'Activo'
            ORDER BY stock
        """)

        return cursor.fetchall()

    # ==========================================
    # CREAR PRODUCTO
    # ==========================================

    @staticmethod
    def create(conn: sqlite3.Connection, producto_data: dict):
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO productos (
                nombre,
                categoria,
                descripcion,
                precio,
                stock,
                stock_minimo,
                estado
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            producto_data["nombre"],
            producto_data.get("categoria"),
            producto_data.get("descripcion"),
            producto_data["precio"],
            producto_data.get("stock", 0),
            producto_data.get("stock_minimo", 5),
            producto_data.get("estado", "Activo")
        ))

        conn.commit()

        return cursor.lastrowid

    # ==========================================
    # ACTUALIZAR PRODUCTO
    # ==========================================

    @staticmethod
    def update(
        conn: sqlite3.Connection,
        producto_id: int,
        producto_data: dict
    ):
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE productos
            SET nombre = ?,
                categoria = ?,
                descripcion = ?,
                precio = ?,
                stock = ?,
                stock_minimo = ?,
                estado = ?
            WHERE id = ?
        """, (
            producto_data["nombre"],
            producto_data.get("categoria"),
            producto_data.get("descripcion"),
            producto_data["precio"],
            producto_data.get("stock", 0),
            producto_data.get("stock_minimo", 5),
            producto_data.get("estado", "Activo"),
            producto_id
        ))

        conn.commit()

        return cursor.rowcount > 0

    # ==========================================
    # ACTUALIZAR STOCK
    # ==========================================

    @staticmethod
    def actualizar_stock(
        conn: sqlite3.Connection,
        producto_id: int,
        cantidad: int
    ):
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE productos
            SET stock = stock + ?
            WHERE id = ?
              AND stock + ? >= 0
        """, (
            cantidad,
            producto_id,
            cantidad
        ))

        conn.commit()

        return cursor.rowcount > 0

    # ==========================================
    # ELIMINAR PRODUCTO
    # ==========================================

    @staticmethod
    def delete(conn: sqlite3.Connection, producto_id: int):
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM productos
            WHERE id = ?
        """, (producto_id,))

        conn.commit()

        return cursor.rowcount > 0
