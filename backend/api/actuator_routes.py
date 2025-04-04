from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

# Crear el router para los actuadores
router = APIRouter(
    prefix="/actuators",
    tags=["actuators"],
    responses={404: {"description": "Actuador no encontrado"}},
)

# Modelos Pydantic para los actuadores
class ActuatorBase(BaseModel):
    name: str
    type: str  # "pump", "light", "fan", "heater", etc.
    location: str
    description: Optional[str] = None

class ActuatorState(BaseModel):
    actuator_id: int
    state: bool  # True = encendido, False = apagado
    value: Optional[float] = None  # Para actuadores con valores variables (ej. intensidad)
    timestamp: datetime = datetime.now()

class ActuatorCreate(ActuatorBase):
    pass

class Actuator(ActuatorBase):
    id: int
    created_at: datetime
    is_active: bool
    current_state: bool
    last_activated: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# Datos de ejemplo para desarrollo
SAMPLE_ACTUATORS = [
    {
        "id": 1,
        "name": "Bomba de Riego Invernadero 1",
        "type": "pump",
        "location": "Invernadero 1",
        "description": "Bomba principal del sistema de riego del invernadero 1",
        "created_at": datetime.now(),
        "is_active": True,
        "current_state": False,
        "last_activated": datetime.now()
    },
    {
        "id": 2,
        "name": "Luces LED Invernadero 1",
        "type": "light",
        "location": "Invernadero 1",
        "description": "Sistema de iluminación LED del invernadero 1",
        "created_at": datetime.now(),
        "is_active": True,
        "current_state": True,
        "last_activated": datetime.now()
    },
    {
        "id": 3,
        "name": "Ventilador Principal",
        "type": "fan",
        "location": "Invernadero 1",
        "description": "Ventilador para control de temperatura del invernadero 1",
        "created_at": datetime.now(),
        "is_active": True,
        "current_state": False,
        "last_activated": datetime.now()
    }
]

# Rutas para los actuadores
@router.get("/", response_model=List[Actuator])
async def get_all_actuators():
    """
    Obtiene todos los actuadores registrados en el sistema.
    """
    return SAMPLE_ACTUATORS

@router.get("/{actuator_id}", response_model=Actuator)
async def get_actuator(actuator_id: int):
    """
    Obtiene un actuador específico por su ID.
    """
    for actuator in SAMPLE_ACTUATORS:
        if actuator["id"] == actuator_id:
            return actuator
    raise HTTPException(status_code=404, detail="Actuador no encontrado")

@router.post("/", response_model=Actuator, status_code=status.HTTP_201_CREATED)
async def create_actuator(actuator: ActuatorCreate):
    """
    Crea un nuevo actuador en el sistema.
    """
    # En una implementación real, esto se guardaría en la base de datos
    new_id = len(SAMPLE_ACTUATORS) + 1
    new_actuator = {
        "id": new_id,
        "name": actuator.name,
        "type": actuator.type,
        "location": actuator.location,
        "description": actuator.description,
        "created_at": datetime.now(),
        "is_active": True,
        "current_state": False,
        "last_activated": None
    }
    SAMPLE_ACTUATORS.append(new_actuator)
    return new_actuator

@router.post("/{actuator_id}/control", response_model=ActuatorState)
async def control_actuator(actuator_id: int, state: ActuatorState):
    """
    Controla el estado de un actuador específico.
    """
    # Verificar que el actuador existe
    actuator_exists = False
    for actuator in SAMPLE_ACTUATORS:
        if actuator["id"] == actuator_id:
            actuator_exists = True
            # Actualizar el estado del actuador
            actuator["current_state"] = state.state
            if state.state:
                actuator["last_activated"] = datetime.now()
            break
    
    if not actuator_exists:
        raise HTTPException(status_code=404, detail="Actuador no encontrado")
    
    # En una implementación real, esto enviaría comandos al hardware
    # y se guardaría en la base de datos
    
    # Simular conexión con Mycodo o sistema de control
    # En este punto se enviarían los comandos al hardware real
    
    return state

@router.get("/{actuator_id}/history", response_model=List[ActuatorState])
async def get_actuator_history(actuator_id: int, limit: int = 10):
    """
    Obtiene el historial de estados de un actuador específico.
    """
    # Verificar que el actuador existe
    actuator_exists = False
    for actuator in SAMPLE_ACTUATORS:
        if actuator["id"] == actuator_id:
            actuator_exists = True
            break
    
    if not actuator_exists:
        raise HTTPException(status_code=404, detail="Actuador no encontrado")
    
    # En una implementación real, esto se obtendría de la base de datos
    # Generamos datos de ejemplo para desarrollo
    sample_history = []
    for i in range(limit):
        sample_history.append(
            ActuatorState(
                actuator_id=actuator_id,
                state=i % 2 == 0,  # Alternar entre True y False
                value=50.0 if i % 3 == 0 else None,  # Algunos valores tienen intensidad
                timestamp=datetime.now()
            )
        )
    
    return sample_history
