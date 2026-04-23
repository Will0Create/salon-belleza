# Usamos una imagen ligera de Python
FROM python:3.11-slim

# Evita que Python genere archivos .pyc y permite ver logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Carpeta de trabajo dentro del servidor
WORKDIR /app

# Instalamos dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copiamos el resto del código
COPY . /app/

# Exponemos el puerto 8000 (típico de Django)
EXPOSE 8000

# Comando para arrancar la app con Gunicorn
# Reemplaza 'tu_proyecto' por el nombre de la carpeta donde está tu settings.py
CMD python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT