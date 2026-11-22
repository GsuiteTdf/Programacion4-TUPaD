import os

from dotenv import load_dotenv
from sqlmodel import Session, select

from app.core.database import create_db_and_tables, engine
from app.core.security import hash_password
from app.modules.catalogos.model import EstadoPedido, FormaPago
from app.modules.usuarios.model import Rol, Usuario, UsuarioRol

load_dotenv()

ROLES = [
    Rol(nombre="admin", descripcion="Administración completa del Food Store"),
    Rol(nombre="user", descripcion="Usuario autenticado con acceso de lectura"),
]

ESTADOS = [
    EstadoPedido(codigo="PENDIENTE", descripcion="Pendiente", orden=1, es_terminal=False),
    EstadoPedido(codigo="CONFIRMADO", descripcion="Confirmado", orden=2, es_terminal=False),
    EstadoPedido(codigo="EN_PREP", descripcion="En preparación", orden=3, es_terminal=False),
    EstadoPedido(codigo="EN_CAMINO", descripcion="En camino", orden=4, es_terminal=False),
    EstadoPedido(codigo="ENTREGADO", descripcion="Entregado", orden=5, es_terminal=True),
    EstadoPedido(codigo="CANCELADO", descripcion="Cancelado", orden=6, es_terminal=True),
]

FORMAS_PAGO = [
    FormaPago(codigo="EFECTIVO", descripcion="Efectivo", activo=True),
    FormaPago(codigo="TARJETA", descripcion="Tarjeta", activo=True),
    FormaPago(codigo="TRANSFERENCIA", descripcion="Transferencia", activo=True),
]


def seed() -> None:
    create_db_and_tables()
    with Session(engine) as session:
        for rol in ROLES:
            if session.exec(select(Rol).where(Rol.nombre == rol.nombre)).first() is None:
                session.add(rol)
        for estado in ESTADOS:
            if session.get(EstadoPedido, estado.codigo) is None:
                session.add(estado)
        for forma in FORMAS_PAGO:
            if session.get(FormaPago, forma.codigo) is None:
                session.add(forma)
        session.commit()

        admin_email = os.getenv("SEED_ADMIN_EMAIL")
        admin_password = os.getenv("SEED_ADMIN_PASSWORD")
        if admin_email and admin_password:
            existing = session.exec(select(Usuario).where(Usuario.email == admin_email.lower())).first()
            if existing is None:
                admin = Usuario(
                    nombre=os.getenv("SEED_ADMIN_NOMBRE", "Admin"),
                    apellido=os.getenv("SEED_ADMIN_APELLIDO", "Food Store"),
                    email=admin_email.lower(),
                    password_hash=hash_password(admin_password),
                )
                session.add(admin)
                session.flush()
                rol_admin = session.exec(select(Rol).where(Rol.nombre == "admin")).one()
                session.add(UsuarioRol(usuario_id=admin.id, rol_id=rol_admin.id, asignado_por_id=None))
                session.commit()


if __name__ == "__main__":
    seed()
    print("Seed completado: roles, estados, formas de pago y admin opcional.")
