"""Demo integradora exigida por la Parte 5 del TPI."""

from __future__ import annotations

import gc
import weakref

from figuras import (
    Cuadrado,
    Etiqueta,
    Exportable,
    Hexagono,
    Pentagono,
    Poligono,
    Taller,
    Triangulo,
    exportar_todo,
)
from libreria_externa import PlanoCAD


def mostrar_falla_temprana() -> None:
    print("\n=== Falla temprana de ABC ===")

    class PoligonoIncompleto(Poligono):
        def area(self) -> float:
            return 0.0

    try:
        PoligonoIncompleto("Incompleto", "gris", [1, 1, 1])  # type: ignore[abstract]
    except TypeError as error:
        print(f"No se puede construir sin lados_esperados(): {error}")


def mostrar_ciclos_de_vida() -> None:
    print("\n=== Ciclos de vida ===")

    temporal = Triangulo([3, 4, 5], color="violeta")
    referencia_lado = weakref.ref(temporal.lados()[0])
    del temporal
    gc.collect()
    print(
        "Composición Polígono-Lado: al desaparecer el todo y sin referencias externas, "
        f"el lado también desaparece -> {referencia_lado() is None}"
    )

    poligono = Cuadrado([2, 2, 2, 2], color="celeste")
    taller = Taller()
    taller.recibir(poligono)
    del taller
    gc.collect()
    print(
        "Agregación Taller-Polígono: el polígono recibido sobrevive al Taller -> "
        f"perímetro {poligono.perimetro():.2f}"
    )


def main() -> None:
    triangulo = Triangulo([3, 4, 5], color="rojo")
    cuadrado = Cuadrado([4, 4, 4, 4], color="azul")
    pentagono = Pentagono([3, 3, 3, 3, 3], color="verde")
    hexagono = Hexagono([2, 2, 2, 2, 2, 2], color="amarillo")

    # Asociación 0..1: las Etiqueta existen antes de ser asociadas a los Lado.
    etiqueta_base = Etiqueta("base")
    etiqueta_control = Etiqueta("lado a revisar")
    triangulo.lados()[0].etiquetar(etiqueta_base)
    cuadrado.lados()[1].etiquetar(etiqueta_control)

    taller = Taller()
    for figura in (triangulo, cuadrado, pentagono, hexagono):
        taller.recibir(figura)
        taller.restaurar(figura)

    print("=== Inventario del taller ===")
    for indice, poligono in enumerate(taller.inventario(), start=1):
        print(
            f"{indice}. {poligono.exportar()} | área={poligono.area():.2f} | "
            f"observaciones={poligono.observaciones()}"
        )

    print("\nEtiquetas:")
    print(f"Triángulo lado 1 -> {triangulo.lados()[0].descripcion_etiqueta()}")
    print(f"Cuadrado lado 2 -> {cuadrado.lados()[1].descripcion_etiqueta()}")

    plano = PlanoCAD("PL-UTN-03", "1:50")
    items: list[Exportable] = [*taller.inventario(), plano]
    print("\n=== Exportación estructural (Protocol) ===")
    for linea in exportar_todo(items):
        print(linea)

    mostrar_ciclos_de_vida()
    mostrar_falla_temprana()


if __name__ == "__main__":
    main()
