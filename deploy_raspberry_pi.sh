#!/bin/bash

# Script para desplegar el agente autónomo de Joy's Farm en Raspberry Pi

echo "Iniciando despliegue del agente autónomo de Joy's Farm..."

# Verificar que estamos en Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo &> /dev/null; then
    echo "⚠️ Advertencia: Este script está optimizado para Raspberry Pi. Puede continuar, pero podría haber problemas de compatibilidad."
    read -p "¿Desea continuar? (s/n): " respuesta
    if [[ "$respuesta" != "s" ]]; then
        echo "Despliegue cancelado."
        exit 0
    fi
fi

# Actualizar el sistema
echo "Actualizando el sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
echo "Instalando dependencias..."
sudo apt install -y docker.io docker-compose git

# Añadir usuario al grupo docker
echo "Configurando permisos de Docker..."
sudo usermod -aG docker $USER
echo "⚠️ Nota: Es posible que necesite reiniciar para que los cambios de permisos surtan efecto."

# Clonar el repositorio si no existe
if [ ! -d "joys-agent" ]; then
    echo "Clonando el repositorio..."
    git clone https://github.com/joysfarm/joys-agent.git
    cd joys-agent
else
    echo "El directorio joys-agent ya existe, actualizando..."
    cd joys-agent
    git pull
fi

# Crear archivo .env a partir del ejemplo si no existe
if [ ! -f .env ]; then
    echo "Creando archivo .env a partir de .env.example..."
    cp .env.example .env
    echo "Por favor, edite el archivo .env con sus configuraciones específicas."
    nano .env
fi

# Construir y ejecutar los contenedores
echo "Construyendo y ejecutando los contenedores..."
docker-compose -f docker/docker-compose.yml up -d --build

# Verificar que los servicios están funcionando
echo "Verificando que los servicios están funcionando..."
sleep 10

# Verificar el backend
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo "✅ Backend funcionando correctamente"
else
    echo "❌ Error: El backend no está respondiendo correctamente"
fi

# Verificar el frontend
if curl -s http://localhost:80 | grep -q "Joy's Farm"; then
    echo "✅ Frontend funcionando correctamente"
else
    echo "❌ Error: El frontend no está respondiendo correctamente"
fi

echo "Despliegue completado. El agente autónomo de Joy's Farm está disponible en http://localhost"
echo "Para acceder desde otros dispositivos en la red, use la dirección IP de esta Raspberry Pi."
echo "Para ver los logs, ejecute: docker-compose -f docker/docker-compose.yml logs -f"
