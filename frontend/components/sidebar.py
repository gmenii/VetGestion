
import tkinter as tk

from frontend.config import COLORS, FONT_BUTTON


class Sidebar(tk.Frame):

    def __init__(self, parent, on_navigate):
        super().__init__(
            parent,
            bg=COLORS["sidebar"],
            width=220
        )

        self.on_navigate = on_navigate
        self.pack_propagate(False)

        # Encabezado
        header = tk.Frame(
            self,
            bg=COLORS["sidebar"],
            height=100
        )
        header.pack(fill="x", pady=(20, 15))

        tk.Label(
            header,
            text="VetGestión",
            bg=COLORS["sidebar"],
            fg=COLORS["white"],
            font=("Segoe UI", 20, "bold")
        ).pack(pady=(10, 5))

        tk.Label(
            header,
            text="Sistema de gestión veterinaria",
            bg=COLORS["sidebar"],
            fg="#BDC3C7",
            font=("Segoe UI", 8)
        ).pack()

        # Opciones del menú
        self.options = [
            ("Inicio", "inicio"),
            ("Clientes", "clientes"),
            ("Mascotas", "mascotas"),
            ("Profesionales", "profesionales"),
            ("Servicios", "servicios"),
            ("Turnos", "turnos"),
            ("Consultas", "consultas"),
            ("Productos", "productos"),
            ("Ventas", "ventas")
        ]

        self.buttons = {}

        for title, section in self.options:
            button = tk.Button(
                self,
                text=f"   {title}",
                font=FONT_BUTTON,
                bg=COLORS["sidebar"],
                fg=COLORS["white"],
                activebackground=COLORS["sidebar_hover"],
                activeforeground=COLORS["white"],
                relief="flat",
                bd=0,
                anchor="w",
                padx=20,
                pady=12,
                cursor="hand2",
                command=lambda s=section: self.navigate(s)
            )

            button.pack(fill="x", padx=8, pady=2)

            self.buttons[section] = button

        self.select_option("inicio")

    def navigate(self, section):
        self.select_option(section)
        self.on_navigate(section)

    def select_option(self, section):
        for name, button in self.buttons.items():
            if name == section:
                button.config(
                    bg=COLORS["primary"],
                    fg=COLORS["white"]
                )
            else:
                button.config(
                    bg=COLORS["sidebar"],
                    fg=COLORS["white"]
                )
