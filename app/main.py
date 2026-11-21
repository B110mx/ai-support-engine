from fastapi import FastAPI

from app.api.routes import router


def create_app() -> FastAPI:
    application = FastAPI(
        title="AI Support Engine",
        version="0.1.0",
        description="Compara análisis tradicional y generativo de solicitudes de soporte.",
    )
    application.include_router(router)
    return application


app = create_app()
