from sqlalchemy.sql import func
from dataton_anticorrupcion.extensions import db


class ResourceMixin(object):

    creado = db.Column(db.DateTime, server_default=func.now())
    modificado = db.Column(db.DateTime, onupdate=func.now(), server_default=func.now())
    estatus = db.Column(db.String(1), nullable=False, server_default='A')

    def delete(self):
        if self.estatus == 'A':
            self.estatus = 'B'
            return self.save()
        return None

    def recover(self):
        if self.estatus == 'B':
            self.estatus = 'A'
            return self.save()
        return None

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __str__(self):
        obj_id = hex(id(self))
        columns = self.__table__.c.keys()
        values = ', '.join("%s=%r" % (n, getattr(self, n)) for n in columns)
        return '<%s %s(%s)>' % (obj_id, self.__class__.__name__, values)
