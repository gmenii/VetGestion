
import sqlite3
from typing import Generator

DB_NAME = "vetgestion.db"


def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")

    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        # Creación de tablas
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dni TEXT NOT NULL UNIQUE,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        email TEXT,
        telefono TEXT,
        direccion TEXT,
        estado TEXT NOT NULL DEFAULT 'Activo'
            CHECK (estado IN ('Activo', 'Inactivo'))
    )
""")

        cursor.execute("""
    CREATE TABLE IF NOT EXISTS mascotas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        nombre TEXT NOT NULL,
        especie TEXT NOT NULL CHECK (especie IN ('Perro', 'Gato')),
        raza TEXT,
        fecha_nacimiento TEXT,
        sexo TEXT CHECK (sexo IN ('Hembra', 'Macho')),
        observaciones TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            ON DELETE RESTRICT
    )
""")

        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profesionales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricula TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                email TEXT,
                estado TEXT NOT NULL DEFAULT 'Activo'
                    CHECK (estado IN ('Activo', 'Inactivo'))
            )
""")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS servicios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio REAL NOT NULL CHECK (precio >= 0),
                estado TEXT NOT NULL DEFAULT 'Activo'
                    CHECK (estado IN ('Activo', 'Inactivo'))
            )
        """)


        cursor.execute("""
            CREATE TABLE IF NOT EXISTS turnos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mascota_id INTEGER NOT NULL,
                profesional_id INTEGER NOT NULL,
                servicio_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                estado TEXT NOT NULL DEFAULT 'Confirmado'
                    CHECK (estado IN ('Confirmado', 'En curso', 'Completado', 'Cancelado')),
                motivo TEXT,
                FOREIGN KEY (mascota_id) REFERENCES mascotas(id)
                    ON DELETE RESTRICT,
                FOREIGN KEY (profesional_id) REFERENCES profesionales(id)
                    ON DELETE RESTRICT,
                FOREIGN KEY (servicio_id) REFERENCES servicios(id)
                    ON DELETE RESTRICT,
                CHECK (strftime('%H:%M', hora) = hora)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                turno_id INTEGER NOT NULL UNIQUE,
                fecha TEXT NOT NULL,
                diagnostico TEXT NOT NULL,
                observaciones TEXT,
                FOREIGN KEY (turno_id) REFERENCES turnos(id)
                    ON DELETE RESTRICT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria TEXT,
                descripcion TEXT,
                precio REAL NOT NULL CHECK (precio >= 0),
                stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
                stock_minimo INTEGER NOT NULL DEFAULT 5 CHECK (stock_minimo >= 0),
                estado TEXT NOT NULL DEFAULT 'Activo'
                    CHECK (estado IN ('Activo', 'Inactivo'))
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                total REAL NOT NULL DEFAULT 0 CHECK (total >= 0),
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
                    ON DELETE RESTRICT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detalle_ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id INTEGER NOT NULL,
                producto_id INTEGER,
                servicio_id INTEGER,
                cantidad INTEGER NOT NULL CHECK (cantidad > 0),
                precio_unitario REAL NOT NULL CHECK (precio_unitario >= 0),
                subtotal REAL NOT NULL CHECK (subtotal >= 0),

                FOREIGN KEY (venta_id) REFERENCES ventas(id)
                    ON DELETE RESTRICT,
                FOREIGN KEY (producto_id) REFERENCES productos(id)
                    ON DELETE RESTRICT,
                FOREIGN KEY (servicio_id) REFERENCES servicios(id)
                    ON DELETE RESTRICT,

                CHECK (
                    (producto_id IS NOT NULL AND servicio_id IS NULL)
                    OR
                    (producto_id IS NULL AND servicio_id IS NOT NULL)
                )
            )
        """)
        # Migración segura para bases de datos creadas antes de agregar
        # el estado de los clientes. Los registros existentes quedan Activos.
        columnas_clientes = [
            fila[1] for fila in cursor.execute("PRAGMA table_info(clientes)").fetchall()
        ]

        if "estado" not in columnas_clientes:
            cursor.execute("""
                ALTER TABLE clientes
                ADD COLUMN estado TEXT NOT NULL DEFAULT 'Activo'
                CHECK (estado IN ('Activo', 'Inactivo'))
            """)

        conn.commit()

