# Programacion IV - TP1 Fundamentos de Spring

## Sistema de Gestion de Pedidos

Proyecto realizado a partir de la consigna del TP de Fundamentos de Spring.

### Requisitos cubiertos

- Spring Web
- Spring Data JPA
- Lombok
- H2 Database
- Spring Boot DevTools
- Modelo UML: Base, Usuario, Pedido, DetallePedido, Producto, Categoria, Calculable y enums
- Capa de DTOs solicitada por la consigna
- Inyeccion de dependencias por constructor
- Estereotipos `@Service`, `@Repository` y `@Component`
- Configuracion mediante `application.properties`
- `DataLoader` que instancia desde DTOs:
  - 2 usuarios
  - 3 pedidos, con 2 detalles cada uno
  - 3 categorias
  - 10 productos

## Ejecucion en Windows / VS Code

Desde la carpeta raiz del proyecto:

```powershell
.\gradlew.bat bootRun
```

El proyecto esta configurado para **Java 21**, que es el JDK instalado en el equipo.

Al iniciar, `DataLoader` carga automaticamente los datos del TP y muestra un resumen en la terminal.

## Consola H2

Abrir en el navegador:

`http://localhost:8080/h2-console`

Datos de conexion:

- JDBC URL: `jdbc:h2:mem:pedidosdb`
- User Name: `sa`
- Password: dejar vacio

Tablas principales:

- `USUARIOS`
- `PEDIDOS`
- `DETALLES_PEDIDO`
- `PRODUCTOS`
- `CATEGORIAS`

## Pruebas

```powershell
.\gradlew.bat test
```

La prueba comprueba que se carguen exactamente 2 usuarios, 3 pedidos, 3 categorias y 10 productos, y al menos 6 detalles de pedido.

## Estructura DTO requerida

```text
dto/
├── categoria/
│   ├── CategoriaCreate.java
│   ├── CategoriaDto.java
│   └── CategoriaEdit.java
├── detallePedido/
│   ├── DetallePedidoCreate.java
│   └── DetallePedidoDto.java
├── pedido/
│   ├── PedidoDto.java
│   └── PedidoEdit.java
├── producto/
│   ├── ProductoCreate.java
│   ├── ProductoDto.java
│   └── ProductoEdit.java
└── usuario/
    ├── UsuarioCreate.java
    ├── UsuarioDto.java
    └── UsuarioEdit.java
```
