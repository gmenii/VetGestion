import tkinter as tk
from tkinter import ttk, messagebox

from frontend.config import (
    COLORS,
    FONT_NORMAL,
    FONT_SUBTITLE,
    FONT_BUTTON
)

from frontend.services.api_service import APIService


class ClientesView(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["background"])

        self.pack(fill="both", expand=True)

        self.crear_interfaz()
        self.cargar_clientes()

    def crear_interfaz(self):

        top = tk.Frame(self, bg=COLORS["background"])
        top.pack(fill="x", pady=(0, 15))

        tk.Label(
            top,
            text="Administración de clientes",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_SUBTITLE
        ).pack(side="left")

        tk.Button(
            top,
            text="+ Nuevo cliente",
            bg=COLORS["primary"],
            fg="white",
            font=FONT_NORMAL,
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.nuevo_cliente
        ).pack(side="right")

        columns = (
            "id",
            "dni",
            "nombre",
            "apellido",
            "email",
            "telefono",
            "direccion",
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
            "dni": "DNI",
            "nombre": "Nombre",
            "apellido": "Apellido",
            "email": "Email",
            "telefono": "Teléfono",
            "direccion": "Dirección",
            "estado": "Estado"
        }

        anchos = {
            "id": 45,
            "dni": 85,
            "nombre": 100,
            "apellido": 100,
            "email": 135,
            "telefono": 95,
            "direccion": 145,
            "estado": 85
        }

        for col, texto in encabezados.items():
            self.tabla.heading(col, text=texto)
            self.tabla.column(
                col,
                anchor="center",
                width=anchos[col],
                minwidth=55
            )

        self.tabla.tag_configure(
            "inactivo",
            foreground=COLORS["danger"]
        )

        self.tabla.pack(fill="both", expand=True)

        actions = tk.Frame(self, bg=COLORS["background"])
        actions.pack(fill="x", pady=15)

        tk.Button(
            actions,
            text="Actualizar lista",
            command=self.cargar_clientes
        ).pack(side="left", padx=5)

        tk.Button(
            actions,
            text="Editar seleccionado",
            command=self.editar_cliente
        ).pack(side="left", padx=5)

        tk.Button(
            actions,
            text="Eliminar seleccionado",
            command=self.eliminar_cliente
        ).pack(side="left", padx=5)

    def cargar_clientes(self):

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        clientes = APIService.get("/clientes/")

        if clientes is None:
            messagebox.showerror(
                "Error",
                "No se pudieron cargar los clientes."
            )
            return

        for cliente in clientes:
            estado = cliente.get("estado", "Activo")

            self.tabla.insert(
                "",
                "end",
                values=(
                    cliente.get("id"),
                    cliente.get("dni"),
                    cliente.get("nombre"),
                    cliente.get("apellido"),
                    cliente.get("email"),
                    cliente.get("telefono"),
                    cliente.get("direccion"),
                    estado
                ),
                tags=("inactivo",) if estado == "Inactivo" else ()
            )

    def nuevo_cliente(self):
        self.formulario_cliente()

    def editar_cliente(self):

        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Atención",
                "Seleccioná un cliente para editar."
            )
            return

        valores = self.tabla.item(seleccionado[0], "values")
        cliente_id = valores[0]

        cliente = APIService.get(f"/clientes/{cliente_id}")

        if cliente is None:
            messagebox.showerror(
                "Error",
                "No se pudieron obtener los datos del cliente."
            )
            return

        self.formulario_cliente(cliente)

    def formulario_cliente(self, cliente=None):

        ventana = tk.Toplevel(self)
        ventana.title("Datos del cliente")
        ventana.geometry("470x650")
        ventana.resizable(False, False)
        ventana.configure(bg=COLORS["white"])
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        campos = [
            ("DNI", "dni"),
            ("Nombre", "nombre"),
            ("Apellido", "apellido"),
            ("Email", "email"),
            ("Teléfono", "telefono"),
            ("Dirección", "direccion")
        ]

        entradas = {}

        tk.Label(
            ventana,
            text="Datos del cliente",
            font=FONT_SUBTITLE,
            bg=COLORS["white"],
            fg=COLORS["text"]
        ).pack(pady=15)

        formulario = tk.Frame(ventana, bg=COLORS["white"])
        formulario.pack(fill="both", expand=True, padx=30)

        for i, (etiqueta, clave) in enumerate(campos):

            tk.Label(
                formulario,
                text=etiqueta,
                bg=COLORS["white"],
                fg=COLORS["text"],
                font=FONT_NORMAL
            ).grid(row=i, column=0, sticky="w", pady=7)

            entrada = tk.Entry(formulario, width=35)
            entrada.grid(row=i, column=1, pady=7, padx=10)
            entradas[clave] = entrada

            if cliente:
                entrada.insert(0, cliente.get(clave) or "")

        fila_estado = len(campos)

        tk.Label(
            formulario,
            text="Estado",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=fila_estado, column=0, sticky="w", pady=7)

        estado_var = tk.StringVar(
            value=cliente.get("estado", "Activo") if cliente else "Activo"
        )

        estado_combo = ttk.Combobox(
            formulario,
            textvariable=estado_var,
            values=("Activo", "Inactivo"),
            state="readonly",
            width=32
        )
        estado_combo.grid(
            row=fila_estado,
            column=1,
            pady=7,
            padx=10
        )

        def guardar():

            datos = {
                clave: entrada.get().strip()
                for clave, entrada in entradas.items()
            }
            datos["estado"] = estado_var.get()

            if (
                not datos["dni"]
                or not datos["nombre"]
                or not datos["apellido"]
            ):
                messagebox.showwarning(
                    "Atención",
                    "DNI, nombre y apellido son obligatorios."
                )
                return

            if cliente:
                resultado = APIService.put(
                    f"/clientes/{cliente['id']}",
                    datos
                )
            else:
                resultado = APIService.post(
                    "/clientes/",
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
                self.cargar_clientes()
            else:
                messagebox.showerror(
                    "Error",
                    "No se pudo guardar el cliente. Revisá los datos."
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

    def eliminar_cliente(self):

        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Atención",
                "Seleccioná un cliente para eliminar."
            )
            return

        valores = self.tabla.item(seleccionado[0], "values")
        cliente_id = valores[0]

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Estás seguro de eliminar este cliente?"
        )

        if not confirmar:
            return

        resultado = APIService.delete(f"/clientes/{cliente_id}")

        if resultado is not None:
            messagebox.showinfo(
                "Éxito",
                "Cliente eliminado correctamente."
            )
            self.cargar_clientes()
        else:
            messagebox.showerror(
                "Error",
                "No se pudo eliminar el cliente."
            )
