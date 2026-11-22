
from app.database import get_db_connection
from app.models.producto import ProductoModel


db_generator = get_db_connection()
conn = next(db_generator)

producto_id = None
vacuna_id = None

try:
    # ==========================================
    # 1. CREAR MEDICAMENTO
    # ==========================================

    medicamento = {
        "nombre": "Antiparasitario",
        "categoria": "Medicamentos",
        "descripcion": "Antiparasitario para perros y gatos",
        "precio": 8500,
        "stock": 10,
        "stock_minimo": 5,
        "estado": "Activo"
    }

    producto_id = ProductoModel.create(conn, medicamento)

    print("Medicamento creado. ID:", producto_id)

    # ==========================================
    # 2. CREAR VACUNA
    # ==========================================

    vacuna = {
        "nombre": "Vacuna antirrábica",
        "categoria": "Vacunas",
        "descripcion": "Vacuna antirrábica veterinaria",
        "precio": 12000,
        "stock": 3,
        "stock_minimo": 5,
        "estado": "Activo"
    }

    vacuna_id = ProductoModel.create(conn, vacuna)

    print("Vacuna creada. ID:", vacuna_id)

    # ==========================================
    # 3. BUSCAR POR ID
    # ==========================================

    resultado = ProductoModel.get_by_id(conn, producto_id)

    print("\nProducto encontrado:")
    print(dict(resultado))

    # ==========================================
    # 4. LISTAR TODOS LOS PRODUCTOS
    # ==========================================

    productos = ProductoModel.get_all(conn)

    print("\nLista de productos:")

    for p in productos:
        print(dict(p))

    # ==========================================
    # 5. LISTAR PRODUCTOS ACTIVOS
    # ==========================================

    activos = ProductoModel.get_activos(conn)

    print("\nProductos activos:")

    for p in activos:
        print(dict(p))

    # ==========================================
    # 6. BUSCAR POR CATEGORIA
    # ==========================================

    medicamentos = ProductoModel.get_by_categoria(
        conn,
        "Medicamentos"
    )

    print("\nProductos de la categoria Medicamentos:")

    for p in medicamentos:
        print(dict(p))

    # ==========================================
    # 7. DETECTAR STOCK BAJO
    # ==========================================

    stock_bajo = ProductoModel.get_stock_bajo(conn)

    print("\nProductos con stock bajo:")

    for p in stock_bajo:
        print(dict(p))

    # ==========================================
    # 8. ACTUALIZAR PRODUCTO
    # ==========================================

    medicamento["precio"] = 9500
    medicamento["stock"] = 10

    actualizado = ProductoModel.update(
        conn,
        producto_id,
        medicamento
    )

    print("\nProducto actualizado:", actualizado)

    # ==========================================
    # 9. AUMENTAR STOCK
    # ==========================================

    stock_actualizado = ProductoModel.actualizar_stock(
        conn,
        producto_id,
        5
    )

    print("Aumento de stock realizado:", stock_actualizado)

    resultado = ProductoModel.get_by_id(conn, producto_id)

    print("Stock actual:", resultado["stock"])

    # ==========================================
    # 10. DISMINUIR STOCK
    # ==========================================

    stock_actualizado = ProductoModel.actualizar_stock(
        conn,
        producto_id,
        -3
    )

    print("\nDisminucion de stock realizada:", stock_actualizado)

    resultado = ProductoModel.get_by_id(conn, producto_id)

    print("Stock actual:", resultado["stock"])

    # ==========================================
    # 11. INTENTAR GENERAR STOCK NEGATIVO
    # ==========================================

    stock_actualizado = ProductoModel.actualizar_stock(
        conn,
        producto_id,
        -100
    )

    print("\nIntento de generar stock negativo:", stock_actualizado)

    resultado = ProductoModel.get_by_id(conn, producto_id)

    print("Stock final:", resultado["stock"])

finally:
    # ==========================================
    # LIMPIAR DATOS DE PRUEBA
    # ==========================================

    if producto_id is not None:
        ProductoModel.delete(conn, producto_id)

    if vacuna_id is not None:
        ProductoModel.delete(conn, vacuna_id)

    db_generator.close()

    print("\nDatos de prueba eliminados.")
