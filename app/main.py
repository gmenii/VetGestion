
from fastapi import FastAPI

from app.database import init_db

from app.routes import (
    cliente_routes,
    mascota_routes,
    profesional_routes,
    servicio_routes,
    turno_routes,
    consulta_routes,
    producto_routes,
    venta_routes
)


app = FastAPI(
    title="VetGestión API",
    description="API para la gestión de una clínica veterinaria",
    version="1.0.0"
)


# Inicializar la base de datos
init_db()


# Registrar las rutas
app.include_router(cliente_routes.router)
app.include_router(mascota_routes.router)
app.include_router(profesional_routes.router)
app.include_router(servicio_routes.router)
app.include_router(turno_routes.router)
app.include_router(consulta_routes.router)
app.include_router(producto_routes.router)
app.include_router(venta_routes.router)


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a VetGestión API",
        "estado": "Funcionando correctamente"
    }
