
import tkinter as tk
from tkinter import ttk, messagebox

from frontend.config import COLORS, FONT_NORMAL, FONT_SUBTITLE
from frontend.services.api_service import APIService


class ProductosView:

    def __init__(self, parent):
        self.parent = parent
        self.crear_interfaz()
        self.cargar_productos()

    def crear_interfaz(self):
        encabezado = tk.Frame(self.parent, bg=COLORS["background"])
        encabezado.pack(fill="x", pady=(0, 15))

        tk.Label(
            encabezado,
            text="Gestión de productos",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_SUBTITLE
        ).pack(side="left")

        tk.Button(
            encabezado,
            text="+ Nuevo producto",
            command=self.formulario_producto,
            bg=COLORS["primary"],
            fg=COLORS["white"],
            font=FONT_NORMAL,
            relief="flat",
            padx=12,
            pady=7,
            cursor="hand2"
        ).pack(side="right")

        tk.Label(
            self.parent,
            text="Los productos con stock igual o inferior al mínimo se muestran resaltados.",
            bg=COLORS["background"],
            fg=COLORS["secondary_text"],
            font=FONT_NORMAL
        ).pack(anchor="w", pady=(0, 10))

        tabla_frame = tk.Frame(self.parent, bg=COLORS["white"])
        tabla_frame.pack(fill="both", expand=True)

        columnas = (
            "id", "nombre", "categoria", "precio",
            "stock", "stock_minimo", "estado"
        )

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            height=18
        )

        encabezados = {
            "id": "ID",
            "nombre": "Nombre",
            "categoria": "Categoría",
            "precio": "Precio",
            "stock": "Stock",
            "stock_minimo": "Stock mínimo",
            "estado": "Estado"
        }

        anchos = {
            "id": 45,
            "nombre": 190,
            "categoria": 130,
            "precio": 100,
            "stock": 80,
            "stock_minimo": 110,
            "estado": 90
        }

        for columna in columnas:
            self.tabla.heading(
                columna,
                text=encabezados[columna]
            )
            self.tabla.column(
                columna,
                width=anchos[columna],
                anchor="center"
            )

        self.tabla.tag_configure(
            "stock_bajo",
            background="#FCE4E4",
            foreground="#C0392B"
        )

        scrollbar = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        botones = tk.Frame(self.parent, bg=COLORS["background"])
        botones.pack(fill="x", pady=15)

        tk.Button(
            botones,
            text="Editar producto",
            command=self.editar_producto,
            bg=COLORS["primary"],
            fg=COLORS["white"],
            font=FONT_NORMAL,
            relief="flat",
            padx=12,
            pady=7,
            cursor="hand2"
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            botones,
            text="Eliminar producto",
            command=self.eliminar_producto,
            bg=COLORS["danger"],
            fg=COLORS["white"],
            font=FONT_NORMAL,
            relief="flat",
            padx=12,
            pady=7,
            cursor="hand2"
        ).pack(side="left")

        tk.Button(
            botones,
            text="Actualizar listado",
            command=self.cargar_productos,
            bg=COLORS["sidebar"],
            fg=COLORS["white"],
            font=FONT_NORMAL,
            relief="flat",
            padx=12,
            pady=7,
            cursor="hand2"
        ).pack(side="right")

    def cargar_productos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        productos = APIService.get("/productos/")

        if productos is None:
            messagebox.showerror(
                "Error",
                "No se pudieron cargar los productos."
            )
            return

        for producto in productos:
            stock = producto.get("stock", 0)
            stock_minimo = producto.get("stock_minimo", 0)

            valores = (
                producto.get("id"),
                producto.get("nombre", ""),
                producto.get("categoria", ""),
                f"$ {producto.get('precio', 0):,.2f}",
                stock,
                stock_minimo,
                producto.get("estado", "")
            )

            tag = ()
            if stock <= stock_minimo:
                tag = ("stock_bajo",)

            self.tabla.insert(
                "",
                "end",
                values=valores,
                tags=tag
            )

    def formulario_producto(self, producto=None):
        ventana = tk.Toplevel(self.parent)
        ventana.title(
            "Editar producto" if producto else "Nuevo producto"
        )
        ventana.geometry("420x570")
        ventana.resizable(False, False)
        ventana.configure(bg=COLORS["background"])
        ventana.transient(self.parent.winfo_toplevel())
        ventana.grab_set()

        tk.Label(
            ventana,
            text="Editar producto" if producto else "Registrar producto",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_SUBTITLE
        ).pack(pady=20)

        formulario = tk.Frame(
            ventana,
            bg=COLORS["background"]
        )
        formulario.pack(fill="both", padx=30)

        entradas = {}

        def agregar_campo(nombre, etiqueta, valor=""):
            tk.Label(
                formulario,
                text=etiqueta,
                bg=COLORS["background"],
                fg=COLORS["text"],
                font=FONT_NORMAL
            ).pack(anchor="w", pady=(8, 3))

            entrada = tk.Entry(
                formulario,
                font=FONT_NORMAL,
                relief="solid",
                bd=1
            )
            entrada.pack(fill="x", ipady=5)
            entrada.insert(0, str(valor) if valor is not None else "")

            entradas[nombre] = entrada

        agregar_campo(
            "nombre",
            "Nombre:",
            producto.get("nombre", "") if producto else ""
        )

        tk.Label(
            formulario,
            text="Categoría:",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).pack(anchor="w", pady=(8, 3))

        categoria = ttk.Combobox(
            formulario,
            values=["Medicamentos", "Vacunas"],
            state="readonly",
            font=FONT_NORMAL
        )
        categoria.pack(fill="x", ipady=3)

        if producto:
            categoria.set(producto.get("categoria") or "Medicamentos")
        else:
            categoria.set("Medicamentos")

        agregar_campo(
            "descripcion",
            "Descripción:",
            producto.get("descripcion", "") if producto else ""
        )

        agregar_campo(
            "precio",
            "Precio:",
            producto.get("precio", 0) if producto else ""
        )

        agregar_campo(
            "stock",
            "Cantidad en stock:",
            producto.get("stock", 0) if producto else "0"
        )

        agregar_campo(
            "stock_minimo",
            "Stock mínimo:",
            producto.get("stock_minimo", 5) if producto else "5"
        )

        tk.Label(
            formulario,
            text="Estado:",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).pack(anchor="w", pady=(8, 3))

        estado = ttk.Combobox(
            formulario,
            values=["Activo", "Inactivo"],
            state="readonly",
            font=FONT_NORMAL
        )
        estado.pack(fill="x", ipady=3)
        estado.set(producto.get("estado", "Activo") if producto else "Activo")

        def guardar():
            nombre = entradas["nombre"].get().strip()
            descripcion = entradas["descripcion"].get().strip()

            if not nombre:
                messagebox.showwarning(
                    "Validación",
                    "Ingresá el nombre del producto.",
                    parent=ventana
                )
                return

            try:
                precio = float(entradas["precio"].get())
                stock = int(entradas["stock"].get())
                stock_minimo = int(entradas["stock_minimo"].get())

                if precio < 0 or stock < 0 or stock_minimo < 0:
                    raise ValueError

            except ValueError:
                messagebox.showwarning(
                    "Validación",
                    "El precio y las cantidades deben ser números válidos y no negativos.",
                    parent=ventana
                )
                return

            datos = {
                "nombre": nombre,
                "categoria": categoria.get(),
                "descripcion": descripcion or None,
                "precio": precio,
                "stock": stock,
                "stock_minimo": stock_minimo,
                "estado": estado.get()
            }

            if producto:
                respuesta = APIService.put(
                    f"/productos/{producto['id']}",
                    datos
                )
                mensaje = "Producto actualizado correctamente."
            else:
                respuesta = APIService.post(
                    "/productos/",
                    datos
                )
                mensaje = "Producto registrado correctamente."

            if respuesta is not None:
                messagebox.showinfo(
                    "Éxito",
                    mensaje,
                    parent=ventana
                )
                ventana.destroy()
                self.cargar_productos()
            else:
                messagebox.showerror(
                    "Error",
                    "No se pudo guardar el producto. Revisá los datos.",
                    parent=ventana
                )

        tk.Button(
            ventana,
            text="Guardar",
            command=guardar,
            bg=COLORS["success"],
            fg=COLORS["white"],
            font=FONT_NORMAL,
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=20)

    def obtener_seleccionado(self):
        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Atención",
                "Seleccioná un producto de la tabla."
            )
            return None

        valores = self.tabla.item(seleccion[0], "values")
        return valores[0]

    def editar_producto(self):
        producto_id = self.obtener_seleccionado()

        if producto_id is None:
            return

        producto = APIService.get(f"/productos/{producto_id}")

        if producto is None:
            messagebox.showerror(
                "Error",
                "No se pudo obtener el producto."
            )
            return

        self.formulario_producto(producto)

    def eliminar_producto(self):
        producto_id = self.obtener_seleccionado()

        if producto_id is None:
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Estás segura de que querés eliminar este producto?"
        )

        if not confirmar:
            return

        respuesta = APIService.delete(
            f"/productos/{producto_id}"
        )

        if respuesta is not None:
            messagebox.showinfo(
                "Éxito",
                "Producto eliminado correctamente."
            )
            self.cargar_productos()
        else:
            messagebox.showerror(
                "Error",
                "No se pudo eliminar el producto. "
                "Si ya fue utilizado en una venta, probá cambiar su estado a Inactivo."
            )
