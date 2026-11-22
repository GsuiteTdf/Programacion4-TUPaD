from datetime import datetime, timezone

from sqlmodel import Session, select

from app.core.repository import Repository

from .model import Rol, Usuario, UsuarioRol


class UsuarioRepository(Repository[Usuario]):
    def __init__(self, session: Session):
        super().__init__(session, Usuario)

    def get_any(self, user_id: int) -> Usuario | None:
        return self.session.get(Usuario, user_id)

    def get_active(self, user_id: int) -> Usuario | None:
        statement = select(Usuario).where(Usuario.id == user_id, Usuario.deleted_at.is_(None))
        return self.session.exec(statement).first()

    def find_by_email(self, email: str, *, include_deleted: bool = True) -> Usuario | None:
        statement = select(Usuario).where(Usuario.email == email.strip().lower())
        if not include_deleted:
            statement = statement.where(Usuario.deleted_at.is_(None))
        return self.session.exec(statement).first()

    def list_all_ordered(self) -> list[Usuario]:
        return list(self.session.exec(select(Usuario).order_by(Usuario.id)).all())


class RolRepository(Repository[Rol]):
    def __init__(self, session: Session):
        super().__init__(session, Rol)

    def find_by_name(self, nombre: str) -> Rol | None:
        return self.session.exec(select(Rol).where(Rol.nombre == nombre)).first()

    def list_ordered(self) -> list[Rol]:
        return list(self.session.exec(select(Rol).order_by(Rol.id)).all())


class UsuarioRolRepository(Repository[UsuarioRol]):
    def __init__(self, session: Session):
        super().__init__(session, UsuarioRol)

    def role_names_for_user(self, user_id: int) -> list[str]:
        now = datetime.now(timezone.utc)
        statement = (
            select(Rol.nombre)
            .join(UsuarioRol, UsuarioRol.rol_id == Rol.id)
            .where(
                UsuarioRol.usuario_id == user_id,
                (UsuarioRol.expires_at.is_(None)) | (UsuarioRol.expires_at > now),
            )
            .order_by(Rol.nombre)
        )
        return list(self.session.exec(statement).all())

    def has_role(self, user_id: int, role_id: int) -> bool:
        return self.session.get(UsuarioRol, (user_id, role_id)) is not None
