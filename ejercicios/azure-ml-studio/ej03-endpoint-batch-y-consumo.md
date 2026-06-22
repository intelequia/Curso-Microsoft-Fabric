# Ejercicio 3 (Azure ML Studio) · Registro de modelo y endpoint

**Tiempo estimado:** 60 min · **Modalidad:** aula / casa

## Objetivo

Registrar un modelo entrenado y preparar una estrategia de consumo mediante endpoint online o batch.

## Prerequisitos

- Ejercicio 2 completado.
- Al menos una ejecución MLflow con modelo o artefacto de modelo.
- Permisos para crear endpoints en Azure ML.

## Pasos

1. Selecciona la mejor ejecución del ejercicio anterior.
2. Registra el modelo como `aurora-prioridad-incidencia`.
3. Anota:
   - versión del modelo
   - métrica usada para seleccionarlo
   - ruta del artefacto
4. Elige el tipo de endpoint:
   - online si quieres probar una predicción síncrona
   - batch si quieres puntuar un fichero completo
5. Si usas online endpoint:
   - crea un endpoint de prueba
   - despliega el modelo con una instancia pequeña
   - envía una petición de ejemplo
6. Si usas batch endpoint:
   - prepara un fichero de incidencias sin etiqueta
   - configura la salida en Storage
   - lanza un scoring de prueba
7. Revisa logs, estado del deployment y coste estimado.
8. Elimina o apaga recursos si no se van a reutilizar.

## Entregable

Captura del modelo registrado y del endpoint o job batch ejecutado.

## Validación

- [ ] El modelo aparece en Models con versión.
- [ ] Existe una decisión justificada online vs batch.
- [ ] Hay una prueba de consumo o un plan claro de consumo.
- [ ] Se ha revisado cómo evitar coste residual.
