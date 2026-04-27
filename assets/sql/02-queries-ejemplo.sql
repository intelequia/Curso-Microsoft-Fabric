-- ============================================================================
-- Aurora Energía · Consultas de ejemplo
-- ============================================================================

-- 1. Top 5 estaciones por importe en el último mes disponible
WITH ult_mes AS (
    SELECT MAX(YEAR(fecha_venta) * 100 + MONTH(fecha_venta)) AS yyyymm
    FROM fact_ventas
)
SELECT TOP 5 e.nombre_estacion, e.provincia, SUM(v.importe) AS importe_total
FROM fact_ventas v
JOIN dim_estacion e ON e.estacion_id = v.estacion_id
JOIN ult_mes u ON YEAR(v.fecha_venta) * 100 + MONTH(v.fecha_venta) = u.yyyymm
GROUP BY e.nombre_estacion, e.provincia
ORDER BY importe_total DESC;

-- 2. Evolución mensual por categoría de producto
SELECT
    YEAR(v.fecha_venta) AS anio,
    MONTH(v.fecha_venta) AS mes,
    p.categoria,
    SUM(v.importe) AS importe
FROM fact_ventas v
JOIN dim_producto p ON p.producto_id = v.producto_id
GROUP BY YEAR(v.fecha_venta), MONTH(v.fecha_venta), p.categoria
ORDER BY anio, mes, p.categoria;

-- 3. Clientes top con > 10 transacciones
SELECT TOP 20 c.cliente_id, c.nombre_cliente,
       COUNT(*) AS transacciones,
       SUM(v.importe) AS importe_total
FROM fact_ventas v
JOIN dim_cliente c ON c.cliente_id = v.cliente_id
GROUP BY c.cliente_id, c.nombre_cliente
HAVING COUNT(*) > 10
ORDER BY importe_total DESC;

-- 4. % de electricidad sobre el total por provincia
SELECT
    e.provincia,
    SUM(CASE WHEN p.categoria = 'electricidad' THEN v.importe ELSE 0 END) AS importe_elec,
    SUM(v.importe) AS importe_total,
    CAST(100.0 * SUM(CASE WHEN p.categoria = 'electricidad' THEN v.importe ELSE 0 END)
         / NULLIF(SUM(v.importe), 0) AS DECIMAL(5,2)) AS pct_elec
FROM fact_ventas v
JOIN dim_estacion e ON e.estacion_id = v.estacion_id
JOIN dim_producto p ON p.producto_id = v.producto_id
GROUP BY e.provincia
ORDER BY pct_elec DESC;

-- 5. Top 3 días de la semana con más ventas
SELECT TOP 3
    DATENAME(WEEKDAY, v.fecha_venta) AS dia,
    SUM(v.importe) AS importe_total
FROM fact_ventas v
GROUP BY DATENAME(WEEKDAY, v.fecha_venta)
ORDER BY importe_total DESC;

-- 6. Variación YoY por mes (último año completo)
WITH meses AS (
    SELECT YEAR(fecha_venta) AS anio, MONTH(fecha_venta) AS mes,
           SUM(importe) AS importe
    FROM fact_ventas
    GROUP BY YEAR(fecha_venta), MONTH(fecha_venta)
)
SELECT a.anio, a.mes, a.importe,
       b.importe AS importe_anio_anterior,
       CAST(100.0 * (a.importe - b.importe) / NULLIF(b.importe, 0) AS DECIMAL(8,2)) AS var_yoy_pct
FROM meses a
LEFT JOIN meses b ON b.anio = a.anio - 1 AND b.mes = a.mes
ORDER BY a.anio, a.mes;
