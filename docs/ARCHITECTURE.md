# Arquitectura

El proyecto utiliza un monolito modular por capas. El contrato del dominio no depende de FastAPI ni de Gemini, por lo que ambos motores pueden desarrollarse y probarse de forma aislada.

```text
Cliente
  │
  ▼
FastAPI / Pydantic
  │
  ▼
SupportAnalyzer
  │
  ├── traditional ──► TraditionalEngine
  └── generative  ──► GeminiEngine ──► Gemini API
  │
  ▼
AnalysisResult
```

## Capas

- `app/api`: transporte HTTP, dependencias y códigos de estado.
- `app/domain`: modelos, errores y contrato `SupportEngine`.
- `app/services`: selección del motor y reglas compartidas.
- `app/engines`: implementaciones tradicional y Gemini.
- `app/bootstrap.py`: composición final de implementaciones.
- `data` y `scripts`: casos comparativos y generación de evidencia.
- `tests`: pruebas del contrato común y de la API.

## Reglas de integración

1. Cada motor implementa `SupportEngine.analyze(message)`.
2. Cada motor devuelve `EngineResult`; no construye respuestas HTTP.
3. El motor tradicional siempre se registra; Gemini solamente cuando existe `GEMINI_API_KEY`.
4. Toda categoría `SECURITY` activa revisión humana aunque un motor la omita.
5. Las credenciales nunca forman parte de modelos, respuestas o commits.
6. La salida de Gemini se valida nuevamente con Pydantic antes de responder.
