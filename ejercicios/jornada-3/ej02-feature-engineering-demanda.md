# Ejercicio 2 (Jornada 3) · Feature engineering del forecast de demanda

**Tiempo estimado:** 45 min · **Modalidad:** fuera de aula

## Objetivo

Construir la tabla `features_demanda_horaria` con lags, ventanas y enriquecimiento meteorológico.

## Requisitos previos

- Ejercicio 1 completado (`env_aurora_ml`, `lh_aurora_ml`).
- CSV `clima_historico.csv` en `Files/raw/`.

## Pasos

1. Crea el notebook `02-features-demanda` y adjunta el Lakehouse y el Environment.
2. Copia el contenido del notebook de referencia: [assets/ml/notebooks/02-features-demanda.ipynb.md](../../assets/ml/notebooks/02-features-demanda.ipynb.md).
3. Construye paso a paso:
   - Carga de `fact_ventas` filtrada a categoría *electricidad*, agregada a granularidad horaria.
   - Carga del CSV de clima a tabla Delta `clima_horario`.
   - Join por `estacion_id` y `ts_hora`.
   - Lags 1 h, 24 h, 168 h.
   - Rolling 24 h (media y desviación).
   - Features de calendario.
   - Filtrado de filas sin lag 168 h.
4. Escribe la tabla `features_demanda_horaria` particionada por `anio` y `mes`.
5. Documenta al menos 3 columnas con `ALTER TABLE ... ALTER COLUMN ... COMMENT '...'` desde el SQL endpoint.

## Entregable

- Tabla `features_demanda_horaria` con > 100.000 filas.
- Captura del `DESCRIBE EXTENDED features_demanda_horaria` mostrando comentarios.

## Validación

- ✅ Esquema con columnas técnicas (`feature_version`, `generado_en`).
- ✅ Sin nulos en columnas de lags después del filtro.
- ✅ Particionado por `anio`/`mes` verificable en `Files/.../features_demanda_horaria/`.
- ✅ Comentarios visibles en SQL endpoint.
