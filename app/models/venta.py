
import sqlite3
from datetime import datetime


class VentaModel:

    # ==========================================
    # CONSULTAS
    # ==========================================

    @staticmethod
    def get_all(conn: sqlite3.Connection):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                ventas.*,
                clientes.nombre AS nombre_cliente,
                clientes.apellido AS apellido_cliente
            FROM ventas
            INNER JOIN clientes
                ON ventas.cliente_id = clientes.id
            ORDER BY ventas.fecha DESC, ventas.id DESC
        """)

        return cursor.fetchall()

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, venta_id: int):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                ventas.*,
                clientes.nombre AS nombre_cliente,
                clientes.apellido AS apellido_cliente
            FROM ventas
            INNER JOIN clientes
                ON ventas.cliente_id = clientes.id
            WHERE ventas.id = ?
        """, (venta_id,))

        return cursor.fetchone()

    @staticmethod
    def get_by_cliente(conn: sqlite3.Connection, cliente_id: int):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM ventas
            WHERE cliente_id = ?
            ORDER BY fecha DESC
        """, (cliente_id,))

        return cursor.fetchall()

    @staticmethod
    def get_detalles(conn: sqlite3.Connection, venta_id: int):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                detalle_ventas.*,
                COALESCE(productos.nombre, servicios.nombre) AS concepto,
                CASE
                    WHEN detalle_ventas.producto_id IS NOT NULL
                    THEN 'Producto'
                    ELSE 'Servicio'
                END AS tipo
            FROM detalle_ventas
            LEFT JOIN productos
                ON detalle_ventas.producto_id = productos.id
            LEFT JOIN servicios
                ON detalle_ventas.servicio_id = servicios.id
            WHERE detalle_ventas.venta_id = ?
            ORDER BY detalle_ventas.id
        """, (venta_id,))

        return cursor.fetchall()

    # ==========================================
    # CREAR VENTA CON TRANSACCION
    # ==========================================

    @staticmethod
    def create_transaction(
        conn: sqlite3.Connection,
        cliente_id: int,
        items: list,
        fecha: str = None
    ):
        cursor = conn.cursor()

        try:
            # Iniciamos una transaccion
            cursor.execute("BEGIN")

            # ----------------------------------
            # VALIDAR CLIENTE
            # ----------------------------------

            cursor.execute("""
                SELECT id, estado
                FROM clientes
                WHERE id = ?
            """, (cliente_id,))

            cliente = cursor.fetchone()

            if not cliente:
                raise ValueError("El cliente no existe.")

            if cliente["estado"] != "Activo":
                raise ValueError(
                    "No se puede registrar una venta: el cliente está inactivo."
                )

            # ----------------------------------
            # VALIDAR LISTA DE ITEMS
            # ----------------------------------

            if not isinstance(items, list) or len(items) == 0:
                raise ValueError("La venta debe contener al menos un item.")

            # ----------------------------------
            # CREAR CABECERA DE VENTA
            # ----------------------------------

            if fecha is None:
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
                INSERT INTO ventas (cliente_id, fecha, total)
                VALUES (?, ?, 0)
            """, (cliente_id, fecha))

            venta_id = cursor.lastrowid

            total_venta = 0

            # ----------------------------------
            # PROCESAR CADA ITEM
            # ----------------------------------

            for item in items:

                producto_id = item.get("producto_id")
                servicio_id = item.get("servicio_id")
                cantidad = item.get("cantidad")

                # Debe ser un entero positivo
                if (
                    not isinstance(cantidad, int)
                    or isinstance(cantidad, bool)
                    or cantidad <= 0
                ):
                    raise ValueError(
                        "La cantidad debe ser un numero entero mayor a cero."
                    )

                # Debe ser producto o servicio, no ambos
                if (producto_id is None) == (servicio_id is None):
                    raise ValueError(
                        "Cada item debe corresponder a un producto o servicio."
                    )

                # ----------------------------------
                # SI ES UN PRODUCTO
                # ----------------------------------

                if producto_id is not None:

                    cursor.execute("""
                        SELECT id, nombre, precio, stock
                        FROM productos
                        WHERE id = ?
                          AND estado = 'Activo'
                    """, (producto_id,))

                    producto = cursor.fetchone()

                    if not producto:
                        raise ValueError(
                            f"El producto con ID {producto_id} no existe o esta inactivo."
                        )

                    if producto["stock"] < cantidad:
                        raise ValueError(
                            f"Stock insuficiente para {producto['nombre']}."
                        )

                    precio_unitario = producto["precio"]

                    # Descontar stock
                    cursor.execute("""
                        UPDATE productos
                        SET stock = stock - ?
                        WHERE id = ?
                          AND stock >= ?
                    """, (
                        cantidad,
                        producto_id,
                        cantidad
                    ))

                    if cursor.rowcount == 0:
                        raise ValueError(
                            "No se pudo actualizar el stock del producto."
                        )

                # ----------------------------------
                # SI ES UN SERVICIO
                # ----------------------------------

                else:

                    cursor.execute("""
                        SELECT id, nombre, precio
                        FROM servicios
                        WHERE id = ?
                          AND estado = 'Activo'
                    """, (servicio_id,))

                    servicio = cursor.fetchone()

                    if not servicio:
                        raise ValueError(
                            f"El servicio con ID {servicio_id} no existe o esta inactivo."
                        )

                    precio_unitario = servicio["precio"]

                # ----------------------------------
                # CALCULAR SUBTOTAL
                # ----------------------------------

                subtotal = precio_unitario * cantidad

                total_venta += subtotal

                # ----------------------------------
                # GUARDAR DETALLE
                # ----------------------------------

                cursor.execute("""
                    INSERT INTO detalle_ventas (
                        venta_id,
                        producto_id,
                        servicio_id,
                        cantidad,
                        precio_unitario,
                        subtotal
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    venta_id,
                    producto_id,
                    servicio_id,
                    cantidad,
                    precio_unitario,
                    subtotal
                ))

            # ----------------------------------
            # ACTUALIZAR TOTAL DE LA VENTA
            # ----------------------------------

            cursor.execute("""
                UPDATE ventas
                SET total = ?
                WHERE id = ?
            """, (total_venta, venta_id))

            # Confirmar todos los cambios
            conn.commit()

            return venta_id

        except Exception:
            # Si algo falla, deshacer todos los cambios
            conn.rollback()
            raise
