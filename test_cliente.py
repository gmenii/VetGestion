from app.database import get_db_connection
from app.models.cliente import ClienteModel


# Obtener conexión a la base de datos
db_generator = get_db_connection()
conn = next(db_generator)

# Crear un cliente de prueba
cliente = {
    "dni": "40123456",
    "nombre": "Juan",
    "apellido": "Perez",
    "email": "juan@gmail.com",
    "telefono": "1123456789",
    "direccion": "San Justo"
}

# 1. CREAR
cliente_id = ClienteModel.create(conn, cliente)
print("Cliente creado. ID:", cliente_id)

# 2. BUSCAR POR ID
resultado = ClienteModel.get_by_id(conn, cliente_id)
print("Cliente encontrado:", dict(resultado))

# 3. LISTAR TODOS
clientes = ClienteModel.get_all(conn)
print("Lista de clientes:")
for c in clientes:
    print(dict(c))

# 4. ACTUALIZAR
cliente["telefono"] = "1198765432"
actualizado = ClienteModel.update(conn, cliente_id, cliente)
print("Cliente actualizado:", actualizado)

# 5. ELIMINAR
eliminado = ClienteModel.delete(conn, cliente_id)
print("Cliente eliminado:", eliminado)

db_generator.close()