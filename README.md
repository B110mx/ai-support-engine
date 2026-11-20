# AI Support Engine

Prototipo de clasificación inteligente de solicitudes de soporte con dos enfoques: reglas deterministas e inteligencia artificial generativa real mediante la API de Gemini.

## Funcionalidades

- Categorías: `ACCESS`, `BUG`, `FEATURE` y `SECURITY`.
- Prioridades: `LOW`, `MEDIUM`, `HIGH` y `CRITICAL`.
- Modos `traditional` y `generative` con el mismo contrato JSON.
- Validación de entradas, límite de tamaño y errores controlados.
- Revisión humana obligatoria para posibles incidentes de seguridad.
- Salida estructurada del modelo generativo y defensa contra prompt injection.
- Suite automática y comparación de 10 casos para ambos motores.

## Requisitos

- Node.js 20 o posterior.
- Una clave de la API de Gemini para el modo generativo.

## Configuración

1. Copia `.env.example` como `.env`.
2. Define `GEMINI_API_KEY` en tu terminal o carga las variables de `.env` con la herramienta que prefieras.

PowerShell:

```powershell
$env:GEMINI_API_KEY="tu_clave"
$env:GEMINI_MODEL="gemini-2.5-flash"
```

No subas claves al repositorio. El archivo `.env` está ignorado por Git.

## Ejecución

```bash
npm start
```

El servidor escucha en `http://localhost:3000`. Comprueba su estado con `GET /health`.

## API

`POST /api/analyze`

```json
{
  "message": "No puedo iniciar sesión",
  "mode": "traditional"
}
```

Respuesta:

```json
{
  "category": "ACCESS",
  "priority": "MEDIUM",
  "response": "Lamentamos el inconveniente...",
  "requiresHumanReview": false,
  "mode": "traditional"
}
```

Ejemplo con PowerShell:

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:3000/api/analyze -ContentType application/json -Body '{"message":"No puedo iniciar sesión","mode":"traditional"}'
```

## Pruebas

```bash
npm test
```

Para ejecutar 10 solicitudes en ambos motores y generar evidencia real:

```bash
npm run compare
```

El resultado se guarda en `results/comparison.json`. Ejecútalo con una clave válida antes de entregar; después agrega el archivo generado al repositorio como evidencia.

## Decisiones técnicas

El motor tradicional usa reglas explícitas y da prioridad a seguridad antes que a las demás categorías. El motor generativo trata el mensaje como datos no confiables, exige JSON mediante un esquema y valida nuevamente la salida. Se eligió Node.js sin dependencias de producción para reducir la superficie de ataque y facilitar la ejecución.

## Conclusión técnica

La comparación debe ejecutarse con una clave real antes de completar esta sección. El motor tradicional ofrece resultados rápidos, reproducibles y explicables para mensajes claros, pero pierde precisión ante lenguaje ambiguo. El motor generativo puede comprender mejor el contexto y redactar respuestas personalizadas, aunque depende de un proveedor externo y requiere validar estrictamente su salida. La tabla generada por `npm run compare` permite elegir el mejor motor con evidencia cuantitativa y documentar fallos de formato o clasificación.
