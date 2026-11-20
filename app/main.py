from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="AI Support Engine",
    version="1.0.0",
    description="Clasificación de solicitudes de soporte con reglas e IA generativa.",
)
app.include_router(router)
