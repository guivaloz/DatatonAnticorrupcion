#
# Produccion
#
DEBUG = True
SECRET_KEY = 'CambieClaveUnTextoGrande'

# SQLAlchemy para PostgreSQL en un contenedor Docker
#   postgresql://USER:PASSWORD@postgres:5432/DATABASE
SQLALCHEMY_DATABASE_URI = 'postgresql://datatonadmin:LaContrasenaDeLaBD@postgres:5432/dataton'

# Para todos
SQLALCHEMY_TRACK_MODIFICATIONS = False
