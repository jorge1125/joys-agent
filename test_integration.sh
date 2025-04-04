#!/bin/bash

# Script para probar la integración de componentes del agente autónomo de Joy's Farm

echo "Iniciando pruebas de integración..."

# Verificar que Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "Error: Docker no está instalado. Por favor, instale Docker antes de continuar."
    exit 1
fi

# Verificar que Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose no está instalado. Por favor, instale Docker Compose antes de continuar."
    exit 1
fi

# Crear archivo .env a partir del ejemplo si no existe
if [ ! -f .env ]; then
    echo "Creando archivo .env a partir de .env.example..."
    cp .env.example .env
    echo "Por favor, revise y ajuste las variables en el archivo .env según sea necesario."
fi

# Construir las imágenes de Docker
echo "Construyendo imágenes de Docker..."
docker-compose -f docker/docker-compose.yml build

# Iniciar los servicios
echo "Iniciando servicios..."
docker-compose -f docker/docker-compose.yml up -d

# Esperar a que los servicios estén disponibles
echo "Esperando a que los servicios estén disponibles..."
sleep 10

# Verificar que el backend está funcionando
echo "Verificando el backend..."
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo "✅ Backend funcionando correctamente"
else
    echo "❌ Error: El backend no está respondiendo correctamente"
fi

# Verificar que el frontend está funcionando
echo "Verificando el frontend..."
if curl -s http://localhost:80 | grep -q "Joy's Farm"; then
    echo "✅ Frontend funcionando correctamente"
else
    echo "❌ Error: El frontend no está respondiendo correctamente"
fi

# Realizar pruebas de integración
echo "Realizando pruebas de integración..."

# Prueba 1: Verificar que se pueden obtener los sensores
echo "Prueba 1: Obteniendo lista de sensores..."
if curl -s http://localhost:8000/sensors/ | grep -q "id"; then
    echo "✅ Prueba 1 exitosa: Se pueden obtener los sensores"
else
    echo "❌ Prueba 1 fallida: No se pueden obtener los sensores"
fi

# Prueba 2: Verificar que se pueden obtener los actuadores
echo "Prueba 2: Obteniendo lista de actuadores..."
if curl -s http://localhost:8000/actuators/ | grep -q "id"; then
    echo "✅ Prueba 2 exitosa: Se pueden obtener los actuadores"
else
    echo "❌ Prueba 2 fallida: No se pueden obtener los actuadores"
fi

# Prueba 3: Verificar la conexión con Mycodo
echo "Prueba 3: Verificando conexión con Mycodo..."
if curl -s http://localhost:8000/mycodo/status | grep -q "status"; then
    echo "✅ Prueba 3 exitosa: Se puede verificar el estado de Mycodo"
else
    echo "❌ Prueba 3 fallida: No se puede verificar el estado de Mycodo"
fi

# Detener los servicios
echo "Deteniendo servicios..."
docker-compose -f docker/docker-compose.yml down

echo "Pruebas de integración completadas."
