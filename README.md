# AI Support Engine

API local para analizar solicitudes de soporte mediante dos estrategias intercambiables: un motor tradicional y un motor generativo con Gemini.

## Estado actual

El proyecto incluye:

- API con FastAPI y documentación automática.
- Contrato único validado con Pydantic.
- Motor tradicional basado en reglas deterministas.
- Motor generativo con salida JSON estructurada mediante Gemini.
- Servicio coordinador que selecciona el motor solicitado.
- Manejo inicial de errores y revisión humana obligatoria para `SECURITY`.
- Pruebas automáticas y flujo de CI.

## Requisitos

- Python 3.11 o superior.

## Instalación local

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env
```

Para usar `generative`, coloca una clave real en `GEMINI_API_KEY` dentro de `.env` o defínela como variable de entorno. Nunca subas el archivo `.env`.

```dotenv
GEMINI_API_KEY=tu_clave_local
GEMINI_MODEL=gemini-3.5-flash-lite
```

Nombre visible recomendado para la credencial de desarrollo en Google AI Studio: `ase-dev-gemini-api-key`.

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

Sin `GEMINI_API_KEY`, el modo tradicional funciona normalmente y el generativo devuelve `503 Service Unavailable`. Consulta [la arquitectura](docs/ARCHITECTURE.md) y [la guía de colaboración](docs/CONTRIBUTING.md).

## Pruebas

```powershell
pytest
```

## Evidencia comparativa

`data/test_cases.json` contiene 10 solicitudes, incluyendo casos ambiguos y dos adversariales. Con una clave real configurada:

```powershell
python scripts/compare.py
```

El comando genera 20 registros en `results/comparison.csv` y las métricas de precisión en `results/summary.json`. No se generan respuestas simuladas para el motor generativo.

Última ejecución real validada (22 de noviembre de 2026):

- 10 casos por motor y 20 registros totales.
- 20/20 respuestas con contrato JSON válido.
- 0 errores de proveedor.
- Precisión tradicional: 100%.
- Precisión generativa con `gemini-3.5-flash-lite`: 90%.
