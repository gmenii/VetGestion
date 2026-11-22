
from app.database import get_db_connection
from app.models.servicio import ServicioModel


# Obtener conexión a la base de datos
db_generator = get_db_connection()
conn = next(db_generator)


# Datos de un servicio de prueba
servicio = {
    "nombre": "Consulta general",
    "descripcion": "Consulta veterinaria general",
    "precio": 15000,
    "estado": "Activo"
}


# 1. CREAR SERVICIO
servicio_id = ServicioModel.create(conn, servicio)
print("Servicio creado. ID:", servicio_id)


# 2. BUSCAR POR ID
resultado = ServicioModel.get_by_id(conn, servicio_id)
print("\nServicio encontrado:")
print(dict(resultado))


# 3. LISTAR TODOS
servicios = ServicioModel.get_all(conn)

print("\nLista de servicios:")

for s in servicios:
    print(dict(s))


# 4. LISTAR SOLO ACTIVOS
activos = ServicioModel.get_activos(conn)

print("\nServicios activos:")

for s in activos:
    print(dict(s))


# 5. ACTUALIZAR SERVICIO
servicio["precio"] = 18000
servicio["estado"] = "Inactivo"

actualizado = ServicioModel.update(conn, servicio_id, servicio)
print("\nServicio actualizado:", actualizado)


# 6. VOLVER A CONSULTAR ACTIVOS
activos = ServicioModel.get_activos(conn)

print("\nServicios activos después de desactivar el servicio:")

for s in activos:
    print(dict(s))


# 7. ELIMINAR SERVICIO
eliminado = ServicioModel.delete(conn, servicio_id)
print("\nServicio eliminado:", eliminado)


# Cerrar conexión
db_generator.close()
