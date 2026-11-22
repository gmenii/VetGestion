
import tkinter as tk

from frontend.config import (
    APP_NAME,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_MIN_HEIGHT,
    COLORS,
    FONT_TITLE,
    FONT_NORMAL
)

from frontend.components.sidebar import Sidebar

from frontend.views.inicio_view import InicioView
from frontend.views.clientes_view import ClientesView
from frontend.views.mascotas_view import MascotasView
from frontend.views.profesionales_view import ProfesionalesView
from frontend.views.servicios_view import ServiciosView
from frontend.views.turnos_view import TurnosView
from frontend.views.consultas_view import ConsultasView
from frontend.views.productos_view import ProductosView
from frontend.views.ventas_view import VentasView


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.configure(bg=COLORS["background"])

        self.crear_interfaz()
        self.show_section("inicio")

    # ==========================================
    # CREAR INTERFAZ PRINCIPAL
    # ==========================================

    def crear_interfaz(self):

        self.sidebar = Sidebar(
            self,
            self.show_section
        )
        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.main_container = tk.Frame(
            self,
            bg=COLORS["background"]
        )
        self.main_container.pack(
            side="right",
            fill="both",
            expand=True
        )

        # ENCABEZADO

        self.header = tk.Frame(
            self.main_container,
            bg=COLORS["white"],
            height=75
        )
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        self.title_label = tk.Label(
            self.header,
            text="Inicio",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_TITLE
        )
        self.title_label.pack(
            side="left",
            padx=25,
            pady=15
        )

        # CONTENIDO

        self.content = tk.Frame(
            self.main_container,
            bg=COLORS["background"]
        )
        self.content.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

    # ==========================================
    # CAMBIAR SECCION
    # ==========================================

    def show_section(self, section):

        titulos = {
            "inicio": "Inicio",
            "clientes": "Clientes",
            "mascotas": "Mascotas",
            "profesionales": "Profesionales",
            "servicios": "Servicios",
            "turnos": "Turnos",
            "consultas": "Consultas",
            "productos": "Productos",
            "ventas": "Ventas"
        }

        self.title_label.config(
            text=titulos.get(section, "VetGestión")
        )

        # Limpiar contenido anterior

        for widget in self.content.winfo_children():
            widget.destroy()

        # Cargar sección seleccionada

        if section == "inicio":
            InicioView(self.content)

        elif section == "clientes":
            ClientesView(self.content)

        elif section == "mascotas":
            MascotasView(self.content)

        elif section == "profesionales":
            ProfesionalesView(self.content)

        elif section == "servicios":
            ServiciosView(self.content)

        elif section == "turnos":
            TurnosView(self.content)

        elif section == "consultas":
            ConsultasView(self.content)

        elif section == "productos":
            ProductosView(self.content)

        elif section == "ventas":
            VentasView(self.content)

        else:
            tk.Label(
                self.content,
                text=f"Sección {titulos.get(section, section)} en construcción",
                bg=COLORS["background"],
                fg=COLORS["secondary_text"],
                font=FONT_NORMAL
            ).pack(pady=30)
