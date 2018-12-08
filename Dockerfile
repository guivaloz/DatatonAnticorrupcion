FROM python:2.7-slim
MAINTAINER Guillermo Valdes Lozano <guillermo.valdes@seacoahuila.org.mx>

# Instalar librerías para soportar PostgreSQL
RUN apt-get update && \
  apt-get install build-essential libpq-dev -qq -y --no-install-recommends

# Crear directorio
RUN mkdir /app
WORKDIR /app

# Instalar requerimientos
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copiar
COPY . .

# Instalar comandos Click
RUN pip install --editable .

# Arrancar el servidor
CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "dataton_anticorrupcion.app:create_app()"
