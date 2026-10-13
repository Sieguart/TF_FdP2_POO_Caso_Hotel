from abc import ABC, abstractmethod
from typing import List, Optional

# ---------------------------------------------------------
# 0. excepción personalizada para validación de DNI
# ---------------------------------------------------------
class DniInvalidoException(Exception):
    def __init__(self, mensaje="El DNI ingresado no es válido."):
        super().__init__(mensaje)


# ---------------------------------------------------------
# 1. clases de dominio y asociación
# ---------------------------------------------------------

class Cliente:
    def __init__(self, dni: str, nombre: str, apellido: str, direccion: str, plan_internet: str):
        self._dni = dni
        self._nombre = nombre
        self._apellido = apellido
        self._direccion = direccion
        self._plan_internet = plan_internet

    @property
    def dni(self) -> str:
        return self._dni

    @property
    def nombre_completo(self) -> str:
        return f"{self._nombre} {self._apellido}"

    def __str__(self) -> str:
        return f"Cliente: {self.nombre_completo} (DNI: {self._dni}) - Plan: {self._plan_internet}"


class Incidencia:
    def __init__(self, codigo: str, cliente: Cliente, descripcion: str):
        self._codigo = codigo
        self._cliente = cliente
        self._descripcion = descripcion
        self._estado = "Pendiente"  # Pendiente / Atendida
        self._tecnico_asignado: Optional['Tecnico'] = None

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def estado(self) -> str:
        return self._estado

    def asignar_tecnico(self, tecnico: 'Tecnico'):
        self._tecnico_asignado = tecnico
        self._estado = "Atendida"

    def __str__(self) -> str:
        tec_str = self._tecnico_asignado.nombre_completo if self._tecnico_asignado else "Sin Asignar"
        return f"Ticket: {self._codigo} | Cliente: {self._cliente.nombre_completo} | Estado: {self._estado} | Técnico: {tec_str}"


# ----------------------------------------------------------
# 2. clase abstracta y jerarquia
# ----------------------------------------------------------

class Empleado(ABC):
    def __init__(self, dni: str, nombre: str, apellido: str, sueldo_base: float):
        self._dni = dni
        self._nombre = nombre
        self._apellido = apellido
        self._sueldo_base = sueldo_base

    @property
    def dni(self) -> str:
        return self._dni

    @property
    def nombre_completo(self) -> str:
        return f"{self._nombre} {self._apellido}"

    @property
    def sueldo_base(self) -> float:
        return self._sueldo_base

    # Reglas de negocio de retenciones legales
    def calcular_afp(self) -> float:
        """Descuento obligatorio del 10% por AFP"""
        return self._sueldo_base * 0.10

    def calcular_essalud(self) -> float:
        """Aporte del 8% a EsSalud"""
        return self._sueldo_base * 0.08

    @abstractmethod
    def calcular_sueldo_neto(self) -> float:
        """Método abstracto polimórfico"""
        pass


class Tecnico(Empleado):
    def __init__(self, dni: str, nombre: str, apellido: str, sueldo_base: float, especialidad: str):
        super().__init__(dni, nombre, apellido, sueldo_base)
        self._especialidad = especialidad
        self._incidencias_resueltas = 0

    @property
    def incidencias_resueltas(self) -> int:
        return self._incidencias_resueltas

    def incrementar_incidencias(self):
        self._incidencias_resueltas += 1

    def calcular_bono(self) -> float:
        # El personal técnico recibe un bono del 10% por cada incidencia resuelta
        bono_por_incidencia = self._sueldo_base * 0.10
        return self._incidencias_resueltas * bono_por_incidencia

    def calcular_sueldo_neto(self) -> float:
        # Sueldo Base + Bono por Rendimiento - AFP
        ingresos = self._sueldo_base + self.calcular_bono()
        return ingresos - self.calcular_afp()


class Administrativo(Empleado):
    def __init__(self, dni: str, nombre: str, apellido: str, sueldo_base: float):
        super().__init__(dni, nombre, apellido, sueldo_base)
        self._incidencias_gestionadas = 0

    @property
    def incidencias_gestionadas(self) -> int:
        return self._incidencias_gestionadas

    def incrementar_gestion(self):
        self._incidencias_gestionadas += 1

    def calcular_bono(self) -> float:
        # El personal administrativo recibe un bono del 5% por incidencias supervisadas/gestionadas
        bono_por_gestion = self._sueldo_base * 0.05
        return self._incidencias_gestionadas * bono_por_gestion

    def calcular_sueldo_neto(self) -> float:
        # Sueldo Base + Bono de Gestión - AFP
        ingresos = self._sueldo_base + self.calcular_bono()
        return ingresos - self.calcular_afp()


# ---------------------------------------------------------
# 3. sistema central
# ---------------------------------------------------------

class SistemaWOWPeru:
    def __init__(self):
        self._empleados: List[Empleado] = []
        self._clientes: List[Cliente] = []
        self._incidencias: List[Incidencia] = []

    def registrar_empleado(self, emp: Empleado):
        if self.buscar_empleado(emp.dni):
            raise DniInvalidoException(f"Ya existe un empleado registrado con el DNI {emp.dni}.")
        self._empleados.append(emp)

    def buscar_empleado(self, dni: str) -> Optional[Empleado]:
        for emp in self._empleados:
            if emp.dni == dni:
                return emp
        return None

    def registrar_cliente(self, cli: Cliente):
        if self.buscar_cliente(cli.dni):
            raise DniInvalidoException(f"Ya existe un cliente registrado con el DNI {cli.dni}.")
        self._clientes.append(cli)

    def buscar_cliente(self, dni: str) -> Optional[Cliente]:
        for cli in self._clientes:
            if cli.dni == dni:
                return cli
        return None

    def registrar_incidencia(self, ticket: str, dni_cliente: str, descripcion: str):
        cliente = self.buscar_cliente(dni_cliente)
        if not cliente:
            raise ValueError("El DNI del cliente no se encuentra registrado en el sistema.")
        
        if any(i.codigo == ticket for i in self._incidencias):
            raise ValueError(f"El código de ticket '{ticket}' ya existe.")

        incidencia = Incidencia(ticket, cliente, descripcion)
        self._incidencias.append(incidencia)

    def asignar_tecnico_a_incidencia(self, ticket: str, dni_tecnico: str):
        incidencia = next((i for i in self._incidencias if i.codigo == ticket), None)
        if not incidencia:
            raise ValueError("Ticket de incidencia no encontrado.")
        
        if incidencia.estado == "Atendida":
            raise ValueError("Esta incidencia ya cuenta con un técnico asignado y fue atendida.")

        emp = self.buscar_empleado(dni_tecnico)
        if not isinstance(emp, Tecnico):
            raise ValueError("El DNI ingresado no corresponde a un personal Técnico operativo.")

        incidencia.asignar_tecnico(emp)
        emp.incrementar_incidencias()

    def listar_incidencias(self):
        if not self._incidencias:
            print("\n>> No hay incidencias registradas en el sistema.")
            return
        print("\n" + "="*80)
        print("                     LISTADO DE INCIDENCIAS OPERATIVAS")
        print("="*80)
        for inc in self._incidencias:
            print(inc)
        print("="*80)

    def listar_planilla_sueldos(self):
        if not self._empleados:
            print("\n>> No hay empleados registrados en la planilla.")
            return

        print("\n" + "="*105)
        print(f"{'DNI':<10} | {'Nombre Completo':<22} | {'Cargo':<15} | {'S. Base':<10} | {'Bono':<10} | {'AFP (10%)':<10} | {'Neto':<10}")
        print("="*105)
        for emp in self._empleados:
            cargo = "Técnico" if isinstance(emp, Tecnico) else "Administrativo"
            bono = emp.calcular_bono()
            print(f"{emp.dni:<10} | {emp.nombre_completo:<22} | {cargo:<15} | "
                  f"S/{emp.sueldo_base:<8.2f} | S/{bono:<8.2f} | S/{emp.calcular_afp():<8.2f} | "
                  f"S/{emp.calcular_sueldo_neto():<8.2f}")
        print("="*105)


# -----------------------------------------------------------
# 4. validacion de DNI
# -----------------------------------------------------------

def validar_dni_personalizado(dni: str) -> str:
    dni = dni.strip()
    if not dni.isdigit() or len(dni) != 8:
        raise DniInvalidoException("Error de validación: El DNI debe ser estrictamente numérico y contener exactamente 8 dígitos.")
    return dni


# -----------------------------------------------------------
# 5. menu y control
# -----------------------------------------------------------

def ejecutar_menu():
    sistema = SistemaWOWPeru()
    
   # Datos iniciales de prueba para demostración
    sistema.registrar_empleado(Tecnico("00000001", "Andree", "Pajuelo", 2500.0, "Fibra Óptica"))
    sistema.registrar_empleado(Tecnico("00000002", "Jairo", "Ibañez", 2500.0, "Fibra Óptica"))
    sistema.registrar_empleado(Administrativo("00000003", "Borelly", "Medina", 2000.0))
    sistema.registrar_empleado(Administrativo("00000004", "Kolver", "Valer", 2000.0))
    sistema.registrar_cliente(Cliente("99999993", "Borelly", "Medina", "Av. La Molina 123", "300 Mbps"))
    sistema.registrar_cliente(Cliente("99999994", "Kolver", "Valer", "Av. La Molina 321", "200 Mbps"))
    sistema.registrar_cliente(Cliente("99999991", "Andree", "Pajuelo", "Av. La Molina 987", "300 Mbps"))
    sistema.registrar_cliente(Cliente("99999992", "Jairo", "Ibañez", "Av. La Molina 789", "200 Mbps"))
    sistema.registrar_incidencia("tck001", "99999991", "Falla de conexion del router")
    sistema.registrar_incidencia("tck002", "99999992", "Sin conexion a internet")

    while True:
        print("\n=== SISTEMA DE GESTIÓN OPERATIVA Y RRHH - WOW PERÚ ===")
        print("1. Registrar Empleado (Técnico / Administrativo) - HU01")
        print("2. Registrar Cliente")
        print("3. Registrar Incidencia Técnica")
        print("4. Buscar Cliente por DNI - HU02")
        print("5. Asignar Técnico a Incidencia ")
        print("6. Listar Incidencias Operativas - HU03")
        print("7. Calcular y Listar Planilla de Sueldos y Bonos - HU04")
        print("8. Salir")

        try:
            print("_"*80)
            opcion = int(input("\nSeleccione una opción (1-8): "))

            if opcion == 1:
                print("\n-- Registro de Personal --")
                tipo = input("Tipo (1: Técnico, 2: Administrativo): ").strip()
                dni = validar_dni_personalizado(input("DNI (8 dígitos): "))
                nombre = input("Nombres: ").strip()
                apellido = input("Apellidos: ").strip()
                if not nombre or not apellido:
                    raise ValueError("Los nombres y apellidos no pueden estar vacíos.")
                
                sueldo = float(input("Sueldo Base (S/): "))
                if sueldo <= 0:
                    raise ValueError("El sueldo base debe ser mayor a 0.")

                if tipo == "1":
                    especialidad = input("Especialidad técnica: ").strip()
                    sistema.registrar_empleado(Tecnico(dni, nombre, apellido, sueldo, especialidad))
                elif tipo == "2":
                    sistema.registrar_empleado(Administrativo(dni, nombre, apellido, sueldo))
                else:
                    raise ValueError("Opción de tipo de empleado inválida.")
                print(">> ¡Empleado registrado correctamente en el sistema!")
                print("-"*80)
                print("_"*80)

            elif opcion == 2:
                print("\n-- Registro de Cliente --")
                dni = validar_dni_personalizado(input("DNI del Cliente (8 dígitos): "))
                nombre = input("Nombres: ").strip()
                apellido = input("Apellidos: ").strip()
                direccion = input("Dirección de instalación: ").strip()
                plan = input("Plan de internet contratado: ").strip()
                
                sistema.registrar_cliente(Cliente(dni, nombre, apellido, direccion, plan))
                print(">> ¡Cliente registrado con éxito!")
                print("-"*80)
                print("_"*80)

            elif opcion == 3:
                print("\n-- Registro de Incidencia --")
                ticket = input("Código de Ticket (ej. tck001): ").strip()
                dni_cli = validar_dni_personalizado(input("DNI del Cliente afectado: "))
                desc = input("Descripción de la falla técnica: ").strip()
                
                sistema.registrar_incidencia(ticket, dni_cli, desc)
                print(">> ¡Incidencia registrada y en espera de técnico!")
                print("-"*80)
                print("_"*80)

            elif opcion == 4:
                print("\n-- Búsqueda de Cliente --")
                dni_cli = validar_dni_personalizado(input("Ingrese DNI a buscar: "))
                cli = sistema.buscar_cliente(dni_cli)
                if cli:
                    print(f"\n[CLIENTE ENCONTRADO]: {cli}")
                    print("-"*80)
                    print("_"*80)
                else:
                    print(">> No se encontró ningún cliente registrado con ese DNI.")
                    print("-"*80)
                    print("_"*80)

            elif opcion == 5:
                print("\n-- Asignación Inmediata de Técnico --")
                ticket = input("Código del Ticket a atender (ej. tck001): ").strip()
                dni_tec = validar_dni_personalizado(input("DNI del Técnico disponible: "))
                sistema.asignar_tecnico_a_incidencia(ticket, dni_tec)
                print(">> ¡Técnico asignado exitosamente! (Conflicto de doble asignación prevenido).")
                print("-"*80)
                print("_"*80)

            elif opcion == 6:
                sistema.listar_incidencias()

            elif opcion == 7:
                sistema.listar_planilla_sueldos()

            elif opcion == 8:
                print("\nSaliendo del sistema de WOW PERÚ... ¡Hasta pronto!")
                print("-"*80)
                print("#"*80)
                break
            else:
                print(">> Opción no válida. Ingrese un número del 1 al 8.")
                print("-"*80)
                print("_"*80)

        except DniInvalidoException as die:
            print(f"\n[EXCEPCIÓN PERSONALIZADA DE DNI]: {die}")
            print("-"*80)
            print("_"*80)
        except ValueError as ve:
            print(f"\n[ERROR DE VALIDACIÓN]: {ve}")
            print("-"*80)
            print("_"*80)
        except Exception as e:
            print(f"\n[ERROR INESPERADO]: {e}")
            print("-"*80)
            print("_"*80)

if __name__ == "__main__":
    ejecutar_menu()

    # Fin

# Para guardar en git
#  git add .
#  git status
#  git commit -m "Mensaje"
#  git push