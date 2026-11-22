package com.example.mi.primer.springboot.config;

import com.example.mi.primer.springboot.domain.enums.Estado;
import com.example.mi.primer.springboot.domain.enums.FormaPago;
import com.example.mi.primer.springboot.domain.enums.Rol;
import com.example.mi.primer.springboot.dto.categoria.CategoriaCreate;
import com.example.mi.primer.springboot.dto.categoria.CategoriaDto;
import com.example.mi.primer.springboot.dto.detallePedido.DetallePedidoCreate;
import com.example.mi.primer.springboot.dto.pedido.PedidoDto;
import com.example.mi.primer.springboot.dto.pedido.PedidoEdit;
import com.example.mi.primer.springboot.dto.producto.ProductoCreate;
import com.example.mi.primer.springboot.dto.producto.ProductoDto;
import com.example.mi.primer.springboot.dto.usuario.UsuarioCreate;
import com.example.mi.primer.springboot.dto.usuario.UsuarioDto;
import com.example.mi.primer.springboot.service.CategoriaService;
import com.example.mi.primer.springboot.service.PedidoService;
import com.example.mi.primer.springboot.service.ProductoService;
import com.example.mi.primer.springboot.service.UsuarioService;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.util.List;

@Component
public class DataLoader implements CommandLineRunner {

    private final CategoriaService categoriaService;
    private final ProductoService productoService;
    private final UsuarioService usuarioService;
    private final PedidoService pedidoService;

    // Inyeccion de dependencias por constructor, tal como exige el TP.
    public DataLoader(
            CategoriaService categoriaService,
            ProductoService productoService,
            UsuarioService usuarioService,
            PedidoService pedidoService
    ) {
        this.categoriaService = categoriaService;
        this.productoService = productoService;
        this.usuarioService = usuarioService;
        this.pedidoService = pedidoService;
    }

    @Override
    public void run(String... args) {
        if (usuarioService.cantidad() > 0) {
            return;
        }

        // 3 categorias creadas a partir de DTOs.
        CategoriaDto tecnologia = categoriaService.crear(
                new CategoriaCreate("Tecnologia", "Productos tecnologicos y accesorios")
        );
        CategoriaDto hogar = categoriaService.crear(
                new CategoriaCreate("Hogar", "Articulos para el hogar")
        );
        CategoriaDto libreria = categoriaService.crear(
                new CategoriaCreate("Libreria", "Articulos de estudio y oficina")
        );

        // 10 productos creados a partir de DTOs.
        ProductoDto mouse = productoService.crear(new ProductoCreate(
                "Mouse inalambrico", 18500.0, "Mouse optico USB", 25, "mouse.jpg", true, tecnologia.getId()));
        ProductoDto teclado = productoService.crear(new ProductoCreate(
                "Teclado mecanico", 62000.0, "Teclado mecanico retroiluminado", 12, "teclado.jpg", true, tecnologia.getId()));
        ProductoDto auriculares = productoService.crear(new ProductoCreate(
                "Auriculares", 45000.0, "Auriculares con microfono", 18, "auriculares.jpg", true, tecnologia.getId()));
        ProductoDto webcam = productoService.crear(new ProductoCreate(
                "Webcam Full HD", 52000.0, "Camara web 1080p", 10, "webcam.jpg", true, tecnologia.getId()));
        ProductoDto lampara = productoService.crear(new ProductoCreate(
                "Lampara LED", 21500.0, "Lampara de escritorio LED", 20, "lampara.jpg", true, hogar.getId()));
        ProductoDto taza = productoService.crear(new ProductoCreate(
                "Taza termica", 14900.0, "Taza termica de acero", 30, "taza.jpg", true, hogar.getId()));
        ProductoDto organizador = productoService.crear(new ProductoCreate(
                "Organizador", 12900.0, "Organizador multiproposito", 15, "organizador.jpg", true, hogar.getId()));
        ProductoDto cuaderno = productoService.crear(new ProductoCreate(
                "Cuaderno universitario", 7800.0, "Cuaderno A4 de 100 hojas", 40, "cuaderno.jpg", true, libreria.getId()));
        ProductoDto lapiceras = productoService.crear(new ProductoCreate(
                "Set de lapiceras", 6500.0, "Set de 5 lapiceras", 50, "lapiceras.jpg", true, libreria.getId()));
        ProductoDto resaltadores = productoService.crear(new ProductoCreate(
                "Resaltadores", 5900.0, "Set de 4 resaltadores", 35, "resaltadores.jpg", true, libreria.getId()));

        // 2 usuarios creados a partir de DTOs.
        UsuarioDto usuario1 = usuarioService.crear(new UsuarioCreate(
                "Gaston", "Cejas", "gaston@example.com", "3510000001", "clave123", Rol.ADMIN));
        UsuarioDto usuario2 = usuarioService.crear(new UsuarioCreate(
                "Paula", "Gomez", "paula@example.com", "3510000002", "clave456", Rol.USUARIO));

        // 3 pedidos, cada uno con al menos 2 detalles, creados a partir de DTOs.
        PedidoDto pedido1 = pedidoService.crear(new PedidoEdit(
                usuario1.getId(),
                LocalDate.now(),
                Estado.CONFIRMADO,
                FormaPago.TARJETA,
                List.of(
                        new DetallePedidoCreate(mouse.getId(), 2),
                        new DetallePedidoCreate(teclado.getId(), 1)
                )
        ));

        PedidoDto pedido2 = pedidoService.crear(new PedidoEdit(
                usuario2.getId(),
                LocalDate.now().minusDays(1),
                Estado.PENDIENTE,
                FormaPago.TRANSFERENCIA,
                List.of(
                        new DetallePedidoCreate(cuaderno.getId(), 3),
                        new DetallePedidoCreate(lapiceras.getId(), 2)
                )
        ));

        PedidoDto pedido3 = pedidoService.crear(new PedidoEdit(
                usuario1.getId(),
                LocalDate.now().minusDays(2),
                Estado.TERMINADO,
                FormaPago.EFECTIVO,
                List.of(
                        new DetallePedidoCreate(lampara.getId(), 1),
                        new DetallePedidoCreate(taza.getId(), 2)
                )
        ));

        System.out.println("\n================ TP1 PROGRAMACION IV ================");
        System.out.println("Datos cargados correctamente desde DTOs:");
        System.out.println("Usuarios:   " + usuarioService.cantidad() + " (requeridos: 2)");
        System.out.println("Categorias: " + categoriaService.cantidad() + " (requeridas: 3)");
        System.out.println("Productos:  " + productoService.cantidad() + " (requeridos: 10)");
        System.out.println("Pedidos:    " + pedidoService.cantidad() + " (requeridos: 3)");
        System.out.printf("Pedido 1 - Total: $%.2f - Detalles: %d%n", pedido1.getTotal(), pedido1.getDetalles().size());
        System.out.printf("Pedido 2 - Total: $%.2f - Detalles: %d%n", pedido2.getTotal(), pedido2.getDetalles().size());
        System.out.printf("Pedido 3 - Total: $%.2f - Detalles: %d%n", pedido3.getTotal(), pedido3.getDetalles().size());
        System.out.println("H2 Console: http://localhost:8080/h2-console");
        System.out.println("JDBC URL: jdbc:h2:mem:pedidosdb | usuario: sa | password: vacio");
        System.out.println("======================================================\n");
    }
}
