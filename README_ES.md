# 🎂 Birthday Invitations App

Una aplicación **SaaS completa** para crear y vender invitaciones de cumpleaños digitales personalizables. Backend profesional con Flask, listo para monetizar.

## 🌟 Características Clave

### Para Ti (Vendedor)
- ✅ **Administración multi-cliente** - Cada cliente aislado
- ✅ **Templates reutilizables** - Diseña una vez, vende muchas veces
- ✅ **Panel de control** - Estadísticas en tiempo real
- ✅ **Generación de URL** - Códigos únicos por invitación
- ✅ **Monitoreo RSVP** - Ve respuestas en tiempo real

### Para Tus Clientes
- ✅ **Interfaz simple** - No requiere conocimientos técnicos
- ✅ **Personalización rápida** - 5 minutos para crear invitación
- ✅ **Diseños profesionales** - Templates listos para usar
- ✅ **Compartir fácil** - URLs únicas para cada invitado
- ✅ **RSVP automático** - Control de asistencias

## 🚀 Inicio Rápido (3 minutos)

### 1. Clonar y instalar

```bash
git clone <repo>
cd python-tests-tablet

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar

```bash
# Copiar y editar configuración
cp .env.example .env

# Cambiar SECRET_KEY y JWT_SECRET_KEY en .env
```

### 3. Ejecutar

```bash
python run.py
```

**Servidor disponible en:** `http://localhost:5000`

## 📚 Documentación

- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Referencia completa de endpoints
- **[PERSONALIZATION_GUIDE.md](PERSONALIZATION_GUIDE.md)** - Cómo vender y personalizar
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Guías de producción (Heroku, Docker, AWS, etc.)

## 💻 Arquitectura

```
┌─────────────────────────────────────────┐
│         Frontend (Tu cliente)            │
│      (React, Vue, Mobile, etc)          │
└────────────────────┬────────────────────┘
                     │
                     │ REST API
                     │
┌────────────────────▼────────────────────┐
│      Backend Flask (Este repo)          │
│  ┌────────────────────────────────────┐ │
│  │ Routes (Auth, Invitations, Admin)  │ │
│  ├────────────────────────────────────┤ │
│  │ Models (User, Template, Guest)     │ │
│  ├────────────────────────────────────┤ │
│  │ Database (SQLite/PostgreSQL)       │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## 📊 Modelos de Datos

### User (Admin/Seller)
- Email y contraseña (encriptada)
- Nombre de empresa
- Fecha de creación

### Template
- Nombre y descripción
- Textos personalizables
- Colores (primario, secundario, fondo)
- URLs de logo e imágenes
- Marcar como "default"

### Invitation
- Información del cumpleañero
- Detalles de la fiesta
- Organizador y contacto
- Código único (URL amigable)
- Estado: borrador/publicada

### Guest
- Nombre, email, teléfono
- RSVP status (pendiente/aceptado/rechazado)
- Número de acompañantes
- Restricciones dietéticas

## 🔑 Endpoints Principales

### Autenticación
```bash
POST /api/auth/register          # Registrar nuevo vendedor
POST /api/auth/login             # Login
GET  /api/auth/me                # Perfil actual
```

### Templates (Admin)
```bash
POST   /api/admin/templates      # Crear template
GET    /api/admin/templates      # Listar mis templates
PUT    /api/admin/templates/{id} # Editar template
DELETE /api/admin/templates/{id} # Eliminar template
```

### Invitaciones (Admin)
```bash
POST   /api/invitations          # Crear invitación
GET    /api/invitations          # Listar mis invitaciones
PUT    /api/invitations/{id}     # Editar invitación
DELETE /api/invitations/{id}     # Eliminar invitación
POST   /api/invitations/{id}/publish  # Publicar
GET    /api/admin/stats          # Estadísticas
```

### Público (Para invitados)
```bash
GET    /api/public/invitations/{code}       # Ver invitación
POST   /api/public/invitations/{code}/rsvp  # Confirmar asistencia
GET    /api/public/invitations/{code}/guests # Ver lista de invitados
```

## 💡 Casos de Uso

### Caso 1: Vendedor individual
- Creas templates una vez
- Vendes invitaciones bajo demanda
- Tus clientes ahorran tiempo y dinero

### Caso 2: Agencia de eventos
- Varias personas venden
- Cada una con sus clientes
- Templates profesionales de marca

### Caso 3: Tienda digital
- Vender templates directamente
- Diferentes paquetes y precios
- Soporte automatizado

## 🔒 Seguridad

- ✅ Contraseñas encriptadas con Werkzeug
- ✅ JWT para autenticación stateless
- ✅ CORS configurado
- ✅ Validación de entrada en todos los endpoints
- ✅ Datos aislados por usuario
- ✅ Variables sensibles en .env

## 🛠️ Stack Técnico

| Capa | Tecnología |
|------|-----------|
| **Backend** | Flask 3.0 |
| **ORM** | SQLAlchemy |
| **Auth** | JWT + Werkzeug |
| **BD** | SQLite (dev) / PostgreSQL (prod) |
| **API** | RESTful |
| **Deployment** | Docker, Heroku, AWS, etc |

## 📦 Dependencias

```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-JWT-Extended==4.5.3
Flask-CORS==4.0.0
SQLAlchemy==2.0.23
Werkzeug==3.0.1
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

## 🚢 Despliegue

### Opción 1: Local (Desarrollo)
```bash
python run.py
```

### Opción 2: Docker
```bash
docker-compose up
```

### Opción 3: Heroku
```bash
heroku create
git push heroku main
```

Ver [DEPLOYMENT.md](DEPLOYMENT.md) para todas las opciones.

## 📈 Escalabilidad

**Desarrollo**
- SQLite ✅
- 1 usuario ✅

**Producción**
- PostgreSQL ✅
- Multi-usuario ✅
- 100+ usuarios ✅

**Escalado empresarial**
- PostgreSQL + Redis
- Múltiples workers
- Arquitectura de microservicios

## 🧪 Testing

### Probar la API

```bash
# Opción 1: Con script incluido
python test_api.py

# Opción 2: Con curl
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"pass123"}'
```

### Crear múltiples invitaciones

```bash
# Desde CSV
python bulk_create_invitations.py --file invitados.csv --token TOKEN --template-id 1
```

## 📝 Personalización por Cliente

### Flujo típico:
1. **Cliente se registra** - Obtiene cuenta
2. **Tú creas template** - Colores, textos, imágenes
3. **Cliente crea invitación** - Rellena datos
4. **Selecciona template** - Elige diseño
5. **Publica** - Genera URL única
6. **Comparte** - WhatsApp, email, redes
7. **Monitorea RSVP** - Ve confirmaciones

Ver [PERSONALIZATION_GUIDE.md](PERSONALIZATION_GUIDE.md) para guía detallada.

## 🎨 Ejemplos de Colores

**Clásica Rosa** `#FF69B4` + `#FFD700`
**Azul Moderno** `#2E86DE` + `#00D2FC`
**Arcoíris** `#FF6B9D` + `#C44569`
**Verde Fresco** `#00B894` + `#00CEC9`

## 📞 Soporte para Clientes

Incluir en tu sitio web:
- Documentación de uso
- Video tutorial (5 min)
- Email de soporte
- FAQ frecuentes
- Demo en vivo

## 🔄 Roadmap

### V1 (Actual)
- ✅ Backend completo
- ✅ API RESTful
- ✅ Multi-usuario
- ✅ Templates

### V2 (Próximo)
- [ ] Frontend web (React/Vue)
- [ ] Email automático
- [ ] Galería de fotos
- [ ] App móvil

### V3 (Futuro)
- [ ] Pagos (Stripe/PayPal)
- [ ] Integración WhatsApp
- [ ] IA para sugerir colores
- [ ] Estadísticas avanzadas

## 💰 Modelo de Negocio

### Opción 1: Suscripción
- Plan Basic: $10/mes (10 invitaciones)
- Plan Pro: $30/mes (ilimitadas)
- Plan Enterprise: Precio personalizado

### Opción 2: Por uso
- $0.50 por invitación
- $5 por template premium
- Comisión por servicios adicionales

### Opción 3: Blanco
- Vendedor reseller
- Marca blanca
- Licencia anual

## 📄 Licencia

MIT - Libre para usar, modificar y vender

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Contacto

- Email: soporte@ejemplo.com
- Sitio: https://ejemplo.com
- Docs: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

**¡Listo para monetizar! 🎉**

Tienes un backend profesional, seguro y escalable. Ahora solo falta:
1. Crear un frontend atractivo
2. Establecer tu estrategia de marketing
3. ¡Vender a clientes! 💸
