from __future__ import annotations

import gc
import weakref

import pytest

from figuras import (
    Cuadrado,
    Etiqueta,
    Exportable,
    Poligono,
    Taller,
    Triangulo,
    exportar_todo,
)
from libreria_externa import PlanoCAD


def test_property_longitud_valida_invariante() -> None:
    lado = Triangulo([3, 4, 5]).lados()[0]
    lado.longitud = 6
    assert lado.longitud == 6
    with pytest.raises(ValueError):
        lado.longitud = 0


def test_lados_devuelve_copia_defensiva_del_contenedor() -> None:
    triangulo = Triangulo([3, 4, 5])
    copia = triangulo.lados()
    assert isinstance(copia, tuple)
    assert len(copia) == 3


def test_inventario_es_agregacion_y_copia_defensiva() -> None:
    cuadrado = Cuadrado([2, 2, 2, 2])
    taller = Taller()
    taller.recibir(cuadrado)
    inventario = taller.inventario()
    assert inventario == (cuadrado,)
    del taller
    assert cuadrado.perimetro() == 8


def test_composicion_lado_desaparece_con_poligono_sin_refs_externas() -> None:
    triangulo = Triangulo([3, 4, 5])
    lado_ref = weakref.ref(triangulo.lados()[0])
    del triangulo
    gc.collect()
    assert lado_ref() is None


def test_abc_falla_temprano_si_falta_lados_esperados() -> None:
    class Incompleto(Poligono):
        def area(self) -> float:
            return 0.0

    with pytest.raises(TypeError):
        Incompleto("x", "negro", [1, 1, 1])  # type: ignore[abstract]


def test_protocol_acepta_plano_cad_sin_herencia() -> None:
    triangulo = Triangulo([3, 4, 5])
    plano = PlanoCAD("A-1")
    items: list[Exportable] = [triangulo, plano]
    salida = exportar_todo(items)
    assert salida[0].startswith("Triangulo[")
    assert salida[1] == "PlanoCAD[A-1 @ 1:100]"


def test_etiqueta_es_inmutable() -> None:
    etiqueta = Etiqueta("base")
    with pytest.raises(Exception):
        etiqueta.texto = "otra"  # type: ignore[misc]
