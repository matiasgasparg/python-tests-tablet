# Birthday Invitations App 🎂

Una aplicación Flask para crear y gestionar invitaciones de cumpleaños. Diseñada para ser vendida como SaaS con panel de administración.

## 🎯 Características

- ✅ **Autenticación segura** con JWT
- ✅ **Gestión de invitaciones** - CRUD completo
- ✅ **Sistema de RSVP** - Confirmación de invitados
- ✅ **URLs únicas** - Código único para cada invitación
- ✅ **Landing pública** para compartir por WhatsApp (link por invitación)
- ✅ **Templates + media** (campos para template_key + imágenes + video)
- ✅ **Registro de asistencia** (lista de RSVPs para el dueño via endpoint autenticado)
- ✅ **API RESTful** - Integración con cualquier frontend
- ✅ **Multi-usuario** - Cada cliente con sus datos aislados
- ✅ **Dashboard Admin** - Estadísticas en tiempo real

## 🚀 Quick Start

### 1. Instalación

```bash
# Clonar y navegar al proyecto
git clone <repo>
cd python-tests-tablet

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
```

### 2. Ejecutar la aplicación

```bash
python run.py
```

La API estará disponible en `http://localhost:5000`

### Endpoints clave (MVP WhatsApp)
- Public landing: `GET /api/public/invitations/<code>`
- RSVP: `POST /api/public/invitations/<code>/rsvp`
- Registro (dueño, con JWT): `GET /api/invitations/<id>/guests`

> Nota dev: si agregás columnas nuevas al modelo (templates/media), y usás SQLite con `db.create_all()`, puede que tengas que borrar `birthday_invitations.db` para recrear la DB.

## 📚 Documentación API

Ver [API_DOCUMENTATION.md](API_DOCUMENTATION.md) para documentación completa de endpoints.

Swagger UI disponible en `http://localhost:5000/docs/` (requiere app en ejecución).

### Ejemplo rápido

```bash
# 1. Registrarse
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "password123",
    "company_name": "Mi Empresa"
  }'

# 2. Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "password123"
  }'

# 3. Crear invitacion
curl -X POST http://localhost:5000/api/invitations \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "birthday_name": "Maria Garcia",
    "birthday_date": "2005-03-15T00:00:00",
    "event_title": "Cumpleanos de Maria",
    "event_date": "2024-03-16T19:00:00"
  }'
```

## 📁 Estructura del proyecto

```
.
├── app/
│   ├── models/              # Modelos de BD
│   │   ├── user.py         # Usuarios/Admins
│   │   ├── invitation.py   # Invitaciones
│   │   └── guest.py        # Invitados
│   ├── routes/              # APIs
│   │   ├── auth.py         # Autenticación
│   │   ├── invitations.py  # CRUD invitaciones
│   │   ├── admin.py        # Estadísticas admin
│   │   └── public.py       # Endpoints públicos
│   ├── static/              # CSS, JS, imágenes
│   └── __init__.py
├── config.py               # Configuración
├── run.py                  # Punto de entrada
├── requirements.txt        # Dependencias
└── API_DOCUMENTATION.md    # Docs
```

## 🔄 Flujo de uso

### Vendedor (Tú)
1. **Crear cuenta** - Registrarse en la plataforma
2. **Crear invitaciones** - Cargar datos de la fiesta
3. **Publicar y compartir** - Generar URL para compartir

### Cliente (Tu cliente)
1. **Recibir credenciales** - Email y contraseña
2. **Crear invitación** - Llenar datos de la fiesta
3. **Ver confirmaciones** - Consultar invitados confirmados
4. **Compartir** - Enviar por WhatsApp, email, redes sociales

### Invitados
1. **Recibir link** - URL única con código
2. **Ver invitación** - Información formateada
3. **Responder RSVP** - Confirmar asistencia

## 🔐 Seguridad

- Contraseñas encriptadas con bcrypt
- JWT para autenticación
- CORS habilitado
- Variables de entorno para datos sensibles
- Validación de entrada en todos los endpoints

## 💾 Base de datos

SQLite por defecto (desarrollo)
PostgreSQL recomendado (producción)

Cambiar en `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## 🛠️ Tecnologías

- **Flask** - Framework web
- **SQLAlchemy** - ORM
- **JWT** - Autenticación
- **SQLite/PostgreSQL** - Base de datos
- **CORS** - Cross-origin requests

## 📝 Modelos de datos

### User
- Email, contraseña (encriptada)
- Nombre de empresa
- Nombre y apellido

### Invitation
- Información del cumpleañero
- Detalles de la fiesta
- Organizador (contacto)
- Código único para compartir

### Guest
- Nombre, email, teléfono
- RSVP (pendiente, aceptado, rechazado, tentativo)
- Número de acompañantes
- Restricciones dietéticas

## 🚢 Deployment

### Heroku
```bash
heroku create
git push heroku main
```

### Docker
```bash
docker build -t birthday-app .
docker run -p 5000:5000 birthday-app
```

## 📊 Próximas features

- [ ] Frontend web (React/Vue)
- [ ] App móvil
- [ ] Envío de emails
- [ ] Integración WhatsApp
- [ ] Sistema de pagos
- [ ] Galería de fotos
- [ ] Contador regresivo

## 📄 Licencia

MIT

## 🤝 Contribuir

Las contribuciones son bienvenidas. Abre un issue o PR para mejoras.
