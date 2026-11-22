package com.example.mi.primer.springboot.service;

import com.example.mi.primer.springboot.domain.model.Categoria;
import com.example.mi.primer.springboot.domain.model.Producto;
import com.example.mi.primer.springboot.dto.producto.ProductoCreate;
import com.example.mi.primer.springboot.dto.producto.ProductoDto;
import com.example.mi.primer.springboot.repository.ProductoRepository;
import org.springframework.stereotype.Service;

@Service
public class ProductoService {

    private final ProductoRepository productoRepository;
    private final CategoriaService categoriaService;

    public ProductoService(ProductoRepository productoRepository, CategoriaService categoriaService) {
        this.productoRepository = productoRepository;
        this.categoriaService = categoriaService;
    }

    public ProductoDto crear(ProductoCreate dto) {
        Categoria categoria = categoriaService.buscarEntidad(dto.getCategoriaId());

        Producto producto = new Producto();
        producto.setNombre(dto.getNombre());
        producto.setPrecio(dto.getPrecio());
        producto.setDescripcion(dto.getDescripcion());
        producto.setStock(dto.getStock());
        producto.setImagen(dto.getImagen());
        producto.setDisponible(dto.getDisponible());
        producto.setCategoria(categoria);

        producto = productoRepository.save(producto);
        return toDto(producto);
    }

    public Producto buscarEntidad(Long id) {
        return productoRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Producto no encontrado: " + id));
    }

    public long cantidad() {
        return productoRepository.count();
    }

    private ProductoDto toDto(Producto producto) {
        return new ProductoDto(
                producto.getId(),
                producto.getNombre(),
                producto.getPrecio(),
                producto.getDescripcion(),
                producto.getStock(),
                producto.getImagen(),
                producto.getDisponible(),
                producto.getCategoria().getId(),
                producto.getCategoria().getNombre()
        );
    }
}
