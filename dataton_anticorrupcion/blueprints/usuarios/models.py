from collections import OrderedDict
from flask import current_app
from flask_login import UserMixin

from dataton_anticorrupcion.extensions import db, pwd_context
from lib.util_sqlalchemy import ResourceMixin


class Usuarios(UserMixin, ResourceMixin, db.Model):

    # Roles
    ROLES = OrderedDict([
        ('usuario', 'Usuario'),
        ('admin', 'Administrador')
    ])

    # Tabla
    __tablename__ = 'usuarios'

    # ID
    id = db.Column(db.Integer(), primary_key=True)

    # Columnas
    nombre     = db.Column(db.String(256), unique=True, nullable=False, index=True)
    email      = db.Column(db.String(256), unique=True, nullable=False, index=True)
    contrasena = db.Column(db.String(256), nullable=False)
    activo     = db.Column(db.Boolean(), nullable=False, server_default='1')
    notas      = db.Column(db.String(8192))
    rol        = db.Column(db.Enum(*ROLES, name='roles_tipos', native_enum=False),
                           index=True,
                           nullable=False,
                           server_default='usuario')

    def __repr__(self):
        return self.nombre

    @classmethod
    def find_by_identity(cls, identity):
        """
        Find a user by their e-mail or username.
        """
        return Usuarios.query.filter(
          (Usuarios.email == identity) | (Usuarios.nombre == identity)).first()

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.activo

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def authenticated(self, with_password=True, password=''):
        """
        Ensure a user is authenticated, and optionally check their password.
        """
        if self.id and with_password:
            return pwd_context.verify(password, self.contrasena)
        return False
