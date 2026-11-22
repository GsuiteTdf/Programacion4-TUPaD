"""Dominio final del TPI de Programación Orientada a Objetos.

La implementación prioriza Python idiomático: encapsulamiento por convención,
ABC cuando el dominio expresa una relación "es-un" y Protocol para contratos
estructurales que también pueden cumplir clases externas.
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

from libreria_externa import PlanoCAD


class Exportable(Protocol):
    """Contrato estructural: cualquier objeto con exportar() lo satisface."""

    def exportar(self) -> str:
        """Devuelve una representación exportable del objeto."""
        ...


@dataclass(frozen=True, slots=True)
class Etiqueta:
    """Dato inmutable asociado opcionalmente a un lado."""

    texto: str

    def __post_init__(self) -> None:
        if not self.texto.strip():
            raise ValueError("La etiqueta no puede estar vacía")


class Figura(ABC):
    """Concepto abstracto del dominio."""

    def __init__(self, nombre: str, color: str) -> None:
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        if not color.strip():
            raise ValueError("El color no puede estar vacío")
        self._nombre = nombre
        self._color = color

    @abstractmethod
    def area(self) -> float:
        """Calcula el área de la figura."""
        raise NotImplementedError


class Lado:
    """Parte componente de un polígono."""

    def __init__(self, longitud: float, etiqueta: Etiqueta | None = None) -> None:
        self._longitud = 1.0
        self.longitud = longitud
        # Asociación: la Etiqueta llega ya construida y puede existir sin el Lado.
        self._etiqueta = etiqueta

    @property
    def longitud(self) -> float:
        """Longitud validada del lado.

        Aquí @property sí se justifica: el setter contiene una invariante.
        """

        return self._longitud

    @longitud.setter
    def longitud(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("La longitud debe ser positiva")
        self._longitud = float(valor)

    def escalar(self, factor: float) -> None:
        if factor <= 0:
            raise ValueError("El factor debe ser positivo")
        self.longitud = self._longitud * factor

    def etiquetar(self, etiqueta: Etiqueta | None) -> None:
        """Asocia o quita una etiqueta ya existente."""

        self._etiqueta = etiqueta

    def descripcion_etiqueta(self) -> str | None:
        return None if self._etiqueta is None else self._etiqueta.texto


class Poligono(Figura, ABC):
    """Jerarquía abstracta justificada por el dominio: todo subtipo es un polígono."""

    def __init__(
        self,
        nombre: str,
        color: str,
        longitudes: list[float] | tuple[float, ...],
        observaciones: list[str] | tuple[str, ...] | None = None,
    ) -> None:
        super().__init__(nombre, color)
        # Composición: el Poligono fabrica y posee sus Lado a partir de longitudes.
        self._lados = [Lado(longitud) for longitud in longitudes]
        self._observaciones = list(observaciones) if observaciones is not None else []
        esperados = self.lados_esperados()
        if len(self._lados) != esperados:
            raise ValueError(
                f"{type(self).__name__} requiere {esperados} lados; "
                f"se recibieron {len(self._lados)}"
            )

    @abstractmethod
    def lados_esperados(self) -> int:
        """Cantidad de lados exigida por cada subtipo concreto."""
        raise NotImplementedError

    def perimetro(self) -> float:
        return sum(lado.longitud for lado in self._lados)

    def lados(self) -> tuple[Lado, ...]:
        """Copia defensiva del contenedor interno."""

        return tuple(self._lados)

    def agregar_observacion(self, texto: str) -> None:
        if texto.strip():
            self._observaciones.append(texto)

    def observaciones(self) -> tuple[str, ...]:
        return tuple(self._observaciones)

    def exportar(self) -> str:
        medidas = ", ".join(f"{lado.longitud:g}" for lado in self._lados)
        return (
            f"{type(self).__name__}[nombre={self._nombre}, color={self._color}, "
            f"lados=({medidas}), perimetro={self.perimetro():.2f}]"
        )


def _validar_lados_iguales(lados: tuple[Lado, ...], figura: str) -> float:
    medida = lados[0].longitud
    if not all(math.isclose(lado.longitud, medida) for lado in lados[1:]):
        raise ValueError(f"{figura} requiere lados de igual longitud para calcular su área")
    return medida


def _area_regular(cantidad: int, lado: float) -> float:
    return cantidad * lado**2 / (4 * math.tan(math.pi / cantidad))


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
        semiperimetro = (a + b + c) / 2
        radicando = semiperimetro * (semiperimetro - a) * (semiperimetro - b) * (
            semiperimetro - c
        )
        if radicando <= 0:
            raise ValueError("Las longitudes no forman un triángulo válido")
        return math.sqrt(radicando)


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
        lado = _validar_lados_iguales(self.lados(), type(self).__name__)
        return lado**2


class Pentagono(Poligono):
    def __init__(
        self,
        longitudes: list[float] | tuple[float, ...],
        nombre: str = "Pentágono",
        color: str = "negro",
    ) -> None:
        super().__init__(nombre, color, longitudes)

    def lados_esperados(self) -> int:
        return 5

    def area(self) -> float:
        lado = _validar_lados_iguales(self.lados(), type(self).__name__)
        return _area_regular(self.lados_esperados(), lado)


class Hexagono(Poligono):
    def __init__(
        self,
        longitudes: list[float] | tuple[float, ...],
        nombre: str = "Hexágono",
        color: str = "negro",
    ) -> None:
        super().__init__(nombre, color, longitudes)

    def lados_esperados(self) -> int:
        return 6

    def area(self) -> float:
        lado = _validar_lados_iguales(self.lados(), type(self).__name__)
        return _area_regular(self.lados_esperados(), lado)


class PoligonoRegular:
    """Rediseño sin herencia.

    En el código de partida heredaba de Poligono para obtener un tipo común.
    En Python no necesita esa herencia: ofrece el comportamiento que requiere
    (perímetro, área y exportar) y participa por duck typing/Protocol.
    """

    def __init__(self, nombre: str, color: str, medida: float, cantidad: int) -> None:
        if cantidad < 3:
            raise ValueError("Un polígono regular requiere al menos 3 lados")
        if medida <= 0:
            raise ValueError("La medida debe ser positiva")
        self._nombre = nombre
        self._color = color
        self._cantidad = cantidad
        self._lados = [Lado(medida) for _ in range(cantidad)]

    def perimetro(self) -> float:
        return sum(lado.longitud for lado in self._lados)

    def area(self) -> float:
        return _area_regular(self._cantidad, self._lados[0].longitud)

    def lados(self) -> tuple[Lado, ...]:
        return tuple(self._lados)

    def exportar(self) -> str:
        return (
            f"PoligonoRegular[nombre={self._nombre}, color={self._color}, "
            f"cantidad={self._cantidad}, perimetro={self.perimetro():.2f}]"
        )


class Taller:
    """Agrega polígonos ya construidos; no controla su ciclo de vida."""

    def __init__(self) -> None:
        self._poligonos: list[Poligono] = []

    def recibir(self, poligono: Poligono) -> None:
        # Agregación: se guarda la referencia recibida, no se fabrica un Poligono.
        if poligono not in self._poligonos:
            self._poligonos.append(poligono)

    def restaurar(self, poligono: Poligono) -> None:
        if poligono not in self._poligonos:
            self.recibir(poligono)
        poligono.agregar_observacion("Restaurado en el taller")

    def inventario(self) -> tuple[Poligono, ...]:
        """Copia defensiva del inventario."""

        return tuple(self._poligonos)


def exportar_todo(items: list[Exportable]) -> list[str]:
    """Exporta objetos heterogéneos mediante contrato estructural."""

    return [item.exportar() for item in items]


# La importación explícita prueba que la clase externa está disponible sin tocarla.
# El chequeo estructural lo realiza mypy al usar PlanoCAD donde se espera Exportable.
def exportar_plano_externo(plano: PlanoCAD) -> str:
    return plano.exportar()


__all__ = [
    "Cuadrado",
    "Etiqueta",
    "Exportable",
    "Figura",
    "Hexagono",
    "Lado",
    "Pentagono",
    "Poligono",
    "PoligonoRegular",
    "Taller",
    "Triangulo",
    "exportar_todo",
]
