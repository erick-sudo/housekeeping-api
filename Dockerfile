FROM python:latest

# Create a non-root user
RUN adduser --disabled-password --gecos '' keeper

# Switch to the non-root user
USER keeper

# Set environment variables
ENV PATH="/home/keeper/.local/bin:${PATH}"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
# Allows docker to cache installed dependencies between builds
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY . /app

EXPOSE 8000

RUN python manage.py migrate

CMD ["gunicorn", "--config", "gunicorn_config.py", "app.wsgi:application"]