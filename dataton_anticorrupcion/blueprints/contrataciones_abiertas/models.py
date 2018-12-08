from dataton_anticorrupcion.extensions import db
from lib.util_sqlalchemy import ResourceMixin


class ContratacionesAbiertas(db.Model, ResourceMixin):

    # Tabla
    __tablename__ = 'contrataciones_abiertas'

    # ID
    id = db.Column(db.Integer(), primary_key=True)

    # Columnas
    ocid = db.Column(db.String())
    tag = db.Column(db.String())
    date = db.Column(db.DateTime())
    buyer_name = db.Column(db.String())
    parties = db.Column(db.JSON())
    contracts = db.Column(db.JSON())
    contracts_title = db.Column(db.String())
    contracts_amount = db.Column(db.Float())
    contracts_supplier = db.Column(db.String())

    def __repr__(self):
        return None
