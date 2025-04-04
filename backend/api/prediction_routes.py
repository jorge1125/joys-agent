from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

# Crear el router para las predicciones
router = APIRouter(
    prefix="/predictions",
    tags=["predictions"],
    responses={404: {"description": "Predicción no encontrada"}},
)

# Modelos Pydantic para las predicciones
class PredictionBase(BaseModel):
    sensor_id: int
    prediction_type: str  # "temperature", "humidity", "ph", etc.
    time_horizon: str  # "1h", "6h", "24h", "7d"
    
class PredictionResult(BaseModel):
    sensor_id: int
    prediction_type: str
    time_horizon: str
    predicted_values: List[Dict[str, Any]]
    confidence_interval: Optional[Dict[str, List[float]]] = None
    created_at: datetime = datetime.now()
    status: str = "success"  # success, failed, processing
    
class PredictionRequest(PredictionBase):
    pass

# Datos de ejemplo para desarrollo
SAMPLE_PREDICTIONS = [
    {
        "id": 1,
        "sensor_id": 1,
        "prediction_type": "temperature",
        "time_horizon": "24h",
        "predicted_values": [
            {"timestamp": datetime.now(), "value": 25.2},
            {"timestamp": datetime.now(), "value": 26.1},
            {"timestamp": datetime.now(), "value": 27.3}
        ],
        "confidence_interval": {
            "lower": [24.5, 25.3, 26.1],
            "upper": [26.0, 27.0, 28.5]
        },
        "created_at": datetime.now(),
        "status": "success"
    }
]

# Rutas para las predicciones
@router.post("/", response_model=PredictionResult)
async def create_prediction(prediction_request: PredictionRequest):
    """
    Crea una nueva predicción basada en datos históricos de un sensor.
    """
    # En una implementación real, esto invocaría al módulo de IA para generar predicciones
    # Aquí generamos datos de ejemplo para desarrollo
    
    # Verificar que el tipo de predicción es válido
    valid_types = ["temperature", "humidity", "ph", "soil_moisture", "light"]
    if prediction_request.prediction_type not in valid_types:
        raise HTTPException(
            status_code=400, 
            detail=f"Tipo de predicción no válido. Debe ser uno de: {', '.join(valid_types)}"
        )
    
    # Verificar que el horizonte temporal es válido
    valid_horizons = ["1h", "6h", "24h", "7d"]
    if prediction_request.time_horizon not in valid_horizons:
        raise HTTPException(
            status_code=400, 
            detail=f"Horizonte temporal no válido. Debe ser uno de: {', '.join(valid_horizons)}"
        )
    
    # Generar predicción de ejemplo
    predicted_values = []
    lower_bounds = []
    upper_bounds = []
    
    # Generar valores según el tipo de predicción
    base_value = 0
    if prediction_request.prediction_type == "temperature":
        base_value = 25.0
    elif prediction_request.prediction_type == "humidity":
        base_value = 65.0
    elif prediction_request.prediction_type == "ph":
        base_value = 6.8
    elif prediction_request.prediction_type == "soil_moisture":
        base_value = 70.0
    elif prediction_request.prediction_type == "light":
        base_value = 5000.0
    
    # Generar valores de predicción
    num_points = 24  # Por defecto, 24 puntos
    if prediction_request.time_horizon == "1h":
        num_points = 12
    elif prediction_request.time_horizon == "6h":
        num_points = 18
    elif prediction_request.time_horizon == "7d":
        num_points = 28
    
    for i in range(num_points):
        # Simular variación en los valores
        variation = (i * 0.2) - (i * 0.1 if i % 2 == 0 else 0)
        value = base_value + variation
        
        # Añadir a las listas
        predicted_values.append({
            "timestamp": datetime.now(),
            "value": round(value, 2)
        })
        lower_bounds.append(round(value - 0.5, 2))
        upper_bounds.append(round(value + 0.5, 2))
    
    # Crear objeto de predicción
    prediction_result = PredictionResult(
        sensor_id=prediction_request.sensor_id,
        prediction_type=prediction_request.prediction_type,
        time_horizon=prediction_request.time_horizon,
        predicted_values=predicted_values,
        confidence_interval={
            "lower": lower_bounds,
            "upper": upper_bounds
        },
        created_at=datetime.now(),
        status="success"
    )
    
    return prediction_result

@router.get("/{sensor_id}", response_model=List[PredictionResult])
async def get_predictions_for_sensor(sensor_id: int):
    """
    Obtiene todas las predicciones para un sensor específico.
    """
    # En una implementación real, esto se obtendría de la base de datos
    sensor_predictions = [p for p in SAMPLE_PREDICTIONS if p["sensor_id"] == sensor_id]
    
    if not sensor_predictions:
        # Si no hay predicciones, devolver lista vacía
        return []
    
    return sensor_predictions

@router.get("/{sensor_id}/{prediction_type}", response_model=PredictionResult)
async def get_latest_prediction(sensor_id: int, prediction_type: str):
    """
    Obtiene la predicción más reciente de un tipo específico para un sensor.
    """
    # En una implementación real, esto se obtendría de la base de datos
    matching_predictions = [
        p for p in SAMPLE_PREDICTIONS 
        if p["sensor_id"] == sensor_id and p["prediction_type"] == prediction_type
    ]
    
    if not matching_predictions:
        raise HTTPException(
            status_code=404, 
            detail=f"No se encontraron predicciones de tipo {prediction_type} para el sensor {sensor_id}"
        )
    
    # Ordenar por fecha de creación y devolver la más reciente
    latest_prediction = sorted(matching_predictions, key=lambda p: p["created_at"], reverse=True)[0]
    
    return latest_prediction
