# VetGestión 🐾

Sistema de gestión para una clínica veterinaria, desarrollado como proyecto final del curso Python Intermedio de Tecno3F.

## Descripción

VetGestión es una aplicación de escritorio que permite administrar las principales actividades de una clínica veterinaria, centralizando la información de clientes, mascotas, profesionales, turnos, consultas, servicios, productos y ventas.

El sistema cuenta con una interfaz gráfica desarrollada en Python y un backend que expone una API REST para gestionar la información almacenada en una base de datos SQLite.

## Funcionalidades principales

- **Clientes:** registro, consulta, modificación y eliminación de clientes. Permite administrar su estado (Activo/Inactivo) y realizar búsquedas por DNI.
- **Mascotas:** gestión de mascotas asociadas a sus respectivos propietarios.
- **Profesionales:** administración de veterinarios y sus estados.
- **Servicios:** gestión de los servicios ofrecidos por la clínica.
- **Turnos:** creación, consulta, reprogramación y cancelación de turnos.
- **Consultas:** registro de diagnósticos y observaciones, con historial por mascota.
- **Productos:** administración de medicamentos y vacunas, incluyendo control de stock.
- **Ventas:** registro de ventas de productos y servicios, consulta del historial y detalle de cada operación.
- **Dashboard:** visualización de indicadores generales de la clínica.

## Tecnologías utilizadas

- Python
- SQLite3
- FastAPI
- Pydantic
- Uvicorn
- Tkinter
- Requests

## Estructura del proyecto

```text
VetGestion/
│
├── app/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   ├── views/
│   ├── database.py
│   └── main.py
│
├── frontend/
│   ├── components/
│   ├── services/
│   ├── views/
│   └── config.py
│
├── run_gui.py
├── requirements.txt
└── README.md
```

## Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/gmenii/VetGestion.git
```

Ingresar a la carpeta del proyecto:

```bash
cd VetGestion
```

### 2. Crear un entorno virtual (recomendado)

```bash
python -m venv .venv
```

### 3. Activar el entorno virtual

En Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar las dependencias

```bash
pip install -r requirements.txt
```

## Ejecución del sistema

Para utilizar VetGestión es necesario iniciar el backend y la interfaz gráfica en dos terminales separadas.

### 1. Iniciar el servidor

Desde la carpeta principal del proyecto, ejecutar:

```bash
python -m uvicorn app.main:app --reload
```

El servidor estará disponible en:

```text
http://127.0.0.1:8000
```

La documentación interactiva de la API se encuentra en:

```text
http://127.0.0.1:8000/docs
```

### 2. Iniciar la interfaz gráfica

Abrir una segunda terminal, activar el entorno virtual si todavía no está activado e ingresar a la carpeta del proyecto.

Ejecutar:

```bash
python run_gui.py
```

Se abrirá la aplicación de escritorio VetGestión.

## Desafíos del trabajo final

### Challenge A: Búsqueda de clientes por identificador único

Se implementó una búsqueda de clientes mediante DNI, utilizando un endpoint específico de la API.

Al ingresar un DNI y ejecutar la búsqueda, el sistema:

- Verifica si el cliente existe.
- Muestra su nombre, identificador y estado.
- Informa cuando no se encuentra un cliente.
- Permite identificar si el cliente está Activo o Inactivo.

Además, los clientes inactivos no pueden realizar ventas. Esta validación se aplica tanto desde la interfaz gráfica como desde el backend.

### Challenge B: Búsqueda de productos y servicios

Se incorporó una funcionalidad de búsqueda por nombre que permite:

- Buscar productos y servicios mediante coincidencias parciales.
- Mostrar una lista cuando existen varios resultados.
- Seleccionar el elemento deseado.
- Consultar su precio y, en el caso de los productos, su stock disponible.
- Informar cuando no se encuentran coincidencias.

También se implementaron validaciones para impedir que se agreguen a una venta cantidades superiores al stock disponible.

## Base de datos

El sistema utiliza SQLite3 para almacenar la información. La base de datos se inicializa automáticamente al iniciar el backend.

## Proyecto académico

Proyecto desarrollado como trabajo final del curso Python Intermedio de Tecno3F.