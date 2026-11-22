"""Parte 1 corregida: mismo dominio de partida, ahora con decisiones Python idiomáticas.

Los ocho java-ismos diagnosticados y su justificación están documentados en
``informe.md``. Este archivo conserva el alcance de la Parte 1 para que pueda
compararse con el material entregado por la cátedra.
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod


class Figura(ABC):
    def __init__(self, nombre: str, color: str) -> None:
        self._nombre = nombre
        self._color = color

    @abstractmethod
    def area(self) -> float:
        raise NotImplementedError


class Lado:
    def __init__(self, longitud: float) -> None:
        self._longitud = 1.0
        self.longitud = longitud

    @property
    def longitud(self) -> float:
        return self._longitud

    @longitud.setter
    def longitud(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("La longitud debe ser positiva")
        self._longitud = float(valor)


class Poligono(Figura, ABC):
    def __init__(
        self,
        nombre: str,
        color: str,
        longitudes: list[float] | tuple[float, ...],
        observaciones: list[str] | tuple[str, ...] | None = None,
    ) -> None:
        super().__init__(nombre, color)
        self._lados = [Lado(longitud) for longitud in longitudes]
        self._observaciones = list(observaciones) if observaciones is not None else []
        if len(self._lados) != self.lados_esperados():
            raise ValueError("Cantidad de lados incorrecta")

    @abstractmethod
    def lados_esperados(self) -> int:
        raise NotImplementedError

    def perimetro(self) -> float:
        return sum(lado.longitud for lado in self._lados)

    def agregar_observacion(self, texto: str) -> None:
        self._observaciones.append(texto)

    def lados(self) -> tuple[Lado, ...]:
        return tuple(self._lados)


class Triangulo(Poligono):
    def __init__(
        self,
        longitudes: list[float] | tuple[float, ...],
        nombre: str = "Triángulo",
        color: str = "negro",
    ) -> None:
        super().__init__(nombre, color, longitudes)

    def lados_esperados(self) -> int:
        return 3

    def area(self) -> float:
        a, b, c = (lado.longitud for lado in self._lados)
        s = (a + b + c) / 2
        return math.sqrt(s * (s - a) * (s - b) * (s - c))


class Cuadrado(Poligono):
    def __init__(
        self,
        longitudes: list[float] | tuple[float, ...],
        nombre: str = "Cuadrado",
        color: str = "negro",
    ) -> None:
        super().__init__(nombre, color, longitudes)

    def lados_esperados(self) -> int:
        return 4

    def area(self) -> float:
        return self._lados[0].longitud**2


class PoligonoRegular:
    """Rediseñado sin heredar de Poligono: participa por comportamiento."""

    def __init__(self, nombre: str, color: str, medida: float, cantidad: int) -> None:
        if cantidad < 3 or medida <= 0:
            raise ValueError("Datos inválidos para un polígono regular")
        self._nombre = nombre
        self._color = color
        self._cantidad = cantidad
        self._lados = [Lado(medida) for _ in range(cantidad)]

    def perimetro(self) -> float:
        return sum(lado.longitud for lado in self._lados)

    def area(self) -> float:
        lado = self._lados[0].longitud
        return self._cantidad * lado**2 / (4 * math.tan(math.pi / self._cantidad))


if __name__ == "__main__":
    activo = True
    if activo:
        t = Triangulo([3, 4, 5], "Triángulo", "rojo")
        c = Cuadrado([2, 2, 2, 2], "Cuadrado", "azul")
        print(f"Perímetro del triángulo: {t.perimetro()}")
        print(f"Perímetro del cuadrado: {c.perimetro()}")
        t.agregar_observacion("revisar el vértice A")
        print(f"Longitud del primer lado: {t.lados()[0].longitud}")
        r = PoligonoRegular("Pentágono regular", "verde", 4, 5)
        print(f"Perímetro del pentágono regular: {r.perimetro()}")
