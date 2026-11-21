# AI Support Engine

Base de una API local para analizar solicitudes de soporte mediante dos estrategias intercambiables: un motor tradicional y un motor generativo.

## Estado actual

Esta rama contiene la base común del equipo:

- API con FastAPI y documentación automática.
- Contrato único validado con Pydantic.
- Servicio coordinador preparado para registrar ambos motores.
- Manejo inicial de errores y revisión humana obligatoria para `SECURITY`.
- Pruebas automáticas y flujo de CI.

Los motores tradicional y generativo se implementarán en ramas separadas.

## Requisitos

- Python 3.11 o superior.

## Instalación local

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Ejecución

```powershell
uvicorn app.main:app --reload
```

- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- Salud: `GET /health`

## Contrato principal

`POST /api/analyze`

```json
{
  "message": "No puedo iniciar sesión",
  "mode": "traditional"
}
```

```json
{
  "category": "ACCESS",
  "priority": "MEDIUM",
  "response": "Respuesta para el usuario",
  "requiresHumanReview": false,
  "mode": "traditional"
}
```

Mientras un motor no esté registrado, su modo devuelve `503 Service Unavailable`. Consulta [la arquitectura](docs/ARCHITECTURE.md) y [la guía de colaboración](docs/CONTRIBUTING.md).

## Pruebas

```powershell
pytest
```
