# Colaboración

## Flujo de trabajo

1. Actualizar `main` antes de comenzar.
2. Crear una rama propia desde `main`.
3. Hacer commits pequeños y descriptivos.
4. Publicar la rama y abrir un pull request.
5. Esperar CI y una aprobación antes de fusionar.

No se permiten commits directos a `main`.

## Ramas acordadas

- `feature/base-api`: arquitectura y contrato compartido.
- `feature/traditional-engine`: reglas y respuestas predeterminadas.
- `feature/gemini-engine`: integración generativa y salida estructurada.

## Antes de abrir un pull request

```powershell
pytest
```

El PR debe explicar qué se agregó, cómo se probó y qué archivos toca.
