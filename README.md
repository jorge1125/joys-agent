# Joy's Farm Agent

Sistema de agente autónomo para Joy's Farm que permite visualizar datos agrícolas, hacer predicciones y tomar decisiones automáticas, integrando inteligencia artificial y conectividad con sistemas como Mycodo.

## Características

- Visualización en tiempo real de sensores Atlas Scientific
- Predicciones basadas en IA para variables agrícolas
- Control de actuadores desde panel web
- Sistema de alertas y recomendaciones
- Optimizado para Raspberry Pi

## Tecnologías

- **Backend**: FastAPI
- **Frontend**: React.js
- **IA**: Prophet/NeuralProphet + Scikit-learn
- **BD**: PostgreSQL + TimescaleDB
- **Contenerización**: Docker
- **Despliegue**: Render / Railway / VPS
- **Monitoreo**: Prometheus + Grafana

## Estructura del Proyecto

```
joys-agent/
├── backend/           # API y lógica de negocio
│   ├── api/           # Endpoints de la API
│   ├── models/        # Modelos de datos
│   ├── database/      # Configuración de base de datos
│   ├── utils/         # Utilidades
│   └── tests/         # Pruebas
├── frontend/          # Interfaz de usuario
│   ├── src/           # Código fuente
│   │   ├── components/# Componentes React
│   │   ├── pages/     # Páginas de la aplicación
│   │   ├── assets/    # Recursos estáticos
│   │   └── utils/     # Utilidades
│   └── public/        # Archivos públicos
├── docker/            # Configuración de Docker
│   ├── backend/       # Configuración específica del backend
│   └── frontend/      # Configuración específica del frontend
└── .env.example       # Ejemplo de variables de entorno
```

## Requisitos

- Docker y Docker Compose
- Raspberry Pi (recomendado) o cualquier servidor Linux
- Sensores Atlas Scientific conectados a Mycodo

## Instalación en Raspberry Pi

```bash
# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install docker.io docker-compose git -y
sudo usermod -aG docker $USER
sudo reboot

# Clonar el repositorio
git clone https://github.com/joysfarm/joys-agent.git
cd joys-agent

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Construir y ejecutar
docker-compose -f docker/docker-compose.yml up -d --build
```

## Desarrollo

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm start
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios importantes antes de enviar un pull request.

## Licencia

[MIT](LICENSE)
