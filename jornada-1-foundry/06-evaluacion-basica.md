# J1-M6 · Evaluación básica de calidad y seguridad

**Duración:** 25 min · **Formato:** explicación + práctica guiada

## Objetivos

1. Entender por qué evaluar IA generativa requiere datasets y métricas.
2. Usar evaluadores de calidad, groundedness, relevancia y seguridad.
3. Crear una primera batería de regresión.

## Contenido

Evaluar una aplicación de IA no consiste en probar tres preguntas en el playground. Necesitamos un conjunto de casos representativos, resultados esperados y métricas repetibles.

### Métricas habituales

| Métrica | Qué detecta |
| --- | --- |
| Groundedness | Si la respuesta se apoya en las fuentes. |
| Relevance | Si responde a la pregunta del usuario. |
| Coherence / fluency | Calidad lingüística y consistencia. |
| Safety | Riesgos de odio, violencia, sexual, autolesión o jailbreak. |
| Tool call accuracy | Si el agente llama a la herramienta correcta. |
| Task completion | Si completa el objetivo del usuario. |

## Demo en vivo

1. Abrir `assets/data/eval_questions.csv`.
2. Ejecutar una evaluación básica desde portal o SDK.
3. Revisar resultados.
4. Identificar una pregunta fallida.
5. Ajustar instrucciones y repetir.

## Mensajes clave

- Sin evaluación no hay control de regresiones.
- Las preguntas trampa son tan importantes como las preguntas felices.
- La evaluación cuesta dinero: debe planificarse como parte de la operación.
