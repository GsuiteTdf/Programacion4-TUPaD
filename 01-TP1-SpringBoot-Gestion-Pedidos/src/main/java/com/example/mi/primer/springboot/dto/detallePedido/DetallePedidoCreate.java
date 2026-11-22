package com.example.mi.primer.springboot.dto.detallePedido;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class DetallePedidoCreate {
    private Long productoId;
    private int cantidad;
}
