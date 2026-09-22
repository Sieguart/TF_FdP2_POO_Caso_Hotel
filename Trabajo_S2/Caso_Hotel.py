#Inicio
from abc import ABC, abstractmethod

# 1
class Empleado(ABC):
    def __init__(self, dni: str, nombre: str, sueldo_base: float):
        self._dni = dni
        self._nombre = nombre
        self._sueldo_base = sueldo_base

    @property
    def dni(self):
        return self._dni

    @property
    def sueldo_base(self):
        return self._sueldo_base

    # Reglas
    def calcular_afp(self) -> float:
        return self._sueldo_base * 0.10  # 10% AFP

    def calcular_essalud(self) -> float:
        return self._sueldo_base * 0.08  # 8% EsSalud

    # Método abstracto
    @abstractmethod
    def calcular_sueldo_neto(self) -> float:
        pass


# 2
class EmpleadoPlanilla(Empleado):
    def __init__(self, dni: str, nombre: str, sueldo_base: float, asignacion_familiar: float = 102.50):
        super().__init__(dni, nombre, sueldo_base)
        self._asignacion_familiar = asignacion_familiar

    def calcular_sueldo_neto(self) -> float:
        descuentos = self.calcular_afp()
        return self._sueldo_base + self._asignacion_familiar - descuentos


class EmpleadoPorHoras(Empleado):
    def __init__(self, dni: str, nombre: str, horas_trabajadas: int, tarifa_hora: float):
        super().__init__(dni, nombre, horas_trabajadas * tarifa_hora)
        self.horas_trabajadas = horas_trabajadas
        self.tarifa_hora = tarifa_hora

    def calcular_sueldo_neto(self) -> float:
        return self.horas_trabajadas * self.tarifa_hora


# 3
class GestionRRHH:
    def __init__(self):
        self._empleados = [] 

    def agregar_empleado(self, emp: Empleado):
        self._empleados.append(emp)

    def listar_planilla_pago(self):
        print("\n--- PLANILLA DE SUELDOS ---")
        for emp in self._empleados:
            print(f"DNI: {emp.dni} | Nombre: {emp._nombre} | "
                  f"AFP: S/{emp.calcular_afp():.2f} | "
                  f"EsSalud: S/{emp.calcular_essalud():.2f} | "
                  f"Neto: S/{emp.calcular_sueldo_neto():.2f}")


# 4
def ejecutar_menu():
    sistema = GestionRRHH()
    while True:
        print("\n=== SISTEMA DE GESTIÓN DE RRHH - HOTEL ===")
        print("1. Registrar Empleado Planilla")
        print("2. Registrar Empleado Por Horas")
        print("3. Listar Planilla de Pagos")
        print("4. Salir")
        
        try:
            opcion = int(input("Seleccione una opción: "))
            if opcion == 1:
                dni = input("DNI: ")
                nombre = input("Nombre: ")
                sueldo = float(input("Sueldo Base: "))
                sistema.agregar_empleado(EmpleadoPlanilla(dni, nombre, sueldo))
                print("¡Empleado registrado con éxito!")
            elif opcion == 2:
                dni = input("DNI: ")
                nombre = input("Nombre: ")
                horas = int(input("Horas trabajadas: "))
                tarifa = float(input("Tarifa por hora: "))
                sistema.agregar_empleado(EmpleadoPorHoras(dni, nombre, horas, tarifa))
                print("¡Empleado registrado con éxito!")
            elif opcion == 3:
                sistema.listar_planilla_pago()
            elif opcion == 4:
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida. Intente nuevamente.")
        except ValueError:
            print("Error: Ingrese un valor numérico válido.")

if __name__ == "__main__":
    ejecutar_menu()