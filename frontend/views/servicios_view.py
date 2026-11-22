
import tkinter as tk
from tkinter import ttk, messagebox

from frontend.config import (
    COLORS,
    FONT_NORMAL,
    FONT_SUBTITLE,
    FONT_BUTTON
)

from frontend.services.api_service import APIService


class ServiciosView(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["background"])

        self.pack(fill="both", expand=True)

        self.crear_interfaz()
        self.cargar_servicios()

    def crear_interfaz(self):

        # Barra superior
        top = tk.Frame(self, bg=COLORS["background"])
        top.pack(fill="x", pady=(0, 15))

        tk.Label(
            top,
            text="Administración de servicios",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_SUBTITLE
        ).pack(side="left")

        tk.Button(
            top,
            text="+ Nuevo servicio",
            bg=COLORS["primary"],
            fg="white",
            font=FONT_NORMAL,
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.nuevo_servicio
        ).pack(side="right")

        # Tabla
        columns = (
            "id",
            "nombre",
            "descripcion",
            "precio",
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
            "nombre": "Servicio",
            "descripcion": "Descripción",
            "precio": "Precio",
            "estado": "Estado"
        }

        anchos = {
            "id": 50,
            "nombre": 160,
            "descripcion": 300,
            "precio": 120,
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
            command=self.cargar_servicios
        ).pack(side="left", padx=5)

        tk.Button(
            actions,
            text="Editar seleccionado",
            command=self.editar_servicio
        ).pack(side="left", padx=5)

        tk.Button(
            actions,
            text="Eliminar seleccionado",
            command=self.eliminar_servicio
        ).pack(side="left", padx=5)

    def cargar_servicios(self):

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        servicios = APIService.get("/servicios/")

        if servicios is None:
            messagebox.showerror(
                "Error",
                "No se pudieron cargar los servicios."
            )
            return

        for servicio in servicios:
            self.tabla.insert(
                "",
                "end",
                values=(
                    servicio.get("id"),
                    servicio.get("nombre"),
                    servicio.get("descripcion"),
                    f"$ {servicio.get('precio', 0)}",
                    servicio.get("estado")
                )
            )

    def nuevo_servicio(self):
        self.formulario_servicio()

    def editar_servicio(self):

        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Atención",
                "Seleccioná un servicio para editar."
            )
            return

        valores = self.tabla.item(
            seleccionado[0],
            "values"
        )

        servicio_id = valores[0]

        servicio = APIService.get(
            f"/servicios/{servicio_id}"
        )

        if servicio is None:
            messagebox.showerror(
                "Error",
                "No se pudieron obtener los datos del servicio."
            )
            return

        self.formulario_servicio(servicio)

    def formulario_servicio(self, servicio=None):

        ventana = tk.Toplevel(self)
        ventana.title("Datos del servicio")
        ventana.geometry("480x550")
        ventana.resizable(False, False)
        ventana.configure(bg=COLORS["white"])
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        tk.Label(
            ventana,
            text="Datos del servicio",
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

        # Nombre
        tk.Label(
            formulario,
            text="Nombre",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=0, column=0, sticky="w", pady=12)

        entrada_nombre = tk.Entry(formulario, width=35)
        entrada_nombre.grid(row=0, column=1, pady=12, padx=10)

        # Descripción
        tk.Label(
            formulario,
            text="Descripción",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=1, column=0, sticky="w", pady=12)

        entrada_descripcion = tk.Entry(formulario, width=35)
        entrada_descripcion.grid(row=1, column=1, pady=12, padx=10)

        # Precio
        tk.Label(
            formulario,
            text="Precio",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=2, column=0, sticky="w", pady=12)

        entrada_precio = tk.Entry(formulario, width=35)
        entrada_precio.grid(row=2, column=1, pady=12, padx=10)

        # Estado
        tk.Label(
            formulario,
            text="Estado",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=3, column=0, sticky="w", pady=12)

        selector_estado = ttk.Combobox(
            formulario,
            width=32,
            state="readonly",
            values=["Activo", "Inactivo"]
        )

        selector_estado.grid(
            row=3,
            column=1,
            pady=12,
            padx=10
        )

        selector_estado.set(
            servicio.get("estado", "Activo")
            if servicio else "Activo"
        )

        # Cargar datos si estamos editando
        if servicio:

            entrada_nombre.insert(
                0,
                servicio.get("nombre") or ""
            )

            entrada_descripcion.insert(
                0,
                servicio.get("descripcion") or ""
            )

            entrada_precio.insert(
                0,
                str(servicio.get("precio", ""))
            )

        def guardar():

            nombre = entrada_nombre.get().strip()
            descripcion = entrada_descripcion.get().strip()
            precio_texto = entrada_precio.get().strip().replace(",", ".")

            if not nombre:
                messagebox.showwarning(
                    "Atención",
                    "El nombre del servicio es obligatorio."
                )
                return

            try:
                precio = float(precio_texto)

                if precio < 0:
                    raise ValueError

            except ValueError:
                messagebox.showwarning(
                    "Atención",
                    "Ingresá un precio válido mayor o igual a cero."
                )
                return

            datos = {
                "nombre": nombre,
                "descripcion": descripcion,
                "precio": precio,
                "estado": selector_estado.get()
            }

            if servicio:
                resultado = APIService.put(
                    f"/servicios/{servicio['id']}",
                    datos
                )
            else:
                resultado = APIService.post(
                    "/servicios/",
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
                self.cargar_servicios()

            else:
                messagebox.showerror(
                    "Error",
                    "No se pudo guardar el servicio. Revisá los datos."
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

    def eliminar_servicio(self):

        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Atención",
                "Seleccioná un servicio para eliminar."
            )
            return

        valores = self.tabla.item(
            seleccionado[0],
            "values"
        )

        servicio_id = valores[0]

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Estás seguro de eliminar este servicio?"
        )

        if not confirmar:
            return

        resultado = APIService.delete(
            f"/servicios/{servicio_id}"
        )

        if resultado is not None:

            messagebox.showinfo(
                "Éxito",
                "Servicio eliminado correctamente."
            )

            self.cargar_servicios()

        else:
            messagebox.showerror(
                "Error",
                "No se pudo eliminar el servicio. Puede estar asociado a turnos o ventas."
            )
