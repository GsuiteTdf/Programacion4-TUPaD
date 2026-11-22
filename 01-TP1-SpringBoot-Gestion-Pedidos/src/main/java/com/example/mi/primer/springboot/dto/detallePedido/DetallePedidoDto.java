package com.example.mi.primer.springboot.dto.detallePedido;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class DetallePedidoDto {
    private Long id;
    private Long productoId;
    private String productoNombre;
    private int cantidad;
    private Double subtotal;
}
