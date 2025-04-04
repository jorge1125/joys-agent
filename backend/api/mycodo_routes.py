from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

# Crear el router para la integración con Mycodo
router = APIRouter(
    prefix="/mycodo",
    tags=["mycodo"],
    responses={404: {"description": "Recurso no encontrado"}},
)

# Modelos Pydantic para los sensores Atlas Scientific
class AtlasSensorType(BaseModel):
    name: str
    code: str
    unit: str
    description: str

# Definición de los tipos de sensores Atlas Scientific
ATLAS_SENSOR_TYPES = [
    {
        "name": "pH",
        "code": "ph",
        "unit": "pH",
        "description": "Sensor de pH Atlas Scientific"
    },
    {
        "name": "Conductividad Eléctrica",
        "code": "ec",
        "unit": "μS/cm",
        "description": "Sensor de conductividad eléctrica Atlas Scientific"
    },
    {
        "name": "Oxígeno Disuelto",
        "code": "do",
        "unit": "mg/L",
        "description": "Sensor de oxígeno disuelto Atlas Scientific"
    },
    {
        "name": "Temperatura",
        "code": "rtd",
        "unit": "°C",
        "description": "Sensor de temperatura RTD Atlas Scientific"
    },
    {
        "name": "ORP (Potencial de Oxidación-Reducción)",
        "code": "orp",
        "unit": "mV",
        "description": "Sensor ORP Atlas Scientific"
    },
    {
        "name": "Dióxido de Carbono",
        "code": "co2",
        "unit": "ppm",
        "description": "Sensor de CO2 Atlas Scientific"
    }
]

class MycodoSensorReading(BaseModel):
    sensor_id: str
    sensor_type: str
    value: float
    timestamp: datetime = datetime.now()
    unit: str
    location: Optional[str] = None

class MycodoConfig(BaseModel):
    host: str
    port: int
    api_key: Optional[str] = None
    use_ssl: bool = False

# Rutas para la integración con Mycodo
@router.get("/sensor-types", response_model=List[AtlasSensorType])
async def get_atlas_sensor_types():
    """
    Obtiene todos los tipos de sensores Atlas Scientific soportados.
    """
    return ATLAS_SENSOR_TYPES

@router.post("/readings", status_code=status.HTTP_201_CREATED)
async def receive_mycodo_readings(readings: List[MycodoSensorReading]):
    """
    Recibe lecturas de sensores desde Mycodo.
    """
    # En una implementación real, esto guardaría las lecturas en la base de datos
    # y posiblemente activaría análisis o alertas
    
    # Verificar que los tipos de sensores son válidos
    valid_sensor_types = [sensor["code"] for sensor in ATLAS_SENSOR_TYPES]
    for reading in readings:
        if reading.sensor_type not in valid_sensor_types:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de sensor no válido: {reading.sensor_type}. Debe ser uno de: {', '.join(valid_sensor_types)}"
            )
    
    # Procesar las lecturas (en una implementación real)
    processed_readings = []
    for reading in readings:
        # Aquí se procesarían las lecturas según sea necesario
        processed_readings.append({
            "sensor_id": reading.sensor_id,
            "sensor_type": reading.sensor_type,
            "value": reading.value,
            "timestamp": reading.timestamp,
            "processed": True
        })
    
    return {
        "status": "success",
        "message": f"Recibidas {len(readings)} lecturas de sensores",
        "processed": len(processed_readings)
    }

@router.post("/config", status_code=status.HTTP_200_OK)
async def set_mycodo_config(config: MycodoConfig):
    """
    Configura la conexión con Mycodo.
    """
    # En una implementación real, esto guardaría la configuración en la base de datos
    # o en un archivo de configuración
    
    return {
        "status": "success",
        "message": f"Configuración de Mycodo actualizada: {config.host}:{config.port}",
        "config": {
            "host": config.host,
            "port": config.port,
            "use_ssl": config.use_ssl
        }
    }

@router.get("/status", status_code=status.HTTP_200_OK)
async def check_mycodo_connection():
    """
    Verifica la conexión con Mycodo.
    """
    # En una implementación real, esto intentaría conectarse a Mycodo
    # y verificaría el estado de la conexión
    
    # Simulamos una conexión exitosa para desarrollo
    return {
        "status": "connected",
        "version": "8.13.5",  # Versión de ejemplo de Mycodo
        "sensors_count": 6,
        "controllers_count": 3,
        "last_sync": datetime.now()
    }

class MycodoCommand(BaseModel):
    controller_id: str
    command: str
    parameters: Optional[Dict[str, Any]] = None

@router.post("/command", status_code=status.HTTP_200_OK)
async def send_mycodo_command(command: MycodoCommand):
    """
    Envía un comando a un controlador en Mycodo.
    """
    # En una implementación real, esto enviaría comandos a Mycodo
    # para controlar actuadores o cambiar configuraciones
    
    # Verificar que el comando es válido
    valid_commands = ["activate", "deactivate", "set_duty_cycle", "set_value", "restart"]
    if command.command not in valid_commands:
        raise HTTPException(
            status_code=400,
            detail=f"Comando no válido: {command.command}. Debe ser uno de: {', '.join(valid_commands)}"
        )
    
    # Simular respuesta para desarrollo
    return {
        "status": "success",
        "message": f"Comando '{command.command}' enviado al controlador {command.controller_id}",
        "executed_at": datetime.now()
    }
