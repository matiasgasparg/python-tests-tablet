# Birthday Invitations App - API Documentation

## Descripción
Backend Flask para una aplicación web de invitaciones de cumpleaños personalizables. Permite a los administradores crear y configurar plantillas, así como gestionar invitaciones y respuestas de invitados.

## Características principales

- **Autenticación segura** con JWT
- **Gestión de templates personalizables** con colores, textos e imágenes
- **Creación y distribución de invitaciones** con código único
- **Sistema de RSVP** para invitados
- **Dashboard admin** con estadísticas
- **Multi-usuario** - cada usuario tiene sus propias invitaciones

## Instalación

### Requisitos previos
- Python 3.8+
- pip

### Pasos de instalación

1. **Clonar el repositorio**
```bash
git clone <repo-url>
cd python-tests-tablet
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Ejecutar la aplicación**
```bash
python run.py
```

La aplicación estará disponible en `http://localhost:5000`

## Estructura del proyecto

```
.
├── app/
│   ├── models/              # Modelos de base de datos
│   │   ├── user.py         # Modelo de usuario/admin
│   │   ├── invitation.py   # Modelo de invitación
│   │   ├── template.py     # Modelo de plantilla
│   │   └── guest.py        # Modelo de invitado
│   ├── routes/              # Rutas/APIs
│   │   ├── auth.py         # Autenticación
│   │   ├── invitations.py  # CRUD de invitaciones
│   │   ├── admin.py        # Panel admin
│   │   └── public.py       # Endpoints públicos
│   ├── templates/           # Templates HTML
│   ├── static/              # Archivos estáticos
│   └── __init__.py         # Inicialización de la app
├── config.py               # Configuración
├── run.py                  # Punto de entrada
└── requirements.txt        # Dependencias Python
```

## API Endpoints

### Autenticación (`/api/auth`)

#### Registrar usuario
```
POST /api/auth/register
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "securepassword",
  "company_name": "Mi Empresa",
  "first_name": "Juan",
  "last_name": "Pérez"
}
```

#### Iniciar sesión
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "securepassword"
}

Respuesta:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {...}
}
```

#### Obtener usuario actual
```
GET /api/auth/me
Authorization: Bearer {access_token}
```

#### Cambiar contraseña
```
POST /api/auth/change-password
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "old_password": "securepassword",
  "new_password": "newsecurepassword"
}
```

#### Actualizar perfil
```
PUT /api/auth/update-profile
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "company_name": "Nueva Empresa",
  "first_name": "Carlos",
  "last_name": "López"
}
```

### Plantillas (`/api/admin/templates`)

#### Crear plantilla
```
POST /api/admin/templates
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Plantilla Clásica",
  "description": "Diseño elegante para cumpleaños",
  "title": "¡Te invitamos a celebrar!",
  "subtitle": "Un día especial",
  "header_text": "Texto del encabezado",
  "footer_text": "Texto del pie de página",
  "primary_color": "#FF69B4",
  "secondary_color": "#FFD700",
  "text_color": "#333333",
  "background_color": "#FFFFFF",
  "logo_url": "https://example.com/logo.png",
  "background_image_url": "https://example.com/bg.jpg",
  "is_default": false
}
```

#### Listar plantillas
```
GET /api/admin/templates
Authorization: Bearer {access_token}
```

#### Obtener plantilla
```
GET /api/admin/templates/{template_id}
Authorization: Bearer {access_token}
```

#### Actualizar plantilla
```
PUT /api/admin/templates/{template_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Plantilla Actualizada",
  "primary_color": "#FF1493",
  ...
}
```

#### Eliminar plantilla
```
DELETE /api/admin/templates/{template_id}
Authorization: Bearer {access_token}
```

### Invitaciones (`/api/invitations`)

#### Crear invitación
```
POST /api/invitations
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "birthday_name": "María García",
  "birthday_date": "2005-03-15T00:00:00",
  "birthday_age": 18,
  "template_id": 1,
  "event_title": "Cumpleaños de María",
  "event_date": "2024-03-16T19:00:00",
  "event_time": "19:00",
  "event_location": "Salón de fiestas El Dorado",
  "event_address": "Calle Principal 123, Ciudad",
  "organizer_name": "Carlos García",
  "organizer_phone": "+34 123 456 789",
  "organizer_email": "carlos@example.com",
  "dress_code": "Casual elegante",
  "rsvp_deadline": "2024-03-12T23:59:59",
  "special_notes": "Por favor confirmar antes del viernes"
}
```

#### Listar invitaciones
```
GET /api/invitations?page=1&per_page=10
Authorization: Bearer {access_token}
```

#### Obtener invitación
```
GET /api/invitations/{invitation_id}
Authorization: Bearer {access_token}
```

#### Actualizar invitación
```
PUT /api/invitations/{invitation_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "event_title": "Título actualizado",
  "event_location": "Nueva ubicación",
  ...
}
```

#### Publicar invitación
```
POST /api/invitations/{invitation_id}/publish
Authorization: Bearer {access_token}

Respuesta:
{
  "invitation": {...},
  "share_url": "/invitations/abcd1234efgh5678"
}
```

#### Eliminar invitación
```
DELETE /api/invitations/{invitation_id}
Authorization: Bearer {access_token}
```

### Dashboard Admin (`/api/admin/stats`)

#### Obtener estadísticas
```
GET /api/admin/stats
Authorization: Bearer {access_token}

Respuesta:
{
  "total_invitations": 5,
  "published_invitations": 3,
  "total_templates": 2,
  "total_guests": 45,
  "rsvp_accepted": 30,
  "rsvp_declined": 8,
  "rsvp_pending": 7
}
```

### Endpoints Públicos (`/api/public`)

#### Obtener invitación (público)
```
GET /api/public/invitations/{unique_code}

Respuesta:
{
  "invitation": {...},
  "guests": [...]
}
```

#### Enviar RSVP
```
POST /api/public/invitations/{unique_code}/rsvp
Content-Type: application/json

{
  "guest_name": "Juan Martínez",
  "guest_email": "juan@example.com",
  "guest_phone": "+34 987 654 321",
  "rsvp_status": "accepted",  # accepted, declined, tentative
  "number_of_guests": 2,
  "dietary_restrictions": "Vegetariano",
  "notes": "No puedo ir a la comida pero sí a la torta"
}
```

#### Obtener lista de invitados
```
GET /api/public/invitations/{unique_code}/guests
```

## Flujo de uso

### Para el vendedor de la aplicación:

1. **Registrarse**: Crear cuenta con email, contraseña y nombre de empresa
2. **Crear plantillas**: Diseñar plantillas reutilizables con colores y textos personalizables
3. **Vender a clientes**: Cada cliente recibe su propia cuenta

### Para el cliente:

1. **Recibir credenciales**: Email y contraseña para acceder
2. **Crear invitación**: Llenar formulario con datos de la fiesta
3. **Seleccionar plantilla**: Elegir diseño y personalizarlo (colores, textos)
4. **Publicar**: Generar URL única para compartir
5. **Compartir**: Enviar link a través de WhatsApp, email, redes sociales, etc.

### Para los invitados:

1. **Recibir invitación**: Link con código único
2. **Ver detalles**: Información de la fiesta
3. **Responder**: Confirmar asistencia (sí, no, talvez) con detalles

## Seguridad

- Contraseñas encriptadas con `werkzeug.security`
- Autenticación con JWT
- CORS habilitado para integración frontend
- Variables de entorno para configuraciones sensibles

## Próximas mejoras

- [ ] Frontend web (React/Vue)
- [ ] Aplicación móvil
- [ ] Envío de emails automático
- [ ] Integración con WhatsApp
- [ ] Sistema de pagos
- [ ] Más templates predefinidos
- [ ] Galería de fotos
- [ ] Contador de días para la fiesta

## Soporte

Para preguntas o problemas, contacta con el equipo de desarrollo.

## Licencia

Este proyecto está bajo licencia [Tu Licencia]
