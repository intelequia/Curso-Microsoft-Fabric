# AML-M4 · AutoML, Designer y pipelines

**Duración:** 35 min · **Formato:** explicación + demo

## Objetivos

1. Entender cuándo usar AutoML, Designer o pipelines code-first.
2. Diseñar un flujo reproducible desde datos hasta modelo.
3. Separar exploración, entrenamiento y operación.

## Hilo narrativo

> "Azure ML Studio permite entrar por UI o por código, pero el objetivo final siempre es el mismo: un flujo repetible y gobernable."

## Contenido

Azure ML ofrece varias formas de crear modelos. La elección depende de madurez del equipo, necesidad de control y velocidad del laboratorio.

### Opciones de trabajo

| Opción | Encaje |
| --- | --- |
| **Notebooks** | Exploración, prototipos, debugging y explicación técnica. |
| **AutoML** | Baseline rápido para clasificación, regresión, series temporales y NLP soportado. |
| **Designer** | Flujos visuales para formación, prototipos low-code y equipos mixtos. |
| **Pipelines** | Automatización reproducible de preparación, entrenamiento, evaluación y registro. |
| **CLI/SDK** | Industrialización, CI/CD y control de configuración. |

### Criterio práctico

- Empieza con notebook si aún estás entendiendo datos y features.
- Usa AutoML para obtener una referencia rápida y comparar enfoques.
- Usa Designer cuando la audiencia necesita ver el flujo visualmente.
- Pasa a pipelines cuando el proceso deba repetirse con datos nuevos.

## Demo en vivo

1. Mostrar AutoML y las decisiones mínimas: dataset, target, métrica, límites.
2. Mostrar Designer con un pipeline simple de preparación y entrenamiento.
3. Revisar un pipeline como grafo de componentes.
4. Explicar cómo se movería a CI/CD con YAML, CLI o SDK.
5. Conectar con Fabric: un pipeline de datos prepara features y Azure ML entrena o puntúa.

## Mensajes clave

- AutoML no elimina criterio; acelera la comparación inicial.
- Designer ayuda a enseñar y validar flujos, pero producción suele requerir versionado.
- Pipeline es el puente entre experimento y operación.
