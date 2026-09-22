from abc import ABC, abstractmethod

# ==========================================
# 1. CLASES DE SOPORTE
# ==========================================
class Capacitacion:
    def __init__(self, curso: str, horas: int):
        self.curso = curso
        self.horas = horas

    def __str__(self):
        return f"Curso: {self.curso} ({self.horas} hrs)"

class Vacacion:
    def __init__(self, dias: int, estado: str = "Aprobado"):
        self.dias = dias
        self.estado = estado

    def __str__(self):
        return f"Días: {self.dias} | Estado: {self.estado}"


# ==========================================
# 2. CLASE BASE
# ==========================================
class Empleado(ABC):
    def __init__(self, dni: str, nombre: str, sueldo_base: float):
        self._dni = dni
        self._nombre = nombre
        self._sueldo_base = sueldo_base
        self._capacitaciones = [] 
        self._vacaciones = []    

    @property
    def dni(self):
        return self._dni

    @property
    def nombre(self):
        return self._nombre

    @property
    def sueldo_base(self):
        return self._sueldo_base

    # Reglas de negocio
    def calcular_afp(self) -> float:
        """10% de AFP sobre el sueldo base"""
        return self._sueldo_base * 0.10

    def calcular_essalud(self) -> float:
        """8% de EsSalud sobre el sueldo base"""
        return self._sueldo_base * 0.08

    def calcular_impuesto_renta(self) -> float:
        """Cálculo aproximado de Impuesto a la Renta 5ta Categoría (8% si supera UIT mensual ~ S/2300)"""
        if self._sueldo_base > 2300:
            return (self._sueldo_base - 2300) * 0.08
        return 0.0

    def agregar_capacitacion(self, curso: str, horas: int):
        self._capacitaciones.append(Capacitacion(curso, horas))

    def registrar_vacaciones(self, dias: int):
        self._vacaciones.append(Vacacion(dias))

    @abstractmethod
    def calcular_sueldo_neto(self) -> float:
        """Método abstracto polimórfico a implementar en subclases"""
        pass


# ==========================================
# 3. SUBCLASES CONCRETAS
# ==========================================
class EmpleadoPlanilla(Empleado):
    def __init__(self, dni: str, nombre: str, sueldo_base: float, asignacion_familiar: float = 102.50):
        super().__init__(dni, nombre, sueldo_base)
        self._asignacion_familiar = asignacion_familiar

    def calcular_sueldo_neto(self) -> float:
        descuentos = self.calcular_afp() + self.calcular_impuesto_renta()
        ingresos = self._sueldo_base + self._asignacion_familiar
        return ingresos - descuentos


class EmpleadoPorHoras(Empleado):
    def __init__(self, dni: str, nombre: str, horas_trabajadas: int, tarifa_hora: float):
        super().__init__(dni, nombre, horas_trabajadas * tarifa_hora)
        self.horas_trabajadas = horas_trabajadas
        self.tarifa_hora = tarifa_hora

    def calcular_sueldo_neto(self) -> float:
        descuentos = self.calcular_afp()
        return (self.horas_trabajadas * self.tarifa_hora) - descuentos
