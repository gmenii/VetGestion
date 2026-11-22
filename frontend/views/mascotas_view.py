
import tkinter as tk
from tkinter import ttk, messagebox

from frontend.config import (
    COLORS,
    FONT_NORMAL,
    FONT_SUBTITLE,
    FONT_BUTTON
)

from frontend.services.api_service import APIService


class MascotasView(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["background"])

        self.pack(fill="both", expand=True)

        self.crear_interfaz()
        self.cargar_mascotas()

    def crear_interfaz(self):

        # Barra superior
        top = tk.Frame(self, bg=COLORS["background"])
        top.pack(fill="x", pady=(0, 15))

        tk.Label(
            top,
            text="Administración de mascotas",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_SUBTITLE
        ).pack(side="left")

        tk.Button(
            top,
            text="+ Nueva mascota",
            bg=COLORS["primary"],
            fg="white",
            font=FONT_NORMAL,
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.nueva_mascota
        ).pack(side="right")

        # Tabla
        columns = (
            "id",
            "nombre",
            "especie",
            "raza",
            "sexo",
            "fecha_nacimiento",
            "cliente"
        )

        self.tabla = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=15
        )

        encabezados = {
            "id": "ID",
            "nombre": "Nombre",
            "especie": "Especie",
            "raza": "Raza",
            "sexo": "Sexo",
            "fecha_nacimiento": "Nacimiento",
            "cliente": "Dueño"
        }

        anchos = {
            "id": 45,
            "nombre": 110,
            "especie": 90,
            "raza": 120,
            "sexo": 80,
            "fecha_nacimiento": 110,
            "cliente": 180
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
            command=self.cargar_mascotas
        ).pack(side="left", padx=5)

        tk.Button(
            actions,
            text="Editar seleccionada",
            command=self.editar_mascota
        ).pack(side="left", padx=5)

        tk.Button(
            actions,
            text="Eliminar seleccionada",
            command=self.eliminar_mascota
        ).pack(side="left", padx=5)

    def cargar_mascotas(self):

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        mascotas = APIService.get("/mascotas/")

        if mascotas is None:
            messagebox.showerror(
                "Error",
                "No se pudieron cargar las mascotas."
            )
            return

        for mascota in mascotas:

            nombre_cliente = (
                f"{mascota.get('nombre_cliente', '')} "
                f"{mascota.get('apellido_cliente', '')}"
            ).strip()

            self.tabla.insert(
                "",
                "end",
                values=(
                    mascota.get("id"),
                    mascota.get("nombre"),
                    mascota.get("especie"),
                    mascota.get("raza"),
                    mascota.get("sexo"),
                    mascota.get("fecha_nacimiento"),
                    nombre_cliente
                )
            )

    def nueva_mascota(self):
        self.formulario_mascota()

    def editar_mascota(self):

        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Atención",
                "Seleccioná una mascota para editar."
            )
            return

        valores = self.tabla.item(
            seleccionado[0],
            "values"
        )

        mascota_id = valores[0]

        mascota = APIService.get(
            f"/mascotas/{mascota_id}"
        )

        if mascota is None:
            messagebox.showerror(
                "Error",
                "No se pudieron obtener los datos de la mascota."
            )
            return

        self.formulario_mascota(mascota)

    def formulario_mascota(self, mascota=None):

        ventana = tk.Toplevel(self)
        ventana.title("Datos de la mascota")
        ventana.geometry("480x650")
        ventana.resizable(False, False)
        ventana.configure(bg=COLORS["white"])
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        clientes = APIService.get("/clientes/")

        if clientes is None:
            messagebox.showerror(
                "Error",
                "No se pudieron cargar los clientes."
            )
            ventana.destroy()
            return

        # Diccionario para relacionar nombre mostrado con ID
        clientes_opciones = {}

        for cliente in clientes:
            nombre_completo = (
                f"{cliente.get('nombre', '')} "
                f"{cliente.get('apellido', '')} "
                f"(DNI: {cliente.get('dni', '')})"
            )

            clientes_opciones[nombre_completo] = cliente.get("id")

        tk.Label(
            ventana,
            text="Datos de la mascota",
            font=FONT_SUBTITLE,
            bg=COLORS["white"],
            fg=COLORS["text"]
        ).pack(pady=15)

        formulario = tk.Frame(
            ventana,
            bg=COLORS["white"]
        )
        formulario.pack(
            fill="both",
            expand=True,
            padx=30
        )

        # Cliente responsable
        tk.Label(
            formulario,
            text="Dueño / Cliente",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=0, column=0, sticky="w", pady=8)

        selector_cliente = ttk.Combobox(
            formulario,
            width=32,
            state="readonly",
            values=list(clientes_opciones.keys())
        )

        selector_cliente.grid(
            row=0,
            column=1,
            pady=8,
            padx=10
        )

        # Nombre
        tk.Label(
            formulario,
            text="Nombre",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=1, column=0, sticky="w", pady=8)

        entrada_nombre = tk.Entry(formulario, width=35)
        entrada_nombre.grid(row=1, column=1, pady=8, padx=10)

        # Especie
        tk.Label(
            formulario,
            text="Especie",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=2, column=0, sticky="w", pady=8)

        selector_especie = ttk.Combobox(
            formulario,
            width=32,
            state="readonly",
            values=["Perro", "Gato"]
        )

        selector_especie.grid(
            row=2,
            column=1,
            pady=8,
            padx=10
        )

        # Raza
        tk.Label(
            formulario,
            text="Raza",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=3, column=0, sticky="w", pady=8)

        entrada_raza = tk.Entry(formulario, width=35)
        entrada_raza.grid(row=3, column=1, pady=8, padx=10)

        # Fecha de nacimiento
        tk.Label(
            formulario,
            text="Fecha de nacimiento",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=4, column=0, sticky="w", pady=8)

        entrada_fecha = tk.Entry(formulario, width=35)
        entrada_fecha.grid(row=4, column=1, pady=8, padx=10)

        # Sexo
        tk.Label(
            formulario,
            text="Sexo",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=5, column=0, sticky="w", pady=8)

        selector_sexo = ttk.Combobox(
            formulario,
            width=32,
            state="readonly",
            values=["Hembra", "Macho"]
        )

        selector_sexo.grid(
            row=5,
            column=1,
            pady=8,
            padx=10
        )

        # Observaciones
        tk.Label(
            formulario,
            text="Observaciones",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=6, column=0, sticky="nw", pady=8)

        entrada_observaciones = tk.Text(
            formulario,
            width=26,
            height=4
        )

        entrada_observaciones.grid(
            row=6,
            column=1,
            pady=8,
            padx=10
        )

        # Cargar datos si estamos editando
        if mascota:

            entrada_nombre.insert(
                0,
                mascota.get("nombre") or ""
            )

            selector_especie.set(
                mascota.get("especie") or ""
            )

            entrada_raza.insert(
                0,
                mascota.get("raza") or ""
            )

            entrada_fecha.insert(
                0,
                mascota.get("fecha_nacimiento") or ""
            )

            selector_sexo.set(
                mascota.get("sexo") or ""
            )

            entrada_observaciones.insert(
                "1.0",
                mascota.get("observaciones") or ""
            )

            cliente_id = mascota.get("cliente_id")

            for nombre, id_cliente in clientes_opciones.items():
                if id_cliente == cliente_id:
                    selector_cliente.set(nombre)
                    break

        def guardar():

            nombre_cliente = selector_cliente.get()

            if nombre_cliente not in clientes_opciones:
                messagebox.showwarning(
                    "Atención",
                    "Seleccioná un cliente responsable."
                )
                return

            datos = {
                "cliente_id": clientes_opciones[nombre_cliente],
                "nombre": entrada_nombre.get().strip(),
                "especie": selector_especie.get(),
                "raza": entrada_raza.get().strip(),
                "fecha_nacimiento": entrada_fecha.get().strip(),
                "sexo": selector_sexo.get(),
                "observaciones": entrada_observaciones.get(
                    "1.0",
                    "end"
                ).strip()
            }

            if not datos["nombre"]:
                messagebox.showwarning(
                    "Atención",
                    "El nombre de la mascota es obligatorio."
                )
                return

            if not datos["especie"]:
                messagebox.showwarning(
                    "Atención",
                    "Seleccioná una especie."
                )
                return

            if not datos["sexo"]:
                messagebox.showwarning(
                    "Atención",
                    "Seleccioná el sexo de la mascota."
                )
                return

            if mascota:
                resultado = APIService.put(
                    f"/mascotas/{mascota['id']}",
                    datos
                )
            else:
                resultado = APIService.post(
                    "/mascotas/",
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
                self.cargar_mascotas()

            else:
                messagebox.showerror(
                    "Error",
                    "No se pudo guardar la mascota. Revisá los datos."
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
        ).pack(pady=15)

    def eliminar_mascota(self):

        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Atención",
                "Seleccioná una mascota para eliminar."
            )
            return

        valores = self.tabla.item(
            seleccionado[0],
            "values"
        )

        mascota_id = valores[0]

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Estás seguro de eliminar esta mascota?"
        )

        if not confirmar:
            return

        resultado = APIService.delete(
            f"/mascotas/{mascota_id}"
        )

        if resultado is not None:

            messagebox.showinfo(
                "Éxito",
                "Mascota eliminada correctamente."
            )

            self.cargar_mascotas()

        else:
            messagebox.showerror(
                "Error",
                "No se pudo eliminar la mascota."
            )
