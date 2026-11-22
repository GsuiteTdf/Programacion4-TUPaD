# Cejas_Gaston_TPI_POO

**Programación IV — Unidad 3 — Programación Orientada a Objetos**  
**Alumno:** Gastón Cejas  
**Carrera:** Tecnicatura Universitaria en Programación — UTN

## Contenido

- `figuras.py`: dominio completo de las Partes 1 a 4: ABC, relaciones, `Etiqueta`, `Taller`, `Protocol` y exportación.
- `parte1_diagnostico.py`: módulo de partida ya corregido, para comparar el antes y el después.
- `demo_sintomas.py`: reproduce dos síntomas de los java-ismos de la Parte 1 y muestra el caso de `@property`.
- `libreria_externa.py`: archivo original de la cátedra, **sin modificaciones**.
- `main.py`: demo ejecutable integradora con cuatro polígonos, etiquetas, Taller, PlanoCAD, ciclos de vida y falla temprana.
- `informe.md`: diagnóstico de los 8 java-ismos, equivalencias y respuestas obligatorias.
- `uml/modelo_final.md`: diagrama Mermaid coherente con el código final.
- `tests/test_figuras.py`: 7 tests complementarios sobre decisiones de diseño.
- `pyproject.toml`: configuración estricta de mypy y pytest.

## Verificación mínima exigida

```bash
python main.py
python demo_sintomas.py
```

## Verificación adicional

```bash
python -m pytest -q
python -m mypy --strict figuras.py parte1_diagnostico.py main.py demo_sintomas.py
```

Si `pytest` o `mypy` no están instalados:

```bash
python -m pip install -r requirements-dev.txt
```

## Decisiones principales

1. `Poligono` es ABC porque la herencia está justificada por el dominio.
2. `PoligonoRegular` deja de heredar: su comportamiento común se resuelve por duck typing.
3. `Exportable` es `Protocol`; por eso `PlanoCAD` cumple el contrato sin modificar la librería externa.
4. La composición, agregación y asociación se distinguen por ciclo de vida y por quién construye cada objeto.
5. Las colecciones internas se exponen mediante copias defensivas (`tuple`).
