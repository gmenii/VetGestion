
from app.database import get_db_connection
from app.models.venta import VentaModel
from app.models.cliente import ClienteModel
from app.models.producto import ProductoModel
from app.models.servicio import ServicioModel


db_generator = get_db_connection()
conn = next(db_generator)

cliente_id = None
producto_id = None
vacuna_id = None
servicio_id = None
venta_id = None

try:
    # ==========================================
    # 1. CREAR DATOS DE PRUEBA
    # ==========================================

    cliente_id = ClienteModel.create(conn, {
        "dni": "99999999",
        "nombre": "Laura",
        "apellido": "Prueba",
        "email": "laura.prueba@email.com",
        "telefono": "1111111111",
        "direccion": "Calle de prueba 123"
    })

    producto_id = ProductoModel.create(conn, {
        "nombre": "Antiparasitario prueba",
        "categoria": "Medicamentos",
        "descripcion": "Producto para probar ventas",
        "precio": 5000,
        "stock": 10,
        "stock_minimo": 2,
        "estado": "Activo"
    })

    vacuna_id = ProductoModel.create(conn, {
        "nombre": "Vacuna prueba",
        "categoria": "Vacunas",
        "descripcion": "Vacuna para probar ventas",
        "precio": 8000,
        "stock": 3,
        "stock_minimo": 1,
        "estado": "Activo"
    })

    servicio_id = ServicioModel.create(conn, {
        "nombre": "Consulta veterinaria prueba",
        "descripcion": "Servicio para probar ventas",
        "precio": 15000,
        "estado": "Activo"
    })

    print("Datos de prueba creados correctamente.")

    # ==========================================
    # 2. CREAR VENTA MIXTA
    # ==========================================

    items = [
        {
            "producto_id": producto_id,
            "servicio_id": None,
            "cantidad": 2
        },
        {
            "producto_id": vacuna_id,
            "servicio_id": None,
            "cantidad": 1
        },
        {
            "producto_id": None,
            "servicio_id": servicio_id,
            "cantidad": 1
        }
    ]

    venta_id = VentaModel.create_transaction(
        conn,
        cliente_id,
        items
    )

    print("\nVenta creada. ID:", venta_id)

    # ==========================================
    # 3. CONSULTAR VENTA
    # ==========================================

    venta = VentaModel.get_by_id(conn, venta_id)

    print("\nVenta encontrada:")
    print(dict(venta))

    # ==========================================
    # 4. CONSULTAR TODAS LAS VENTAS
    # ==========================================

    ventas = VentaModel.get_all(conn)

    print("\nLista de ventas:")

    for v in ventas:
        print(dict(v))

    # ==========================================
    # 5. CONSULTAR VENTAS DEL CLIENTE
    # ==========================================

    ventas_cliente = VentaModel.get_by_cliente(
        conn,
        cliente_id
    )

    print("\nVentas del cliente:")

    for v in ventas_cliente:
        print(dict(v))

    # ==========================================
    # 6. CONSULTAR DETALLES DE LA VENTA
    # ==========================================

    detalles = VentaModel.get_detalles(conn, venta_id)

    print("\nDetalles de la venta:")

    for detalle in detalles:
        print(dict(detalle))

    # ==========================================
    # 7. COMPROBAR DESCUENTO DE STOCK
    # ==========================================

    producto = ProductoModel.get_by_id(conn, producto_id)
    vacuna = ProductoModel.get_by_id(conn, vacuna_id)

    print("\nStock del antiparasitario:", producto["stock"])
    print("Stock de la vacuna:", vacuna["stock"])

    # ==========================================
    # 8. COMPROBAR ROLLBACK
    # ==========================================

    print("\nProbando rollback...")

    items_error = [
        {
            "producto_id": producto_id,
            "servicio_id": None,
            "cantidad": 1
        },
        {
            "producto_id": vacuna_id,
            "servicio_id": None,
            "cantidad": 100
        }
    ]

    try:
        VentaModel.create_transaction(
            conn,
            cliente_id,
            items_error
        )

    except ValueError as error:
        print("Venta rechazada:", error)

    # ==========================================
    # 9. VERIFICAR QUE SE DESHICIERON LOS CAMBIOS
    # ==========================================

    producto = ProductoModel.get_by_id(conn, producto_id)
    vacuna = ProductoModel.get_by_id(conn, vacuna_id)

    print("\nStock del antiparasitario después del error:",
          producto["stock"])

    print("Stock de la vacuna después del error:",
          vacuna["stock"])

    ventas_cliente = VentaModel.get_by_cliente(
        conn,
        cliente_id
    )

    print("Cantidad de ventas del cliente:",
          len(ventas_cliente))

finally:
    # ==========================================
    # LIMPIAR DATOS DE PRUEBA
    # ==========================================

    if venta_id is not None:
        conn.execute(
            "DELETE FROM detalle_ventas WHERE venta_id = ?",
            (venta_id,)
        )
        conn.execute(
            "DELETE FROM ventas WHERE id = ?",
            (venta_id,)
        )
        conn.commit()

    if servicio_id is not None:
        ServicioModel.delete(conn, servicio_id)

    if producto_id is not None:
        ProductoModel.delete(conn, producto_id)

    if vacuna_id is not None:
        ProductoModel.delete(conn, vacuna_id)

    if cliente_id is not None:
        ClienteModel.delete(conn, cliente_id)

    db_generator.close()

    print("\nDatos de prueba eliminados.")
