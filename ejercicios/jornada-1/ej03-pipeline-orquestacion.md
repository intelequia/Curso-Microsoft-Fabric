# Ejercicio 3 (Jornada 1) · Pipeline orquestador

**Tiempo estimado:** 30 min · **Modalidad:** fuera de aula

## Objetivo

Orquestar la ejecución diaria de varios Dataflows + un Notebook con un Data Pipeline.

## Pasos

1. **+ New → Data Pipeline** → `pl_aurora_ingesta_diaria`.
2. Añade actividades en este orden:
   1. **Dataflow** → `df_aurora_clientes`.
   2. **Dataflow** → `df_aurora_productos`.
   3. **Dataflow** → `df_aurora_estaciones`.
   4. **Notebook** → `nb_aurora_lab` (lo crearás en el ejercicio siguiente; deja un placeholder).
   5. **Stored procedure** sobre `wh_aurora` (procedimiento `sp_refresh_dim_tiempo`).
3. Encadena los pasos con dependencia **On success**.
4. Añade un trigger de **Schedule diario a las 02:00 Europe/Madrid**.
5. Configura **email de alerta** en On failure (apuntando a tu dirección).

## Entregable

- Captura del pipeline con dependencias.
- Captura del schedule activo.
- Captura de una ejecución completa.

## Validación

- ✅ Pipeline ejecuta los 5 pasos en orden.
- ✅ Si un paso falla, el siguiente no se ejecuta.
- ✅ Schedule activo.
