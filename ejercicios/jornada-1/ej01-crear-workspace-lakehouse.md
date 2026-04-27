# Ejercicio 1 (Jornada 1) · Crear workspace y Lakehouse para Aurora Energía

**Tiempo estimado:** 30 min · **Modalidad:** fuera de aula

## Objetivo

Dejar listo tu workspace personal con el Lakehouse `lh_aurora` que servirá de base para el resto de ejercicios.

## Requisitos previos

- Acceso a Microsoft Fabric (trial, M365 Dev Program o capacidad asignada). Ver [00-preparacion-entorno.md](../../00-preparacion-entorno.md).
- Power BI Desktop instalado (no obligatorio en este ejercicio).

## Pasos

1. Entra a `https://app.fabric.microsoft.com`.
2. Crea un nuevo **workspace** llamado `aurora-curso-fabric-<tus-iniciales>`.
   - Capacidad: la del curso o tu trial.
   - Asigna **Admin** a ti mismo y **Member** al instructor.
3. Dentro del workspace, **+ New → Lakehouse** → `lh_aurora`.
4. Sube los ficheros CSV de `assets/data/` a la carpeta `Files/raw/` del Lakehouse:
   - `clientes.csv`
   - `productos.csv`
   - `estaciones.csv`
   - `ventas.csv`
5. Carga cada CSV a una **tabla Delta** con el wizard *Load to Tables*:
   - Tabla `dim_cliente_raw` ← `clientes.csv`
   - Tabla `dim_producto_raw` ← `productos.csv`
   - Tabla `dim_estacion_raw` ← `estaciones.csv`
   - Tabla `fact_ventas_raw` ← `ventas.csv`
6. Verifica con el **SQL endpoint** que puedes hacer:

   ```sql
   SELECT COUNT(*) FROM fact_ventas_raw;
   SELECT TOP 10 * FROM dim_cliente_raw;
   ```

## Entregable

Captura de pantalla del **explorador del Lakehouse** mostrando las 4 tablas y screenshot del resultado del SELECT COUNT.

## Validación

- ✅ Workspace creado con naming correcto.
- ✅ Lakehouse `lh_aurora` con 4 tablas.
- ✅ `fact_ventas_raw` con ~50.000 filas.
