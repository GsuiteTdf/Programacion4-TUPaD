package com.example.mi.primer.springboot.service;

import com.example.mi.primer.springboot.domain.model.Usuario;
import com.example.mi.primer.springboot.dto.usuario.UsuarioCreate;
import com.example.mi.primer.springboot.dto.usuario.UsuarioDto;
import com.example.mi.primer.springboot.repository.UsuarioRepository;
import org.springframework.stereotype.Service;

@Service
public class UsuarioService {

    private final UsuarioRepository usuarioRepository;

    public UsuarioService(UsuarioRepository usuarioRepository) {
        this.usuarioRepository = usuarioRepository;
    }

    public UsuarioDto crear(UsuarioCreate dto) {
        Usuario usuario = new Usuario();
        usuario.setNombre(dto.getNombre());
        usuario.setApellido(dto.getApellido());
        usuario.setEmail(dto.getEmail());
        usuario.setCelular(dto.getCelular());
        usuario.setContrasena(dto.getContrasena());
        usuario.setRol(dto.getRol());
        usuario = usuarioRepository.save(usuario);
        return toDto(usuario);
    }

    public Usuario buscarEntidad(Long id) {
        return usuarioRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Usuario no encontrado: " + id));
    }

    public long cantidad() {
        return usuarioRepository.count();
    }

    private UsuarioDto toDto(Usuario usuario) {
        return new UsuarioDto(
                usuario.getId(),
                usuario.getNombre(),
                usuario.getApellido(),
                usuario.getEmail(),
                usuario.getCelular(),
                usuario.getRol()
        );
    }
}
