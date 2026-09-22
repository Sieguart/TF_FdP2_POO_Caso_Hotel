#Inicio
from abc import ABC, abstractmethod
from typing import List, Optional

# -----------------------------------------
# 1. CLASES DE DOMINIO Y DE NEGOCIO
# -----------------------------------------

class Cliente:
    def __init__(self, dni: str, nombre: str, direccion: str, plan_internet: str):
        self._dni = dni
        self._nombre = nombre
        self._direccion = direccion
        self._plan_internet = plan_internet

    @property
    def dni(self) -> str:
        return self._dni

    @property
    def nombre(self) -> str:
        return self._nombre

    def __str__(self) -> str:
        return f"Cliente: {self._nombre} (DNI: {self._dni}) - Plan: {self._plan_internet}"


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
        tec_str = self._tecnico_asignado.nombre if self._tecnico_asignado else "Sin Asignar"
        return f"Ticket: {self._codigo} | Cliente: {self._cliente.nombre} | Estado: {self._estado} | Técnico: {tec_str}"


# ------------------------------------------
# 2. JERARQUÍA DE CLASES: EMPLEADOS
# ------------------------------------------

class Empleado(ABC):
    def __init__(self, dni: str, nombre: str, sueldo_base: float):
        self._dni = dni
        self._nombre = nombre
        self._sueldo_base = sueldo_base

    @property
    def dni(self) -> str:
        return self._dni

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def sueldo_base(self) -> float:
        return self._sueldo_base

    # Reglas de negocio
    def calcular_afp(self) -> float:
        """Descuento del 10% obligatorio de AFP"""
        return self._sueldo_base * 0.10

    def calcular_essalud(self) -> float:
        """Aporte del 8% a EsSalud por parte del empleador"""
        return self._sueldo_base * 0.08

    @abstractmethod
    def calcular_sueldo_neto(self) -> float:
        """Método polimórfico a ser implementado por las subclases"""
        pass


class Tecnico(Empleado):
    def __init__(self, dni: str, nombre: str, sueldo_base: float, especialidad: str):
        super().__init__(dni, nombre, sueldo_base)
        self._especialidad = especialidad
        self._incidencias_resueltas = 0

    @property
    def incidencias_resueltas(self) -> int:
        return self._incidencias_resueltas

    def incrementar_incidencias(self):
        self._incidencias_resueltas += 1

    def calcular_bono(self) -> float:
        # Bono de S/ 50 por cada incidencia resuelta
        return self._incidencias_resueltas * 50.0

    def calcular_sueldo_neto(self) -> float:
        # Sueldo Base + Bono - AFP
        return (self._sueldo_base + self.calcular_bono()) - self.calcular_afp()


class Administrativo(Empleado):
    def __init__(self, dni: str, nombre: str, sueldo_base: float, bono_gestion: float = 200.0):
        super().__init__(dni, nombre, sueldo_base)
        self._bono_gestion = bono_gestion

    def calcular_sueldo_neto(self) -> float:
        # Sueldo Base + Bono de Gestión - AFP
        return (self._sueldo_base + self._bono_gestion) - self.calcular_afp()


# ------------------------------------------
# 3. GESTOR CENTRAL DEL SISTEMA
# ------------------------------------------

class SistemaWOWPeru:
    def __init__(self):
        self._empleados: List[Empleado] = []
        self._clientes: List[Cliente] = []
        self._incidencias: List[Incidencia] = []

    def registrar_empleado(self, emp: Empleado):
        if self.buscar_empleado(emp.dni):
            raise ValueError(f"Ya existe un empleado con el DNI {emp.dni}.")
        self._empleados.append(emp)

    def buscar_empleado(self, dni: str) -> Optional[Empleado]:
        for emp in self._empleados:
            if emp.dni == dni:
                return emp
        return None

    def registrar_cliente(self, cli: Cliente):
        if self.buscar_cliente(cli.dni):
            raise ValueError(f"Ya existe un cliente registrado con el DNI {cli.dni}.")
        self._clientes.append(cli)

    def buscar_cliente(self, dni: str) -> Optional[Cliente]:
        for cli in self._clientes:
            if cli.dni == dni:
                return cli
        return None

    def registrar_incidencia(self, ticket: str, dni_cliente: str, descripcion: str):
        cliente = self.buscar_cliente(dni_cliente)
        if not cliente:
            raise ValueError("El DNI del cliente no se encuentra en la base de datos.")
        incidencia = Incidencia(ticket, cliente, descripcion)
        self._incidencias.append(incidencia)

    def asignar_tecnico_a_incidencia(self, ticket: str, dni_tecnico: str):
        incidencia = next((i for i in self._incidencias if i.codigo == ticket), None)
        if not incidencia:
            raise ValueError("Ticket de incidencia no encontrado.")
        
        emp = self.buscar_empleado(dni_tecnico)
        if not isinstance(emp, Tecnico):
            raise ValueError("El DNI ingresado no corresponde a un Técnico operativo.")

        incidencia.asignar_tecnico(emp)
        emp.incrementar_incidencias()

    def listar_planilla_sueldos(self):
        if not self._empleados:
            print("\nNo existen empleados registrados.")
            return

        print("\n" + "="*85)
        print(f"{'DNI':<10} | {'Nombre':<20} | {'AFP (10%)':<10} | {'EsSalud (8%)':<12} | {'Sueldo Neto':<10}")
        print("="*85)
        for emp in self._empleados:
            print(f"{emp.dni:<10} | {emp.nombre:<20} | S/{emp.calcular_afp():<8.2f} | "
                  f"S/{emp.calcular_essalud():<10.2f} | S/{emp.calcular_sueldo_neto():<8.2f}")
        print("="*85)

    def listar_incidencias(self):
        if not self._incidencias:
            print("\nNo hay incidencias registradas.")
            return
        print("\n--- LISTADO DE INCIDENCIAS OPERATIVAS ---")
        for inc in self._incidencias:
            print(inc)


# ------------------------------------------
# 4. MENÚ INTERACTIVO Y VALIDACIONES
# ------------------------------------------

def validar_dni(dni: str) -> str:
    dni = dni.strip()
    if not dni.isdigit() or len(dni) != 8:
        raise ValueError("El DNI debe ser numérico y contener exactamente 8 dígitos.")
    return dni

def menu_principal():
    sistema = SistemaWOWPeru()
    
    # Carga inicial de datos de prueba
    tec1 = Tecnico("71234567", "Carlos Mendoza", 2500.0, "Fibra Óptica")
    cli1 = Cliente("10987654", "Ana Torres", "Av. Primavera 123", "100 Mbps Fibra")
    sistema.registrar_empleado(tec1)
    sistema.registrar_cliente(cli1)

    while True:
        print("\n=== SISTEMA DE GESTIÓN OPERATIVA Y RRHH - WOW PERÚ ===")
        print("1. Registrar Empleado (Técnico / Administrativo) - HU01")
        print("2. Registrar Cliente")
        print("3. Registrar Incidencia Técnica")
        print("4. Buscar Cliente por DNI - HU02")
        print("5. Asignar Técnico a Incidencia")
        print("6. Listar Incidencias Pendientes/Atendidas - HU03")
        print("7. Calcular y Listar Planilla de Sueldos - HU04")
        print("8. Salir")

        try:
            opcion = int(input("\nSeleccione una opción: "))

            if opcion == 1:
                tipo = input("Tipo (1: Técnico, 2: Administrativo): ").strip()
                dni = validar_dni(input("DNI: "))
                nombre = input("Nombre completo: ").strip()
                sueldo = float(input("Sueldo base (S/): "))

                if tipo == "1":
                    esp = input("Especialidad técnica: ").strip()
                    sistema.registrar_empleado(Tecnico(dni, nombre, sueldo, esp))
                elif tipo == "2":
                    sistema.registrar_empleado(Administrativo(dni, nombre, sueldo))
                else:
                    raise ValueError("Tipo de empleado no válido.")
                print(">> ¡Empleado registrado exitosamente!")

            elif opcion == 2:
                dni = validar_dni(input("DNI del Cliente: "))
                nombre = input("Nombre completo: ").strip()
                dir_cli = input("Dirección de instalación: ").strip()
                plan = input("Plan contratado: ").strip()
                sistema.registrar_cliente(Cliente(dni, nombre, dir_cli, plan))
                print(">> ¡Cliente registrado correctamente!")

            elif opcion == 3:
                ticket = input("Código de Ticket (ej. TCK-101): ").strip()
                dni_cli = validar_dni(input("DNI del Cliente: "))
                desc = input("Descripción de la falla técnica: ").strip()
                sistema.registrar_incidencia(ticket, dni_cli, desc)
                print(">> ¡Incidencia registrada!")

            elif opcion == 4:
                dni_cli = validar_dni(input("Ingrese DNI a buscar: "))
                cli = sistema.buscar_cliente(dni_cli)
                if cli:
                    print(f"\n[ENCONTRADO]: {cli}")
                else:
                    print(">> Cliente no registrado.")

            elif opcion == 5:
                ticket = input("Código de Ticket: ").strip()
                dni_tec = validar_dni(input("DNI del Técnico a asignar: "))
                sistema.asignar_tecnico_a_incidencia(ticket, dni_tec)
                print(">> ¡Técnico asignado e incidencia actualizada!")

            elif opcion == 6:
                sistema.listar_incidencias()

            elif opcion == 7:
                sistema.listar_planilla_sueldos()

            elif opcion == 8:
                print("Saliendo del sistema de WOW PERÚ...")
                break

            else:
                print(">> Opción fuera de rango (1-8).")

        except ValueError as ve:
            print(f"\n[ERROR DE VALIDACIÓN]: {ve}")
        except Exception as e:
            print(f"\n[ERROR DEL SISTEMA]: {e}")

if __name__ == "__main__":
    menu_principal()

# Fin

# Para guardar en git
#  git add .
#  git status
#  git commit -m "Mensaje"
#  git push