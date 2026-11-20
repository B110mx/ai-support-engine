# AI Support Engine

API en Python para clasificar solicitudes de soporte mediante reglas deterministas o IA generativa real con Gemini.

## Tecnologías

- Python 3.11+
- FastAPI y Uvicorn
- Pydantic y pydantic-settings
- Google Gen AI SDK
- pytest y pytest-cov
- GitHub Actions

Consulta el [plan](docs/PLAN.md) y la [arquitectura](docs/ARCHITECTURE.md).

## Configuración

```bash
python -m venv .venv
```

PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env
```

Define `GEMINI_API_KEY` dentro de `.env`. Nunca subas ese archivo al repositorio.

## Ejecución

```bash
uvicorn app.main:app --reload
```

- API: `http://localhost:8000`
- Documentación interactiva: `http://localhost:8000/docs`
- Salud: `GET /health`

## Contrato

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
  "response": "Lamentamos el inconveniente...",
  "requiresHumanReview": false,
  "mode": "traditional"
}
```

`mode` acepta `traditional` o `generative`. Ambos motores respetan el mismo contrato.

## Pruebas

```bash
pytest
```

## Evidencia comparativa

El archivo `data/test_cases.json` contiene 10 solicitudes normales, ambiguas y adversariales. Para ejecutar ambos motores realmente:

```bash
python scripts/compare.py
```

Se generan:

- `results/comparison.csv`: 20 filas, 10 por motor.
- `results/summary.json`: precisión de cada motor.

Estos archivos deben conservarse como evidencia antes de la entrega.

## Seguridad

- Entrada limitada a 5,000 caracteres y sin campos desconocidos.
- El mensaje se delimita como contenido no confiable.
- La salida generativa se valida con Pydantic.
- Cualquier resultado `SECURITY` exige revisión humana.
- Las credenciales solo se leen desde variables de entorno.

## Conclusión técnica

La conclusión final se redactará después de ejecutar los 10 casos con una clave real. El motor tradicional es rápido, reproducible y explicable, pero depende de vocabulario previsto. El motor generativo comprende mejor lenguaje ambiguo y redacta respuestas contextuales, aunque introduce latencia, costo y dependencia externa. La decisión sobre cuál funcionó mejor debe basarse en la precisión registrada en `results/summary.json`, no en respuestas simuladas.
