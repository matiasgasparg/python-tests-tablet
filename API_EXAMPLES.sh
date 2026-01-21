#!/bin/bash

# EJEMPLOS DE USO DE LA API
# Birthday Invitations App - Casos de uso prácticos

echo "╔════════════════════════════════════════════╗"
echo "║  EJEMPLOS DE USO DE LA API                ║"
echo "║  Birthday Invitations                    ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Variables útiles
API_URL="http://localhost:5000/api"
ADMIN_EMAIL="admin@example.com"
ADMIN_PASSWORD="securepassword123"

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# ============================================================
# 1. REGISTRO Y AUTENTICACIÓN
# ============================================================

echo -e "${BLUE}1. REGISTRO DE NUEVO USUARIO${NC}"
echo ""
echo "POST $API_URL/auth/register"
echo ""
echo "curl -X POST $API_URL/auth/register \\"
echo '  -H "Content-Type: application/json" \'
echo "  -d '{"
echo '    "email": "admin@example.com",'
echo '    "password": "securepassword123",'
echo '    "company_name": "Mi Empresa de Eventos",'
echo '    "first_name": "Juan",'
echo '    "last_name": "Pérez"'
echo "  }'"
echo ""

echo -e "${BLUE}2. INICIAR SESIÓN (LOGIN)${NC}"
echo ""
echo "POST $API_URL/auth/login"
echo ""
echo "curl -X POST $API_URL/auth/login \\"
echo '  -H "Content-Type: application/json" \'
echo "  -d '{"
echo '    "email": "admin@example.com",'
echo '    "password": "securepassword123"'
echo "  }'"
echo ""
echo -e "${GREEN}Respuesta incluye: access_token${NC}"
echo ""

echo -e "${BLUE}3. OBTENER PERFIL ACTUAL${NC}"
echo ""
echo "GET $API_URL/auth/me"
echo ""
echo "curl -X GET $API_URL/auth/me \\"
echo '  -H "Authorization: Bearer {TOKEN}"'
echo ""

# ============================================================
# 2. GESTIÓN DE TEMPLATES
# ============================================================

echo -e "${BLUE}4. CREAR TEMPLATE${NC}"
echo ""
echo "POST $API_URL/admin/templates"
echo ""
echo "curl -X POST $API_URL/admin/templates \\"
echo '  -H "Authorization: Bearer {TOKEN}" \'
echo '  -H "Content-Type: application/json" \'
echo "  -d '{"
echo '    "name": "Cumpleaños Clásico Rosa",'
echo '    "description": "Plantilla elegante con colores rosa y dorado",'
echo '    "title": "¡Te invitamos a celebrar!",'
echo '    "subtitle": "Un día especial lleno de alegría",'
echo '    "header_text": "Únete a nosotros en una celebración inolvidable",'
echo '    "footer_text": "¡Esperamos tu confirmación!",'
echo '    "primary_color": "#FF69B4",'
echo '    "secondary_color": "#FFD700",'
echo '    "text_color": "#333333",'
echo '    "background_color": "#FFFFFF",'
echo '    "logo_url": "https://ejemplo.com/logo.png",'
echo '    "background_image_url": "https://ejemplo.com/bg.jpg",'
echo '    "is_default": true'
echo "  }'"
echo ""

echo -e "${BLUE}5. LISTAR TEMPLATES${NC}"
echo ""
echo "GET $API_URL/admin/templates"
echo ""
echo "curl -X GET $API_URL/admin/templates \\"
echo '  -H "Authorization: Bearer {TOKEN}"'
echo ""

echo -e "${BLUE}6. ACTUALIZAR TEMPLATE${NC}"
echo ""
echo "PUT $API_URL/admin/templates/1"
echo ""
echo "curl -X PUT $API_URL/admin/templates/1 \\"
echo '  -H "Authorization: Bearer {TOKEN}" \'
echo '  -H "Content-Type: application/json" \'
echo "  -d '{"
echo '    "primary_color": "#00B894",'
echo '    "secondary_color": "#00CEC9"'
echo "  }'"
echo ""

echo -e "${BLUE}7. ELIMINAR TEMPLATE${NC}"
echo ""
echo "DELETE $API_URL/admin/templates/1"
echo ""
echo "curl -X DELETE $API_URL/admin/templates/1 \\"
echo '  -H "Authorization: Bearer {TOKEN}"'
echo ""

# ============================================================
# 3. GESTIÓN DE INVITACIONES
# ============================================================

echo -e "${BLUE}8. CREAR INVITACIÓN${NC}"
echo ""
echo "POST $API_URL/invitations"
echo ""
echo "curl -X POST $API_URL/invitations \\"
echo '  -H "Authorization: Bearer {TOKEN}" \'
echo '  -H "Content-Type: application/json" \'
echo "  -d '{"
echo '    "birthday_name": "Sofia",'
echo '    "birthday_date": "2019-02-14T00:00:00",'
echo '    "birthday_age": 5,'
echo '    "event_title": "Fiesta de Cumpleaños de Sofia",'
echo '    "event_date": "2024-02-14T15:00:00",'
echo '    "event_time": "15:00",'
echo '    "event_location": "Salón de Eventos La Alegría",'
echo '    "event_address": "Calle Principal 123, Madrid",'
echo '    "organizer_name": "María García",'
echo '    "organizer_phone": "+34 612 345 678",'
echo '    "organizer_email": "maria@example.com",'
echo '    "dress_code": "Casual",'
echo '    "special_notes": "Confirmación antes del 5 de febrero",'
echo '    "rsvp_deadline": "2024-02-05T00:00:00",'
echo '    "template_id": 1'
echo "  }'"
echo ""

echo -e "${BLUE}9. LISTAR MIS INVITACIONES${NC}"
echo ""
echo "GET $API_URL/invitations?page=1&per_page=10"
echo ""
echo "curl -X GET '$API_URL/invitations?page=1&per_page=10' \\"
echo '  -H "Authorization: Bearer {TOKEN}"'
echo ""

echo -e "${BLUE}10. OBTENER DETALLES DE UNA INVITACIÓN${NC}"
echo ""
echo "GET $API_URL/invitations/1"
echo ""
echo "curl -X GET $API_URL/invitations/1 \\"
echo '  -H "Authorization: Bearer {TOKEN}"'
echo ""

echo -e "${BLUE}11. ACTUALIZAR INVITACIÓN${NC}"
echo ""
echo "PUT $API_URL/invitations/1"
echo ""
echo "curl -X PUT $API_URL/invitations/1 \\"
echo '  -H "Authorization: Bearer {TOKEN}" \'
echo '  -H "Content-Type: application/json" \'
echo "  -d '{"
echo '    "event_time": "16:00",'
echo '    "special_notes": "Cambio de hora: 16:00 hrs"'
echo "  }'"
echo ""

echo -e "${BLUE}12. PUBLICAR INVITACIÓN${NC}"
echo ""
echo "POST $API_URL/invitations/1/publish"
echo ""
echo "curl -X POST $API_URL/invitations/1/publish \\"
echo '  -H "Authorization: Bearer {TOKEN}"'
echo ""
echo -e "${GREEN}Respuesta incluye: share_url (URL para compartir)${NC}"
echo ""

echo -e "${BLUE}13. ELIMINAR INVITACIÓN${NC}"
echo ""
echo "DELETE $API_URL/invitations/1"
echo ""
echo "curl -X DELETE $API_URL/invitations/1 \\"
echo '  -H "Authorization: Bearer {TOKEN}"'
echo ""

# ============================================================
# 4. ESTADÍSTICAS
# ============================================================

echo -e "${BLUE}14. VER ESTADÍSTICAS${NC}"
echo ""
echo "GET $API_URL/admin/stats"
echo ""
echo "curl -X GET $API_URL/admin/stats \\"
echo '  -H "Authorization: Bearer {TOKEN}"'
echo ""
echo "Retorna:"
echo "- total_invitations"
echo "- published_invitations"
echo "- total_templates"
echo "- total_guests"
echo "- rsvp_accepted"
echo "- rsvp_declined"
echo "- rsvp_pending"
echo ""

# ============================================================
# 5. ENDPOINTS PÚBLICOS (SIN AUTENTICACIÓN)
# ============================================================

echo -e "${BLUE}15. VER INVITACIÓN PÚBLICA${NC}"
echo ""
echo "GET $API_URL/public/invitations/{codigo-unico}"
echo ""
echo "curl -X GET $API_URL/public/invitations/abc123def456"
echo ""
echo "Nota: El código se obtiene al crear la invitación"
echo ""

echo -e "${BLUE}16. ENVIAR RSVP (CONFIRMAR ASISTENCIA)${NC}"
echo ""
echo "POST $API_URL/public/invitations/{codigo-unico}/rsvp"
echo ""
echo "curl -X POST $API_URL/public/invitations/abc123def456/rsvp \\"
echo '  -H "Content-Type: application/json" \'
echo "  -d '{"
echo '    "guest_name": "Carlos López",'
echo '    "guest_email": "carlos@example.com",'
echo '    "guest_phone": "+34 612 111 222",'
echo '    "rsvp_status": "accepted",'
echo '    "number_of_guests": 2,'
echo '    "dietary_restrictions": "Sin gluten",'
echo '    "notes": "Nos encanta las fiestas"'
echo "  }'"
echo ""
echo "Valores válidos para rsvp_status:"
echo "- accepted (aceptado)"
echo "- declined (rechazado)"
echo "- tentative (indeciso)"
echo ""

echo -e "${BLUE}17. VER LISTA DE INVITADOS${NC}"
echo ""
echo "GET $API_URL/public/invitations/{codigo-unico}/guests"
echo ""
echo "curl -X GET $API_URL/public/invitations/abc123def456/guests"
echo ""
echo "Retorna:"
echo "- guests: array de invitados"
echo "- total_rsvp: cantidad total"
echo "- rsvp_summary: resumen de respuestas"
echo ""

# ============================================================
# 6. EJEMPLOS PRÁCTICOS
# ============================================================

echo -e "${BLUE}FLUJO PRÁCTICO COMPLETO:${NC}"
echo ""
echo "1. Registrarse"
echo "   curl -X POST $API_URL/auth/register ..."
echo ""
echo "2. Login (obtener TOKEN)"
echo "   curl -X POST $API_URL/auth/login ..."
echo "   → Copiar el access_token"
echo ""
echo "3. Crear template"
echo "   curl -X POST $API_URL/admin/templates \\"
echo '     -H "Authorization: Bearer {TOKEN}" ...'
echo "   → Notar el template_id (ej: 1)"
echo ""
echo "4. Crear invitación"
echo "   curl -X POST $API_URL/invitations \\"
echo '     -H "Authorization: Bearer {TOKEN}" ...'
echo "   → Notar el invitation_id y unique_code"
echo ""
echo "5. Publicar invitación"
echo "   curl -X POST $API_URL/invitations/1/publish \\"
echo '     -H "Authorization: Bearer {TOKEN}"'
echo "   → Obtener share_url"
echo ""
echo "6. Compartir URL con invitados"
echo "   https://tu-dominio.com{share_url}"
echo ""
echo "7. Los invitados confirman asistencia"
echo "   curl -X POST $API_URL/public/invitations/{code}/rsvp ..."
echo ""
echo "8. Ver respuestas"
echo "   curl -X GET $API_URL/public/invitations/{code}/guests"
echo ""

# ============================================================
# 7. TROUBLESHOOTING
# ============================================================

echo -e "${BLUE}TROUBLESHOOTING:${NC}"
echo ""
echo "Error 401 Unauthorized:"
echo "  → Token expirado o inválido"
echo "  → Hacer login nuevamente para obtener nuevo token"
echo ""
echo "Error 404 Not Found:"
echo "  → Recurso no existe"
echo "  → Verificar el ID o código"
echo ""
echo "Error 409 Conflict:"
echo "  → Email ya registrado"
echo "  → Intentar con otro email"
echo ""
echo "Error 400 Bad Request:"
echo "  → Falta algún campo requerido"
echo "  → Revisar documentación de los campos necesarios"
echo ""

echo -e "${GREEN}¡Para ver la documentación completa: API_DOCUMENTATION.md${NC}"
