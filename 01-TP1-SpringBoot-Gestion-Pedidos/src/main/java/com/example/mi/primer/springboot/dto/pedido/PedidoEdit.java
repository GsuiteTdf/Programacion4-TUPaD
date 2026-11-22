package com.example.mi.primer.springboot.dto.pedido;

import com.example.mi.primer.springboot.domain.enums.Estado;
import com.example.mi.primer.springboot.domain.enums.FormaPago;
import com.example.mi.primer.springboot.dto.detallePedido.DetallePedidoCreate;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PedidoEdit {
    private Long usuarioId;
    private LocalDate fecha;
    private Estado estado;
    private FormaPago formaPago;
    private List<DetallePedidoCreate> detalles = new ArrayList<>();
}
