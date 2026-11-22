
from app.database import get_db_connection
from app.models.profesional import ProfesionalModel


# Obtener conexión a la base de datos
db_generator = get_db_connection()
conn = next(db_generator)


# Datos de un veterinario de prueba
profesional = {
    "matricula": "MN-12345",
    "nombre": "Carlos",
    "apellido": "Rodriguez",
    "email": "carlos@gmail.com",
    "estado": "Activo"
}


# 1. CREAR PROFESIONAL
profesional_id = ProfesionalModel.create(conn, profesional)
print("Profesional creado. ID:", profesional_id)


# 2. BUSCAR POR ID
resultado = ProfesionalModel.get_by_id(conn, profesional_id)
print("\nProfesional encontrado:")
print(dict(resultado))


# 3. LISTAR TODOS
profesionales = ProfesionalModel.get_all(conn)

print("\nLista de profesionales:")

for p in profesionales:
    print(dict(p))


# 4. LISTAR SOLO ACTIVOS
activos = ProfesionalModel.get_activos(conn)

print("\nProfesionales activos:")

for p in activos:
    print(dict(p))


# 5. ACTUALIZAR ESTADO
profesional["estado"] = "Inactivo"

actualizado = ProfesionalModel.update(
    conn, profesional_id, profesional
)

print("\nProfesional actualizado:", actualizado)


# 6. VOLVER A CONSULTAR ACTIVOS
activos = ProfesionalModel.get_activos(conn)

print("\nProfesionales activos después de desactivar a Carlos:")

for p in activos:
    print(dict(p))


# 7. ELIMINAR
eliminado = ProfesionalModel.delete(conn, profesional_id)
print("\nProfesional eliminado:", eliminado)


# Cerrar conexión
db_generator.close()
