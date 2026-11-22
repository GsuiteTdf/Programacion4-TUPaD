"""Demostración reproducible de síntomas presentes antes del refactor de la Parte 1.

No reintroduce los problemas en el dominio final: usa mini-clases locales que
replican exclusivamente el comportamiento defectuoso del código de partida.
"""

from __future__ import annotations

from figuras import Lado, Triangulo


class PoligonoJavaistaDefaultMutable:
    def __init__(self, observaciones: list[str] = []) -> None:  # noqa: B006
        self._observaciones = observaciones


class PoligonoJavaistaAlias:
    def __init__(self, lados: list[float]) -> None:
        self._lados = lados


def demostrar_default_mutable() -> None:
    print("\nSÍNTOMA 1 — argumento por defecto mutable compartido")
    p1 = PoligonoJavaistaDefaultMutable()
    p2 = PoligonoJavaistaDefaultMutable()
    p1._observaciones.append("solo debía pertenecer a p1")
    print(f"p1._observaciones is p2._observaciones -> {p1._observaciones is p2._observaciones}")
    print(f"p2 ve la observación de p1 -> {p2._observaciones}")

    correcto1 = Triangulo([3, 4, 5])
    correcto2 = Triangulo([3, 4, 5])
    correcto1.agregar_observacion("solo pertenece al primero")
    print(f"Versión corregida, observaciones del segundo -> {correcto2.observaciones()}")


def demostrar_alias_externo() -> None:
    print("\nSÍNTOMA 2 — alias de una colección recibida")
    lista = [3.0, 4.0, 5.0]
    defectuoso = PoligonoJavaistaAlias(lista)
    lista.append(99.0)
    print(f"Mutar la lista externa cambia el objeto defectuoso -> {defectuoso._lados}")

    longitudes = [3.0, 4.0, 5.0]
    correcto = Triangulo(longitudes)
    longitudes.append(99.0)
    print(f"Versión corregida conserva 3 lados -> {len(correcto.lados())}")


def demostrar_property_sin_cambiar_cliente() -> None:
    print("\nPROPERTY — el cliente conserva la misma sintaxis")

    class LadoAntes:
        def __init__(self, longitud: float) -> None:
            self.longitud = longitud

    antes = LadoAntes(5)
    despues = Lado(5)
    # La línea cliente es idéntica. En la segunda clase, @property puede validar
    # sin obligar a migrar a getLongitud()/setLongitud().
    print(f"Antes: lado.longitud -> {antes.longitud}")
    print(f"Después: lado.longitud -> {despues.longitud}")
    try:
        despues.longitud = 0
    except ValueError as error:
        print(f"La property agrega validación sin cambiar el acceso: {error}")


if __name__ == "__main__":
    demostrar_default_mutable()
    demostrar_alias_externo()
    demostrar_property_sin_cambiar_cliente()
