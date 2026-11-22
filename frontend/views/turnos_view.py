
import tkinter as tk
from tkinter import ttk, messagebox

from frontend.config import (
    COLORS,
    FONT_NORMAL,
    FONT_SUBTITLE,
    FONT_BUTTON
)

from frontend.services.api_service import APIService


class TurnosView(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["background"])

        self.pack(fill="both", expand=True)

        self.mascotas = []
        self.profesionales = []
        self.servicios = []

        self.crear_interfaz()
        self.cargar_turnos()

    def crear_interfaz(self):

        # Barra superior
        top = tk.Frame(self, bg=COLORS["background"])
        top.pack(fill="x", pady=(0, 15))

        tk.Label(
            top,
            text="Administración de turnos",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=FONT_SUBTITLE
        ).pack(side="left")

        tk.Button(
            top,
            text="+ Nuevo turno",
            bg=COLORS["primary"],
            fg="white",
            font=FONT_NORMAL,
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.nuevo_turno
        ).pack(side="right")

        # Tabla
        columns = (
            "id",
            "mascota",
            "profesional",
            "servicio",
            "fecha",
            "hora",
            "estado",
            "motivo"
        )

        self.tabla = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=13
        )

        encabezados = {
            "id": "ID",
            "mascota": "Mascota",
            "profesional": "Veterinario",
            "servicio": "Servicio",
            "fecha": "Fecha",
            "hora": "Hora",
            "estado": "Estado",
            "motivo": "Motivo"
        }

        anchos = {
            "id": 45,
            "mascota": 110,
            "profesional": 140,
            "servicio": 130,
            "fecha": 95,
            "hora": 70,
            "estado": 100,
            "motivo": 180
        }

        for col, texto in encabezados.items():
            self.tabla.heading(col, text=texto)
            self.tabla.column(
                col,
                anchor="center",
                width=anchos[col],
                minwidth=55
            )

        self.tabla.pack(fill="both", expand=True)

        # Botones inferiores
        actions = tk.Frame(self, bg=COLORS["background"])
        actions.pack(fill="x", pady=12)

        tk.Button(
            actions,
            text="Actualizar lista",
            command=self.cargar_turnos
        ).pack(side="left", padx=4)

        tk.Button(
            actions,
            text="Reprogramar seleccionado",
            command=self.editar_turno
        ).pack(side="left", padx=4)

        tk.Button(
            actions,
            text="Cambiar estado",
            command=self.cambiar_estado
        ).pack(side="left", padx=4)

        tk.Button(
            actions,
            text="Cancelar turno",
            command=self.cancelar_turno
        ).pack(side="left", padx=4)

    def cargar_datos_formulario(self):

        self.mascotas = APIService.get("/mascotas/")
        self.profesionales = APIService.get("/profesionales/activos")
        self.servicios = APIService.get("/servicios/activos")

        if (
            self.mascotas is None
            or self.profesionales is None
            or self.servicios is None
        ):
            messagebox.showerror(
                "Error",
                "No se pudieron cargar las mascotas, profesionales o servicios."
            )
            return False

        return True

    def nombre_mascota(self, mascota_id):

        for mascota in self.mascotas:
            if mascota.get("id") == mascota_id:
                return mascota.get("nombre", f"ID {mascota_id}")

        return f"ID {mascota_id}"

    def nombre_profesional(self, profesional_id):

        for profesional in self.profesionales:
            if profesional.get("id") == profesional_id:
                return (
                    f"{profesional.get('nombre', '')} "
                    f"{profesional.get('apellido', '')}"
                ).strip()

        return f"ID {profesional_id}"

    def nombre_servicio(self, servicio_id):

        for servicio in self.servicios:
            if servicio.get("id") == servicio_id:
                return servicio.get("nombre", f"ID {servicio_id}")

        return f"ID {servicio_id}"

    def cargar_turnos(self):

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # Cargar datos auxiliares para mostrar nombres
        self.mascotas = APIService.get("/mascotas/") or []
        self.profesionales = APIService.get("/profesionales/") or []
        self.servicios = APIService.get("/servicios/") or []

        turnos = APIService.get("/turnos/")

        if turnos is None:
            messagebox.showerror(
                "Error",
                "No se pudieron cargar los turnos."
            )
            return

        for turno in turnos:

            mascota = (
                turno.get("nombre_mascota")
                or self.nombre_mascota(turno.get("mascota_id"))
            )

            profesional = (
                turno.get("nombre_profesional")
                or self.nombre_profesional(turno.get("profesional_id"))
            )

            servicio = (
                turno.get("nombre_servicio")
                or self.nombre_servicio(turno.get("servicio_id"))
            )

            self.tabla.insert(
                "",
                "end",
                values=(
                    turno.get("id"),
                    mascota,
                    profesional,
                    servicio,
                    turno.get("fecha"),
                    turno.get("hora"),
                    turno.get("estado"),
                    turno.get("motivo") or ""
                )
            )

    def obtener_turno_seleccionado(self):

        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Atención",
                "Seleccioná un turno de la lista."
            )
            return None

        valores = self.tabla.item(
            seleccionado[0],
            "values"
        )

        turno_id = valores[0]

        turno = APIService.get(f"/turnos/{turno_id}")

        if turno is None:
            messagebox.showerror(
                "Error",
                "No se pudieron obtener los datos del turno."
            )
            return None

        return turno

    def nuevo_turno(self):
        self.formulario_turno()

    def editar_turno(self):

        turno = self.obtener_turno_seleccionado()

        if turno is None:
            return

        if turno.get("estado") != "Confirmado":
            messagebox.showwarning(
                "Atención",
                "Solo se pueden reprogramar turnos confirmados."
            )
            return

        self.formulario_turno(turno)

    def formulario_turno(self, turno=None):

        if not self.cargar_datos_formulario():
            return

        ventana = tk.Toplevel(self)
        ventana.title("Datos del turno")
        ventana.geometry("520x650")
        ventana.resizable(False, False)
        ventana.configure(bg=COLORS["white"])
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        tk.Label(
            ventana,
            text="Datos del turno",
            font=FONT_SUBTITLE,
            bg=COLORS["white"],
            fg=COLORS["text"]
        ).pack(pady=18)

        formulario = tk.Frame(
            ventana,
            bg=COLORS["white"]
        )
        formulario.pack(
            fill="both",
            expand=True,
            padx=30
        )

        # Mascota
        tk.Label(
            formulario,
            text="Mascota",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=0, column=0, sticky="w", pady=10)

        opciones_mascotas = {
            f"{m.get('nombre', '')} (ID: {m.get('id')})": m.get("id")
            for m in self.mascotas
        }

        selector_mascota = ttk.Combobox(
            formulario,
            width=34,
            state="readonly",
            values=list(opciones_mascotas.keys())
        )
        selector_mascota.grid(row=0, column=1, padx=10, pady=10)

        # Profesional
        tk.Label(
            formulario,
            text="Veterinario",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=1, column=0, sticky="w", pady=10)

        opciones_profesionales = {
            (
                f"{p.get('nombre', '')} {p.get('apellido', '')} "
                f"(ID: {p.get('id')})"
            ): p.get("id")
            for p in self.profesionales
        }

        selector_profesional = ttk.Combobox(
            formulario,
            width=34,
            state="readonly",
            values=list(opciones_profesionales.keys())
        )
        selector_profesional.grid(row=1, column=1, padx=10, pady=10)

        # Servicio
        tk.Label(
            formulario,
            text="Servicio",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=2, column=0, sticky="w", pady=10)

        opciones_servicios = {
            f"{s.get('nombre', '')} (ID: {s.get('id')})": s.get("id")
            for s in self.servicios
        }

        selector_servicio = ttk.Combobox(
            formulario,
            width=34,
            state="readonly",
            values=list(opciones_servicios.keys())
        )
        selector_servicio.grid(row=2, column=1, padx=10, pady=10)

        # Fecha
        tk.Label(
            formulario,
            text="Fecha (AAAA-MM-DD)",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=3, column=0, sticky="w", pady=10)

        entrada_fecha = tk.Entry(formulario, width=37)
        entrada_fecha.grid(row=3, column=1, padx=10, pady=10)

        # Hora
        tk.Label(
            formulario,
            text="Hora (HH:MM)",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=4, column=0, sticky="w", pady=10)

        entrada_hora = tk.Entry(formulario, width=37)
        entrada_hora.grid(row=4, column=1, padx=10, pady=10)

        # Motivo
        tk.Label(
            formulario,
            text="Motivo",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_NORMAL
        ).grid(row=5, column=0, sticky="nw", pady=10)

        entrada_motivo = tk.Text(
            formulario,
            width=28,
            height=4
        )
        entrada_motivo.grid(row=5, column=1, padx=10, pady=10)

        # Cargar los datos cuando se reprograma
        if turno:

            for nombre, id_mascota in opciones_mascotas.items():
                if id_mascota == turno.get("mascota_id"):
                    selector_mascota.set(nombre)
                    break

            for nombre, id_profesional in opciones_profesionales.items():
                if id_profesional == turno.get("profesional_id"):
                    selector_profesional.set(nombre)
                    break

            for nombre, id_servicio in opciones_servicios.items():
                if id_servicio == turno.get("servicio_id"):
                    selector_servicio.set(nombre)
                    break

            entrada_fecha.insert(0, turno.get("fecha") or "")
            entrada_hora.insert(0, turno.get("hora") or "")
            entrada_motivo.insert(
                "1.0",
                turno.get("motivo") or ""
            )

        def guardar():

            mascota_seleccionada = selector_mascota.get()
            profesional_seleccionado = selector_profesional.get()
            servicio_seleccionado = selector_servicio.get()

            if mascota_seleccionada not in opciones_mascotas:
                messagebox.showwarning(
                    "Atención",
                    "Seleccioná una mascota."
                )
                return

            if profesional_seleccionado not in opciones_profesionales:
                messagebox.showwarning(
                    "Atención",
                    "Seleccioná un veterinario."
                )
                return

            if servicio_seleccionado not in opciones_servicios:
                messagebox.showwarning(
                    "Atención",
                    "Seleccioná un servicio."
                )
                return

            fecha = entrada_fecha.get().strip()
            hora = entrada_hora.get().strip()

            if len(fecha) != 10:
                messagebox.showwarning(
                    "Atención",
                    "Ingresá la fecha con formato AAAA-MM-DD."
                )
                return

            if len(hora) != 5:
                messagebox.showwarning(
                    "Atención",
                    "Ingresá la hora con formato HH:MM."
                )
                return

            datos = {
                "mascota_id": opciones_mascotas[mascota_seleccionada],
                "profesional_id": opciones_profesionales[profesional_seleccionado],
                "servicio_id": opciones_servicios[servicio_seleccionado],
                "fecha": fecha,
                "hora": hora,
                "motivo": entrada_motivo.get("1.0", "end").strip()
            }

            if turno:
                resultado = APIService.put(
                    f"/turnos/{turno['id']}",
                    datos
                )
            else:
                resultado = APIService.post(
                    "/turnos/",
                    datos
                )

            if resultado is not None:

                messagebox.showinfo(
                    "Éxito",
                    resultado.get(
                        "mensaje",
                        "Turno guardado correctamente."
                    )
                )

                ventana.destroy()
                self.cargar_turnos()

            else:
                messagebox.showerror(
                    "Error",
                    "No se pudo guardar el turno. Revisá la fecha, horario y disponibilidad."
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

    def cambiar_estado(self):

        turno = self.obtener_turno_seleccionado()

        if turno is None:
            return

        ventana = tk.Toplevel(self)
        ventana.title("Cambiar estado")
        ventana.geometry("350x220")
        ventana.resizable(False, False)
        ventana.configure(bg=COLORS["white"])
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        tk.Label(
            ventana,
            text="Seleccioná el nuevo estado",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONT_SUBTITLE
        ).pack(pady=20)

        selector = ttk.Combobox(
            ventana,
            state="readonly",
            values=[
                "Confirmado",
                "En curso",
                "Completado",
                "Cancelado"
            ],
            width=25
        )
        selector.pack(pady=10)
        selector.set(turno.get("estado", "Confirmado"))

        def guardar_estado():

            nuevo_estado = selector.get()

            if not nuevo_estado:
                return

            resultado = APIService.patch(
                f"/turnos/{turno['id']}/estado",
                {"estado": nuevo_estado}
            )

            if resultado is not None:

                messagebox.showinfo(
                    "Éxito",
                    resultado.get(
                        "mensaje",
                        "Estado actualizado correctamente."
                    )
                )

                ventana.destroy()
                self.cargar_turnos()

            else:
                messagebox.showerror(
                    "Error",
                    "No se pudo cambiar el estado. Puede que la transición no esté permitida."
                )

        tk.Button(
            ventana,
            text="Guardar",
            command=guardar_estado,
            bg=COLORS["success"],
            fg="white",
            font=FONT_BUTTON,
            relief="flat",
            padx=25,
            pady=8
        ).pack(pady=15)

    def cancelar_turno(self):

        turno = self.obtener_turno_seleccionado()

        if turno is None:
            return

        if turno.get("estado") == "Cancelado":
            messagebox.showinfo(
                "Información",
                "Este turno ya está cancelado."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar cancelación",
            "¿Estás seguro de cancelar este turno?"
        )

        if not confirmar:
            return

        resultado = APIService.delete(
            f"/turnos/{turno['id']}"
        )

        if resultado is not None:

            messagebox.showinfo(
                "Éxito",
                resultado.get(
                    "mensaje",
                    "Turno cancelado correctamente."
                )
            )

            self.cargar_turnos()

        else:
            messagebox.showerror(
                "Error",
                "No se pudo cancelar el turno."
            )
