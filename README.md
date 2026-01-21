# Birthday Invitations App 🎂

Una aplicación Flask para crear y gestionar invitaciones de cumpleaños personalizables. Diseñada para ser vendida como SaaS con panel de administración para rápida personalización por cliente.

## 🎯 Características

- ✅ **Autenticación segura** con JWT
- ✅ **Plantillas personalizables** - Colores, textos, imágenes
- ✅ **Gestión de invitaciones** - CRUD completo
- ✅ **Sistema de RSVP** - Confirmación de invitados
- ✅ **URLs únicas** - Código único para cada invitación
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

## 📚 Documentación API

Ver [API_DOCUMENTATION.md](API_DOCUMENTATION.md) para documentación completa de endpoints.

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

# 3. Crear plantilla
curl -X POST http://localhost:5000/api/admin/templates \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Plantilla Clásica",
    "primary_color": "#FF69B4",
    "secondary_color": "#FFD700"
  }'
```

## 📁 Estructura del proyecto

```
.
├── app/
│   ├── models/              # Modelos de BD
│   │   ├── user.py         # Usuarios/Admins
│   │   ├── invitation.py   # Invitaciones
│   │   ├── template.py     # Plantillas
│   │   └── guest.py        # Invitados
│   ├── routes/              # APIs
│   │   ├── auth.py         # Autenticación
│   │   ├── invitations.py  # CRUD invitaciones
│   │   ├── admin.py        # Panel admin
│   │   └── public.py       # Endpoints públicos
│   ├── templates/           # HTML templates
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
2. **Crear plantillas base** - Diseñar templates reutilizables
3. **Vender a clientes** - Cada cliente obtiene su propia cuenta

### Cliente (Tu cliente)
1. **Recibir credenciales** - Email y contraseña
2. **Crear invitación** - Llenar datos de la fiesta
3. **Elegir plantilla** - Seleccionar diseño base
4. **Personalizar** - Cambiar colores y textos
5. **Publicar** - Generar URL para compartir
6. **Compartir** - Enviar por WhatsApp, email, redes sociales

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

### Template
- Nombre y descripción
- Textos personalizables (título, subtítulo, encabezado, pie)
- Colores (primario, secundario, texto, fondo)
- URLs de logo e imagen de fondo

### Invitation
- Información del cumpleañero
- Detalles de la fiesta
- Organizador (contacto)
- Código único para compartir
- Plantilla asociada

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
- [ ] Más templates
- [ ] Galería de fotos
- [ ] Contador regresivo

## 📄 Licencia

MIT

## 🤝 Contribuir

Las contribuciones son bienvenidas. Abre un issue o PR para mejoras.