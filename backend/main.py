from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import uvicorn
import os
from dotenv import load_dotenv

# Importar routers
from api import sensor_routes, prediction_routes, actuator_routes, mycodo_routes, history_routes

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación FastAPI
app = FastAPI(
    title="Joy's Farm Agent API",
    description="API para el agente autónomo de Joy's Farm",
    version="0.1.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(sensor_routes.router)
app.include_router(prediction_routes.router)
app.include_router(actuator_routes.router)
app.include_router(mycodo_routes.router)
app.include_router(history_routes.router)

# Ruta básica
@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API del Agente Autónomo de Joy's Farm",
        "status": "online",
        "version": "0.1.0"
    }

# Ruta de estado de salud
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "api": "online",
            "database": "pending",
            "ai_module": "pending"
        }
    }

# Punto de entrada para ejecutar la aplicación directamente
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
