
import time

from app.database import get_db_connection
from app.models.cliente import ClienteModel
from app.models.mascota import MascotaModel
from app.models.profesional import ProfesionalModel
from app.models.servicio import ServicioModel
from app.models.turno import TurnoModel


db_generator = get_db_connection()
conn = next(db_generator)

# IDs para poder limpiar los datos de prueba al terminar
cliente_id = None
mascota_id = None
profesional_id = None
servicio_id = None
turno_id = None
turno_cancelado_id = None

try:
    # ==========================================
    # 1. CREAR DATOS NECESARIOS
    # ==========================================

    identificador = str(int(time.time()))

    cliente = {
        "dni": identificador[-8:],
        "nombre": "Maria",
        "apellido": "Lopez",
        "email": "maria@gmail.com",
        "telefono": "1122334455",
        "direccion": "San Justo"
    }

    cliente_id = ClienteModel.create(conn, cliente)

    mascota = {
        "cliente_id": cliente_id,
        "nombre": "Toby",
        "especie": "Perro",
        "raza": "Golden Retriever",
        "fecha_nacimiento": "2022-05-10",
        "sexo": "Macho",
        "observaciones": "Muy juguetón"
    }

    mascota_id = MascotaModel.create(conn, mascota)

    profesional = {
        "matricula": "TEST" + identificador,
        "nombre": "Carlos",
        "apellido": "Rodriguez",
        "email": "carlos@gmail.com",
        "estado": "Activo"
    }

    profesional_id = ProfesionalModel.create(conn, profesional)

    servicio = {
        "nombre": "Consulta de prueba " + identificador,
        "descripcion": "Consulta veterinaria general",
        "precio": 15000,
        "estado": "Activo"
    }

    servicio_id = ServicioModel.create(conn, servicio)

    print("Datos de prueba creados correctamente.")

    # ==========================================
    # 2. CREAR UN TURNO
    # ==========================================

    turno = {
        "mascota_id": mascota_id,
        "profesional_id": profesional_id,
        "servicio_id": servicio_id,
        "fecha": "2026-11-17",
        "hora": "10:00",
        "motivo": "Control general"
    }

    turno_id = TurnoModel.create(conn, turno)

    print("\nTurno creado. ID:", turno_id)

    # ==========================================
    # 3. BUSCAR TURNO POR ID
    # ==========================================

    resultado = TurnoModel.get_by_id(conn, turno_id)

    print("\nTurno encontrado:")
    print(dict(resultado))

    # ==========================================
    # 4. LISTAR TODOS LOS TURNOS
    # ==========================================

    turnos = TurnoModel.get_all(conn)

    print("\nLista de turnos:")

    for t in turnos:
        print(dict(t))

    # ==========================================
    # 5. PROBAR DISPONIBILIDAD
    # ==========================================

    try:
        TurnoModel.create(conn, turno)

    except ValueError as error:
        print("\nConflicto detectado correctamente:")
        print(error)

    # ==========================================
    # 6. PROBAR HORARIO NO HABILITADO
    # ==========================================

    turno_domingo = {
        "mascota_id": mascota_id,
        "profesional_id": profesional_id,
        "servicio_id": servicio_id,
        "fecha": "2026-11-22",
        "hora": "10:00",
        "motivo": "Prueba de domingo"
    }

    try:
        TurnoModel.create(conn, turno_domingo)

    except ValueError as error:
        print("\nHorario no habilitado detectado:")
        print(error)

    # ==========================================
    # 7. REPROGRAMAR TURNO
    # ==========================================

    turno["hora"] = "10:30"

    actualizado = TurnoModel.update(
        conn,
        turno_id,
        turno
    )

    print("\nTurno reprogramado:", actualizado)

    # ==========================================
    # 8. CAMBIAR ESTADO A EN CURSO
    # ==========================================

    en_curso = TurnoModel.cambiar_estado(
        conn,
        turno_id,
        "En curso"
    )

    print("Turno en curso:", en_curso)

    # ==========================================
    # 9. COMPLETAR TURNO
    # ==========================================

    completado = TurnoModel.cambiar_estado(
        conn,
        turno_id,
        "Completado"
    )

    print("Turno completado:", completado)

    # ==========================================
    # 10. PROBAR CANCELACIÓN
    # ==========================================

    otro_turno = {
        "mascota_id": mascota_id,
        "profesional_id": profesional_id,
        "servicio_id": servicio_id,
        "fecha": "2026-11-17",
        "hora": "11:00",
        "motivo": "Prueba de cancelación"
    }

    turno_cancelado_id = TurnoModel.create(conn, otro_turno)

    cancelado = TurnoModel.delete(conn, turno_cancelado_id)

    print("\nTurno cancelado:", cancelado)

    resultado_cancelacion = TurnoModel.get_by_id(
        conn,
        turno_cancelado_id
    )

    print("Estado del turno:", resultado_cancelacion["estado"])


finally:
    # ==========================================
    # LIMPIAR DATOS DE PRUEBA
    # ==========================================

    if turno_id is not None:
        conn.execute(
            "DELETE FROM turnos WHERE id = ?",
            (turno_id,)
        )

    if turno_cancelado_id is not None:
        conn.execute(
            "DELETE FROM turnos WHERE id = ?",
            (turno_cancelado_id,)
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
