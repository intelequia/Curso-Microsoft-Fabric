# Ejercicio 5 (Jornada 1) · Warehouse y consultas SQL

**Tiempo estimado:** 45 min · **Modalidad:** fuera de aula

## Objetivo

Construir el Warehouse `wh_aurora` con esquema en estrella, cargar dimensiones y hechos, y resolver consultas analíticas.

## Pasos

1. **+ New → Warehouse** → `wh_aurora`.
2. Ejecuta el script `assets/sql/01-ddl-warehouse.sql` para crear las tablas:
   - `dim_cliente`, `dim_producto`, `dim_estacion`, `dim_tiempo`, `fact_ventas`.
3. Carga las dimensiones con `INSERT ... SELECT` desde el Lakehouse:

   ```sql
   INSERT INTO dim_cliente
   SELECT cliente_id, nombre_cliente, dominio_email, fecha_alta
   FROM lh_aurora.dbo.dim_cliente;
   ```

4. Carga `fact_ventas` desde `lh_aurora.dbo.fact_ventas`.
5. Resuelve estas consultas (escribe el SQL):
   1. Top 5 estaciones por importe en el último mes disponible.
   2. Evolución mensual de ventas por categoría de producto.
   3. Clientes con > 10 transacciones y su importe total.
   4. % de ventas de electricidad sobre el total por provincia.
   5. Top 3 días de la semana con más ventas.

## Bonus

- Configura **Row-Level Security** para que el rol `comercial_andalucia` solo vea estaciones de provincia = "Sevilla", "Málaga", "Granada", "Cádiz", "Córdoba", "Almería", "Huelva", "Jaén".

## Entregable

- Script SQL con tus 5 consultas.
- Capturas de los resultados.
- Script de RLS si has hecho el bonus.

## Validación

- ✅ 5 tablas creadas.
- ✅ Consultas devuelven resultados coherentes.
