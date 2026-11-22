
import tkinter as tk
from tkinter import messagebox

from frontend.config import COLORS, FONT_NORMAL, FONT_SUBTITLE, FONT_TITLE
from frontend.services.api_service import APIService


class InicioView:

    def __init__(self, parent):
        self.parent = parent
        self.crear_interfaz()
        self.cargar_datos()

    def crear_interfaz(self):

        tk.Label(
            self.parent,
            text="¡Bienvenido a VetGestión!",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_TITLE
        ).pack(anchor="w", pady=(0, 5))

        tk.Label(
            self.parent,
            text="Resumen general de la clínica veterinaria",
            bg=COLORS["background"],
            fg=COLORS["secondary_text"],
            font=FONT_NORMAL
        ).pack(anchor="w", pady=(0, 25))

        self.tarjetas_frame = tk.Frame(
            self.parent,
            bg=COLORS["background"]
        )
        self.tarjetas_frame.pack(fill="x")

        self.tarjetas = {}

        indicadores = [
            ("clientes", "Clientes registrados", "#3498DB"),
            ("mascotas", "Mascotas registradas", "#27AE60"),
            ("profesionales", "Profesionales activos", "#9B59B6"),
            ("turnos", "Turnos registrados", "#E67E22"),
            ("ventas", "Ventas realizadas", "#16A085"),
            ("stock", "Productos con stock bajo", "#E74C3C")
        ]

        for indice, (clave, titulo, color) in enumerate(indicadores):

            fila = indice // 3
            columna = indice % 3

            tarjeta = tk.Frame(
                self.tarjetas_frame,
                bg=COLORS["white"],
                highlightbackground=COLORS["border"],
                highlightthickness=1,
                padx=15,
                pady=15
            )

            tarjeta.grid(
                row=fila,
                column=columna,
                sticky="nsew",
                padx=8,
                pady=8
            )

            tk.Label(
                tarjeta,
                text=titulo,
                bg=COLORS["white"],
                fg=COLORS["secondary_text"],
                font=FONT_NORMAL
            ).pack(anchor="w")

            valor = tk.Label(
                tarjeta,
                text="--",
                bg=COLORS["white"],
                fg=color,
                font=("Segoe UI", 26, "bold")
            )
            valor.pack(anchor="w", pady=(8, 0))

            self.tarjetas[clave] = valor

        for columna in range(3):
            self.tarjetas_frame.grid_columnconfigure(
                columna,
                weight=1
            )

        separador = tk.Frame(
            self.parent,
            bg=COLORS["border"],
            height=1
        )
        separador.pack(fill="x", pady=25)

        tk.Label(
            self.parent,
            text="Información del sistema",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_SUBTITLE
        ).pack(anchor="w", pady=(0, 10))

        tk.Label(
            self.parent,
            text="Desde el menú lateral podés administrar clientes, mascotas, "
                 "profesionales, servicios, turnos, consultas, productos y ventas.",
            bg=COLORS["background"],
            fg=COLORS["secondary_text"],
            font=FONT_NORMAL,
            wraplength=750,
            justify="left"
        ).pack(anchor="w")

        tk.Button(
            self.parent,
            text="Actualizar información",
            command=self.cargar_datos,
            bg=COLORS["primary"],
            fg=COLORS["white"],
            font=FONT_NORMAL,
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        ).pack(anchor="w", pady=25)

    def cargar_datos(self):

        clientes = APIService.get("/clientes/")
        mascotas = APIService.get("/mascotas/")
        profesionales = APIService.get("/profesionales/")
        turnos = APIService.get("/turnos/")
        ventas = APIService.get("/ventas/")
        productos = APIService.get("/productos/")

        respuestas = [
            clientes,
            mascotas,
            profesionales,
            turnos,
            ventas,
            productos
        ]

        if any(respuesta is None for respuesta in respuestas):
            messagebox.showerror(
                "Error",
                "No se pudo cargar toda la información del sistema."
            )
            return

        profesionales_activos = sum(
            1 for profesional in profesionales
            if profesional.get("estado") == "Activo"
        )

        productos_stock_bajo = sum(
            1 for producto in productos
            if producto.get("estado") == "Activo"
            and producto.get("stock", 0) <= producto.get("stock_minimo", 0)
        )

        valores = {
            "clientes": len(clientes),
            "mascotas": len(mascotas),
            "profesionales": profesionales_activos,
            "turnos": len(turnos),
            "ventas": len(ventas),
            "stock": productos_stock_bajo
        }

        for clave, valor in valores.items():
            self.tarjetas[clave].config(text=str(valor))
