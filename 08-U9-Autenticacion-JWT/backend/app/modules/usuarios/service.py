from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.core.security import hash_password, verify_password

from .model import Usuario, UsuarioRol
from .schema import AdminUserPublic, UserCreate, UserPublic
from .unit_of_work import UsuarioUnitOfWork


def _public(uow: UsuarioUnitOfWork, usuario: Usuario) -> UserPublic:
    return UserPublic(
        id=usuario.id,
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        email=usuario.email,
        celular=usuario.celular,
        roles=uow.usuario_roles.role_names_for_user(usuario.id),
    )


class UsuarioService:
    def registrar(self, data: UserCreate) -> UserPublic:
        with UsuarioUnitOfWork() as uow:
            email = str(data.email).strip().lower()
            if uow.usuarios.find_by_email(email) is not None:
                raise HTTPException(status_code=409, detail="Ya existe un usuario con ese email")
            rol_user = uow.roles.find_by_name("user")
            if rol_user is None:
                raise HTTPException(status_code=500, detail="El rol user no está cargado. Ejecute seed.py")
            usuario = uow.usuarios.create(
                Usuario(
                    nombre=data.nombre,
                    apellido=data.apellido,
                    email=email,
                    celular=data.celular,
                    password_hash=hash_password(data.password),
                )
            )
            uow.usuario_roles.create(
                UsuarioRol(usuario_id=usuario.id, rol_id=rol_user.id, asignado_por_id=None)
            )
            return _public(uow, usuario)

    def autenticar(self, email: str, password: str) -> UserPublic:
        with UsuarioUnitOfWork() as uow:
            usuario = uow.usuarios.find_by_email(email.strip().lower())
            if usuario is None or not verify_password(password, usuario.password_hash):
                raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
            if usuario.deleted_at is not None:
                raise HTTPException(status_code=400, detail="Cuenta de usuario desactivada")
            return _public(uow, usuario)

    def obtener_publico(self, user_id: int) -> UserPublic:
        with UsuarioUnitOfWork() as uow:
            usuario = uow.usuarios.get_active(user_id)
            if usuario is None:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return _public(uow, usuario)

    def listar_admin(self) -> list[AdminUserPublic]:
        with UsuarioUnitOfWork() as uow:
            return [
                AdminUserPublic(**_public(uow, usuario).model_dump(), activo=usuario.deleted_at is None)
                for usuario in uow.usuarios.list_all_ordered()
            ]

    def desactivar(self, user_id: int, admin_id: int) -> AdminUserPublic:
        if user_id == admin_id:
            # Evita que el administrador pierda el acceso al sistema.
            raise HTTPException(status_code=400, detail="No puede desactivar su propia cuenta")
        with UsuarioUnitOfWork() as uow:
            usuario = uow.usuarios.get_any(user_id)
            if usuario is None:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            usuario.deleted_at = datetime.now(timezone.utc)
            usuario.updated_at = datetime.now(timezone.utc)
            uow.session.add(usuario)
            uow.session.flush()
            return AdminUserPublic(**_public(uow, usuario).model_dump(), activo=False)

    def activar(self, user_id: int) -> AdminUserPublic:
        with UsuarioUnitOfWork() as uow:
            usuario = uow.usuarios.get_any(user_id)
            if usuario is None:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            usuario.deleted_at = None
            usuario.updated_at = datetime.now(timezone.utc)
            uow.session.add(usuario)
            uow.session.flush()
            return AdminUserPublic(**_public(uow, usuario).model_dump(), activo=True)
