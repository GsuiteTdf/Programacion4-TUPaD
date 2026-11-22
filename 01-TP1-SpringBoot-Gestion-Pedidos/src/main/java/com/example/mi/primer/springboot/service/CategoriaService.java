package com.example.mi.primer.springboot.service;

import com.example.mi.primer.springboot.domain.model.Categoria;
import com.example.mi.primer.springboot.dto.categoria.CategoriaCreate;
import com.example.mi.primer.springboot.dto.categoria.CategoriaDto;
import com.example.mi.primer.springboot.repository.CategoriaRepository;
import org.springframework.stereotype.Service;

@Service
public class CategoriaService {

    private final CategoriaRepository categoriaRepository;

    public CategoriaService(CategoriaRepository categoriaRepository) {
        this.categoriaRepository = categoriaRepository;
    }

    public CategoriaDto crear(CategoriaCreate dto) {
        Categoria categoria = new Categoria();
        categoria.setNombre(dto.getNombre());
        categoria.setDescripcion(dto.getDescripcion());
        categoria = categoriaRepository.save(categoria);
        return toDto(categoria);
    }

    public Categoria buscarEntidad(Long id) {
        return categoriaRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Categoria no encontrada: " + id));
    }

    public long cantidad() {
        return categoriaRepository.count();
    }

    private CategoriaDto toDto(Categoria categoria) {
        return new CategoriaDto(categoria.getId(), categoria.getNombre(), categoria.getDescripcion());
    }
}
