# UML final — TPI POO

```mermaid
classDiagram
    class Exportable {
        <<Protocol>>
        +exportar() str
    }

    class Figura {
        <<abstract>>
        #_nombre str
        #_color str
        +area()* float
    }

    class Poligono {
        <<abstract>>
        #_lados list~Lado~
        +lados_esperados()* int
        +perimetro() float
        +lados() tuple~Lado~
        +exportar() str
    }

    class Lado {
        #_longitud float
        #_etiqueta Etiqueta
        +longitud float
        +escalar(factor)
        +etiquetar(etiqueta)
    }

    class Etiqueta {
        <<frozen dataclass>>
        +texto str
    }

    class Taller {
        #_poligonos list~Poligono~
        +recibir(poligono)
        +restaurar(poligono)
        +inventario() tuple~Poligono~
    }

    class Triangulo
    class Cuadrado
    class Pentagono
    class Hexagono

    class PoligonoRegular {
        <<sin herencia: duck typing>>
        +perimetro() float
        +area() float
        +exportar() str
    }

    class PlanoCAD {
        <<libreria externa>>
        +exportar() str
    }

    Figura <|-- Poligono : herencia de dominio
    Poligono <|-- Triangulo
    Poligono <|-- Cuadrado
    Poligono <|-- Pentagono
    Poligono <|-- Hexagono

    Poligono "1" *-- "3..*" Lado : composición
    Lado "1" --> "0..1" Etiqueta : asociación
    Taller "1" o-- "0..*" Poligono : agregación

    Poligono ..|> Exportable : cumple
    PoligonoRegular ..|> Exportable : cumple sin heredar
    PlanoCAD ..|> Exportable : cumple sin saberlo
```

## Decisión reflejada

`PoligonoRegular` ya no hereda de `Poligono`: conserva únicamente el comportamiento que necesita y participa en `Exportable` por contrato estructural. La jerarquía nominal queda reservada para los subtipos que el dominio reconoce como especializaciones concretas de `Poligono`.
