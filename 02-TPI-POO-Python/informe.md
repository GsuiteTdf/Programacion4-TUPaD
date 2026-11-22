# Informe — TPI POO · Gastón Cejas

## 1. Ocho java-ismos

| # | Java-ismo | Dónde | Inversión | Corrección / síntoma |
|---|---|---|---|---|
| 1 | Accesores JavaBean por costumbre | `Figura.getNombre/getColor`, `Lado.getLongitud/setLongitud` | compilador → acuerdo | Se eliminan getters sin lógica; `Lado.longitud` usa `@property` porque valida. |
| 2 | `static` mutable accidental | `Poligono.catalogo` | declaración → runtime | Todas las instancias compartían lista; se elimina ese estado global. |
| 3 | Defaults mutables | `lados=[]`, `observaciones=[]` | declaración → runtime | Dos objetos compartían listas; se usa `None` y una lista nueva por instancia. |
| 4 | Imitar al constructor padre | `Poligono.__init__` reasigna nombre/color | compilador → acuerdo | Se llama `super().__init__()`. |
| 5 | Guardar alias externo | `self._lados = lados` | compilador → acuerdo | Una mutación externa alteraba el objeto; ahora el polígono fabrica sus `Lado` y devuelve tupla. |
| 6 | Acumulador manual | `Poligono.perimetro` | declaración → runtime | Se reemplaza por `sum(...)`. |
| 7 | Tratar hints/override como garantía | `area() -> int` devuelve `str` | declaración → runtime | Se corrige el tipo y el contrato se apoya en ABC, mypy y tests. |
| 8 | Overload simulado con `*args/isinstance` | constructores de `Triangulo/Cuadrado` | declaración → runtime | Firma única explícita con defaults. |

`demo_sintomas.py` reproduce los dos síntomas pedidos (default mutable y alias externo) y muestra el caso de `@property`: el cliente sigue usando `lado.longitud`, pero ahora la asignación se valida.

## 2. Relaciones

La diferencia está en el ciclo de vida. **Composición Polígono–Lado:** `self._lados = [Lado(longitud) for longitud in longitudes]`; el todo fabrica las partes. **Agregación Taller–Polígono:** `self._poligonos.append(poligono)`; recibe un polígono ya construido. **Asociación Lado–Etiqueta:** `self._etiqueta = etiqueta`; la etiqueta también llega construida y es opcional. `Poligono.lados()` y `Taller.inventario()` devuelven `tuple(...)` como copia defensiva del contenedor.

## 3. Herencia y `PoligonoRegular`

Mantengo `Poligono → Triangulo/Cuadrado/Pentagono/Hexagono` porque el dominio sí expresa “es-un”. `Poligono` es `ABC` y `lados_esperados()` es abstracto, de modo que una subclase incompleta falla al construir. **`PoligonoRegular` se rediseña sin heredar**: en el código de partida la herencia buscaba un tipo común; en Python puede ofrecer `perimetro()`, `area()` y `exportar()` por duck typing.

## 4. ABC vs Protocol

`Poligono` usa ABC porque hay parentesco de dominio y conviene falla temprana. `Exportable` usa `Protocol` porque `PlanoCAD` ya posee `exportar()` y no puede modificarse. Una ABC exigiría hacer heredar a la clase externa. Por eso la elección **la decide el dominio**; Python solo ofrece mecanismos nominales y estructurales para expresarla.

## Equivalencias en esta entrega

| Java | Python | Tipo | Criterio |
|---|---|---|---|
| `private/protected` | `_nombre`, `_lados` | Rediseño | Convención. |
| getter/setter validado | `@property longitud` | Rediseño | Hay lógica. |
| `abstract class` | `Poligono(ABC)` | Directa | Herencia de dominio. |
| método abstracto | `@abstractmethod` | Directa | Falla temprana. |
| interfaz | `Protocol Exportable` | Rediseño | Contrato estructural. |
| overload constructor | firma única + defaults | Rediseño | Python no sobrecarga por firma. |
| `static List` mutable | eliminado | Rediseño | Evita estado compartido. |
| acumulador/stream | `sum(...)` | Directa idiomática | Expresa intención. |

**Cierre.** El modelo se mantuvo donde representaba el dominio (figuras, polígonos y ciclos de vida). Cambió dónde vive el rigor: menos ceremonia del compilador y más convención, contratos adecuados, type hints y tests.
