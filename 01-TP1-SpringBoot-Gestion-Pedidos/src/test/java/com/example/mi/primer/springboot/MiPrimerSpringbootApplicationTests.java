package com.example.mi.primer.springboot;

import com.example.mi.primer.springboot.repository.CategoriaRepository;
import com.example.mi.primer.springboot.repository.DetallePedidoRepository;
import com.example.mi.primer.springboot.repository.PedidoRepository;
import com.example.mi.primer.springboot.repository.ProductoRepository;
import com.example.mi.primer.springboot.repository.UsuarioRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
class MiPrimerSpringbootApplicationTests {

    @Autowired
    private UsuarioRepository usuarioRepository;

    @Autowired
    private PedidoRepository pedidoRepository;

    @Autowired
    private CategoriaRepository categoriaRepository;

    @Autowired
    private ProductoRepository productoRepository;

    @Autowired
    private DetallePedidoRepository detallePedidoRepository;

    @Test
    void contextLoadsAndDataLoaderCreatesRequiredData() {
        assertThat(usuarioRepository.count()).isEqualTo(2);
        assertThat(pedidoRepository.count()).isEqualTo(3);
        assertThat(categoriaRepository.count()).isEqualTo(3);
        assertThat(productoRepository.count()).isEqualTo(10);
        assertThat(detallePedidoRepository.count()).isGreaterThanOrEqualTo(6);
    }
}
