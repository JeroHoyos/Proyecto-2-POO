import tkinter as tk
from tkinter import messagebox, ttk
from sistema import Sistema
from enums import TipoSilla, TipoEquipaje
from vuelo import Vuelo
from pasajero import Pasajero
from checkin import CheckIn
from equipaje import Equipaje

sistema = Sistema()
sistema.cargar_datos()

class App:
    """Clase principal de la aplicación GUI para el sistema de reservas de vuelos."""
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto 2 POO")
        self.usuario_actual = None
        self.vuelo_seleccionado = None
        self.reservas_usuario_actual = []

        self.pantalla_inicio()

    def pantalla_inicio(self):
        """
        Pantalla de inicio donde se ve botones de login y registro
        """
        self.limpiar_ventana()

        tk.Label(self.root, text="Bienvenido al sistema de reservas", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Iniciar Sesión", width=20, command=self.pantalla_login).pack(pady=5)
        tk.Button(self.root, text="Registrarse", width=20, command=self.pantalla_registro).pack(pady=5)
        tk.Button(self.root, text="Salir", width=20, command=self.root.quit).pack(pady=5)

    def pantalla_login(self):
        """
        Muestra TEXT EDITS para ingresar documento y contraseña
        """
        self.limpiar_ventana()
        tk.Label(self.root, text="Iniciar Sesión", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Documento").pack()
        doc_entry = tk.Entry(self.root)
        doc_entry.pack()

        tk.Label(self.root, text="Contraseña").pack()
        pass_entry = tk.Entry(self.root, show="*")
        pass_entry.pack()

        def intentar_login():
            doc = doc_entry.get()
            pw = pass_entry.get()
            usuario = sistema.iniciar_sesion(doc, pw)
            if usuario:

                #Revisar las credenciales

                self.usuario_actual = usuario
                messagebox.showinfo("Éxito", f"Bienvenido {usuario.nombre}")

                #Revisar tipo de cuenta que está usando

                if usuario.__class__.__name__ == "Administrador":
                    self.menu_administrador()
                else:
                    self.menu_cliente()
            else:
                messagebox.showerror("Error", "Credenciales inválidas.")

        tk.Button(self.root, text="Ingresar", command=intentar_login).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.pantalla_inicio).pack()

    def pantalla_registro(self):
        """
        Muestra TEXT EDITS para ingresar nombre, correo, documento y contraseña. también un check por si es administrador
        """
        self.limpiar_ventana()
        tk.Label(self.root, text="Registro de Usuario", font=("Arial", 14)).pack(pady=10)

        labels = ["Nombre", "Correo", "Documento", "Contraseña"]
        entradas = {}
        for lbl in labels:
            tk.Label(self.root, text=lbl).pack()
            entradas[lbl] = tk.Entry(self.root)
            entradas[lbl].pack()

        is_admin = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Administrador", variable=is_admin).pack()

        def registrar():
            r = sistema.registrar_usuario(
                entradas["Nombre"].get(),
                entradas["Correo"].get(),
                entradas["Documento"].get(),
                entradas["Contraseña"].get(),
                is_admin.get()
            )
            messagebox.showinfo("Registro", r)
            self.pantalla_inicio()

        tk.Button(self.root, text="Registrar", command=registrar).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.pantalla_inicio).pack()

    def menu_administrador(self):
        """
        Muestra botones para agregar vuelo, consultar ventas y consultar pasajeros
        """
        self.limpiar_ventana()
        tk.Label(self.root, text="Menú Administrador", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="Agregar vuelo", command=self.pantalla_agregar_vuelo).pack(pady=5)
        tk.Button(self.root, text="Consultar reservas vendidas", command=self.consultar_reservas).pack(pady=5)
        tk.Button(self.root, text="Consultar pasajeros", command=self.consultar_pasajeros).pack(pady=5)
        tk.Button(self.root, text="Cerrar sesión", command=self.pantalla_inicio).pack(pady=10)

    def pantalla_agregar_vuelo(self):
        """
        Muestra TEXT EDIT de código, origen, destino, día, horario y número de silla preferenciales
        """
        self.limpiar_ventana()
        tk.Label(self.root, text="Agregar vuelo", font=("Arial", 14)).pack(pady=10)

        labels = ["Código", "Origen", "Destino", "Día", "Horario", "Sillas Preferencial", "Sillas Económica"]
        entradas = {}
        for lbl in labels:
            tk.Label(self.root, text=lbl).pack()
            entradas[lbl] = tk.Entry(self.root)
            entradas[lbl].pack()

        def agregar():
            try:
                vuelo = sistema.crear_vuelo(
                    entradas["Código"].get(),
                    entradas["Origen"].get(),
                    entradas["Destino"].get(),
                    entradas["Día"].get(),
                    entradas["Horario"].get(),
                    int(entradas["Sillas Preferencial"].get()),
                    int(entradas["Sillas Económica"].get())
                )
                sistema.guardar_datos()
                messagebox.showinfo("Vuelo", f"Vuelo {vuelo.codigo} agregado.")
                self.menu_administrador()
            except ValueError as ve:
                messagebox.showerror("Error", str(ve))
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}")

        tk.Button(self.root, text="Agregar", command=agregar).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.menu_administrador).pack()

    def menu_cliente(self):
        """
        Muestra botones para buscar vuelo, gestionar reserva, cambiar contraseña y ver millas
        """
        self.limpiar_ventana()
        tk.Label(self.root, text=self.usuario_actual.ver_menu(), font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="Buscar vuelos", command=self.pantalla_buscar_vuelos).pack(pady=5)
        tk.Button(self.root, text="Gestionar mis reservas", command=self.pantalla_gestionar_reservas).pack(pady=5)
        tk.Button(self.root, text="Cambiar contraseña", command=self.pantalla_cambiar_contrasena).pack(pady=5)
        tk.Button(self.root, text="Ver mis millas", command=self.ver_mis_millas).pack(pady=5)
        tk.Button(self.root, text="Cerrar sesión", command=self.pantalla_inicio).pack(pady=10)

    def ver_mis_millas(self):
        """
        Muestra millas
        """
        messagebox.showinfo("Mis Millas", f"Actualmente tienes {self.usuario_actual.millas} millas acumuladas.")

    def pantalla_cambiar_contrasena(self):
        """Muestra la pantalla para cambiar la contraseña del usuario."""
        self.limpiar_ventana()
        tk.Label(self.root, text="Cambiar Contraseña", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Contraseña Actual").pack()
        current_pass_entry = tk.Entry(self.root, show="*")
        current_pass_entry.pack()

        tk.Label(self.root, text="Nueva Contraseña").pack()
        new_pass_entry = tk.Entry(self.root, show="*")
        new_pass_entry.pack()

        tk.Label(self.root, text="Confirmar Nueva Contraseña").pack()
        confirm_pass_entry = tk.Entry(self.root, show="*")
        confirm_pass_entry.pack()

        def cambiar_contrasena():
            actual = current_pass_entry.get()
            nueva = new_pass_entry.get()
            confirmacion = confirm_pass_entry.get()

            if self.usuario_actual.contrasena != actual:
                messagebox.showerror("Error", "La contraseña actual es incorrecta.")
                return
            if nueva != confirmacion:
                messagebox.showerror("Error", "La nueva contraseña y su confirmación no coinciden.")
                return
            if not nueva:
                messagebox.showerror("Error", "La nueva contraseña no puede estar vacía.")
                return

            self.usuario_actual.cambiar_contrasena(nueva)
            sistema.guardar_datos()
            messagebox.showinfo("Éxito", "Contraseña cambiada exitosamente.")
            self.menu_cliente()

        tk.Button(self.root, text="Cambiar", command=cambiar_contrasena).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.menu_cliente).pack()

    def pantalla_buscar_vuelos(self):
        """Muestra la pantalla para buscar vuelos."""
        self.limpiar_ventana()
        tk.Label(self.root, text="Buscar vuelos", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Ciudad de origen o destino").pack()
        ciudad_entry = tk.Entry(self.root)
        ciudad_entry.pack()

        opcion_origen = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="Buscar por origen", variable=opcion_origen).pack()

        columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7")
        self.vuelos_tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.vuelos_tree.heading("#1", text="Código")
        self.vuelos_tree.heading("#2", text="Origen")
        self.vuelos_tree.heading("#3", text="Destino")
        self.vuelos_tree.heading("#4", text="Día")
        self.vuelos_tree.heading("#5", text="Horario")
        self.vuelos_tree.heading("#6", text="Disp. Pref.")
        self.vuelos_tree.heading("#7", text="Disp. Econ.")
        self.vuelos_tree.column("#1", width=70)
        self.vuelos_tree.column("#2", width=100)
        self.vuelos_tree.column("#3", width=100)
        self.vuelos_tree.column("#4", width=70)
        self.vuelos_tree.column("#5", width=70)
        self.vuelos_tree.column("#6", width=80)
        self.vuelos_tree.column("#7", width=80)
        self.vuelos_tree.pack(pady=10, fill="both", expand=True)

        self.vuelos_encontrados = []

        def buscar():
            for i in self.vuelos_tree.get_children():
                self.vuelos_tree.delete(i)
            
            self.vuelos_encontrados = sistema.buscar_vuelos(ciudad_entry.get(), por_origen=opcion_origen.get())
            
            if not self.vuelos_encontrados:
                messagebox.showinfo("Búsqueda", "No se encontraron vuelos con los criterios especificados.")
                return

            for v in self.vuelos_encontrados:
                disp = v.obtener_disponibilidad()
                self.vuelos_tree.insert("", tk.END, values=(
                    v.codigo, v.ciudad_origen, v.ciudad_destino, v.dia, v.horario,
                    disp[TipoSilla.PREFERENCIAL.value], disp[TipoSilla.ECONOMICA.value]
                ))

        tk.Button(self.root, text="Buscar", command=buscar).pack(pady=5)
        tk.Button(self.root, text="Seleccionar Vuelo para Reservar", command=self.seleccionar_vuelo_para_reserva).pack(pady=5)
        tk.Button(self.root, text="Volver", command=self.menu_cliente).pack()

    def seleccionar_vuelo_para_reserva(self):
        """Selecciona un vuelo de la lista para proceder con la reserva."""
        selected_item = self.vuelos_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un vuelo de la lista.")
            return

        item_values = self.vuelos_tree.item(selected_item, 'values')
        codigo_vuelo = item_values[0]

        self.vuelo_seleccionado = next((v for v in self.vuelos_encontrados if v.codigo == codigo_vuelo), None)

        if self.vuelo_seleccionado:
            self.pantalla_reservar_vuelo()
        else:
            messagebox.showerror("Error", "No se pudo encontrar el vuelo seleccionado.")

    def pantalla_reservar_vuelo(self):
        """Muestra la pantalla para reservar un vuelo."""
        if not self.vuelo_seleccionado:
            messagebox.showerror("Error", "Ningún vuelo seleccionado para reservar.")
            self.menu_cliente()
            return

        self.limpiar_ventana()
        tk.Label(self.root, text=f"Reservar Vuelo: {self.vuelo_seleccionado.codigo}", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text=f"Origen: {self.vuelo_seleccionado.ciudad_origen} - Destino: {self.vuelo_seleccionado.ciudad_destino}").pack()
        tk.Label(self.root, text=f"Día: {self.vuelo_seleccionado.dia} - Horario: {self.vuelo_seleccionado.horario}").pack()

        disp = self.vuelo_seleccionado.obtener_disponibilidad()
        tk.Label(self.root, text=f"Sillas Preferencial disponibles: {disp[TipoSilla.PREFERENCIAL.value]}").pack()
        tk.Label(self.root, text=f"Sillas Económica disponibles: {disp[TipoSilla.ECONOMICA.value]}").pack()

        pasajeros_frame = tk.LabelFrame(self.root, text="Datos de los Pasajeros (máx 3)")
        pasajeros_frame.pack(pady=10, padx=10, fill="x")

        self.pasajeros_entries = []

        def agregar_campo_pasajero():
            if len(self.pasajeros_entries) >= 3:
                messagebox.showwarning("Advertencia", "No puedes agregar más de 3 pasajeros por reserva.")
                return

            idx = len(self.pasajeros_entries)
            frame = tk.Frame(pasajeros_frame)
            frame.pack(fill="x", padx=5, pady=2)

            tk.Label(frame, text=f"Pasajero {idx+1}").pack(side=tk.LEFT)

            tk.Label(frame, text="Nombre:").pack(side=tk.LEFT)
            nombre_entry = tk.Entry(frame, width=15)
            nombre_entry.pack(side=tk.LEFT, padx=2)

            tk.Label(frame, text="Documento:").pack(side=tk.LEFT)
            doc_entry = tk.Entry(frame, width=10)
            doc_entry.pack(side=tk.LEFT, padx=2)

            tk.Label(frame, text="Tipo Silla:").pack(side=tk.LEFT)
            tipo_silla_var = tk.StringVar(value=TipoSilla.ECONOMICA.value)
            silla_option_menu = ttk.Combobox(frame, textvariable=tipo_silla_var,
                                             values=[ts.value for ts in TipoSilla], state="readonly", width=12)
            silla_option_menu.pack(side=tk.LEFT, padx=2)

            self.pasajeros_entries.append({
                "frame": frame,
                "nombre_entry": nombre_entry,
                "doc_entry": doc_entry,
                "tipo_silla_var": tipo_silla_var
            })
            
            if idx == 0 and self.usuario_actual:
                nombre_entry.insert(0, self.usuario_actual.nombre)
                doc_entry.insert(0, self.usuario_actual.documento)
        
        agregar_campo_pasajero()
        tk.Button(self.root, text="Añadir Pasajero", command=agregar_campo_pasajero).pack(pady=5)

        def confirmar_reserva():
            pasajeros_para_reserva = []
            sillas_solicitadas = []
            for p_entry in self.pasajeros_entries:
                nombre = p_entry["nombre_entry"].get()
                documento = p_entry["doc_entry"].get()
                tipo_silla_str = p_entry["tipo_silla_var"].get()

                if not nombre or not documento:
                    messagebox.showerror("Error", "Todos los campos de nombre y documento de pasajero son obligatorios.")
                    return
                try:
                    tipo_silla = TipoSilla(tipo_silla_str)
                except ValueError:
                    messagebox.showerror("Error", f"Tipo de silla inválido: {tipo_silla_str}")
                    return

                pasajeros_para_reserva.append(Pasajero(nombre, documento))
                sillas_solicitadas.append(tipo_silla)

            try:
                reserva_info, precio_total = sistema.crear_reserva(
                    self.usuario_actual,
                    self.vuelo_seleccionado,
                    pasajeros_para_reserva,
                    sillas_solicitadas
                )
                messagebox.showinfo("Reserva Confirmada", f"Reserva creada con éxito!\n{reserva_info}\n"
                                                         f"Precio Total: ${precio_total:,.0f}")
                self.menu_cliente()
            except ValueError as e:
                messagebox.showerror("Error en la Reserva", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

        tk.Button(self.root, text="Confirmar Reserva", command=confirmar_reserva).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.pantalla_buscar_vuelos).pack()

    def pantalla_gestionar_reservas(self):
        """Muestra la pantalla para gestionar las reservas del usuario actual."""
        self.limpiar_ventana()
        tk.Label(self.root, text="Gestionar Mis Reservas", font=("Arial", 14)).pack(pady=10)

        self.reservas_usuario_actual = sistema.obtener_reservas_por_usuario(self.usuario_actual)

        if not self.reservas_usuario_actual:
            tk.Label(self.root, text="No tienes reservas activas.").pack(pady=20)
            tk.Button(self.root, text="Volver", command=self.menu_cliente).pack()
            return

        columns = ("#1", "#2", "#3", "#4", "#5")
        self.reservas_tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.reservas_tree.heading("#1", text="ID Reserva")
        self.reservas_tree.heading("#2", text="Vuelo")
        self.reservas_tree.heading("#3", text="Pasajeros")
        self.reservas_tree.heading("#4", text="Check-in Realizado")
        self.reservas_tree.heading("#5", text="Precio Total")
        self.reservas_tree.column("#1", width=80)
        self.reservas_tree.column("#2", width=100)
        self.reservas_tree.column("#3", width=200)
        self.reservas_tree.column("#4", width=120)
        self.reservas_tree.column("#5", width=100)
        self.reservas_tree.pack(pady=10, fill="both", expand=True)

        for reserva in self.reservas_usuario_actual:
            pasajeros_nombres = ", ".join([p.nombre for p in reserva.pasajeros])
            checkin_estado = "Sí" if reserva.checkin_realizado else "No"
            self.reservas_tree.insert("", tk.END, values=(
                reserva.id_reserva,
                reserva.vuelo.codigo,
                pasajeros_nombres,
                checkin_estado,
                f"${reserva.precio_total:,.0f}"
            ))

        tk.Button(self.root, text="Realizar Check-in", command=self.realizar_checkin_reserva).pack(pady=5)
        tk.Button(self.root, text="Cancelar Reserva", command=self.cancelar_reserva).pack(pady=5)
        tk.Button(self.root, text="Modificar Reserva", command=self.modificar_reserva).pack(pady=5)
        tk.Button(self.root, text="Volver", command=self.menu_cliente).pack()

    def modificar_reserva(self):
        """Prepara la pantalla para modificar la reserva seleccionada."""
        selected_item = self.reservas_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una reserva para modificar.")
            return
        
        item_values = self.reservas_tree.item(selected_item, 'values')
        reserva_id = int(item_values[0])

        reserva_a_modificar = next((r for r in self.reservas_usuario_actual if r.id_reserva == reserva_id), None)
        if not reserva_a_modificar:
            messagebox.showerror("Error", "Reserva no encontrada.")
            return

        if reserva_a_modificar.checkin_realizado:
            messagebox.showwarning("Advertencia", "No se puede modificar una reserva con check-in ya realizado.")
            return

        self.pantalla_modificar_reserva(reserva_a_modificar)

    def pantalla_modificar_reserva(self, reserva_obj):
        """Muestra la pantalla para modificar los detalles de una reserva."""
        self.limpiar_ventana()
        tk.Label(self.root, text=f"Modificar Reserva: {reserva_obj.id_reserva}", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text=f"Vuelo: {reserva_obj.vuelo.codigo} - {reserva_obj.vuelo.ciudad_origen} a {reserva_obj.vuelo.ciudad_destino}").pack()
        tk.Label(self.root, text=f"Precio actual: ${reserva_obj.precio_total:,.0f}").pack(pady=5)

        # Contenedor para los pasajeros actuales y sus sillas
        current_passengers_frame = tk.LabelFrame(self.root, text="Pasajeros y Sillas Actuales")
        current_passengers_frame.pack(pady=10, padx=10, fill="x")

        self.modified_pasajeros_entries = [] # Para almacenar las entradas de los pasajeros (existentes y nuevos)

        # Mostrar y permitir modificar sillas de pasajeros existentes
        for i, pasajero in enumerate(reserva_obj.pasajeros):
            p_frame = tk.Frame(current_passengers_frame)
            p_frame.pack(fill="x", padx=5, pady=2)

            tk.Label(p_frame, text=f"Pasajero {i+1}: {pasajero.nombre} ({pasajero.documento})").pack(side=tk.LEFT)
            tk.Label(p_frame, text="Tipo Silla:").pack(side=tk.LEFT, padx=5)
            
            # Obtener el tipo de silla actual del pasajero
            silla_actual = reserva_obj.sillas[i]
            tipo_silla_var = tk.StringVar(value=silla_actual.tipo.value)
            silla_option_menu = ttk.Combobox(p_frame, textvariable=tipo_silla_var,
                                             values=[ts.value for ts in TipoSilla], state="readonly", width=12)
            silla_option_menu.pack(side=tk.LEFT, padx=2)

            self.modified_pasajeros_entries.append({
                "pasajero_obj": pasajero, # Guardar el objeto pasajero original
                "silla_obj": silla_actual, # Guardar el objeto silla original
                "tipo_silla_var": tipo_silla_var,
                "is_new": False # Marcar como pasajero existente
            })

        # Sección para añadir nuevos pasajeros
        new_passengers_frame = tk.LabelFrame(self.root, text="Añadir Nuevos Pasajeros (máx 3 en total)")
        new_passengers_frame.pack(pady=10, padx=10, fill="x")

        self.new_pasajeros_entries = [] # Para las entradas de nuevos pasajeros

        def add_new_passenger_fields():
            if len(self.modified_pasajeros_entries) + len(self.new_pasajeros_entries) >= 3:
                messagebox.showwarning("Advertencia", "No puedes tener más de 3 pasajeros en total por reserva.")
                return

            idx = len(self.new_pasajeros_entries)
            frame = tk.Frame(new_passengers_frame)
            frame.pack(fill="x", padx=5, pady=2)

            tk.Label(frame, text=f"Nuevo Pasajero {idx+1}").pack(side=tk.LEFT)

            tk.Label(frame, text="Nombre:").pack(side=tk.LEFT)
            nombre_entry = tk.Entry(frame, width=15)
            nombre_entry.pack(side=tk.LEFT, padx=2)

            tk.Label(frame, text="Documento:").pack(side=tk.LEFT)
            doc_entry = tk.Entry(frame, width=10)
            doc_entry.pack(side=tk.LEFT, padx=2)

            tk.Label(frame, text="Tipo Silla:").pack(side=tk.LEFT)
            tipo_silla_var = tk.StringVar(value=TipoSilla.ECONOMICA.value)
            silla_option_menu = ttk.Combobox(frame, textvariable=tipo_silla_var,
                                             values=[ts.value for ts in TipoSilla], state="readonly", width=12)
            silla_option_menu.pack(side=tk.LEFT, padx=2)

            self.new_pasajeros_entries.append({
                "frame": frame,
                "nombre_entry": nombre_entry,
                "doc_entry": doc_entry,
                "tipo_silla_var": tipo_silla_var,
                "is_new": True
            })

        tk.Button(self.root, text="Añadir Nuevo Pasajero", command=add_new_passenger_fields).pack(pady=5)

        def confirmar_modificacion():
            nuevos_pasajeros_datos = []
            nuevas_sillas_solicitadas = []
            
            # Recopilar datos de pasajeros existentes (posiblemente con tipo de silla modificado)
            for p_entry in self.modified_pasajeros_entries:
                pasajero_obj = p_entry["pasajero_obj"]
                tipo_silla_str = p_entry["tipo_silla_var"].get()
                try:
                    tipo_silla = TipoSilla(tipo_silla_str)
                except ValueError:
                    messagebox.showerror("Error", f"Tipo de silla inválido para {pasajero_obj.nombre}: {tipo_silla_str}")
                    return
                nuevos_pasajeros_datos.append(pasajero_obj)
                nuevas_sillas_solicitadas.append(tipo_silla)

            # Recopilar datos de nuevos pasajeros
            for p_entry in self.new_pasajeros_entries:
                nombre = p_entry["nombre_entry"].get()
                documento = p_entry["doc_entry"].get()
                tipo_silla_str = p_entry["tipo_silla_var"].get()

                if not nombre or not documento:
                    messagebox.showerror("Error", "Todos los campos de nombre y documento de los nuevos pasajeros son obligatorios.")
                    return
                try:
                    tipo_silla = TipoSilla(tipo_silla_str)
                except ValueError:
                    messagebox.showerror("Error", f"Tipo de silla inválido para nuevo pasajero: {tipo_silla_str}")
                    return
                nuevos_pasajeros_datos.append(Pasajero(nombre, documento))
                nuevas_sillas_solicitadas.append(tipo_silla)

            if len(nuevos_pasajeros_datos) == 0:
                messagebox.showerror("Error", "Debe haber al menos un pasajero en la reserva.")
                return
            if len(nuevos_pasajeros_datos) > 3:
                messagebox.showerror("Error", "El número total de pasajeros no puede exceder 3.")
                return

            try:
                # Lógica para modificar la reserva en el sistema
                # Primero, liberar las sillas actuales de la reserva original
                for silla_original in reserva_obj.sillas:
                    silla_original.esta_reservada = False
                
                # Intentar reservar las nuevas sillas
                sillas_asignadas_nuevas = []
                precio_total_modificado = 0.0
                
                # Aquí se debería re-implementar la lógica de descuento por millas si aplica
                # Para simplificar, asumiremos que el descuento de millas no se aplica en la modificación
                # o que ya fue manejado en la reserva inicial.
                # Si se necesita, habría que pasar un parámetro `usa_descuento_millas` a esta función
                # y gestionar las millas del usuario. Por ahora, se calcula el precio normal.

                for i, tipo_silla_solicitado in enumerate(nuevas_sillas_solicitadas):
                    silla_encontrada = reserva_obj.vuelo.reservar_silla(tipo_silla_solicitado)
                    if not silla_encontrada:
                        # Si no se puede asignar una silla, revertir todas las asignaciones y restaurar
                        for s_temp in sillas_asignadas_nuevas:
                            s_temp.esta_reservada = False
                        # Restaurar las sillas originales de la reserva si no se completó la modificación
                        for silla_original in reserva_obj.sillas:
                            silla_original.esta_reservada = True # Esto es crucial para revertir
                        raise ValueError(f"No hay sillas {tipo_silla_solicitado.value} disponibles para el pasajero {nuevos_pasajeros_datos[i].nombre}.")
                    
                    sillas_asignadas_nuevas.append(silla_encontrada)
                    if tipo_silla_solicitado == TipoSilla.PREFERENCIAL:
                        precio_total_modificado += sistema.PRECIO_SILLA_PREFERENCIAL
                    elif tipo_silla_solicitado == TipoSilla.ECONOMICA:
                        precio_total_modificado += sistema.PRECIO_SILLA_ECONOMICA

                # Actualizar la reserva existente
                reserva_obj.pasajeros = nuevos_pasajeros_datos
                reserva_obj.sillas = sillas_asignadas_nuevas
                reserva_obj.precio_total = precio_total_modificado
                
                sistema.guardar_datos()
                messagebox.showinfo("Modificación Exitosa", f"Reserva {reserva_obj.id_reserva} modificada exitosamente.\nNuevo Precio Total: ${reserva_obj.precio_total:,.0f}")
                self.pantalla_gestionar_reservas() # Refrescar la pantalla
            except ValueError as e:
                messagebox.showerror("Error al Modificar", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error inesperado al modificar la reserva: {e}")

        tk.Button(self.root, text="Confirmar Modificación", command=confirmar_modificacion).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.pantalla_gestionar_reservas).pack()

    def realizar_checkin_reserva(self):
        """Inicia el proceso de check-in para la reserva seleccionada."""
        selected_item = self.reservas_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una reserva para realizar check-in.")
            return

        item_values = self.reservas_tree.item(selected_item, 'values')
        reserva_id = int(item_values[0])

        reserva_a_procesar = next((r for r in self.reservas_usuario_actual if r.id_reserva == reserva_id), None)
        if not reserva_a_procesar:
            messagebox.showerror("Error", "Reserva no encontrada.")
            return

        if reserva_a_procesar.checkin_realizado:
            messagebox.showinfo("Check-in", f"La reserva {reserva_id} ya tiene check-in realizado.")
            return

        self.pantalla_checkin_equipaje(reserva_a_procesar)

    def pantalla_checkin_equipaje(self, reserva):
        """Muestra la pantalla para seleccionar el equipaje durante el check-in."""
        self.limpiar_ventana()
        tk.Label(self.root, text=f"Check-in para Reserva {reserva.id_reserva}", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text=f"Vuelo: {reserva.vuelo.codigo} - {reserva.vuelo.ciudad_origen} a {reserva.vuelo.ciudad_destino}").pack()
        tk.Label(self.root, text="Seleccione equipaje para cada pasajero:").pack(pady=5)

        self.equipaje_entries_por_pasajero = []
        
        checkin_manager = CheckIn(reserva)

        for i, pasajero in enumerate(reserva.pasajeros):
            p_frame = tk.LabelFrame(self.root, text=f"Pasajero: {pasajero.nombre} ({pasajero.documento}), Silla: {reserva.sillas[i].tipo.value}")
            p_frame.pack(pady=5, padx=10, fill="x")

            equipaje_info_para_pasajero = []

            mano_var = tk.IntVar()
            tk.Checkbutton(p_frame, text="Equipaje de Mano (Gratis)", variable=mano_var).pack(anchor="w")
            equipaje_info_para_pasajero.append({"tipo": TipoEquipaje.MANO, "var": mano_var, "peso_entry": None, "volumen_entry": None})

            cabina_frame = tk.Frame(p_frame)
            cabina_frame.pack(anchor="w")
            cabina_var = tk.IntVar()
            tk.Checkbutton(cabina_frame, text="Maleta de Cabina (máx 10 kg)", variable=cabina_var).pack(side=tk.LEFT)
            tk.Label(cabina_frame, text="Peso (kg):").pack(side=tk.LEFT, padx=5)
            cabina_peso_entry = tk.Entry(cabina_frame, width=5)
            cabina_peso_entry.pack(side=tk.LEFT)
            tk.Label(cabina_frame, text="Volumen (L):").pack(side=tk.LEFT, padx=5)
            cabina_volumen_entry = tk.Entry(cabina_frame, width=5)
            cabina_volumen_entry.pack(side=tk.LEFT)
            equipaje_info_para_pasajero.append({"tipo": TipoEquipaje.CABINA, "var": cabina_var,
                                       "peso_entry": cabina_peso_entry, "volumen_entry": cabina_volumen_entry})

            bodega_frame = tk.Frame(p_frame)
            bodega_frame.pack(anchor="w")
            bodega_var = tk.IntVar()
            tk.Checkbutton(bodega_frame, text="Maleta de Bodega", variable=bodega_var).pack(side=tk.LEFT)
            tk.Label(bodega_frame, text="Peso (kg):").pack(side=tk.LEFT, padx=5)
            bodega_peso_entry = tk.Entry(bodega_frame, width=5)
            bodega_peso_entry.pack(side=tk.LEFT)
            tk.Label(bodega_frame, text="Volumen (L):").pack(side=tk.LEFT, padx=5)
            bodega_volumen_entry = tk.Entry(bodega_frame, width=5)
            bodega_volumen_entry.pack(side=tk.LEFT)
            equipaje_info_para_pasajero.append({"tipo": TipoEquipaje.BODEGA, "var": bodega_var,
                                       "peso_entry": bodega_peso_entry, "volumen_entry": bodega_volumen_entry})

            self.equipaje_entries_por_pasajero.append(equipaje_info_para_pasajero)

        def procesar_checkin_con_equipaje():
            for i, pasajero_equipaje_info in enumerate(self.equipaje_entries_por_pasajero):
                silla_asociada = reserva.sillas[i]
                
                for eq_data in pasajero_equipaje_info:
                    if eq_data["var"].get() == 1:
                        tipo = eq_data["tipo"]
                        peso = 0.0
                        volumen = 0.0
                        
                        try:
                            if eq_data["peso_entry"]:
                                peso = float(eq_data["peso_entry"].get() or 0.0)
                            if eq_data["volumen_entry"]:
                                volumen = float(eq_data["volumen_entry"].get() or 0.0)
                        except ValueError:
                            messagebox.showerror("Error", f"Peso/Volumen inválido para {tipo.value} de {pasajero.nombre}")
                            return
                        
                        equipaje_obj = Equipaje(tipo, peso, volumen)
                        checkin_manager.agregar_equipaje((silla_asociada, equipaje_obj))

            try:
                success, checkin_msg = checkin_manager.realizar_check_in()
                if success:
                    sistema.guardar_datos()
                    messagebox.showinfo("Check-in Completado", checkin_msg)
                    self.pantalla_gestionar_reservas()
                else:
                    messagebox.showerror("Error durante Check-in", checkin_msg)
            except Exception as e:
                messagebox.showerror("Error durante Check-in", str(e))

        tk.Button(self.root, text="Confirmar Check-in", command=procesar_checkin_con_equipaje).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.pantalla_gestionar_reservas).pack()

    def cancelar_reserva(self):
        """Cancela la reserva seleccionada por el usuario."""
        selected_item = self.reservas_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una reserva para cancelar.")
            return

        item_values = self.reservas_tree.item(selected_item, 'values')
        reserva_id = int(item_values[0])

        if messagebox.askyesno("Confirmar Cancelación", f"¿Está seguro de que desea cancelar la reserva {reserva_id}?"):
            try:
                msg = sistema.cancelar_reserva(reserva_id, self.usuario_actual)
                messagebox.showinfo("Cancelación", msg)
                self.pantalla_gestionar_reservas()
            except Exception as e:
                messagebox.showerror("Error al Cancelar", str(e))

    def consultar_reservas(self):
        """Muestra todas las reservas vendidas (para administradores)."""
        self.limpiar_ventana()
        tk.Label(self.root, text="Reservas Vendidas", font=("Arial", 14)).pack(pady=10)

        reservas_info = sistema.reservas
        if not reservas_info:
            tk.Label(self.root, text="No hay reservas vendidas para mostrar.").pack(pady=20)
            tk.Button(self.root, text="Volver", command=self.menu_administrador).pack()
            return

        tree = ttk.Treeview(self.root, columns=("ID Reserva", "Vuelo", "Usuario", "Pasajeros", "Check-in", "Precio"), show="headings")
        tree.heading("ID Reserva", text="ID Reserva")
        tree.heading("Vuelo", text="Vuelo")
        tree.heading("Usuario", text="Usuario")
        tree.heading("Pasajeros", text="Pasajeros")
        tree.heading("Check-in", text="Check-in Realizado")
        tree.heading("Precio", text="Precio Total")
        tree.column("ID Reserva", width=80)
        tree.column("Vuelo", width=80)
        tree.column("Usuario", width=150)
        tree.column("Pasajeros", width=200)
        tree.column("Check-in", width=100)
        tree.column("Precio", width=100)
        tree.pack(pady=10, fill="both", expand=True)

        for reserva in reservas_info:
            pasajeros_nombres = ", ".join([p.nombre for p in reserva.pasajeros])
            checkin_estado = "Sí" if reserva.checkin_realizado else "No"
            tree.insert("", tk.END, values=(
                reserva.id_reserva,
                reserva.vuelo.codigo,
                f"{reserva.usuario.nombre} ({reserva.usuario.documento})",
                pasajeros_nombres,
                checkin_estado,
                f"${reserva.precio_total:,.0f}"
            ))

        tk.Button(self.root, text="Cerrar", command=self.menu_administrador).pack(pady=5)

    def consultar_pasajeros(self):
        """Muestra los datos de todos los pasajeros en el sistema (para administradores)."""
        self.limpiar_ventana()
        tk.Label(self.root, text="Datos de Pasajeros", font=("Arial", 14)).pack(pady=10)

        datos_pasajeros_globales = []
        for reserva in sistema.reservas:
            for pasajero in reserva.pasajeros:
                datos_pasajeros_globales.append((reserva.id_reserva, reserva.vuelo.codigo, pasajero.nombre, pasajero.documento))

        if not datos_pasajeros_globales:
            messagebox.showinfo("Datos Pasajeros", "No hay pasajeros registrados en reservas.")
            tk.Button(self.root, text="Cerrar", command=self.menu_administrador).pack(pady=5)
            return

        pasajeros_win = tk.Toplevel(self.root)
        pasajeros_win.title("Datos de Pasajeros por Reserva")
        tk.Label(pasajeros_win, text="Pasajeros por Reserva", font=("Arial", 14)).pack(pady=10)

        tree = ttk.Treeview(pasajeros_win, columns=("ID Reserva", "Vuelo", "Nombre Pasajero", "Documento Pasajero"), show="headings")
        tree.heading("ID Reserva", text="ID Reserva")
        tree.heading("Vuelo", text="Vuelo")
        tree.heading("Nombre Pasajero", text="Nombre del Pasajero")
        tree.heading("Documento Pasajero", text="Documento del Pasajero")
        tree.column("ID Reserva", width=80)
        tree.column("Vuelo", width=80)
        tree.column("Nombre Pasajero", width=150)
        tree.column("Documento Pasajero", width=120)
        tree.pack(pady=10, fill="both", expand=True)

        for rid, vuelo_cod, nombre_p, doc_p in datos_pasajeros_globales:
            tree.insert("", tk.END, values=(rid, vuelo_cod, nombre_p, doc_p))

        tk.Button(pasajeros_win, text="Cerrar", command=pasajeros_win.destroy).pack(pady=5)
        tk.Button(self.root, text="Volver", command=self.menu_administrador).pack()

    def limpiar_ventana(self):
        """Limpia todos los widgets de la ventana principal."""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()