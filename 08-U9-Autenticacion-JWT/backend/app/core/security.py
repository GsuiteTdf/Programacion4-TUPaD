from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
import jwt
from jwt.exceptions import PyJWTError
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.core.config import settings
from app.core.database import get_session


class OAuth2PasswordBearerCookie(OAuth2PasswordBearer):
    """OAuth2 documentado en Swagger, con JWT transportado por cookie HttpOnly."""

    async def __call__(self, request: Request) -> str | None:
        token = request.cookies.get("access_token")
        if token:
            return token
        if self.auto_error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No autenticado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return None


oauth2_cookie = OAuth2PasswordBearerCookie(tokenUrl="/api/v1/auth/token")
SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(oauth2_cookie)]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        return False


def create_access_token(user_id: int) -> tuple[str, int]:
    expire_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expires_at = datetime.now(timezone.utc) + expire_delta
    payload = {"sub": str(user_id), "exp": expires_at}
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token, int(expire_delta.total_seconds())


def _decode_user_id(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        subject = payload.get("sub")
        if subject is None:
            raise ValueError("JWT sin subject")
        return int(subject)
    except (PyJWTError, ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no válidas",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


def get_current_user(token: TokenDep, session: SessionDep):
    from app.modules.usuarios.repository import UsuarioRepository

    user_id = _decode_user_id(token)
    usuario = UsuarioRepository(session).get_any(user_id)
    if usuario is None:
        raise HTTPException(status_code=401, detail="Credenciales no válidas")
    return usuario


def get_current_active_user(
    current_user=Depends(get_current_user),
):
    if current_user.deleted_at is not None:
        raise HTTPException(status_code=400, detail="Cuenta de usuario desactivada")
    return current_user


def require_role(roles: list[str]) -> Callable:
    required = set(roles)

    def dependency(
        session: SessionDep,
        current_user=Depends(get_current_active_user),
    ):
        from app.modules.usuarios.repository import UsuarioRolRepository

        vigentes = set(UsuarioRolRepository(session).role_names_for_user(current_user.id))
        if not required.intersection(vigentes):
            raise HTTPException(status_code=403, detail="No tiene permisos para esta operación")
        return current_user

    return dependency
