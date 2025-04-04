from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime, timedelta

# Crear el router para el registro histórico
router = APIRouter(
    prefix="/history",
    tags=["history"],
    responses={404: {"description": "Datos históricos no encontrados"}},
)

# Modelos Pydantic para el registro histórico
class HistoricalDataPoint(BaseModel):
    sensor_id: int
    sensor_type: str
    value: float
    timestamp: datetime
    status: str = "normal"  # normal, warning, critical
    unit: str

class HistoricalDataQuery(BaseModel):
    sensor_ids: List[int]
    start_date: datetime
    end_date: datetime
    interval: Optional[str] = "raw"  # raw, hourly, daily, weekly
    
class HistoricalDataSummary(BaseModel):
    sensor_id: int
    sensor_type: str
    unit: str
    min_value: float
    max_value: float
    avg_value: float
    count: int
    start_date: datetime
    end_date: datetime

# Rutas para el registro histórico
@router.get("/sensors/{sensor_id}", response_model=List[HistoricalDataPoint])
async def get_sensor_history(
    sensor_id: int, 
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100
):
    """
    Obtiene el historial de lecturas de un sensor específico.
    """
    # Si no se especifican fechas, usar últimas 24 horas
    if not end_date:
        end_date = datetime.now()
    if not start_date:
        start_date = end_date - timedelta(days=1)
    
    # En una implementación real, esto se obtendría de la base de datos
    # Generamos datos de ejemplo para desarrollo
    sample_history = []
    
    # Determinar tipo de sensor y unidad (en una implementación real se obtendría de la BD)
    sensor_type = "temperature"
    unit = "°C"
    if sensor_id == 2:
        sensor_type = "soil_moisture"
        unit = "%"
    elif sensor_id == 3:
        sensor_type = "ph"
        unit = "pH"
    
    # Generar datos de ejemplo
    time_step = (end_date - start_date) / min(limit, 100)
    current_time = start_date
    
    base_value = 0
    if sensor_type == "temperature":
        base_value = 25.0
    elif sensor_type == "soil_moisture":
        base_value = 65.0
    elif sensor_type == "ph":
        base_value = 6.8
    
    for i in range(min(limit, 100)):
        # Simular variación en los valores
        variation = (i * 0.2) - (i * 0.1 if i % 2 == 0 else 0)
        value = base_value + variation
        
        # Determinar estado basado en el valor
        status = "normal"
        if sensor_type == "temperature":
            if value > 30:
                status = "warning"
            if value > 35:
                status = "critical"
        elif sensor_type == "soil_moisture":
            if value < 40:
                status = "warning"
            if value < 20:
                status = "critical"
        elif sensor_type == "ph":
            if value < 6.0 or value > 7.5:
                status = "warning"
            if value < 5.5 or value > 8.0:
                status = "critical"
        
        sample_history.append(
            HistoricalDataPoint(
                sensor_id=sensor_id,
                sensor_type=sensor_type,
                value=round(value, 2),
                timestamp=current_time,
                status=status,
                unit=unit
            )
        )
        current_time += time_step
    
    return sample_history

@router.post("/query", response_model=Dict[int, List[HistoricalDataPoint]])
async def query_historical_data(query: HistoricalDataQuery):
    """
    Consulta datos históricos para múltiples sensores en un rango de fechas.
    """
    # En una implementación real, esto se obtendría de la base de datos
    # Generamos datos de ejemplo para desarrollo
    result = {}
    
    for sensor_id in query.sensor_ids:
        # Determinar tipo de sensor y unidad (en una implementación real se obtendría de la BD)
        sensor_type = "temperature"
        unit = "°C"
        if sensor_id == 2:
            sensor_type = "soil_moisture"
            unit = "%"
        elif sensor_id == 3:
            sensor_type = "ph"
            unit = "pH"
        
        # Generar datos de ejemplo
        sample_history = []
        
        # Ajustar intervalo según lo solicitado
        if query.interval == "hourly":
            time_step = timedelta(hours=1)
        elif query.interval == "daily":
            time_step = timedelta(days=1)
        elif query.interval == "weekly":
            time_step = timedelta(weeks=1)
        else:  # raw
            time_step = timedelta(minutes=10)
        
        current_time = query.start_date
        
        base_value = 0
        if sensor_type == "temperature":
            base_value = 25.0
        elif sensor_type == "soil_moisture":
            base_value = 65.0
        elif sensor_type == "ph":
            base_value = 6.8
        
        while current_time <= query.end_date:
            # Simular variación en los valores
            hours = current_time.hour
            day_factor = (current_time.day % 5) * 0.2
            
            # Crear variación diurna para temperatura
            if sensor_type == "temperature":
                hour_variation = 3 * (1 - abs(hours - 12) / 12)  # Mayor al mediodía
                value = base_value + hour_variation + day_factor
            else:
                value = base_value + day_factor
            
            # Determinar estado basado en el valor
            status = "normal"
            if sensor_type == "temperature":
                if value > 30:
                    status = "warning"
                if value > 35:
                    status = "critical"
            elif sensor_type == "soil_moisture":
                if value < 40:
                    status = "warning"
                if value < 20:
                    status = "critical"
            elif sensor_type == "ph":
                if value < 6.0 or value > 7.5:
                    status = "warning"
                if value < 5.5 or value > 8.0:
                    status = "critical"
            
            sample_history.append(
                HistoricalDataPoint(
                    sensor_id=sensor_id,
                    sensor_type=sensor_type,
                    value=round(value, 2),
                    timestamp=current_time,
                    status=status,
                    unit=unit
                )
            )
            current_time += time_step
        
        result[sensor_id] = sample_history
    
    return result

@router.get("/summary", response_model=List[HistoricalDataSummary])
async def get_historical_summary(
    sensor_ids: List[int],
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Obtiene un resumen estadístico de los datos históricos para los sensores especificados.
    """
    # Si no se especifican fechas, usar últimos 7 días
    if not end_date:
        end_date = datetime.now()
    if not start_date:
        start_date = end_date - timedelta(days=7)
    
    # En una implementación real, esto se calcularía a partir de los datos en la base de datos
    # Generamos datos de ejemplo para desarrollo
    summaries = []
    
    for sensor_id in sensor_ids:
        # Determinar tipo de sensor y unidad (en una implementación real se obtendría de la BD)
        sensor_type = "temperature"
        unit = "°C"
        if sensor_id == 2:
            sensor_type = "soil_moisture"
            unit = "%"
        elif sensor_id == 3:
            sensor_type = "ph"
            unit = "pH"
        
        # Generar resumen de ejemplo
        base_value = 0
        if sensor_type == "temperature":
            base_value = 25.0
            min_value = base_value - 5.0
            max_value = base_value + 8.0
            avg_value = base_value + 1.5
        elif sensor_type == "soil_moisture":
            base_value = 65.0
            min_value = base_value - 15.0
            max_value = base_value + 10.0
            avg_value = base_value - 2.0
        elif sensor_type == "ph":
            base_value = 6.8
            min_value = base_value - 0.5
            max_value = base_value + 0.3
            avg_value = base_value - 0.1
        
        summaries.append(
            HistoricalDataSummary(
                sensor_id=sensor_id,
                sensor_type=sensor_type,
                unit=unit,
                min_value=round(min_value, 2),
                max_value=round(max_value, 2),
                avg_value=round(avg_value, 2),
                count=168,  # Ejemplo: 24 horas * 7 días = 168 lecturas horarias
                start_date=start_date,
                end_date=end_date
            )
        )
    
    return summaries
