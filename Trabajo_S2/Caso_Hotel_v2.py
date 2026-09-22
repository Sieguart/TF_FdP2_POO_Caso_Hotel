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

