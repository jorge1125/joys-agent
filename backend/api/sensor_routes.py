from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# Crear el router para los sensores
router = APIRouter(
    prefix="/sensors",
    tags=["sensors"],
    responses={404: {"description": "Sensor no encontrado"}},
)

# Modelos Pydantic para los sensores
class SensorBase(BaseModel):
    name: str
    type: str
    location: str
    unit: str
    description: Optional[str] = None

class SensorReading(BaseModel):
    sensor_id: int
    value: float
    timestamp: datetime = datetime.now()
    status: str = "normal"  # normal, warning, critical

class SensorCreate(SensorBase):
    pass

class Sensor(SensorBase):
    id: int
    created_at: datetime
    last_reading: Optional[float] = None
    last_reading_time: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# Datos de ejemplo para desarrollo
SAMPLE_SENSORS = [
    {
        "id": 1,
        "name": "Temperatura Invernadero 1",
        "type": "temperature",
        "location": "Invernadero 1",
        "unit": "°C",
        "description": "Sensor de temperatura principal del invernadero 1",
        "created_at": datetime.now(),
        "last_reading": 24.5,
        "last_reading_time": datetime.now()
    },
    {
        "id": 2,
        "name": "Humedad Suelo Invernadero 1",
        "type": "soil_moisture",
        "location": "Invernadero 1",
        "unit": "%",
        "description": "Sensor de humedad del suelo del invernadero 1",
        "created_at": datetime.now(),
        "last_reading": 65.3,
        "last_reading_time": datetime.now()
    },
    {
        "id": 3,
        "name": "pH Tanque Acuaponia",
        "type": "ph",
        "location": "Sistema Acuaponia",
        "unit": "pH",
        "description": "Sensor de pH del tanque principal de acuaponia",
        "created_at": datetime.now(),
        "last_reading": 6.8,
        "last_reading_time": datetime.now()
    }
]

# Rutas para los sensores
@router.get("/", response_model=List[Sensor])
async def get_all_sensors():
    """
    Obtiene todos los sensores registrados en el sistema.
    """
    return SAMPLE_SENSORS

@router.get("/{sensor_id}", response_model=Sensor)
async def get_sensor(sensor_id: int):
    """
    Obtiene un sensor específico por su ID.
    """
    for sensor in SAMPLE_SENSORS:
        if sensor["id"] == sensor_id:
            return sensor
    raise HTTPException(status_code=404, detail="Sensor no encontrado")

@router.post("/", response_model=Sensor, status_code=status.HTTP_201_CREATED)
async def create_sensor(sensor: SensorCreate):
    """
    Crea un nuevo sensor en el sistema.
    """
    # En una implementación real, esto se guardaría en la base de datos
    new_id = len(SAMPLE_SENSORS) + 1
    new_sensor = {
        "id": new_id,
        "name": sensor.name,
        "type": sensor.type,
        "location": sensor.location,
        "unit": sensor.unit,
        "description": sensor.description,
        "created_at": datetime.now(),
        "last_reading": None,
        "last_reading_time": None
    }
    SAMPLE_SENSORS.append(new_sensor)
    return new_sensor

@router.post("/{sensor_id}/readings", response_model=SensorReading)
async def add_sensor_reading(sensor_id: int, reading: SensorReading):
    """
    Registra una nueva lectura para un sensor específico.
    """
    # Verificar que el sensor existe
    sensor_exists = False
    for sensor in SAMPLE_SENSORS:
        if sensor["id"] == sensor_id:
            sensor_exists = True
            # Actualizar la última lectura del sensor
            sensor["last_reading"] = reading.value
            sensor["last_reading_time"] = reading.timestamp
            break
    
    if not sensor_exists:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    
    # En una implementación real, esto se guardaría en la base de datos
    return reading

@router.get("/{sensor_id}/readings", response_model=List[SensorReading])
async def get_sensor_readings(sensor_id: int, limit: int = 10):
    """
    Obtiene las últimas lecturas de un sensor específico.
    """
    # Verificar que el sensor existe
    sensor_exists = False
    for sensor in SAMPLE_SENSORS:
        if sensor["id"] == sensor_id:
            sensor_exists = True
            break
    
    if not sensor_exists:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    
    # En una implementación real, esto se obtendría de la base de datos
    # Generamos datos de ejemplo para desarrollo
    sample_readings = []
    for i in range(limit):
        sample_readings.append(
            SensorReading(
                sensor_id=sensor_id,
                value=20 + (i * 0.5),  # Valores de ejemplo
                timestamp=datetime.now(),
                status="normal"
            )
        )
    
    return sample_readings
