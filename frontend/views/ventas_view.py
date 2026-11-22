
import tkinter as tk
from tkinter import ttk, messagebox
from urllib.parse import quote

from frontend.config import COLORS, FONT_NORMAL, FONT_SUBTITLE
from frontend.services.api_service import APIService


class VentasView:

    def __init__(self, parent):
        self.parent = parent
        self.items_venta = []
        self.clientes = []
        self.productos = []
        self.servicios = []

        self.crear_interfaz()
        self.cargar_ventas()

    # ==========================================
    # INTERFAZ PRINCIPAL
    # ==========================================

    def crear_interfaz(self):

        encabezado = tk.Frame(
            self.parent,
            bg=COLORS["background"]
        )
        encabezado.pack(fill="x", pady=(0, 15))

        tk.Label(
            encabezado,
            text="Gestión de ventas",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_SUBTITLE
        ).pack(side="left")

        tk.Button(
            encabezado,
            text="+ Nueva venta",
            command=self.formulario_venta,
            bg=COLORS["primary"],
            fg=COLORS["white"],
            font=FONT_NORMAL,
            relief="flat",
            padx=12,
            pady=7,
            cursor="hand2"
        ).pack(side="right")

        tabla_frame = tk.Frame(
            self.parent,
            bg=COLORS["white"]
        )
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("id", "cliente", "fecha", "total")

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            height=18
        )

        encabezados = {
            "id": "ID",
            "cliente": "Cliente",
            "fecha": "Fecha",
            "total": "Total"
        }

        anchos = {
            "id": 60,
            "cliente": 250,
            "fecha": 200,
            "total": 150
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

        scrollbar = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(
            yscrollcommand=scrollbar.set
        )

        self.tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        botones = tk.Frame(
            self.parent,
            bg=COLORS["background"]
        )
        botones.pack(fill="x", pady=15)

        tk.Button(
            botones,
            text="Ver detalle",
            command=self.ver_detalle,
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
            text="Actualizar listado",
            command=self.cargar_ventas,
            bg=COLORS["sidebar"],
            fg=COLORS["white"],
            font=FONT_NORMAL,
            relief="flat",
            padx=12,
            pady=7,
            cursor="hand2"
        ).pack(side="right")

    # ==========================================
    # CARGAR VENTAS
    # ==========================================

    def cargar_ventas(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        ventas = APIService.get("/ventas/")

        if ventas is None:
            messagebox.showerror(
                "Error",
                "No se pudieron cargar las ventas."
            )
            return

        for venta in ventas:

            nombre_cliente = (
                f"{venta.get('nombre_cliente', '')} "
                f"{venta.get('apellido_cliente', '')}"
            ).strip()

            if not nombre_cliente:
                nombre_cliente = (
                    f"Cliente #{venta.get('cliente_id', '')}"
                )

            valores = (
                venta.get("id"),
                nombre_cliente,
                venta.get("fecha", ""),
                f"$ {venta.get('total', 0):,.2f}"
            )

            self.tabla.insert(
                "",
                "end",
                values=valores
            )

    # ==========================================
    # FORMULARIO DE NUEVA VENTA
    # ==========================================

    def formulario_venta(self):

        self.items_venta = []

        ventana = tk.Toplevel(self.parent)
        ventana.title("Registrar venta")
        # Adaptar el tamaño a la resolución disponible para que el pie
        # de acciones nunca quede fuera de la pantalla.
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()

        ancho_ventana = min(900, ancho_pantalla - 60)
        alto_ventana = min(650, alto_pantalla - 120)

        # Evitar tamaños demasiado pequeños en pantallas de baja resolución.
        ancho_ventana = max(600, ancho_ventana)
        alto_ventana = max(450, alto_ventana)

        posicion_x = max(0, (ancho_pantalla - ancho_ventana) // 2)
        posicion_y = max(0, (alto_pantalla - alto_ventana) // 2)

        ventana.geometry(
            f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}"
        )
        ventana.minsize(min(600, ancho_ventana), min(450, alto_ventana))
        ventana.resizable(True, True)
        ventana.transient(self.parent.winfo_toplevel())
        ventana.grab_set()
        ventana.configure(bg=COLORS["background"])

        # El contenido del formulario se desplaza verticalmente.
        # Los botones inferiores quedan fijos y siempre visibles.
        contenedor_scroll = tk.Frame(
            ventana,
            bg=COLORS["background"]
        )
        contenedor_scroll.pack(
            side="top",
            fill="both",
            expand=True
        )

        canvas = tk.Canvas(
            contenedor_scroll,
            bg=COLORS["background"],
            highlightthickness=0
        )
        scrollbar_formulario = ttk.Scrollbar(
            contenedor_scroll,
            orient="vertical",
            command=canvas.yview
        )
        canvas.configure(yscrollcommand=scrollbar_formulario.set)

        scrollbar_formulario.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        formulario_contenido = tk.Frame(
            canvas,
            bg=COLORS["background"]
        )
        ventana_canvas = canvas.create_window(
            (0, 0),
            window=formulario_contenido,
            anchor="nw"
        )

        def actualizar_scrollregion(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def ajustar_ancho_contenido(event):
            canvas.itemconfigure(ventana_canvas, width=event.width)

        formulario_contenido.bind(
            "<Configure>",
            actualizar_scrollregion
        )
        canvas.bind("<Configure>", ajustar_ancho_contenido)

        def desplazar_formulario(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", desplazar_formulario)
        formulario_contenido.bind("<MouseWheel>", desplazar_formulario)

        tk.Label(
            formulario_contenido,
            text="Registrar nueva venta",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_SUBTITLE
        ).pack(pady=12)

        formulario = tk.Frame(
            formulario_contenido,
            bg=COLORS["background"]
        )
        formulario.pack(fill="x", padx=25)

        # ======================================
        # CLIENTE: BUSQUEDA POR DNI
        # ======================================

        tk.Label(
            formulario,
            text="DNI del cliente:",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).pack(anchor="w", pady=(5, 3))

        cliente_frame = tk.Frame(
            formulario,
            bg=COLORS["background"]
        )
        cliente_frame.pack(fill="x")

        entrada_dni = tk.Entry(
            cliente_frame,
            font=FONT_NORMAL,
            relief="solid",
            bd=1
        )
        entrada_dni.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=5,
            padx=(0, 10)
        )

        cliente_seleccionado = {"datos": None}

        confirmacion_cliente = tk.Label(
            formulario,
            text="Ingresá el DNI y presioná Buscar.",
            bg=COLORS["background"],
            fg=COLORS["secondary_text"],
            font=FONT_NORMAL,
            anchor="w"
        )
        confirmacion_cliente.pack(
            fill="x",
            pady=(5, 2)
        )

        def buscar_cliente(event=None):

            dni = entrada_dni.get().strip()

            if not dni:
                cliente_seleccionado["datos"] = None
                confirmacion_cliente.config(
                    text="Ingresá un DNI para buscar.",
                    fg=COLORS["danger"]
                )
                messagebox.showwarning(
                    "DNI requerido",
                    "Ingresá el DNI del cliente.",
                    parent=ventana
                )
                entrada_dni.focus_set()
                return

            cliente_seleccionado["datos"] = None
            confirmacion_cliente.config(
                text="Buscando cliente...",
                fg=COLORS["secondary_text"]
            )
            ventana.update_idletasks()

            cliente = APIService.get(
                f"/clientes/buscar/{dni}"
            )

            if cliente is None:
                confirmacion_cliente.config(
                    text="No se encontró ningún cliente con ese DNI.",
                    fg=COLORS["danger"]
                )
                messagebox.showwarning(
                    "Cliente no encontrado",
                    "No existe un cliente registrado con ese DNI. "
                    "Verificá el número e intentá nuevamente.",
                    parent=ventana
                )
                entrada_dni.focus_set()
                return

            nombre_completo = (
                f"{cliente.get('nombre', '')} "
                f"{cliente.get('apellido', '')}"
            ).strip()

            estado_cliente = cliente.get("estado", "Activo")

            if estado_cliente != "Activo":
                cliente_seleccionado["datos"] = None
                confirmacion_cliente.config(
                    text=(
                        f"⚠ Cliente encontrado: {nombre_completo} "
                        f"(ID: {cliente.get('id')}) - Estado: {estado_cliente}. "
                        "No puede realizar ventas."
                    ),
                    fg=COLORS["danger"]
                )
                messagebox.showwarning(
                    "Cliente inactivo",
                    "El cliente está inactivo y no puede realizar una venta.",
                    parent=ventana
                )
                entrada_dni.focus_set()
                return

            cliente_seleccionado["datos"] = cliente

            confirmacion_cliente.config(
                text=(
                    f"✓ Cliente encontrado: {nombre_completo} "
                    f"(ID: {cliente.get('id')}) - Estado: {estado_cliente}"
                ),
                fg=COLORS["success"]
            )

        tk.Button(
            cliente_frame,
            text="Buscar",
            command=buscar_cliente,
            bg=COLORS["primary"],
            fg=COLORS["white"],
            font=FONT_NORMAL,
            relief="flat",
            padx=16,
            pady=5,
            cursor="hand2"
        ).pack(side="right")

        entrada_dni.bind("<Return>", buscar_cliente)

        # ======================================
        # TIPO DE ARTICULO
        # ======================================

        tk.Label(
            formulario,
            text="Tipo de artículo:",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).pack(anchor="w", pady=(10, 3))

        selector_tipo = ttk.Combobox(
            formulario,
            values=["Producto", "Servicio"],
            state="readonly",
            font=FONT_NORMAL
        )
        selector_tipo.pack(fill="x", ipady=4)
        selector_tipo.set("Producto")

        # ======================================
        # BUSQUEDA DE ARTICULOS
        # ======================================

        tk.Label(
            formulario,
            text="Buscar artículo por nombre:",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).pack(anchor="w", pady=(10, 3))

        busqueda_frame = tk.Frame(
            formulario,
            bg=COLORS["background"]
        )
        busqueda_frame.pack(fill="x")

        entrada_articulo = tk.Entry(
            busqueda_frame,
            font=FONT_NORMAL,
            relief="solid",
            bd=1
        )
        entrada_articulo.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=5,
            padx=(0, 10)
        )

        opciones_articulos = {}
        articulo_seleccionado = {"datos": None}

        selector_articulo = ttk.Combobox(
            formulario,
            state="readonly",
            font=FONT_NORMAL
        )
        selector_articulo.pack(fill="x", pady=(7, 3))

        informacion_articulo = tk.Label(
            formulario,
            text="Buscá un artículo para ver sus datos.",
            bg=COLORS["background"],
            fg=COLORS["secondary_text"],
            font=FONT_NORMAL,
            anchor="w"
        )
        informacion_articulo.pack(fill="x", pady=(3, 2))

        def mostrar_articulo(event=None):

            etiqueta = selector_articulo.get()
            articulo = opciones_articulos.get(etiqueta)
            articulo_seleccionado["datos"] = articulo

            if not articulo:
                informacion_articulo.config(
                    text="Seleccioná un artículo de la lista.",
                    fg=COLORS["secondary_text"]
                )
                return

            tipo = selector_tipo.get()

            if tipo == "Producto":
                stock = articulo.get("stock", 0)

                informacion_articulo.config(
                    text=(
                        f"✓ ID: {articulo['id']} | "
                        f"Precio unitario: $ {articulo['precio']:,.2f} | "
                        f"Stock disponible: {stock}"
                    ),
                    fg=(
                        COLORS["success"]
                        if stock > 0
                        else COLORS["danger"]
                    )
                )
            else:
                informacion_articulo.config(
                    text=(
                        f"✓ ID: {articulo['id']} | "
                        f"Precio unitario: $ {articulo['precio']:,.2f}"
                    ),
                    fg=COLORS["success"]
                )

        def buscar_articulo(event=None):

            nombre = entrada_articulo.get().strip()

            articulo_seleccionado["datos"] = None
            opciones_articulos.clear()
            selector_articulo.set("")
            selector_articulo["values"] = []

            if not nombre:
                informacion_articulo.config(
                    text="Ingresá un nombre para buscar.",
                    fg=COLORS["danger"]
                )
                entrada_articulo.focus_set()
                return

            informacion_articulo.config(
                text="Buscando...",
                fg=COLORS["secondary_text"]
            )
            ventana.update_idletasks()

            tipo = selector_tipo.get()
            endpoint = (
                "/productos/buscar"
                if tipo == "Producto"
                else "/servicios/buscar"
            )

            resultados = APIService.get(
                f"{endpoint}?nombre={quote(nombre)}"
            )

            if resultados is None:
                informacion_articulo.config(
                    text="No se pudo realizar la búsqueda.",
                    fg=COLORS["danger"]
                )
                return

            if not resultados:
                informacion_articulo.config(
                    text="No se encontraron artículos con ese nombre.",
                    fg=COLORS["danger"]
                )
                return

            for articulo in resultados:
                etiqueta = f"{articulo['id']} - {articulo['nombre']}"

                if tipo == "Producto":
                    etiqueta += f" (Stock: {articulo.get('stock', 0)})"

                opciones_articulos[etiqueta] = articulo

            selector_articulo["values"] = list(
                opciones_articulos.keys()
            )

            if len(resultados) == 1:
                primera_opcion = list(opciones_articulos.keys())[0]
                selector_articulo.set(primera_opcion)
                mostrar_articulo()
            else:
                informacion_articulo.config(
                    text=(
                        f"Se encontraron {len(resultados)} resultados. "
                        "Seleccioná uno de la lista."
                    ),
                    fg=COLORS["success"]
                )

        tk.Button(
            busqueda_frame,
            text="Buscar",
            command=buscar_articulo,
            bg=COLORS["primary"],
            fg=COLORS["white"],
            font=FONT_NORMAL,
            relief="flat",
            padx=16,
            pady=5,
            cursor="hand2"
        ).pack(side="right")

        entrada_articulo.bind("<Return>", buscar_articulo)

        selector_articulo.bind(
            "<<ComboboxSelected>>",
            mostrar_articulo
        )

        def cambiar_tipo(event=None):
            entrada_articulo.delete(0, tk.END)
            selector_articulo.set("")
            selector_articulo["values"] = []
            opciones_articulos.clear()
            articulo_seleccionado["datos"] = None

            informacion_articulo.config(
                text="Buscá un artículo para ver sus datos.",
                fg=COLORS["secondary_text"]
            )

        selector_tipo.bind(
            "<<ComboboxSelected>>",
            cambiar_tipo
        )

        # ======================================
        # CANTIDAD Y BOTON AGREGAR
        # ======================================

        cantidad_frame = tk.Frame(
            formulario,
            bg=COLORS["background"]
        )
        cantidad_frame.pack(fill="x", pady=10)

        tk.Label(
            cantidad_frame,
            text="Cantidad:",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).pack(side="left")

        entrada_cantidad = tk.Entry(
            cantidad_frame,
            width=10,
            font=FONT_NORMAL,
            relief="solid",
            bd=1
        )
        entrada_cantidad.pack(
            side="left",
            padx=10,
            ipady=4
        )
        entrada_cantidad.insert(0, "1")

        # ======================================
        # TABLA DE ARTICULOS
        # ======================================

        tabla_titulo = tk.Label(
            formulario_contenido,
            text="Artículos de la venta",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_SUBTITLE
        )
        tabla_titulo.pack(
            anchor="w",
            padx=25,
            pady=(12, 8)
        )

        tabla_frame = tk.Frame(
            formulario_contenido,
            bg=COLORS["white"],
            height=170
        )
        tabla_frame.pack(
            fill="x",
            padx=25
        )
        tabla_frame.pack_propagate(False)

        columnas = (
            "tipo",
            "nombre",
            "cantidad",
            "precio"
        )

        tabla_items = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            height=5
        )

        titulos = {
            "tipo": "Tipo",
            "nombre": "Artículo",
            "cantidad": "Cantidad",
            "precio": "Precio unitario"
        }

        anchos = {
            "tipo": 100,
            "nombre": 250,
            "cantidad": 100,
            "precio": 140
        }

        for columna in columnas:

            tabla_items.heading(
                columna,
                text=titulos[columna]
            )

            tabla_items.column(
                columna,
                width=anchos[columna],
                anchor="center"
            )

        tabla_items.pack(
            fill="both",
            expand=True
        )

        # ======================================
        # TOTAL
        # ======================================

        total_label = tk.Label(
            formulario_contenido,
            text="Total estimado: $ 0.00",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_SUBTITLE
        )
        total_label.pack(
            anchor="e",
            padx=25,
            pady=10
        )

        # ======================================
        # ACTUALIZAR TABLA
        # ======================================

        def actualizar_tabla():

            for fila in tabla_items.get_children():
                tabla_items.delete(fila)

            total = 0

            for item in self.items_venta:

                subtotal = item["precio"] * item["cantidad"]
                total += subtotal

                tabla_items.insert(
                    "",
                    "end",
                    values=(
                        item["tipo"],
                        item["nombre"],
                        item["cantidad"],
                        f"$ {item['precio']:,.2f}"
                    )
                )

            total_label.config(
                text=f"Total estimado: $ {total:,.2f}"
            )

        # ======================================
        # AGREGAR ARTICULO
        # ======================================

        def agregar_articulo():

            articulo = articulo_seleccionado["datos"]

            if not articulo:
                messagebox.showwarning(
                    "Atención",
                    "Primero buscá y seleccioná un artículo.",
                    parent=ventana
                )
                return

            try:
                cantidad = int(entrada_cantidad.get())

                if cantidad <= 0:
                    raise ValueError

            except ValueError:
                messagebox.showwarning(
                    "Cantidad inválida",
                    "Ingresá una cantidad mayor a cero.",
                    parent=ventana
                )
                return

            tipo = selector_tipo.get()

            if tipo == "Producto":
                stock_disponible = articulo.get("stock", 0)

                cantidad_existente = sum(
                    item["cantidad"]
                    for item in self.items_venta
                    if item["tipo"] == "Producto"
                    and item["id"] == articulo["id"]
                )

                if stock_disponible <= 0:
                    messagebox.showwarning(
                        "Sin stock",
                        "Este producto no tiene unidades disponibles.",
                        parent=ventana
                    )
                    return

                if cantidad + cantidad_existente > stock_disponible:
                    messagebox.showwarning(
                        "Stock insuficiente",
                        f"Stock disponible: {stock_disponible} unidades.",
                        parent=ventana
                    )
                    return

                item = {
                    "tipo": "Producto",
                    "id": articulo["id"],
                    "nombre": articulo["nombre"],
                    "precio": float(articulo["precio"]),
                    "cantidad": cantidad
                }
            else:
                item = {
                    "tipo": "Servicio",
                    "id": articulo["id"],
                    "nombre": articulo["nombre"],
                    "precio": float(articulo["precio"]),
                    "cantidad": cantidad
                }

            self.items_venta.append(item)
            actualizar_tabla()

            entrada_cantidad.delete(0, tk.END)
            entrada_cantidad.insert(0, "1")

        # ======================================
        # QUITAR ARTICULO
        # ======================================

        def quitar_articulo():

            seleccion = tabla_items.selection()

            if not seleccion:
                messagebox.showwarning(
                    "Atención",
                    "Seleccioná un artículo para quitar.",
                    parent=ventana
                )
                return

            indice = tabla_items.index(seleccion[0])

            self.items_venta.pop(indice)

            actualizar_tabla()

        # ======================================
        # GUARDAR VENTA
        # ======================================

        def guardar_venta():

            if not self.items_venta:
                messagebox.showwarning(
                    "Atención",
                    "Agregá al menos un artículo a la venta.",
                    parent=ventana
                )
                return

            cliente = cliente_seleccionado["datos"]

            if not cliente:
                messagebox.showwarning(
                    "Atención",
                    "Primero buscá y seleccioná un cliente válido por DNI.",
                    parent=ventana
                )
                entrada_dni.focus_set()
                return

            cliente_id = cliente["id"]

            items_api = []

            for item in self.items_venta:

                if item["tipo"] == "Producto":

                    items_api.append({
                        "producto_id": item["id"],
                        "cantidad": item["cantidad"]
                    })

                else:

                    items_api.append({
                        "servicio_id": item["id"],
                        "cantidad": item["cantidad"]
                    })

            datos = {
                "cliente_id": cliente_id,
                "items": items_api
            }

            respuesta = APIService.post(
                "/ventas/",
                datos
            )

            if respuesta is not None:

                messagebox.showinfo(
                    "Éxito",
                    "La venta se registró correctamente.",
                    parent=ventana
                )

                ventana.destroy()
                self.cargar_ventas()

            else:

                messagebox.showerror(
                    "Error",
                    "No se pudo registrar la venta. "
                    "Verificá el stock y los datos ingresados.",
                    parent=ventana
                )

        # ======================================
        # BOTONES
        # ======================================

        tk.Button(
            cantidad_frame,
            text="Agregar artículo",
            command=agregar_articulo,
            bg=COLORS["primary"],
            fg=COLORS["white"],
            font=FONT_NORMAL,
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        ).pack(side="left", padx=10)

        acciones_frame = tk.Frame(
            ventana,
            bg=COLORS["background"]
        )
        acciones_frame.pack(
            side="bottom",
            fill="x",
            padx=25,
            pady=12
        )

        tk.Button(
            acciones_frame,
            text="Quitar artículo seleccionado",
            command=quitar_articulo,
            bg=COLORS["danger"],
            fg=COLORS["white"],
            font=FONT_NORMAL,
            relief="flat",
            padx=10,
            pady=7,
            cursor="hand2"
        ).pack(side="left")

        tk.Button(
            acciones_frame,
            text="Registrar venta",
            command=guardar_venta,
            bg=COLORS["success"],
            fg=COLORS["white"],
            font=FONT_NORMAL,
            relief="flat",
            padx=20,
            pady=7,
            cursor="hand2"
        ).pack(side="right")

    # ==========================================
    # OBTENER VENTA SELECCIONADA
    # ==========================================

    def obtener_seleccionado(self):

        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Atención",
                "Seleccioná una venta de la tabla."
            )
            return None

        valores = self.tabla.item(
            seleccion[0],
            "values"
        )

        return valores[0]

    # ==========================================
    # VER DETALLE DE VENTA
    # ==========================================

    def ver_detalle(self):

        venta_id = self.obtener_seleccionado()

        if venta_id is None:
            return

        detalle = APIService.get(
            f"/ventas/{venta_id}"
        )

        if detalle is None:
            messagebox.showerror(
                "Error",
                "No se pudo obtener el detalle de la venta."
            )
            return

        ventana = tk.Toplevel(self.parent)
        ventana.title(f"Detalle de venta #{venta_id}")
        ventana.geometry("750x480")
        ventana.configure(bg=COLORS["background"])
        ventana.transient(self.parent.winfo_toplevel())

        tk.Label(
            ventana,
            text=f"Detalle de venta #{venta_id}",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_SUBTITLE
        ).pack(pady=15)

        cliente = (
            f"{detalle.get('nombre_cliente', '')} "
            f"{detalle.get('apellido_cliente', '')}"
        ).strip()

        if not cliente:
            cliente = (
                f"Cliente #{detalle.get('cliente_id', '')}"
            )

        tk.Label(
            ventana,
            text=f"Cliente: {cliente}",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).pack(
            anchor="w",
            padx=25,
            pady=3
        )

        tk.Label(
            ventana,
            text=f"Fecha: {detalle.get('fecha', '')}",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).pack(
            anchor="w",
            padx=25,
            pady=3
        )

        tk.Label(
            ventana,
            text="Artículos:",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).pack(
            anchor="w",
            padx=25,
            pady=(15, 5)
        )

        tabla_detalle = ttk.Treeview(
            ventana,
            columns=(
                "tipo",
                "articulo",
                "cantidad",
                "precio",
                "subtotal"
            ),
            show="headings",
            height=9
        )

        titulos = {
            "tipo": "Tipo",
            "articulo": "Artículo",
            "cantidad": "Cantidad",
            "precio": "Precio unitario",
            "subtotal": "Subtotal"
        }

        anchos = {
            "tipo": 100,
            "articulo": 180,
            "cantidad": 80,
            "precio": 140,
            "subtotal": 140
        }

        for columna, titulo in titulos.items():

            tabla_detalle.heading(
                columna,
                text=titulo
            )

            tabla_detalle.column(
                columna,
                anchor="center",
                width=anchos[columna]
            )

        tabla_detalle.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=5
        )

        items = detalle.get("detalles", [])

        for item in items:

            tabla_detalle.insert(
                "",
                "end",
                values=(
                    item.get("tipo", ""),
                    item.get("concepto", "Artículo"),
                    item.get("cantidad", 0),
                    f"$ {item.get('precio_unitario', 0):,.2f}",
                    f"$ {item.get('subtotal', 0):,.2f}"
                )
            )

        tk.Label(
            ventana,
            text=f"Total: $ {detalle.get('total', 0):,.2f}",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_SUBTITLE
        ).pack(
            anchor="e",
            padx=25,
            pady=12
        )
