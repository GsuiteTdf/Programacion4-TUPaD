package com.example.mi.primer.springboot.dto.usuario;

import com.example.mi.primer.springboot.domain.enums.Rol;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class UsuarioDto {
    private Long id;
    private String nombre;
    private String apellido;
    private String email;
    private String celular;
    private Rol rol;
}
