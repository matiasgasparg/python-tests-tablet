#!/usr/bin/env python3
"""
Script para crear múltiples invitaciones desde un CSV
Útil para crear invitaciones en batch para clientes

Uso:
    python bulk_create_invitations.py --file invitados.csv --token TU_TOKEN --template-id 1
"""

import csv
import requests
import argparse
from datetime import datetime, timedelta

def create_invitations_from_csv(file_path, token, template_id, base_url="http://localhost:5000/api"):
    """
    Lee un CSV y crea invitaciones en batch
    
    Formato esperado del CSV:
    birthday_name,birthday_date,birthday_age,event_title,event_date,event_time,event_location,organizer_name,organizer_phone,organizer_email
    Sofia,2019-02-14,5,Fiesta de Sofia,2024-02-14,15:00,Salón La Alegría,María García,+34 612345678,maria@example.com
    """
    
    headers = {"Authorization": f"Bearer {token}"}
    created_count = 0
    failed_count = 0
    
    print(f"📂 Leyendo archivo: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            if not reader.fieldnames:
                print("❌ CSV vacío o inválido")
                return
            
            print(f"📊 Columnas detectadas: {', '.join(reader.fieldnames)}")
            print(f"✅ Usando template ID: {template_id}\n")
            
            for row_num, row in enumerate(reader, start=2):
                try:
                    # Preparar datos
                    data = {
                        "birthday_name": row.get('birthday_name', '').strip(),
                        "birthday_date": row.get('birthday_date', '').strip(),
                        "birthday_age": int(row.get('birthday_age', 0)) if row.get('birthday_age') else None,
                        "event_title": row.get('event_title', '').strip(),
                        "event_date": row.get('event_date', '').strip(),
                        "event_time": row.get('event_time', '').strip(),
                        "event_location": row.get('event_location', '').strip(),
                        "organizer_name": row.get('organizer_name', '').strip(),
                        "organizer_phone": row.get('organizer_phone', '').strip(),
                        "organizer_email": row.get('organizer_email', '').strip(),
                        "template_id": template_id
                    }
                    
                    # Validar campos requeridos
                    if not data['birthday_name']:
                        print(f"⚠️  Fila {row_num}: falta birthday_name")
                        failed_count += 1
                        continue
                    
                    if not data['event_title']:
                        print(f"⚠️  Fila {row_num}: falta event_title")
                        failed_count += 1
                        continue
                    
                    # Realizar request
                    response = requests.post(
                        f"{base_url}/invitations",
                        json=data,
                        headers=headers
                    )
                    
                    if response.status_code == 201:
                        invitation = response.json()['invitation']
                        print(f"✅ Fila {row_num}: {data['birthday_name']} - "
                              f"ID: {invitation['id']}, Código: {invitation['unique_code'][:8]}...")
                        created_count += 1
                    else:
                        error_msg = response.json().get('message', 'Error desconocido')
                        print(f"❌ Fila {row_num}: {data['birthday_name']} - Error: {error_msg}")
                        failed_count += 1
                
                except Exception as e:
                    print(f"❌ Fila {row_num}: Error procesando - {str(e)}")
                    failed_count += 1
                    continue
        
        print(f"\n{'='*50}")
        print(f"✅ Invitaciones creadas exitosamente: {created_count}")
        print(f"❌ Errores: {failed_count}")
        print(f"{'='*50}")
        
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {file_path}")
    except Exception as e:
        print(f"❌ Error leyendo CSV: {str(e)}")

def generate_sample_csv():
    """Genera un archivo CSV de ejemplo"""
    sample_data = """birthday_name,birthday_date,birthday_age,event_title,event_date,event_time,event_location,organizer_name,organizer_phone,organizer_email
Sofia,2019-02-14,5,Fiesta de Sofia,2024-02-14,15:00,Salón La Alegría,María García,+34 612345678,maria@example.com
Lucas,2018-05-20,6,Cumpleaños de Lucas,2024-05-20,14:00,Parque Central,Juan López,+34 622345678,juan@example.com
Emma,2020-08-10,4,Party de Emma,2024-08-10,16:00,Casa de Abuela,Ana Martínez,+34 632345678,ana@example.com
Mateo,2017-11-03,7,Gran Fiesta Mateo,2024-11-03,15:30,Salón de Eventos,Carlos García,+34 642345678,carlos@example.com"""
    
    with open('sample_invitations.csv', 'w', encoding='utf-8') as f:
        f.write(sample_data)
    
    print("✅ Archivo de ejemplo creado: sample_invitations.csv")

def main():
    parser = argparse.ArgumentParser(
        description='Crear múltiples invitaciones desde un archivo CSV'
    )
    parser.add_argument('--file', required=False, help='Ruta al archivo CSV')
    parser.add_argument('--token', required=False, help='Token JWT del usuario')
    parser.add_argument('--template-id', type=int, required=False, help='ID del template a usar')
    parser.add_argument('--sample', action='store_true', help='Generar archivo CSV de ejemplo')
    parser.add_argument('--url', default='http://localhost:5000/api', help='URL base de la API')
    
    args = parser.parse_args()
    
    if args.sample:
        generate_sample_csv()
        return
    
    if not args.file:
        print("❌ Se requiere --file o --sample")
        print("\nUso:")
        print("  Generar ejemplo: python bulk_create_invitations.py --sample")
        print("  Crear invitaciones: python bulk_create_invitations.py --file invitados.csv --token TOKEN --template-id 1")
        return
    
    if not args.token:
        print("❌ Se requiere --token (obtén uno con login)")
        return
    
    if not args.template_id:
        print("❌ Se requiere --template-id")
        return
    
    create_invitations_from_csv(args.file, args.token, args.template_id, args.url)

if __name__ == "__main__":
    main()
