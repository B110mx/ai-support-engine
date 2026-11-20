# Arquitectura

## Estilo

Arquitectura modular en capas, ligera y adecuada para un prototipo académico:

```text
Cliente
  |
  v
FastAPI / Pydantic (app/api)
  |
  v
Servicio de aplicación (app/services)
  |-----------------------------|
  v                             v
Motor tradicional          Puerto generativo
(app/domain)                    |
                               v
                        Adaptador Gemini
                        (app/providers)
```

## Responsabilidades

- `app/api`: expone `/health` y `/api/analyze`, traduce errores a HTTP.
- `app/domain`: enums, contrato y reglas puras sin dependencias externas.
- `app/services`: decide qué motor ejecutar y aplica invariantes comunes.
- `app/providers`: encapsula Gemini detrás de un protocolo intercambiable.
- `tests`: valida API, dominio, servicio y defensa ante instrucciones adversariales.
- `scripts/compare.py`: ejecuta la matriz de 10 casos y produce evidencia.

## Flujo de una solicitud

1. FastAPI recibe JSON y Pydantic valida tamaño, modo y campos.
2. `SupportAnalyzer` elige `traditional` o `generative`.
3. El motor devuelve categoría, prioridad, respuesta y revisión humana.
4. El servicio fuerza revisión humana para `SECURITY`.
5. FastAPI serializa el mismo contrato para ambos modos.

## Decisiones

- **FastAPI:** API pequeña, documentación OpenAPI automática y pruebas sencillas.
- **Pydantic:** contrato único y validación estricta en entrada y salida.
- **Gemini:** integración real con salida JSON regida por un esquema.
- **Protocol:** permite cambiar Gemini por Ollama sin modificar dominio o rutas.
- **pytest:** pruebas parametrizadas, legibles y compatibles con CI.
- **GitHub Actions:** valida cada pull request antes de fusionarlo.
