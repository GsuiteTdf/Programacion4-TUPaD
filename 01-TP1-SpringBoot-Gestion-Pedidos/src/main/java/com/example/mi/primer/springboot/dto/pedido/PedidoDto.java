package com.example.mi.primer.springboot.dto.pedido;

import com.example.mi.primer.springboot.domain.enums.Estado;
import com.example.mi.primer.springboot.domain.enums.FormaPago;
import com.example.mi.primer.springboot.dto.detallePedido.DetallePedidoDto;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PedidoDto {
    private Long id;
    private LocalDate fecha;
    private Estado estado;
    private Double total;
    private FormaPago formaPago;
    private Long usuarioId;
    private List<DetallePedidoDto> detalles = new ArrayList<>();
}
