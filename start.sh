#!/bin/bash

# Birthday Invitations App - Setup & Run Script
# Este script configura y ejecuta la aplicación

set -e  # Salir si hay error

echo "╔════════════════════════════════════════════════╗"
echo "║   Birthday Invitations App - Setup Script     ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Paso 1: Verificar Python
echo -e "${BLUE}📌 Paso 1: Verificando Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python3 no encontrado${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✅ $PYTHON_VERSION encontrado${NC}"
echo ""

# Paso 2: Crear entorno virtual
echo -e "${BLUE}📌 Paso 2: Configurando entorno virtual...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Entorno virtual creado${NC}"
else
    echo -e "${GREEN}✅ Entorno virtual ya existe${NC}"
fi

# Activar entorno virtual
source venv/bin/activate
echo ""

# Paso 3: Instalar dependencias
echo -e "${BLUE}📌 Paso 3: Instalando dependencias...${NC}"
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✅ Dependencias instaladas${NC}"
echo ""

# Paso 4: Verificar archivo .env
echo -e "${BLUE}📌 Paso 4: Verificando configuración...${NC}"
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${YELLOW}⚠️  Archivo .env creado desde .env.example${NC}"
        echo -e "${YELLOW}   ⚠️  IMPORTANTE: Edita .env y cambia SECRET_KEY y JWT_SECRET_KEY${NC}"
    fi
else
    echo -e "${GREEN}✅ Archivo .env configurado${NC}"
fi
echo ""

# Paso 5: Crear carpeta uploads si no existe
if [ ! -d "uploads" ]; then
    mkdir -p uploads
    echo -e "${GREEN}✅ Carpeta 'uploads' creada${NC}"
fi
echo ""

# Paso 6: Ejecutar la aplicación
echo -e "${BLUE}📌 Paso 5: Iniciando aplicación...${NC}"
echo -e "${GREEN}✅ La aplicación está iniciando...${NC}"
echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║            SERVIDOR INICIADO                  ║"
echo "╠════════════════════════════════════════════════╣"
echo "║ URL:     http://localhost:5000                ║"
echo "║ Docs:    http://localhost:5000/api/           ║"
echo "║                                              ║"
echo "║ Para detener: Ctrl+C                          ║"
echo "║ Para probar:  python test_api.py              ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Ejecutar la aplicación
python run.py
