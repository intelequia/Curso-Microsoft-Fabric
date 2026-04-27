# Ejercicio 6 (Jornada 1) · Modelo semántico Direct Lake y reporte Power BI

**Tiempo estimado:** 60 min · **Modalidad:** fuera de aula

## Objetivo

Construir un semantic model en modo **Direct Lake** sobre el Warehouse `wh_aurora` y publicar un reporte ejecutivo.

## Pasos

1. Desde el SQL endpoint del Warehouse → **+ New semantic model** → `sm_aurora_ventas`.
2. Selecciona las tablas: `dim_cliente`, `dim_producto`, `dim_estacion`, `dim_tiempo`, `fact_ventas`.
3. Marca `dim_tiempo` como **tabla de fechas**.
4. Configura las relaciones:
   - `fact_ventas[cliente_id]` → `dim_cliente[cliente_id]`
   - `fact_ventas[producto_id]` → `dim_producto[producto_id]`
   - `fact_ventas[estacion_id]` → `dim_estacion[estacion_id]`
   - `fact_ventas[fecha_id]` → `dim_tiempo[fecha_id]`
5. Crea las medidas DAX:

   ```dax
   Importe Total = SUM(fact_ventas[importe])
   
   Importe Año Anterior = 
       CALCULATE([Importe Total], SAMEPERIODLASTYEAR(dim_tiempo[fecha]))
   
   Variación YoY % = 
       DIVIDE([Importe Total] - [Importe Año Anterior], [Importe Año Anterior])
   
   Ticket Medio = 
       DIVIDE([Importe Total], DISTINCTCOUNT(fact_ventas[transaccion_id]))
   ```

6. Crea un **reporte** con:
   - KPI: Importe Total, Variación YoY %, Ticket Medio.
   - Gráfico de líneas: Importe Total por mes (último año).
   - Mapa de España: importe por provincia.
   - Tabla: Top 10 estaciones.
7. Publica el reporte como `rpt_aurora_ejecutivo`.

## Bonus

- Aplica **Object-Level Security** para ocultar `dim_cliente[email]` al rol `comercial`.
- Habilita **integración con Git** del workspace y haz commit del PBIP.

## Entregable

- Capturas del modelo (vista de relaciones) y del reporte.
- DAX de tus medidas.

## Validación

- ✅ Modelo en modo Direct Lake (verificar en propiedades).
- ✅ KPIs informados.
- ✅ Variación YoY calcula correctamente.
