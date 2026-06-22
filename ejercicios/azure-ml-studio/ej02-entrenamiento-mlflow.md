# Ejercicio 2 (Azure ML Studio) · Entrenamiento y tracking con MLflow

**Tiempo estimado:** 60 min · **Modalidad:** aula / casa

## Objetivo

Entrenar un modelo sencillo desde notebook o job y registrar parámetros, métricas y artefactos con MLflow.

## Prerequisitos

- Workspace `mlw-aurora-curso`.
- Compute instance disponible.
- Data asset `aurora-incidencias`.
- Paquetes Python:

```bash
pip install pandas scikit-learn mlflow
```

## Pasos

1. Abre Notebooks en Azure ML Studio.
2. Crea un notebook `train_incidents_priority.ipynb`.
3. Carga el data asset `aurora-incidencias`.
4. Prepara un dataset tabular con variables simples:
   - tipo de incidencia
   - severidad
   - zona
   - tiempo abierto
5. Define una etiqueta de clasificación, por ejemplo prioridad o riesgo operativo.
6. Entrena un modelo base con scikit-learn.
7. Registra con MLflow:
   - algoritmo
   - parámetros principales
   - métrica `f1_weighted` o equivalente
   - matriz de confusión como artefacto si hay tiempo
8. Ejecuta una segunda prueba cambiando un parámetro.
9. Compara las ejecuciones desde Jobs / Experiments.

## Entregable

Captura de dos runs comparables con métricas visibles.

## Validación

- [ ] Hay al menos dos ejecuciones registradas.
- [ ] Cada ejecución tiene parámetros.
- [ ] Cada ejecución tiene al menos una métrica.
- [ ] Puedes justificar qué modelo registrarías y por qué.
