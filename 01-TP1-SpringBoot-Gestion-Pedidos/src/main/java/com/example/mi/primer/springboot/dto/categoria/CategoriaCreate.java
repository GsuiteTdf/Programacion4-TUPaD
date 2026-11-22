package com.example.mi.primer.springboot.dto.categoria;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CategoriaCreate {
    private String nombre;
    private String descripcion;
}
