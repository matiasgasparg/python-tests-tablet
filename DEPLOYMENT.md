# Guía de Despliegue 🚀

Esta guía te ayudará a desplegar la aplicación Birthday Invitations en diferentes entornos.

## Opción 1: Desarrollo Local

### Requisitos
- Python 3.8+
- pip
- Git

### Instalación

```bash
# Clonar repositorio
git clone <repo-url>
cd python-tests-tablet

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env y cambiar SECRET_KEY y JWT_SECRET_KEY

# Ejecutar
python run.py
```

Acceder a: `http://localhost:5000`

## Opción 2: Docker (Recomendado para Producción)

### Requisitos
- Docker
- Docker Compose

### Instalación

```bash
# 1. Clonar repositorio
git clone <repo-url>
cd python-tests-tablet

# 2. Configurar variables de entorno
cp .env.example .env

# 3. Editar .env
nano .env  # Cambiar SECRET_KEY y JWT_SECRET_KEY

# 4. Construir y ejecutar
docker-compose up -d

# 5. Crear migraciones (primera ejecución)
docker-compose exec web python -c "from app import create_app, db; app=create_app(); db.create_all()"
```

Acceder a:
- API: `http://localhost:5000`
- Health check: `http://localhost/health`

### Detener la aplicación
```bash
docker-compose down
```

### Ver logs
```bash
docker-compose logs -f web
```

## Opción 3: Heroku

### Requisitos
- Cuenta en Heroku
- Heroku CLI instalado

### Pasos

```bash
# 1. Login en Heroku
heroku login

# 2. Crear aplicación
heroku create nombre-de-tu-app

# 3. Agregar PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# 4. Configurar variables de entorno
heroku config:set SECRET_KEY=your-super-secret-key
heroku config:set JWT_SECRET_KEY=your-jwt-secret-key
heroku config:set FLASK_ENV=production

# 5. Desplegar
git push heroku main

# 6. Ver logs
heroku logs --tail
```

### Archivo Procfile (ya incluido)
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT run:app
```

## Opción 4: AWS (EC2)

### Paso 1: Instancia EC2

```bash
# Crear instancia con Ubuntu 20.04 LTS

# Conectar por SSH
ssh -i tu-key.pem ubuntu@tu-instancia-ip

# Actualizar sistema
sudo apt-get update && sudo apt-get upgrade -y

# Instalar dependencias
sudo apt-get install -y python3-pip python3-venv nginx postgresql postgresql-contrib
```

### Paso 2: Configurar Aplicación

```bash
# Clonar repo
cd /var/www
sudo git clone <repo-url> birthday-invitations
sudo chown -R ubuntu:ubuntu birthday-invitations
cd birthday-invitations

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Configurar .env
cp .env.example .env
nano .env  # Editar con datos reales
```

### Paso 3: Configurar Gunicorn

```bash
# Crear servicio systemd
sudo nano /etc/systemd/system/birthday-invitations.service
```

Contenido:
```ini
[Unit]
Description=Birthday Invitations App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/var/www/birthday-invitations
ExecStart=/var/www/birthday-invitations/venv/bin/gunicorn \
    -w 4 \
    -b 127.0.0.1:5000 \
    run:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Habilitar:
```bash
sudo systemctl daemon-reload
sudo systemctl enable birthday-invitations
sudo systemctl start birthday-invitations
```

### Paso 4: Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/default
```

Contenido:
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Habilitar:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

### Paso 5: Certificado SSL (Recomendado)

```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

## Opción 5: DigitalOcean App Platform

### Pasos

1. Conectar repositorio GitHub a DigitalOcean
2. Crear nuevo App
3. Configurar:
   - Build: `pip install -r requirements.txt`
   - Run: `gunicorn -w 4 -b 0.0.0.0:$PORT run:app`
4. Agregar variables de entorno en Settings
5. Desplegar

## Opciones 6: Railway.app (La más fácil)

1. Ir a railway.app y conectar GitHub
2. Crear proyecto nuevo
3. Seleccionar repositorio
4. Railway detecta Flask automáticamente
5. Agregar PostgreSQL plugin
6. Configurar variables de entorno
7. ¡Listo! Obtiene URL automáticamente

## Monitoreo y Mantenimiento

### Ver estado de la aplicación

```bash
# Con Docker
docker-compose ps

# Con systemd
sudo systemctl status birthday-invitations

# Con Heroku
heroku ps
```

### Backup de datos

```bash
# PostgreSQL
pg_dump birthday_db > backup.sql

# Restaurar
psql birthday_db < backup.sql
```

### Actualizar código

```bash
# Desarrollo
git pull
# Reiniciar si es necesario

# Docker
git pull
docker-compose down
docker-compose up -d

# Heroku
git push heroku main

# AWS/EC2
cd /var/www/birthday-invitations
git pull
sudo systemctl restart birthday-invitations
```

## Troubleshooting

### La aplicación no inicia

```bash
# Ver logs
python run.py  # Desarrollo
docker-compose logs web  # Docker
journalctl -u birthday-invitations -n 50  # systemd
```

### Error de base de datos

```bash
# Resetear BD (solo desarrollo)
rm birthday_invitations.db
python run.py

# Producción: migrar BD
alembic upgrade head
```

### Puertos bloqueados

```bash
# Ver qué usa el puerto 5000
lsof -i :5000

# Matar proceso
kill -9 <PID>
```

## Checklist Pre-Producción

- [ ] Cambiar `SECRET_KEY` en .env
- [ ] Cambiar `JWT_SECRET_KEY` en .env
- [ ] Usar PostgreSQL en lugar de SQLite
- [ ] Configurar HTTPS/SSL
- [ ] Configurar CORS para tu dominio
- [ ] Habilitar backups automáticos
- [ ] Configurar monitoreo y alertas
- [ ] Configurar logs centralizados
- [ ] Pruebas de carga completadas
- [ ] Plan de desastre documentado

¡Listo para producción! 🎉
