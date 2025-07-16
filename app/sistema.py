import os # Manejo de rutas y directorios del sistema
import re # Operaciones con expresiones regulares
from tkinter import messagebox
from vuelo import Vuelo
from cliente import Cliente
from administrador import Administrador
from reserva import Reserva
from enums import TipoSilla
from pasajero import Pasajero
from usuario import Usuario

class Sistema:
    """Gestiona usuarios, vuelos y reservas, incluyendo persistencia de datos."""
    PRECIO_SILLA_PREFERENCIAL = 850000.0
    PRECIO_SILLA_ECONOMICA = 235000.0
    MILLAS_PARA_DESCUENTO = 2000

    # Definir la carpeta donde se guardarán y leerán los archivos de datos
    CARPETA_DATOS = "data"

    def __init__(self):
        self.usuarios: list[Usuario] = []
        self.vuelos: list[Vuelo] = []
        self.reservas: list[Reserva] = []
        self.siguiente_id_reserva = 1000

        # Asegurarse de que la carpeta de datos exista al inicializar el sistema
        # Esto creará la carpeta 'data' si no existe
        if not os.path.exists(self.CARPETA_DATOS):
            os.makedirs(self.CARPETA_DATOS)

    def registrar_usuario(self, nombre: str, correo: str, documento: str, contrasena: str, es_admin: bool = False) -> str:
        """Registra un nuevo usuario o administrador."""
        for u in self.usuarios:
            if u.documento == documento:
                return f"Error: Ya existe un usuario con el documento {documento}"
        nuevo_usuario = Administrador(nombre, correo, documento, contrasena) if es_admin else Cliente(nombre, correo, documento, contrasena)
        self.usuarios.append(nuevo_usuario)
        self.guardar_datos()
        return f"Usuario {nombre} ({'Administrador' if es_admin else 'Cliente'}) registrado exitosamente."

    def iniciar_sesion(self, documento: str, contrasena: str) -> Usuario | None:
        """Inicia sesión para un usuario."""
        for u in self.usuarios:
            if u.documento == documento and u.contrasena == contrasena:
                return u
        return None

    def buscar_vuelos(self, criterio: str, por_origen: bool = True) -> list[Vuelo]:
        """Busca vuelos por origen o destino."""
        resultados = []
        for v in self.vuelos:
            if (por_origen and criterio.lower() in v.ciudad_origen.lower()) or \
               (not por_origen and criterio.lower() in v.ciudad_destino.lower()):
                resultados.append(v)
        return resultados

    def crear_vuelo(self, codigo: str, origen: str, destino: str, dia: str, horario: str, sillas_preferencial: int, sillas_economica: int) -> Vuelo:
        """Crea un nuevo vuelo."""
        if any(v.codigo == codigo for v in self.vuelos):
            raise ValueError(f"El vuelo con código {codigo} ya existe.")
        nuevo_vuelo = Vuelo(codigo, origen, destino, dia, horario, sillas_preferencial, sillas_economica)
        self.vuelos.append(nuevo_vuelo)
        self.guardar_datos()
        return nuevo_vuelo

    def crear_reserva(self, usuario: Usuario, vuelo: Vuelo, pasajeros_datos: list[Pasajero], tipos_silla_solicitados: list[TipoSilla]) -> tuple[str, float]:
        """Crea una nueva reserva para uno o más pasajeros en un vuelo."""
        if not pasajeros_datos or not tipos_silla_solicitados or len(pasajeros_datos) != len(tipos_silla_solicitados):
            raise ValueError("Cantidad de pasajeros y tipos de silla no coinciden o están vacíos.")
        if len(pasajeros_datos) > 3:
            raise ValueError("No se pueden reservar más de 3 sillas por reserva.")

        sillas_asignadas = []
        precio_total_reserva = 0.0
        usa_descuento_millas = False

        if usuario.millas >= self.MILLAS_PARA_DESCUENTO:
            respuesta_millas = messagebox.askyesno("Millas Disponibles", f"Tienes {usuario.millas} millas. ¿Deseas usar {self.MILLAS_PARA_DESCUENTO} millas para reservar una silla preferencial al precio de económica?")
            if respuesta_millas:
                usa_descuento_millas = True
                usuario.millas -= self.MILLAS_PARA_DESCUENTO
                messagebox.showinfo("Millas", f"Se han descontado {self.MILLAS_PARA_DESCUENTO} millas. Millas restantes: {usuario.millas}.")

        for i, tipo_silla_solicitado in enumerate(tipos_silla_solicitados):
            silla_encontrada = None
            costo_silla = 0.0

            if tipo_silla_solicitado == TipoSilla.PREFERENCIAL:
                if usa_descuento_millas:
                    silla_encontrada = vuelo.reservar_silla(TipoSilla.PREFERENCIAL)
                    if silla_encontrada:
                        costo_silla = self.PRECIO_SILLA_ECONOMICA
                        usa_descuento_millas = False
                    else:
                        respuesta_eco_fallback = messagebox.askyesno("Silla Preferencial no disponible", f"No hay sillas Preferencial disponibles para el pasajero {pasajeros_datos[i].nombre}. ¿Desea reservar una Económica en su lugar?")
                        if respuesta_eco_fallback:
                            silla_encontrada = vuelo.reservar_silla(TipoSilla.ECONOMICA)
                            if silla_encontrada:
                                costo_silla = self.PRECIO_SILLA_ECONOMICA
                            else:
                                for s in sillas_asignadas: s.esta_reservada = False
                                if usa_descuento_millas:
                                    usuario.millas += self.MILLAS_PARA_DESCUENTO
                                    messagebox.showinfo("Millas Reembolsadas", f"No se pudo reservar la silla preferencial con descuento. Se han devuelto {self.MILLAS_PARA_DESCUENTO} millas.")
                                raise ValueError(f"No hay sillas Económica disponibles para el pasajero {pasajeros_datos[i].nombre}.")
                        else:
                            for s in sillas_asignadas: s.esta_reservada = False
                            if usa_descuento_millas:
                                usuario.millas += self.MILLAS_PARA_DESCUENTO
                                messagebox.showinfo("Millas Reembolsadas", f"No se pudo reservar la silla preferencial con descuento. Se han devuelto {self.MILLAS_PARA_DESCUENTO} millas.")
                            raise ValueError(f"Silla Preferencial no disponible y no se aceptó silla Económica para el pasajero {pasajeros_datos[i].nombre}.")
                else:
                    silla_encontrada = vuelo.reservar_silla(TipoSilla.PREFERENCIAL)
                    if silla_encontrada:
                        costo_silla = self.PRECIO_SILLA_PREFERENCIAL
                    else:
                        respuesta_eco = messagebox.askyesno("Silla Preferencial no disponible", f"No hay sillas Preferencial disponibles para el pasajero {pasajeros_datos[i].nombre}. ¿Desea reservar una Económica en su lugar?")
                        if respuesta_eco:
                            silla_encontrada = vuelo.reservar_silla(TipoSilla.ECONOMICA)
                            if silla_encontrada:
                                costo_silla = self.PRECIO_SILLA_ECONOMICA
                            else:
                                for s in sillas_asignadas: s.esta_reservada = False
                                raise ValueError(f"No hay sillas Económica disponibles para el pasajero {pasajeros_datos[i].nombre}.")
                        else:
                            for s in sillas_asignadas: s.esta_reservada = False
                            raise ValueError(f"Silla Preferencial no disponible y no se aceptó silla Económica para el pasajero {pasajeros_datos[i].nombre}.")
            elif tipo_silla_solicitado == TipoSilla.ECONOMICA:
                silla_encontrada = vuelo.reservar_silla(TipoSilla.ECONOMICA)
                if silla_encontrada:
                    costo_silla = self.PRECIO_SILLA_ECONOMICA
                else:
                    for s in sillas_asignadas: s.esta_reservada = False
                    raise ValueError(f"No hay sillas Económica disponibles para el pasajero {pasajeros_datos[i].nombre}.")

            sillas_asignadas.append(silla_encontrada)
            precio_total_reserva += costo_silla

        id_reserva = self.siguiente_id_reserva
        self.siguiente_id_reserva += 1

        nueva_reserva = Reserva(id_reserva, vuelo, usuario, pasajeros_datos, sillas_asignadas, precio_total=precio_total_reserva)
        self.reservas.append(nueva_reserva)
        usuario.reservas.append(nueva_reserva)
        self.guardar_datos()

        resumen = f"Reserva #{nueva_reserva.id_reserva} para vuelo {vuelo.codigo} con {len(pasajeros_datos)} pasajeros."
        return resumen, precio_total_reserva

    def cancelar_reserva(self, id_reserva: int, usuario_que_cancela: Usuario) -> str:
        """Cancela una reserva y libera las sillas."""
        reserva_a_cancelar = next((r for r in self.reservas if r.id_reserva == id_reserva and r.usuario.documento == usuario_que_cancela.documento), None)

        if not reserva_a_cancelar:
            raise ValueError(f"Reserva {id_reserva} no encontrada o no pertenece al usuario.")

        if reserva_a_cancelar.checkin_realizado:
            raise ValueError(f"No se puede cancelar la reserva {id_reserva} porque ya se realizó el check-in.")

        for silla in reserva_a_cancelar.sillas:
            silla.esta_reservada = False

        self.reservas.remove(reserva_a_cancelar)
        usuario_que_cancela.reservas = [r for r in usuario_que_cancela.reservas if r.id_reserva != id_reserva]
        
        self.guardar_datos()

        return f"Reserva {id_reserva} cancelada exitosamente."

    def obtener_reservas_por_usuario(self, usuario: Usuario) -> list[Reserva]:
        """Obtiene todas las reservas realizadas por un usuario específico."""
        return [r for r in self.reservas if r.usuario.documento == usuario.documento]

    def cargar_datos(self):
        """Carga datos de usuarios, vuelos y reservas desde archivos TXT."""
        ruta_siguiente_id_reserva = os.path.join(self.CARPETA_DATOS, "siguiente_id_reserva.txt")
        if os.path.exists(ruta_siguiente_id_reserva):
            try:
                with open(ruta_siguiente_id_reserva, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        match = re.search(r'(\d+)$', content)
                        if match:
                            self.siguiente_id_reserva = int(match.group(1))
                        else:
                            self.siguiente_id_reserva = int(content)
                    else:
                        raise ValueError("El archivo siguiente_id_reserva.txt está vacío.")
            except (ValueError, FileNotFoundError, IOError) as e:
                print(f"Advertencia: No se pudo cargar el próximo ID de reserva de {ruta_siguiente_id_reserva}. Se reiniciará a 1000. Error: {e}")
                self.siguiente_id_reserva = 1000
        else:
            self.siguiente_id_reserva = 1000

        ruta_usuarios = os.path.join(self.CARPETA_DATOS, "usuarios.txt")
        if os.path.exists(ruta_usuarios):
            try:
                with open(ruta_usuarios, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            try:
                                usuario = Usuario.from_string(line.strip())
                                self.usuarios.append(usuario)
                            except ValueError as ve:
                                print(f"Error al cargar línea de usuario: {ve} en '{line.strip()}'")
                                continue
            except Exception as e:
                print(f"Error al leer usuarios de {ruta_usuarios}: {e}")

        ruta_vuelos_y_sillas = os.path.join(self.CARPETA_DATOS, "vuelos_y_sillas.txt")
        ruta_vuelos_inicial = os.path.join(self.CARPETA_DATOS, "vuelos.txt") # Asumimos que vuelos.txt también estará en 'data'
        
        if os.path.exists(ruta_vuelos_y_sillas) and os.path.getsize(ruta_vuelos_y_sillas) > 0:
            try:
                with open(ruta_vuelos_y_sillas, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            try:
                                vuelo = Vuelo.from_string(line.strip())
                                self.vuelos.append(vuelo)
                            except ValueError as ve:
                                print(f"Error al cargar línea de vuelo persistente: {ve} en '{line.strip()}'")
                                continue
            except Exception as e:
                print(f"Error al leer vuelos de persistencia {ruta_vuelos_y_sillas}: {e}")
        else:
            if os.path.exists(ruta_vuelos_inicial):
                try:
                    with open(ruta_vuelos_inicial, "r", encoding="utf-8") as f:
                        for line in f:
                            if line.strip():
                                try:
                                    vuelo = Vuelo.from_txt_line(line.strip())
                                    self.vuelos.append(vuelo)
                                except ValueError as ve:
                                    print(f"Error al cargar línea de vuelo inicial: {ve} en '{line.strip()}'")
                                    continue
                except Exception as e:
                    print(f"Error al leer vuelos de {ruta_vuelos_inicial}: {e}")

        ruta_reservas = os.path.join(self.CARPETA_DATOS, "reservas.txt")
        if os.path.exists(ruta_reservas):
            try:
                with open(ruta_reservas, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            try:
                                reserva = Reserva.from_string(line.strip(), self.vuelos, self.usuarios)
                                self.reservas.append(reserva)
                                if reserva.id_reserva >= self.siguiente_id_reserva:
                                    self.siguiente_id_reserva = reserva.id_reserva + 1
                            except ValueError as ve:
                                print(f"Error al cargar línea de reserva: {ve} en '{line.strip()}'")
                                continue
            except Exception as e:
                print(f"Error al leer reservas de {ruta_reservas}: {e}")

        for usuario in self.usuarios:
            usuario.reservas = [r for r in self.reservas if r.usuario.documento == usuario.documento]

    def guardar_datos(self):
        """Guarda el estado actual de usuarios, vuelos y reservas en archivos TXT."""
        ruta_siguiente_id_reserva = os.path.join(self.CARPETA_DATOS, "siguiente_id_reserva.txt")
        try:
            with open(ruta_siguiente_id_reserva, "w", encoding="utf-8") as f:
                f.write(str(self.siguiente_id_reserva))
        except Exception as e:
            print(f"Error al guardar el próximo ID de reserva en {ruta_siguiente_id_reserva}: {e}")

        ruta_usuarios = os.path.join(self.CARPETA_DATOS, "usuarios.txt")
        try:
            with open(ruta_usuarios, "w", encoding="utf-8") as f:
                for usuario in self.usuarios:
                    usuario.reservas_ids = [r.id_reserva for r in usuario.reservas]
                    f.write(usuario.to_string() + "\n")
        except Exception as e:
            print(f"Error al guardar usuarios en {ruta_usuarios}: {e}")

        ruta_reservas = os.path.join(self.CARPETA_DATOS, "reservas.txt")
        try:
            with open(ruta_reservas, "w", encoding="utf-8") as f:
                for reserva in self.reservas:
                    f.write(reserva.to_string() + "\n")
        except Exception as e:
            print(f"Error al guardar reservas en {ruta_reservas}: {e}")

        ruta_vuelos_y_sillas = os.path.join(self.CARPETA_DATOS, "vuelos_y_sillas.txt")
        try:
            with open(ruta_vuelos_y_sillas, "w", encoding="utf-8") as f:
                for vuelo in self.vuelos:
                    f.write(vuelo.to_string() + "\n")
        except Exception as e:
            print(f"Error al guardar vuelos en {ruta_vuelos_y_sillas}: {e}")