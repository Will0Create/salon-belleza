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

CMD python manage.py migrate && \
    python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin1234')" && \
    gunicorn core.wsgi:application --bind 0.0.0.0:$PORT