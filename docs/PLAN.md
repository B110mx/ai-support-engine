# Plan de trabajo

## Objetivo

Construir una API verificable que clasifique solicitudes de soporte con un motor tradicional y otro generativo real, manteniendo exactamente el mismo contrato JSON.

## Fases

1. **Base y contrato (30 min).** Definir categorías, prioridades, modelos Pydantic y `POST /api/analyze`.
2. **Motor tradicional (30 min).** Implementar reglas con prioridad explícita para seguridad y respuestas predeterminadas.
3. **Motor generativo (40 min).** Integrar Gemini, solicitar JSON estructurado y validar nuevamente la salida.
4. **Seguridad y errores (25 min).** Limitar entradas, rechazar campos desconocidos, aislar el mensaje del prompt y forzar revisión humana para `SECURITY`.
5. **Pruebas (30 min).** Cubrir contrato, validaciones, reglas, errores del proveedor y prompt injection.
6. **Comparación y evidencia (25 min).** Ejecutar 10 casos en ambos motores, generar CSV, calcular precisión y escribir una conclusión de máximo 150 palabras.
7. **Entrega (20 min).** Revisar README, guardar evidencias, aprobar el pull request y entregar el enlace del repositorio en Classroom.

## Distribución sugerida para tres integrantes

- Integrante 1: API, modelos y validación.
- Integrante 2: motor tradicional y casos de prueba.
- Integrante 3: Gemini, comparación y evidencia.
- Todo el equipo: revisión cruzada mediante pull requests; nadie realiza commits directos a `main`.

## Criterios de terminado

- La API responde en ambos modos con el contrato solicitado.
- Las cuatro categorías y prioridades están validadas.
- `SECURITY` siempre activa revisión humana.
- La integración generativa realiza una llamada real; no hay respuestas manuales simuladas.
- Las pruebas automáticas pasan.
- Existen 20 filas de evidencia: 10 casos por cada motor.
- README contiene instrucciones reproducibles y la conclusión técnica.
