# Guía de Personalización para Clientes 🎉

Esta guía te ayudará a personalizar la app de invitaciones de cumpleaños para tu negocio en menos de 30 minutos.

## 1. Configuración Básica

### 1.1 Variables de Entorno

Edita el archivo `.env` con tus datos:

```env
FLASK_ENV=production
FLASK_APP=run.py
SECRET_KEY=tu-clave-super-segura-cambiar-esto
SQLALCHEMY_DATABASE_URI=sqlite:///birthday_invitations.db
JWT_SECRET_KEY=tu-jwt-secret-key-cambiar-esto
PORT=5000
```

**⚠️ Importante**: Cambiar `SECRET_KEY` y `JWT_SECRET_KEY` con valores únicos y seguros.

### 1.2 Información de la Empresa

Cuando registres tu cuenta admin:

```bash
POST /api/auth/register

{
  "email": "admin@tuempresa.com",
  "password": "password-muy-seguro",
  "company_name": "Invitaciones XYZ",
  "first_name": "Tu Nombre",
  "last_name": "Tu Apellido"
}
```

## 2. Crear Templates Personalizados

Los templates son los estilos base que usarás para todas tus invitaciones.

### 2.1 Crear Template

```bash
POST /api/admin/templates
Authorization: Bearer {tu-token}

{
  "name": "Cumpleaños Clásico",
  "description": "Plantilla clásica elegante",
  "title": "¡Te Invitamos!",
  "subtitle": "A una celebración especial",
  "header_text": "Un día para no olvidar",
  "footer_text": "Confirmanos tu asistencia",
  "primary_color": "#FF69B4",      // Color principal (rosa)
  "secondary_color": "#FFD700",    // Color secundario (dorado)
  "text_color": "#333333",         // Color del texto
  "background_color": "#FFFFFF",   // Color de fondo
  "logo_url": "https://tudominio.com/logo.png",
  "background_image_url": "https://tudominio.com/bg.jpg",
  "is_default": true              // Este será el template por defecto
}
```

### 2.2 Colores Recomendados

**Opción 1 - Clásica Rosa**
- Primary: #FF69B4 (Rosa)
- Secondary: #FFD700 (Dorado)
- Text: #333333 (Gris oscuro)
- Background: #FFFFFF (Blanco)

**Opción 2 - Arcoíris**
- Primary: #FF6B9D (Rosa)
- Secondary: #C44569 (Rojo)
- Text: #2D3436 (Negro)
- Background: #FFF5F7 (Rosa claro)

**Opción 3 - Azul Moderno**
- Primary: #2E86DE (Azul)
- Secondary: #00D2FC (Cyan)
- Text: #1E1E1E (Negro)
- Background: #F0F5FF (Azul muy claro)

## 3. Crear una Invitación

Ahora que tienes un template, crea invitaciones para tus clientes:

```bash
POST /api/invitations
Authorization: Bearer {tu-token}

{
  "birthday_name": "Sofia",
  "birthday_date": "2019-02-14T00:00:00",
  "birthday_age": 5,
  "event_title": "Fiesta de Cumpleaños de Sofia",
  "event_date": "2024-02-14T15:00:00",
  "event_time": "15:00",
  "event_location": "Salón de Eventos La Alegría",
  "event_address": "Calle Principal 123, Madrid",
  "organizer_name": "María García",
  "organizer_phone": "+34 612 345 678",
  "organizer_email": "maria@example.com",
  "dress_code": "Casual",
  "special_notes": "Confirmación antes del 5 de febrero",
  "rsvp_deadline": "2024-02-05T00:00:00",
  "template_id": 1  // ID del template creado
}
```

**Notas importantes:**
- Las fechas deben estar en formato ISO 8601: `YYYY-MM-DDTHH:MM:SS`
- `birthday_age` es opcional pero recomendado
- Todos los campos descritos como "organizer" son opcionales

## 4. Publicar Invitación y Compartir

### 4.1 Publicar

```bash
POST /api/invitations/{invitation_id}/publish
Authorization: Bearer {tu-token}
```

Respuesta:
```json
{
  "message": "Invitación publicada exitosamente",
  "share_url": "/invitations/abc123def456",
  "invitation": { ... }
}
```

### 4.2 URL de Compartir

La invitación estará disponible en:
```
https://tudominio.com{share_url}
```

Puedes compartir esta URL por:
- WhatsApp
- Email
- Facebook
- Redes Sociales
- SMS

## 5. Gestionar Respuestas (RSVP)

### 5.1 Obtener Resumen de Respuestas

```bash
GET /api/public/invitations/{codigo-unico}/guests
```

Recibirás:
```json
{
  "guests": [
    {
      "id": 1,
      "name": "Carlos López",
      "email": "carlos@example.com",
      "rsvp_status": "accepted",
      "number_of_guests": 2,
      "dietary_restrictions": "Sin gluten"
    }
  ],
  "total_rsvp": 15,
  "rsvp_summary": {
    "accepted": 12,
    "declined": 2,
    "pending": 1,
    "tentative": 0
  }
}
```

### 5.2 Ver Estadísticas Generales

```bash
GET /api/admin/stats
Authorization: Bearer {tu-token}
```

Te mostrará:
- Total de invitaciones
- Invitaciones publicadas
- Total de templates
- Total de invitados
- Resumen de RSVP (aceptados, rechazados, pendientes)

## 6. Editar Invitación

```bash
PUT /api/invitations/{invitation_id}
Authorization: Bearer {tu-token}

{
  "event_time": "16:00",  // Cambiar hora
  "event_location": "Nuevo salón",
  "special_notes": "Nueva fecha: 10 de febrero"
  // Solo incluye los campos que quieres cambiar
}
```

## 7. Workflow Completo Para un Cliente

### Paso 1: Cliente te contacta
*"Quiero 50 invitaciones para la fiesta de Mateo"*

### Paso 2: Tú creas un template personalizado
```bash
POST /api/admin/templates
# Colors de acuerdo al tema de la fiesta (dinosaurios, superhéroes, etc.)
```

### Paso 3: Creas 50 invitaciones
```bash
# Usa un script o herramienta para crear múltiples invitaciones
# Ejemplo: cambiar solo el nombre del cumpleañero y fecha
```

### Paso 4: Publicas todas
```bash
# Puedes publicar una por una o con un script
POST /api/invitations/{id1}/publish
POST /api/invitations/{id2}/publish
# ...
```

### Paso 5: Das URLs a tu cliente
*"Aquí están las URLs personalizadas para cada invitado:"*
- https://tudominio.com/invitations/code1
- https://tudominio.com/invitations/code2
- etc.

### Paso 6: Monitoreas respuestas
```bash
GET /api/admin/stats  # Para ver resumen total
GET /api/public/invitations/{code}/guests  # Para ver lista completa
```

## 8. Configuración de Producción

### 8.1 Base de Datos

Para producción, cambiar de SQLite a PostgreSQL:

```env
SQLALCHEMY_DATABASE_URI=postgresql://user:password@localhost/birthday_app
```

### 8.2 Instalar PostgreSQL Driver

```bash
pip install psycopg2-binary
```

### 8.3 SSL/HTTPS

Asegúrate de que tu servidor use HTTPS.

### 8.4 Servidor WSGI

Usar Gunicorn en producción:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 9. Preguntas Frecuentes

**P: ¿Puedo cambiar el template después de crear la invitación?**
R: Sí, puedes actualizar la invitación con un nuevo `template_id`.

**P: ¿Qué pasa si olvido publicar una invitación?**
R: No será accesible públicamente. Los invitados no podrán ver ni responder.

**P: ¿Puedo eliminar una invitación?**
R: Sí, con `DELETE /api/invitations/{id}`, pero los RSVP se eliminarán también.

**P: ¿Hay límite de invitaciones?**
R: No hay límite técnico, depende de tu base de datos.

**P: ¿Puedo cambiar colores después de crear el template?**
R: Sí, actualiza el template con `PUT /api/admin/templates/{id}`.

**P: ¿Cómo hago backup de los datos?**
R: Haz backup de la carpeta con la base de datos SQLite o realiza dump de PostgreSQL.

## 10. Soporte

- Documentación completa: `/API_DOCUMENTATION.md`
- Código fuente: `app/` (routes, models)
- Variables de config: `config.py`

¡Buena suerte con tus invitaciones! 🎈🎂
