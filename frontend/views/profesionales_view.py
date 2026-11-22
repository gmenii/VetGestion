
import tkinter as tk
from tkinter import ttk, messagebox

from frontend.config import (
    COLORS,
    FONT_NORMAL,
    FONT_SUBTITLE,
    FONT_BUTTON
)

from frontend.services.api_service import APIService


class ProfesionalesView(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["background"])

        self.pack(fill="both", expand=True)

        self.crear_interfaz()
        self.cargar_profesionales()

    def crear_interfaz(self):

        # Barra superior
        top = tk.Frame(self, bg=COLORS["background"])
        top.pack(fill="x", pady=(0, 15))

        tk.Label(
            top,
            text="Administración de profesionales",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_SUBTITLE
        ).pack(side="left")

        tk.Button(
            top,
            text="+ Nuevo profesional",
            bg=COLORS["primary"],
            fg="white",
            font=FONT_NORMAL,
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.nuevo_profesional
        ).pack(side="right")

        # Tabla
        columns = (
            "id",
            "matricula",
            "nombre",
            "apellido",
            "email",
            "estado"
        )

        self.tabla = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=15
        )

        encabezados = {
            "id": "ID",
            "matricula": "Matrícula",
            "nombre": "Nombre",
            "apellido": "Apellido",
            "email": "Email",
            "estado": "Estado"
        }

        anchos = {
            "id": 50,
            "matricula": 120,
            "nombre": 130,
            "apellido": 130,
            "email": 200,
            "estado": 100
        }

        for col, texto in encabezados.items():
            self.tabla.heading(col, text=texto)
            self.tabla.column(
                col,
                anchor="center",
                width=anchos[col],
                minwidth=60
            )

        self.tabla.pack(fill="both", expand=True)

        # Botones inferiores
        actions = tk.Frame(self, bg=COLORS["background"])
        actions.pack(fill="x", pady=15)

        tk.Button(
            actions,
            text="Actualizar lista",
            command=self.cargar_profesionales
        ).pack(side="left", padx=5)

        tk.Button(
            actions,
            text="Editar seleccionado",
            command=self.editar_profesional
        ).pack(side="left", padx=5)

        tk.Button(
            actions,
            text="Eliminar seleccionado",
            command=self.eliminar_profesional
        ).pack(side="left", padx=5)

    def cargar_profesionales(self):

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        profesionales = APIService.get("/profesionales/")

        if profesionales is None:
            messagebox.showerror(
                "Error",
                "No se pudieron cargar los profesionales."
            )
            return

        for profesional in profesionales:
            self.tabla.insert(
                "",
                "end",
                values=(
                    profesional.get("id"),
                    profesional.get("matricula"),
                    profesional.get("nombre"),
                    profesional.get("apellido"),
                    profesional.get("email"),
                    profesional.get("estado")
                )
            )

    def nuevo_profesional(self):
        self.formulario_profesional()

    def editar_profesional(self):

        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Atención",
                "Seleccioná un profesional para editar."
            )
            return

        valores = self.tabla.item(
            seleccionado[0],
            "values"
        )

        profesional_id = valores[0]

        profesional = APIService.get(
            f"/profesionales/{profesional_id}"
        )

        if profesional is None:
            messagebox.showerror(
                "Error",
                "No se pudieron obtener los datos del profesional."
            )
            return

        self.formulario_profesional(profesional)

    def formulario_profesional(self, profesional=None):

        ventana = tk.Toplevel(self)
        ventana.title("Datos del profesional")
        ventana.geometry("450x550")
        ventana.resizable(False, False)
        ventana.configure(bg=COLORS["white"])
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        campos = [
            ("Matrícula", "matricula"),
            ("Nombre", "nombre"),
            ("Apellido", "apellido"),
            ("Email", "email")
        ]

        entradas = {}

        tk.Label(
            ventana,
            text="Datos del profesional",
            font=FONT_SUBTITLE,
            bg=COLORS["white"],
            fg=COLORS["text"]
        ).pack(pady=20)

        formulario = tk.Frame(
            ventana,
            bg=COLORS["white"]
        )
        formulario.pack(
            fill="both",
            expand=True,
            padx=30
        )

        for i, (etiqueta, clave) in enumerate(campos):

            tk.Label(
                formulario,
                text=etiqueta,
                bg=COLORS["white"],
                fg=COLORS["text"],
                font=FONT_NORMAL
            ).grid(
                row=i,
                column=0,
                sticky="w",
                pady=12
            )

            entrada = tk.Entry(
                formulario,
                width=35
            )

            entrada.grid(
                row=i,
                column=1,
                pady=12,
                padx=10
            )

            entradas[clave] = entrada

            if profesional:
                entrada.insert(
                    0,
                    profesional.get(clave) or ""
                )

        # Estado del profesional
        tk.Label(
            formulario,
            text="Estado",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=12
        )

        selector_estado = ttk.Combobox(
            formulario,
            width=32,
            state="readonly",
            values=["Activo", "Inactivo"]
        )

        selector_estado.grid(
            row=4,
            column=1,
            pady=12,
            padx=10
        )

        selector_estado.set(
            profesional.get("estado", "Activo")
            if profesional else "Activo"
        )

        def guardar():

            datos = {
                clave: entrada.get().strip()
                for clave, entrada in entradas.items()
            }

            datos["estado"] = selector_estado.get()

            if (
                not datos["matricula"]
                or not datos["nombre"]
                or not datos["apellido"]
            ):
                messagebox.showwarning(
                    "Atención",
                    "Matrícula, nombre y apellido son obligatorios."
                )
                return

            if not datos["estado"]:
                messagebox.showwarning(
                    "Atención",
                    "Seleccioná un estado."
                )
                return

            if profesional:
                resultado = APIService.put(
                    f"/profesionales/{profesional['id']}",
                    datos
                )
            else:
                resultado = APIService.post(
                    "/profesionales/",
                    datos
                )

            if resultado is not None:

                messagebox.showinfo(
                    "Éxito",
                    resultado.get(
                        "mensaje",
                        "Operación realizada correctamente."
                    )
                )

                ventana.destroy()
                self.cargar_profesionales()

            else:
                messagebox.showerror(
                    "Error",
                    "No se pudo guardar el profesional. Revisá los datos."
                )

        tk.Button(
            ventana,
            text="Guardar",
            command=guardar,
            bg=COLORS["success"],
            fg="white",
            font=FONT_BUTTON,
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=10
        ).pack(pady=20)

    def eliminar_profesional(self):

        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Atención",
                "Seleccioná un profesional para eliminar."
            )
            return

        valores = self.tabla.item(
            seleccionado[0],
            "values"
        )

        profesional_id = valores[0]

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Estás seguro de eliminar este profesional?"
        )

        if not confirmar:
            return

        resultado = APIService.delete(
            f"/profesionales/{profesional_id}"
        )

        if resultado is not None:

            messagebox.showinfo(
                "Éxito",
                "Profesional eliminado correctamente."
            )

            self.cargar_profesionales()

        else:
            messagebox.showerror(
                "Error",
                "No se pudo eliminar el profesional."
            )
