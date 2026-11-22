
import tkinter as tk
from tkinter import ttk, messagebox

from frontend.config import COLORS, FONT_NORMAL, FONT_SUBTITLE, FONT_BUTTON
from frontend.services.api_service import APIService


class ConsultasView(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["background"])

        self.pack(fill="both", expand=True)

        self.mascotas = []
        self.turnos = []
        self.consultas = []
        self.filtro_mascotas = {}

        self.crear_interfaz()
        self.cargar_consultas()

    def crear_interfaz(self):

        top = tk.Frame(self, bg=COLORS["background"])
        top.pack(fill="x", pady=(0, 15))

        tk.Label(
            top,
            text="Historial de consultas",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_SUBTITLE
        ).pack(side="left")

        tk.Button(
            top,
            text="+ Nueva consulta",
            bg=COLORS["primary"],
            fg="white",
            font=FONT_NORMAL,
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.nueva_consulta
        ).pack(side="right")

        # Filtro por mascota
        filtro = tk.Frame(self, bg=COLORS["background"])
        filtro.pack(fill="x", pady=(0, 12))

        tk.Label(
            filtro,
            text="Filtrar por mascota:",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).pack(side="left", padx=(0, 8))

        self.selector_filtro = ttk.Combobox(
            filtro,
            state="readonly",
            width=28
        )
        self.selector_filtro.pack(side="left", padx=5)

        tk.Button(
            filtro,
            text="Ver historial",
            command=self.filtrar_historial
        ).pack(side="left", padx=5)

        tk.Button(
            filtro,
            text="Ver todas",
            command=self.cargar_consultas
        ).pack(side="left", padx=5)

        # Tabla
        columnas = (
            "id",
            "mascota",
            "turno_id",
            "fecha",
            "diagnostico",
            "observaciones"
        )

        self.tabla = ttk.Treeview(
            self,
            columns=columnas,
            show="headings",
            height=13
        )

        encabezados = {
            "id": "ID",
            "mascota": "Mascota",
            "turno_id": "Turno",
            "fecha": "Fecha",
            "diagnostico": "Diagnóstico",
            "observaciones": "Observaciones"
        }

        anchos = {
            "id": 45,
            "mascota": 110,
            "turno_id": 65,
            "fecha": 100,
            "diagnostico": 280,
            "observaciones": 280
        }

        for columna, titulo in encabezados.items():
            self.tabla.heading(columna, text=titulo)
            self.tabla.column(
                columna,
                anchor="center",
                width=anchos[columna],
                minwidth=55
            )

        self.tabla.pack(fill="both", expand=True)

        # Acciones
        acciones = tk.Frame(self, bg=COLORS["background"])
        acciones.pack(fill="x", pady=12)

        tk.Button(
            acciones,
            text="Actualizar lista",
            command=self.cargar_consultas
        ).pack(side="left", padx=4)

        tk.Button(
            acciones,
            text="Editar consulta",
            command=self.editar_consulta
        ).pack(side="left", padx=4)

        tk.Button(
            acciones,
            text="Eliminar consulta",
            command=self.eliminar_consulta
        ).pack(side="left", padx=4)

    def cargar_datos(self):

        mascotas = APIService.get("/mascotas/")
        turnos = APIService.get("/turnos/")

        if mascotas is None or turnos is None:
            messagebox.showerror(
                "Error",
                "No se pudieron cargar las mascotas o los turnos."
            )
            return False

        self.mascotas = mascotas
        self.turnos = turnos

        return True

    def obtener_nombre_mascota(self, mascota_id):

        for mascota in self.mascotas:
            if mascota.get("id") == mascota_id:
                return mascota.get("nombre", f"ID {mascota_id}")

        return f"ID {mascota_id}"

    def obtener_mascota_del_turno(self, turno_id):

        for turno in self.turnos:
            if turno.get("id") == turno_id:
                return turno.get("mascota_id")

        return None

    def actualizar_filtro(self):

        opciones = {
            f"{m.get('nombre', '')} (ID: {m.get('id')})": m.get("id")
            for m in self.mascotas
        }

        self.filtro_mascotas = opciones

        self.selector_filtro["values"] = [
            "Todas las mascotas"
        ] + list(opciones.keys())

        self.selector_filtro.set("Todas las mascotas")

    def cargar_consultas(self):

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        if not self.cargar_datos():
            return

        self.actualizar_filtro()

        consultas = APIService.get("/consultas/")

        if consultas is None:
            messagebox.showerror(
                "Error",
                "No se pudieron cargar las consultas."
            )
            return

        self.consultas = consultas
        self.mostrar_consultas(consultas)

    def mostrar_consultas(self, consultas):

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for consulta in consultas:

            mascota_id = self.obtener_mascota_del_turno(
                consulta.get("turno_id")
            )

            nombre_mascota = self.obtener_nombre_mascota(
                mascota_id
            ) if mascota_id is not None else "No disponible"

            self.tabla.insert(
                "",
                "end",
                values=(
                    consulta.get("id"),
                    nombre_mascota,
                    consulta.get("turno_id"),
                    consulta.get("fecha"),
                    consulta.get("diagnostico"),
                    consulta.get("observaciones") or ""
                )
            )

    def filtrar_historial(self):

        seleccion = self.selector_filtro.get()

        if not seleccion:
            return

        if seleccion == "Todas las mascotas":
            self.cargar_consultas()
            return

        mascota_id = self.filtro_mascotas.get(seleccion)

        if mascota_id is None:
            return

        historial = APIService.get(
            f"/consultas/mascota/{mascota_id}"
        )

        if historial is None:
            messagebox.showerror(
                "Error",
                "No se pudo obtener el historial de la mascota."
            )
            return

        self.mostrar_consultas(historial)

    def obtener_consulta_seleccionada(self):

        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Atención",
                "Seleccioná una consulta de la lista."
            )
            return None

        valores = self.tabla.item(
            seleccionado[0],
            "values"
        )

        consulta_id = valores[0]

        consulta = APIService.get(
            f"/consultas/{consulta_id}"
        )

        if consulta is None:
            messagebox.showerror(
                "Error",
                "No se pudo obtener la consulta."
            )
            return None

        return consulta

    def nueva_consulta(self):
        self.formulario_consulta()

    def editar_consulta(self):

        consulta = self.obtener_consulta_seleccionada()

        if consulta is None:
            return

        self.formulario_consulta(consulta)

    def formulario_consulta(self, consulta=None):

        if not self.cargar_datos():
            return

        ventana = tk.Toplevel(self)
        ventana.title("Consulta clínica")
        ventana.geometry("560x520")
        ventana.resizable(False, False)
        ventana.configure(bg=COLORS["white"])
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        tk.Label(
            ventana,
            text="Datos de la consulta",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_SUBTITLE
        ).pack(pady=18)

        formulario = tk.Frame(
            ventana,
            bg=COLORS["white"]
        )
        formulario.pack(fill="both", expand=True, padx=30)

        # Turnos disponibles para registrar una consulta
        turnos_con_consulta = {
            c.get("turno_id")
            for c in (APIService.get("/consultas/") or [])
        }

        turnos_disponibles = [
            t for t in self.turnos
            if t.get("estado") == "En curso"
            and t.get("id") not in turnos_con_consulta
        ]

        tk.Label(
            formulario,
            text="Turno",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=0, column=0, sticky="w", pady=12)

        opciones_turnos = {}

        for turno in turnos_disponibles:

            mascota = self.obtener_nombre_mascota(
                turno.get("mascota_id")
            )

            etiqueta = (
                f"Turno {turno.get('id')} - "
                f"{mascota} - "
                f"{turno.get('fecha')} {turno.get('hora')}"
            )

            opciones_turnos[etiqueta] = turno

        selector_turno = ttk.Combobox(
            formulario,
            width=38,
            state="readonly",
            values=list(opciones_turnos.keys())
        )
        selector_turno.grid(row=0, column=1, padx=10, pady=12)

        # Fecha
        tk.Label(
            formulario,
            text="Fecha (AAAA-MM-DD)",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=1, column=0, sticky="w", pady=12)

        entrada_fecha = tk.Entry(formulario, width=41)
        entrada_fecha.grid(row=1, column=1, padx=10, pady=12)

        # Diagnóstico
        tk.Label(
            formulario,
            text="Diagnóstico",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=2, column=0, sticky="nw", pady=12)

        entrada_diagnostico = tk.Text(
            formulario,
            width=30,
            height=5
        )
        entrada_diagnostico.grid(
            row=2,
            column=1,
            padx=10,
            pady=12
        )

        # Observaciones
        tk.Label(
            formulario,
            text="Observaciones",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=3, column=0, sticky="nw", pady=12)

        entrada_observaciones = tk.Text(
            formulario,
            width=30,
            height=4
        )
        entrada_observaciones.grid(
            row=3,
            column=1,
            padx=10,
            pady=12
        )

        if consulta:

            entrada_fecha.insert(
                0,
                consulta.get("fecha") or ""
            )

            entrada_diagnostico.insert(
                "1.0",
                consulta.get("diagnostico") or ""
            )

            entrada_observaciones.insert(
                "1.0",
                consulta.get("observaciones") or ""
            )

            selector_turno.set(
                f"Turno {consulta.get('turno_id')}"
            )
            selector_turno.configure(state="disabled")

        elif turnos_disponibles:

            primer_turno = turnos_disponibles[0]

            for etiqueta, turno in opciones_turnos.items():
                if turno.get("id") == primer_turno.get("id"):
                    selector_turno.set(etiqueta)
                    entrada_fecha.insert(
                        0,
                        primer_turno.get("fecha") or ""
                    )
                    break

        else:
            selector_turno.configure(state="disabled")

            tk.Label(
                formulario,
                text="No hay turnos en curso disponibles para registrar.",
                bg=COLORS["white"],
                fg=COLORS["danger"],
                font=FONT_NORMAL
            ).grid(row=4, column=0, columnspan=2, pady=8)

        def actualizar_fecha(event=None):

            turno = opciones_turnos.get(selector_turno.get())

            if turno:
                entrada_fecha.delete(0, "end")
                entrada_fecha.insert(
                    0,
                    turno.get("fecha") or ""
                )

        selector_turno.bind(
            "<<ComboboxSelected>>",
            actualizar_fecha
        )

        def guardar():

            fecha = entrada_fecha.get().strip()
            diagnostico = entrada_diagnostico.get(
                "1.0",
                "end"
            ).strip()

            observaciones = entrada_observaciones.get(
                "1.0",
                "end"
            ).strip()

            if len(fecha) != 10:
                messagebox.showwarning(
                    "Atención",
                    "Ingresá la fecha con formato AAAA-MM-DD."
                )
                return

            if len(diagnostico) < 2 or len(diagnostico) > 500:
                messagebox.showwarning(
                    "Atención",
                    "El diagnóstico debe tener entre 2 y 500 caracteres."
                )
                return

            if consulta:
                datos = {
                    "fecha": fecha,
                    "diagnostico": diagnostico,
                    "observaciones": observaciones or None
                }

                resultado = APIService.put(
                    f"/consultas/{consulta['id']}",
                    datos
                )

            else:

                turno = opciones_turnos.get(
                    selector_turno.get()
                )

                if turno is None:
                    messagebox.showwarning(
                        "Atención",
                        "Seleccioná un turno disponible."
                    )
                    return

                datos = {
                    "turno_id": turno.get("id"),
                    "fecha": fecha,
                    "diagnostico": diagnostico,
                    "observaciones": observaciones or None
                }

                resultado = APIService.post(
                    "/consultas/",
                    datos
                )

            if resultado is not None:

                messagebox.showinfo(
                    "Éxito",
                    resultado.get(
                        "mensaje",
                        "Consulta guardada correctamente."
                    )
                )

                ventana.destroy()
                self.cargar_consultas()

            else:
                messagebox.showerror(
                    "Error",
                    "No se pudo guardar la consulta. Revisá que el turno esté En curso y que no tenga otra consulta registrada."
                )

        tk.Button(
            ventana,
            text="Guardar consulta",
            command=guardar,
            bg=COLORS["success"],
            fg="white",
            font=FONT_BUTTON,
            relief="flat",
            cursor="hand2",
            padx=25,
            pady=10
        ).pack(pady=12)

    def eliminar_consulta(self):

        consulta = self.obtener_consulta_seleccionada()

        if consulta is None:
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Estás seguro de eliminar esta consulta del historial clínico?"
        )

        if not confirmar:
            return

        resultado = APIService.delete(
            f"/consultas/{consulta['id']}"
        )

        if resultado is not None:

            messagebox.showinfo(
                "Éxito",
                resultado.get(
                    "mensaje",
                    "Consulta eliminada correctamente."
                )
            )

            self.cargar_consultas()

        else:
            messagebox.showerror(
                "Error",
                "No se pudo eliminar la consulta."
            )
