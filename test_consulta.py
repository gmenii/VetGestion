
from app.database import get_db_connection
from app.models.cliente import ClienteModel
from app.models.mascota import MascotaModel
from app.models.profesional import ProfesionalModel
from app.models.servicio import ServicioModel
from app.models.turno import TurnoModel
from app.models.consulta import ConsultaModel


db_generator = get_db_connection()
conn = next(db_generator)

cliente_id = None
mascota_id = None
profesional_id = None
servicio_id = None
turno_id = None
consulta_id = None

try:
    # ==========================================
    # 1. CREAR DATOS DE PRUEBA
    # ==========================================

    cliente = {
        "dni": "45123456",
        "nombre": "Ana",
        "apellido": "Martinez",
        "email": "ana@gmail.com",
        "telefono": "1122334455",
        "direccion": "San Justo"
    }

    cliente_id = ClienteModel.create(conn, cliente)

    mascota = {
        "cliente_id": cliente_id,
        "nombre": "Luna",
        "especie": "Gato",
        "raza": "Siames",
        "fecha_nacimiento": "2023-04-15",
        "sexo": "Hembra",
        "observaciones": "Tranquila"
    }

    mascota_id = MascotaModel.create(conn, mascota)

    profesional = {
        "matricula": "TEST-CONSULTA-001",
        "nombre": "Martin",
        "apellido": "Garcia",
        "email": "martin@gmail.com",
        "estado": "Activo"
    }

    profesional_id = ProfesionalModel.create(conn, profesional)

    servicio = {
        "nombre": "Consulta clinica de prueba",
        "descripcion": "Consulta veterinaria",
        "precio": 15000,
        "estado": "Activo"
    }

    servicio_id = ServicioModel.create(conn, servicio)

    print("Datos de prueba creados correctamente.")

    # ==========================================
    # 2. CREAR TURNO
    # ==========================================

    turno = {
        "mascota_id": mascota_id,
        "profesional_id": profesional_id,
        "servicio_id": servicio_id,
        "fecha": "2026-11-18",
        "hora": "11:00",
        "motivo": "Revision general"
    }

    turno_id = TurnoModel.create(conn, turno)

    print("\nTurno creado. ID:", turno_id)

    # ==========================================
    # 3. CAMBIAR TURNO A EN CURSO
    # ==========================================

    TurnoModel.cambiar_estado(
        conn,
        turno_id,
        "En curso"
    )

    print("Turno cambiado a En curso.")

    # ==========================================
    # 4. REGISTRAR CONSULTA
    # ==========================================

    consulta = {
        "turno_id": turno_id,
        "fecha": "2026-11-18",
        "diagnostico": "Estado general saludable.",
        "observaciones": "Se recomienda control periódico."
    }

    consulta_id = ConsultaModel.create(conn, consulta)

    print("\nConsulta creada. ID:", consulta_id)

    # ==========================================
    # 5. BUSCAR CONSULTA POR ID
    # ==========================================

    resultado = ConsultaModel.get_by_id(conn, consulta_id)

    print("\nConsulta encontrada:")
    print(dict(resultado))

    # ==========================================
    # 6. LISTAR TODAS LAS CONSULTAS
    # ==========================================

    consultas = ConsultaModel.get_all(conn)

    print("\nLista de consultas:")

    for c in consultas:
        print(dict(c))

    # ==========================================
    # 7. HISTORIA CLINICA DE LA MASCOTA
    # ==========================================

    historial = ConsultaModel.get_by_mascota(
        conn,
        mascota_id
    )

    print("\nHistoria clinica de Luna:")

    for c in historial:
        print(dict(c))

    # ==========================================
    # 8. PROBAR CONSULTA DUPLICADA
    # ==========================================

    try:
        ConsultaModel.create(conn, consulta)

    except ValueError as error:
        print("\nDuplicado detectado correctamente:")
        print(error)

    # ==========================================
    # 9. ACTUALIZAR CONSULTA
    # ==========================================

    consulta["diagnostico"] = "Control realizado. Sin novedades."

    actualizado = ConsultaModel.update(
        conn,
        consulta_id,
        consulta
    )

    print("\nConsulta actualizada:", actualizado)

    # ==========================================
    # 10. PROBAR TURNO QUE NO ESTA EN CURSO
    # ==========================================

    TurnoModel.cambiar_estado(
        conn,
        turno_id,
        "Completado"
    )

    try:
        ConsultaModel.create(conn, consulta)

    except ValueError as error:
        print("\nValidacion de estado correcta:")
        print(error)

finally:
    # ==========================================
    # LIMPIAR DATOS DE PRUEBA
    # ==========================================

    if consulta_id is not None:
        ConsultaModel.delete(conn, consulta_id)

    if turno_id is not None:
        conn.execute(
            "DELETE FROM turnos WHERE id = ?",
            (turno_id,)
        )

    conn.commit()

    if mascota_id is not None:
        MascotaModel.delete(conn, mascota_id)

    if profesional_id is not None:
        ProfesionalModel.delete(conn, profesional_id)

    if servicio_id is not None:
        ServicioModel.delete(conn, servicio_id)

    if cliente_id is not None:
        ClienteModel.delete(conn, cliente_id)

    db_generator.close()

    print("\nDatos de prueba eliminados.")
