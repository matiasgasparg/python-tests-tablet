#!/usr/bin/env python3
"""
Script de prueba para la API de Birthday Invitations
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000/api"

# Colores para output en terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def print_header(text):
    print(f"\n{Colors.HEADER}{'='*50}")
    print(f"{text}")
    print(f"{'='*50}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKBLUE}ℹ️  {text}{Colors.ENDC}")

# Test 1: Registro de usuario
def test_register():
    print_header("1. REGISTRO DE USUARIO")
    
    data = {
        "email": "admin@example.com",
        "password": "securepassword123",
        "company_name": "Mi Empresa de Eventos",
        "first_name": "Juan",
        "last_name": "Pérez"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=data)
        if response.status_code == 201:
            print_success(f"Usuario registrado: {response.json()['user']['email']}")
            return response.json()['user']
        elif response.status_code == 409:
            print_info("Usuario ya existe, continuando...")
            return None
        else:
            print_error(f"Error: {response.json()['message']}")
            return None
    except Exception as e:
        print_error(f"Conexión fallida: {e}")
        return None

# Test 2: Login
def test_login():
    print_header("2. LOGIN")
    
    data = {
        "email": "admin@example.com",
        "password": "securepassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=data)
        if response.status_code == 200:
            token = response.json()['access_token']
            print_success(f"Login exitoso")
            print_info(f"Token: {token[:20]}...")
            return token
        else:
            print_error(f"Error: {response.json()['message']}")
            return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None

# Test 3: Obtener perfil
def test_get_profile(token):
    print_header("3. OBTENER PERFIL")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            user = response.json()
            print_success(f"Perfil obtenido")
            print_info(f"Empresa: {user['company_name']}")
            print_info(f"Email: {user['email']}")
        else:
            print_error(f"Error: {response.json()['message']}")
    except Exception as e:
        print_error(f"Error: {e}")

# Test 4: Crear template
def test_create_template(token):
    print_header("4. CREAR TEMPLATE")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    data = {
        "name": "Template Cumpleaños Rosa",
        "description": "Plantilla clásica con colores rosa y dorado",
        "title": "¡Te invitamos a celebrar!",
        "subtitle": "Un día especial lleno de alegría",
        "header_text": "Únete a nosotros en una celebración inolvidable",
        "footer_text": "¡Esperamos tu confirmación!",
        "primary_color": "#FF69B4",
        "secondary_color": "#FFD700",
        "text_color": "#333333",
        "background_color": "#FFFFFF",
        "is_default": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/admin/templates", json=data, headers=headers)
        if response.status_code == 201:
            template = response.json()['template']
            print_success(f"Template creado: {template['name']}")
            print_info(f"ID: {template['id']}")
            return template['id']
        else:
            print_error(f"Error: {response.json()['message']}")
            return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None

# Test 5: Crear invitación
def test_create_invitation(token, template_id):
    print_header("5. CREAR INVITACIÓN")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    today = datetime.now()
    event_date = today + timedelta(days=30)
    birthday_date = today - timedelta(days=365*5)
    rsvp_deadline = event_date - timedelta(days=7)
    
    data = {
        "birthday_name": "Sofia",
        "birthday_date": birthday_date.isoformat(),
        "birthday_age": 5,
        "event_title": "Fiesta de Cumpleaños de Sofia",
        "event_date": event_date.isoformat(),
        "event_time": "15:00",
        "event_location": "Casa de la Abuela",
        "event_address": "Calle Principal 123, Apartamento 4B",
        "organizer_name": "María García",
        "organizer_phone": "+34 612 345 678",
        "organizer_email": "maria@example.com",
        "dress_code": "Casual",
        "special_notes": "Por favor, confirmar asistencia antes del 1 de febrero",
        "rsvp_deadline": rsvp_deadline.isoformat(),
        "template_id": template_id
    }
    
    try:
        response = requests.post(f"{BASE_URL}/invitations", json=data, headers=headers)
        if response.status_code == 201:
            invitation = response.json()['invitation']
            print_success(f"Invitación creada para {invitation['birthday_name']}")
            print_info(f"ID: {invitation['id']}")
            print_info(f"Código único: {invitation['unique_code']}")
            return invitation['id'], invitation['unique_code']
        else:
            print_error(f"Error: {response.json()['message']}")
            return None, None
    except Exception as e:
        print_error(f"Error: {e}")
        return None, None

# Test 6: Obtener estadísticas
def test_get_stats(token):
    print_header("6. OBTENER ESTADÍSTICAS")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/admin/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print_success("Estadísticas obtenidas")
            print_info(f"Total invitaciones: {stats['total_invitations']}")
            print_info(f"Invitaciones publicadas: {stats['published_invitations']}")
            print_info(f"Templates: {stats['total_templates']}")
            print_info(f"Total invitados: {stats['total_guests']}")
            print_info(f"RSVP Aceptados: {stats['rsvp_accepted']}")
            print_info(f"RSVP Rechazados: {stats['rsvp_declined']}")
            print_info(f"RSVP Pendientes: {stats['rsvp_pending']}")
        else:
            print_error(f"Error: {response.json()['message']}")
    except Exception as e:
        print_error(f"Error: {e}")

# Test 7: Publicar invitación
def test_publish_invitation(token, invitation_id):
    print_header("7. PUBLICAR INVITACIÓN")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(f"{BASE_URL}/invitations/{invitation_id}/publish", 
                               headers=headers)
        if response.status_code == 200:
            invitation = response.json()['invitation']
            share_url = response.json()['share_url']
            print_success(f"Invitación publicada")
            print_info(f"URL de compartir: {share_url}")
            return share_url
        else:
            print_error(f"Error: {response.json()['message']}")
            return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None

# Test 8: Obtener invitación pública
def test_get_public_invitation(code):
    print_header("8. OBTENER INVITACIÓN PÚBLICA")
    
    try:
        response = requests.get(f"{BASE_URL}/public/invitations/{code}")
        if response.status_code == 200:
            invitation = response.json()['invitation']
            print_success(f"Invitación pública obtenida")
            print_info(f"Celebrando a: {invitation['birthday_name']}")
            print_info(f"Fecha del evento: {invitation['event_date']}")
            print_info(f"Ubicación: {invitation['event_location']}")
        else:
            print_error(f"Error: {response.json()['message']}")
    except Exception as e:
        print_error(f"Error: {e}")

# Test 9: Enviar RSVP
def test_submit_rsvp(code):
    print_header("9. ENVIAR RSVP")
    
    data = {
        "guest_name": "Carlos López",
        "guest_email": "carlos@example.com",
        "guest_phone": "+34 612 111 222",
        "rsvp_status": "accepted",
        "number_of_guests": 2,
        "dietary_restrictions": "Sin gluten",
        "notes": "Nos encanta las fiestas"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/public/invitations/{code}/rsvp", 
                               json=data)
        if response.status_code == 201:
            guest = response.json()['guest']
            print_success(f"RSVP registrado para {guest['name']}")
            print_info(f"Estado: {guest['rsvp_status']}")
            print_info(f"Número de invitados: {guest['number_of_guests']}")
        else:
            print_error(f"Error: {response.json()['message']}")
    except Exception as e:
        print_error(f"Error: {e}")

# Test 10: Obtener lista de invitados
def test_get_guests(code):
    print_header("10. OBTENER LISTA DE INVITADOS")
    
    try:
        response = requests.get(f"{BASE_URL}/public/invitations/{code}/guests")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Lista de invitados obtenida")
            print_info(f"Total respuestas: {data['total_rsvp']}")
            print_info(f"Aceptados: {data['rsvp_summary']['accepted']}")
            print_info(f"Rechazados: {data['rsvp_summary']['declined']}")
            print_info(f"Pendientes: {data['rsvp_summary']['pending']}")
            print_info(f"Indecisos: {data['rsvp_summary']['tentative']}")
        else:
            print_error(f"Error: {response.json()['message']}")
    except Exception as e:
        print_error(f"Error: {e}")

def main():
    print(f"{Colors.OKCYAN}")
    print("""
    ╔═══════════════════════════════════════════════╗
    ║   Birthday Invitations API - Test Suite      ║
    ║   Pruebas completas de la API                ║
    ╚═══════════════════════════════════════════════╝
    """)
    print(f"{Colors.ENDC}")
    
    print_info(f"Base URL: {BASE_URL}")
    
    # Ejecutar pruebas
    test_register()
    token = test_login()
    
    if not token:
        print_error("No se pudo obtener token. Abortando pruebas.")
        return
    
    test_get_profile(token)
    
    template_id = test_create_template(token)
    if not template_id:
        print_error("No se pudo crear template. Abortando pruebas.")
        return
    
    invitation_id, code = test_create_invitation(token, template_id)
    if not invitation_id:
        print_error("No se pudo crear invitación. Abortando pruebas.")
        return
    
    test_get_stats(token)
    
    test_publish_invitation(token, invitation_id)
    
    test_get_public_invitation(code)
    
    test_submit_rsvp(code)
    
    test_submit_rsvp(code)  # Otro invitado
    
    test_get_guests(code)
    
    print_header("✨ PRUEBAS COMPLETADAS ✨")
    print("Todo funcionó correctamente. ¡La API está lista para usar!")

if __name__ == "__main__":
    main()
