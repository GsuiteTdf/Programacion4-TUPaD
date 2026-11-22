package com.example.mi.primer.springboot.service;

import com.example.mi.primer.springboot.domain.model.DetallePedido;
import com.example.mi.primer.springboot.domain.model.Pedido;
import com.example.mi.primer.springboot.domain.model.Producto;
import com.example.mi.primer.springboot.domain.model.Usuario;
import com.example.mi.primer.springboot.dto.detallePedido.DetallePedidoCreate;
import com.example.mi.primer.springboot.dto.detallePedido.DetallePedidoDto;
import com.example.mi.primer.springboot.dto.pedido.PedidoDto;
import com.example.mi.primer.springboot.dto.pedido.PedidoEdit;
import com.example.mi.primer.springboot.repository.PedidoRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class PedidoService {

    private final PedidoRepository pedidoRepository;
    private final UsuarioService usuarioService;
    private final ProductoService productoService;

    public PedidoService(
            PedidoRepository pedidoRepository,
            UsuarioService usuarioService,
            ProductoService productoService
    ) {
        this.pedidoRepository = pedidoRepository;
        this.usuarioService = usuarioService;
        this.productoService = productoService;
    }

    @Transactional
    public PedidoDto crear(PedidoEdit dto) {
        Usuario usuario = usuarioService.buscarEntidad(dto.getUsuarioId());

        Pedido pedido = new Pedido();
        pedido.setUsuario(usuario);
        pedido.setFecha(dto.getFecha());
        pedido.setEstado(dto.getEstado());
        pedido.setFormaPago(dto.getFormaPago());

        for (DetallePedidoCreate detalleDto : dto.getDetalles()) {
            Producto producto = productoService.buscarEntidad(detalleDto.getProductoId());
            pedido.addDetallePedido(detalleDto.getCantidad(), producto);
        }

        pedido.calcularTotal();
        pedido = pedidoRepository.save(pedido);
        return toDto(pedido);
    }

    public long cantidad() {
        return pedidoRepository.count();
    }

    private PedidoDto toDto(Pedido pedido) {
        List<DetallePedidoDto> detalles = pedido.getDetalles().stream()
                .map(this::toDetalleDto)
                .toList();

        return new PedidoDto(
                pedido.getId(),
                pedido.getFecha(),
                pedido.getEstado(),
                pedido.getTotal(),
                pedido.getFormaPago(),
                pedido.getUsuario().getId(),
                detalles
        );
    }

    private DetallePedidoDto toDetalleDto(DetallePedido detalle) {
        return new DetallePedidoDto(
                detalle.getId(),
                detalle.getProducto().getId(),
                detalle.getProducto().getNombre(),
                detalle.getCantidad(),
                detalle.getSubtotal()
        );
    }
}
