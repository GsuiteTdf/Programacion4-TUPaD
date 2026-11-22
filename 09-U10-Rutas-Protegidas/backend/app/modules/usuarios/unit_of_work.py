from app.core.unit_of_work import UnitOfWork

from .repository import RolRepository, UsuarioRepository, UsuarioRolRepository


class UsuarioUnitOfWork(UnitOfWork):
    def __enter__(self):
        super().__enter__()
        self.usuarios = UsuarioRepository(self.session)
        self.roles = RolRepository(self.session)
        self.usuario_roles = UsuarioRolRepository(self.session)
        return self
