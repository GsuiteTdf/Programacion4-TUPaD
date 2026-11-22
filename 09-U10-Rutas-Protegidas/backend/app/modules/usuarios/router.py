from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import (
    create_access_token,
    get_current_active_user,
    require_role,
)

from .schema import AdminUserPublic, UserCreate, UserPublic
from .service import UsuarioService

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
service = UsuarioService()


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate) -> UserPublic:
    return service.registrar(data)


@router.post("/token", response_model=UserPublic)
def login(
    response: Response,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> UserPublic:
    user = service.autenticar(form.username, form.password)
    token, max_age = create_access_token(user.id)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=max_age,
        path="/",
    )
    return user


# Alias útil para la nomenclatura resumida del aula; /token es el endpoint canónico del PDF.
@router.post("/login", response_model=UserPublic, include_in_schema=False)
def login_alias(
    response: Response,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> UserPublic:
    return login(response, form)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def logout(response: Response) -> Response:
    response.delete_cookie(key="access_token", path="/", samesite="lax")
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get("/me", response_model=UserPublic)
def me(current_user=Depends(get_current_active_user)) -> UserPublic:
    return service.obtener_publico(current_user.id)


@router.get(
    "/admin/usuarios",
    response_model=list[AdminUserPublic],
    dependencies=[Depends(require_role(["admin"]))],
)
def listar_usuarios() -> list[AdminUserPublic]:
    return service.listar_admin()


@router.post(
    "/admin/usuarios/{user_id}/activar",
    response_model=AdminUserPublic,
    dependencies=[Depends(require_role(["admin"]))],
)
def activar_usuario(user_id: int) -> AdminUserPublic:
    return service.activar(user_id)


@router.post("/admin/usuarios/{user_id}/desactivar", response_model=AdminUserPublic)
def desactivar_usuario(
    user_id: int,
    current_user=Depends(require_role(["admin"])),
) -> AdminUserPublic:
    return service.desactivar(user_id, current_user.id)
