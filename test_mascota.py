
from app.database import get_db_connection
from app.models.cliente import ClienteModel
from app.models.mascota import MascotaModel


# Obtener conexión a la base de datos
db_generator = get_db_connection()
conn = next(db_generator)


# Crear un dueño de prueba
cliente = {
    "dni": "40987654",
    "nombre": "Laura",
    "apellido": "Gomez",
    "email": "laura@gmail.com",
    "telefono": "1122334455",
    "direccion": "San Justo"
}

cliente_id = ClienteModel.create(conn, cliente)
print("Dueño creado. ID:", cliente_id)


# Datos de una mascota de prueba
mascota = {
    "cliente_id": cliente_id,
    "nombre": "Toby",
    "especie": "Perro",
    "raza": "Golden Retriever",
    "fecha_nacimiento": "2022-05-10",
    "sexo": "Macho",
    "observaciones": "Muy juguetón"
}


# 1. CREAR MASCOTA
mascota_id = MascotaModel.create(conn, mascota)
print("\nMascota creada. ID:", mascota_id)


# 2. BUSCAR POR ID
resultado = MascotaModel.get_by_id(conn, mascota_id)
print("\nMascota encontrada:")
print(dict(resultado))


# 3. LISTAR TODAS LAS MASCOTAS
mascotas = MascotaModel.get_all(conn)

print("\nLista de mascotas:")

for m in mascotas:
    print(dict(m))


# 4. ACTUALIZAR MASCOTA
mascota["nombre"] = "Toby actualizado"

actualizado = MascotaModel.update(conn, mascota_id, mascota)
print("\nMascota actualizada:", actualizado)


# 5. ELIMINAR MASCOTA
eliminado = MascotaModel.delete(conn, mascota_id)
print("Mascota eliminada:", eliminado)


# Cerrar conexión
db_generator.close()
