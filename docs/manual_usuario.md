# Manual de Usuario - Agente Autónomo de Joy's Farm

## Introducción

Bienvenido al manual de usuario del Agente Autónomo de Joy's Farm. Este sistema ha sido diseñado para ayudarle a monitorear y gestionar su entorno agrícola utilizando sensores Atlas Scientific conectados a través de Mycodo, con capacidades de inteligencia artificial para predicciones y toma de decisiones.

## Requisitos del Sistema

- Raspberry Pi (recomendado) o cualquier servidor Linux
- Docker y Docker Compose instalados
- Conexión a Internet (para la instalación inicial)
- Sensores Atlas Scientific conectados a Mycodo

## Instalación

### Método Automático (Recomendado)

1. Descargue el repositorio:
   ```bash
   git clone https://github.com/joysfarm/joys-agent.git
   cd joys-agent
   ```

2. Ejecute el script de instalación:
   ```bash
   chmod +x deploy_raspberry_pi.sh
   ./deploy_raspberry_pi.sh
   ```

3. Siga las instrucciones en pantalla para completar la configuración.

### Método Manual

1. Actualice su sistema:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. Instale las dependencias:
   ```bash
   sudo apt install docker.io docker-compose git -y
   sudo usermod -aG docker $USER
   sudo reboot
   ```

3. Clone el repositorio:
   ```bash
   git clone https://github.com/joysfarm/joys-agent.git
   cd joys-agent
   ```

4. Configure las variables de entorno:
   ```bash
   cp .env.example .env
   nano .env
   ```

5. Inicie los servicios:
   ```bash
   docker-compose -f docker/docker-compose.yml up -d --build
   ```

## Acceso al Sistema

Una vez instalado, puede acceder al sistema a través de:

- **Panel de Control**: http://[IP-DE-SU-RASPBERRY]:80
- **API**: http://[IP-DE-SU-RASPBERRY]:8000
- **Documentación API**: http://[IP-DE-SU-RASPBERRY]:8000/docs

## Funcionalidades Principales

### 1. Monitoreo de Sensores

El sistema permite visualizar en tiempo real los datos de sus sensores Atlas Scientific, incluyendo:
- pH
- Conductividad Eléctrica (EC)
- Oxígeno Disuelto (DO)
- Temperatura
- ORP (Potencial de Oxidación-Reducción)
- Dióxido de Carbono (CO2)

Para acceder a esta información:
1. Vaya al Panel de Control
2. Seleccione "Sensores" en el menú principal
3. Visualice los datos en tiempo real y gráficos históricos

### 2. Control de Actuadores

Puede controlar diversos dispositivos como bombas, luces y ventiladores:
1. Vaya a la sección "Actuadores" en el Panel de Control
2. Seleccione el dispositivo que desea controlar
3. Active/desactive o ajuste los parámetros según sea necesario

### 3. Predicciones y Alertas

El sistema utiliza inteligencia artificial para:
- Predecir tendencias futuras de variables ambientales
- Clasificar estados (normal, alerta, crítico)
- Generar recomendaciones de acción

Para acceder a las predicciones:
1. Vaya a la sección "Predicciones" en el Panel de Control
2. Seleccione el tipo de predicción y horizonte temporal
3. Visualice los resultados con intervalos de confianza

### 4. Configuración del Sistema

Para configurar el sistema:
1. Vaya a "Configuración" en el Panel de Control
2. Ajuste los parámetros de conexión con Mycodo
3. Configure umbrales de alerta para cada tipo de sensor
4. Personalice las acciones automáticas

## Solución de Problemas

### El sistema no se inicia correctamente

Verifique los logs de Docker:
```bash
docker-compose -f docker/docker-compose.yml logs
```

### No se detectan los sensores

1. Verifique que Mycodo está correctamente configurado
2. Compruebe la conexión entre Mycodo y los sensores Atlas Scientific
3. Verifique las credenciales en el archivo .env

### Problemas de rendimiento

Si experimenta lentitud:
1. Reinicie los servicios: `docker-compose -f docker/docker-compose.yml restart`
2. Verifique el uso de recursos: `htop`
3. Considere aumentar la memoria asignada a Docker

## Mantenimiento

### Actualización del Sistema

Para actualizar a la última versión:
```bash
cd joys-agent
git pull
docker-compose -f docker/docker-compose.yml up -d --build
```

### Copia de Seguridad

Para realizar una copia de seguridad de los datos:
```bash
docker-compose -f docker/docker-compose.yml exec db pg_dump -U joysfarm joysfarm_db > backup.sql
```

## Soporte

Si necesita ayuda adicional:
- Consulte la documentación completa en la carpeta `/docs`
- Visite el repositorio en GitHub para reportar problemas
- Contacte al equipo de soporte en support@joysfarm.com
