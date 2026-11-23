# Entrega - AI Support Engine

## Integrantes

- Luis Bryan Rojas Rodríguez - Matrícula: `A3524110234` - GitHub: [`B110mx`](https://github.com/B110mx)
- Abril Miranda Baltazar Varillas - Matrícula: `A3524110212` - GitHub: [`Abril0104`](https://github.com/Abril0104)
- Edwin Yahir Cruz Flores - Matrícula: `A3524110337` - GitHub: [`a3524110337-crypto`](https://github.com/a3524110337-crypto)

## Repositorio

[`https://github.com/B110mx/ai-support-engine`](https://github.com/B110mx/ai-support-engine)

## Resultados comparativos

| Motor | Casos evaluados | Formato válido | Precisión |
| --- | ---: | ---: | ---: |
| Tradicional | 10 | 10/10 | 100% |
| Generativo (Gemini) | 10 | 10/10 | 90% |

Las pruebas incluyeron solicitudes normales, un mensaje ambiguo y dos casos adversariales. Los 20 resultados se generaron mediante la ejecución real de ambos motores, sin respuestas generativas simuladas.

## Conclusión técnica

El motor tradicional obtuvo 100% de precisión porque sus reglas fueron diseñadas específicamente para las categorías y prioridades del conjunto de referencia, lo que ofrece resultados deterministas y fáciles de auditar. El motor generativo con Gemini alcanzó 90% y produjo respuestas más contextuales, pero asignó una prioridad distinta en un caso ambiguo. Para solicitudes conocidas y controladas, el motor tradicional fue más preciso; Gemini resulta más flexible ante lenguaje natural y situaciones no previstas. La mejor solución práctica es conservar ambos motores bajo el mismo contrato y seleccionar el enfoque según el contexto, manteniendo revisión humana obligatoria para incidentes de seguridad.
