# Food Store - Backend Unidad 8

Backend FastAPI + SQLModel + PostgreSQL para el TP de Programación IV - Unidad 8.

## Arquitectura

- `core/repository.py`: repositorio base sin `commit()` ni `rollback()`.
- `core/unit_of_work.py`: controla la transacción completa.
- `categoria/`, `producto/`, `ingrediente/`: CRUD del catálogo.
- `pedido/`: Models - Schemas - Repository - UoW - Service - Router.

El módulo `pedido` implementa el modelo simplificado solicitado por la consigna: `Pedido` y `DetallePedido`; no crea Usuario, DirecciónEntrega, FormaPago, EstadoPedido ni HistorialEstadoPedido.

## PostgreSQL

Crear la base:

```sql
CREATE DATABASE foodstore_u8;
```

Configurar `.env`:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/foodstore_u8
```

## Instalación y ejecución

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m fastapi dev app/main.py
```

Swagger: `http://localhost:8000/docs`

## REST Client

- `categorias.http`
- `productos.http`
- `ingredientes.http`
- `pedidos.http`

`pedidos.http` demuestra 201, 204, 404, 409 y 422, el cálculo del total, los estados permitidos y el rollback cuando un detalle referencia un producto inexistente. Se puede ejecutar más de una vez: cada corrida crea sus propios productos.

## Reglas implementadas

- Pedido sin detalles, cantidad menor que 1, producto repetido o estado fuera de PENDIENTE/CONFIRMADO/ENTREGADO/CANCELADO: 422.
- Producto inexistente en un detalle: 404 y rollback completo (no queda el pedido).
- Pedido inexistente o dado de baja lógica: 404.
- Categoría duplicada (sin distinguir mayúsculas) o con productos asociados: 409.
- Producto incluido en pedidos: no se puede eliminar (409), como indica la FK `RESTRICT` de `DetallePedido.producto_id` en el UML.
