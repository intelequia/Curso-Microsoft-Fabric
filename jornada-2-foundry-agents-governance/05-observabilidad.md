# J2-M5 · Observabilidad, tracing, evaluación continua y red teaming

**Duración:** 30 min · **Formato:** explicación + demo

## Objetivos

1. Entender las señales necesarias para operar agentes.
2. Revisar trazas, tool calls, latencia y errores.
3. Diseñar evaluación continua y red teaming.

## Contenido

Foundry Observability agrupa tracing, evaluaciones, métricas y monitorización. En producción, las preguntas relevantes son:

- ¿Qué ha pedido el usuario?
- ¿Qué contexto se recuperó?
- ¿Qué herramienta se llamó?
- ¿Cuánto tardó?
- ¿Qué coste tuvo?
- ¿La respuesta está fundamentada?
- ¿Ha fallado una política de seguridad?

### Señales mínimas

| Señal | Uso |
| --- | --- |
| Trace ID | Diagnóstico de una ejecución concreta. |
| Tool calls | Saber qué acciones realizó el agente. |
| Latencia | Detectar degradación. |
| Tokens | Control de coste. |
| Evaluaciones | Calidad y regresiones. |
| Safety events | Riesgos y ataques. |

## Demo en vivo

1. Abrir una ejecución del agente.
2. Revisar pasos y herramientas.
3. Comparar dos versiones de instrucciones.
4. Mostrar cómo una evaluación detecta una regresión.

## Mensajes clave

- Si no puedes explicar una respuesta, no puedes operarla.
- La evaluación continua debe muestrear tráfico real con cuidado de privacidad.
- Red teaming debe formar parte del ciclo de release.
