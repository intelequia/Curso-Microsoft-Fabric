-- ============================================================================
-- Aurora Energía · DDL del Warehouse (esquema en estrella)
-- Curso Microsoft Fabric · Jornada 1
-- ============================================================================

-- Limpieza (idempotente)
IF OBJECT_ID('dbo.fact_ventas', 'U') IS NOT NULL DROP TABLE dbo.fact_ventas;
IF OBJECT_ID('dbo.dim_cliente', 'U') IS NOT NULL DROP TABLE dbo.dim_cliente;
IF OBJECT_ID('dbo.dim_producto', 'U') IS NOT NULL DROP TABLE dbo.dim_producto;
IF OBJECT_ID('dbo.dim_estacion', 'U') IS NOT NULL DROP TABLE dbo.dim_estacion;
IF OBJECT_ID('dbo.dim_tiempo', 'U') IS NOT NULL DROP TABLE dbo.dim_tiempo;

-- ============================================================================
-- Dimensiones
-- ============================================================================

CREATE TABLE dbo.dim_cliente (
    cliente_id      INT NOT NULL,
    nombre_cliente  VARCHAR(120) NOT NULL,
    email           VARCHAR(150) NULL,
    dominio_email   VARCHAR(80)  NULL,
    segmento        VARCHAR(40)  NULL,
    fecha_alta      DATE         NULL
);

CREATE TABLE dbo.dim_producto (
    producto_id     INT NOT NULL,
    nombre_producto VARCHAR(120) NOT NULL,
    categoria       VARCHAR(40)  NOT NULL,  -- combustible / electricidad / gas / lubricante
    unidad_medida   VARCHAR(20)  NOT NULL   -- litro / kWh / m3 / unidad
);

CREATE TABLE dbo.dim_estacion (
    estacion_id     INT NOT NULL,
    nombre_estacion VARCHAR(120) NOT NULL,
    provincia       VARCHAR(60)  NOT NULL,
    comunidad       VARCHAR(60)  NOT NULL,
    tipo            VARCHAR(40)  NOT NULL,  -- gasolinera / ev_charger / multi
    fecha_apertura  DATE         NULL
);

CREATE TABLE dbo.dim_tiempo (
    fecha_id    INT  NOT NULL,   -- yyyymmdd
    fecha       DATE NOT NULL,
    anio        INT  NOT NULL,
    trimestre   INT  NOT NULL,
    mes         INT  NOT NULL,
    nombre_mes  VARCHAR(20) NOT NULL,
    semana      INT  NOT NULL,
    dia_semana  VARCHAR(20) NOT NULL,
    es_festivo  BIT  NOT NULL
);

-- ============================================================================
-- Hechos
-- ============================================================================

CREATE TABLE dbo.fact_ventas (
    transaccion_id BIGINT NOT NULL, fecha_id INT NOT NULL,   -- yyyymmdd derivado de fecha_venta
    fecha_venta DATETIME2(6) NOT NULL, cliente_id INT NULL,  -- TRY_CAST → NULL en ventas anónimas
    producto_id INT NOT NULL, estacion_id INT NOT NULL,
    cantidad DECIMAL(12,3) NOT NULL, precio_unitario DECIMAL(10,4) NOT NULL,
    importe  DECIMAL(14,2) NOT NULL, canal VARCHAR(20)   NOT NULL    -- 'pos' / 'app' / 'web'
);

-- ============================================================================
-- Procedimientos auxiliares
-- ============================================================================

CREATE OR ALTER PROCEDURE dbo.sp_refresh_dim_tiempo
    @anio_desde INT = 2022,
    @anio_hasta INT = 2027
AS
BEGIN
    TRUNCATE TABLE dbo.dim_tiempo;

    WITH digits AS (
        SELECT 0 AS d UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
        UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9
    ),
    nums AS (
        SELECT a.d + b.d*10 + c.d*100 + d.d*1000 AS n
        FROM digits a
        CROSS JOIN digits b
        CROSS JOIN digits c
        CROSS JOIN digits d   -- genera 0..9999, suficiente para ~27 años
    ),
    fechas AS (
        SELECT DATEADD(DAY, n, CAST(CAST(@anio_desde AS VARCHAR(4)) + '-01-01' AS DATE)) AS fecha
        FROM nums
        WHERE DATEADD(DAY, n, CAST(CAST(@anio_desde AS VARCHAR(4)) + '-01-01' AS DATE)) <= CAST(CAST(@anio_hasta AS VARCHAR(4)) + '-12-31' AS DATE)
    )
    INSERT INTO dbo.dim_tiempo
        (fecha_id, fecha, anio, trimestre, mes, nombre_mes, semana, dia_semana, es_festivo)
    SELECT
        CAST(CONVERT(VARCHAR(8), fecha, 112) AS INT),
        fecha,
        YEAR(fecha),
        DATEPART(QUARTER, fecha),
        MONTH(fecha),
        DATENAME(MONTH, fecha),
        DATEPART(WEEK, fecha),
        DATENAME(WEEKDAY, fecha),
        0
    FROM fechas;
END;
GO

EXEC dbo.sp_refresh_dim_tiempo;
GO

-- ============================================================================
-- Vista de KPIs diarios (ejemplo de agregación multidimensional)
-- ============================================================================
CREATE OR ALTER VIEW dbo.vw_kpi_ventas_diarias AS
SELECT
    -- Tiempo
    t.fecha,
    t.anio,
    t.trimestre,
    t.mes,
    t.nombre_mes,
    t.dia_semana,
    t.es_festivo,

    -- Producto
    p.categoria,

    -- Estacion
    e.provincia,
    e.comunidad,
    e.tipo                                              AS tipo_estacion,

    -- Canal
    v.canal,

    -- KPIs
    COUNT(*)                                            AS n_transacciones,
    COUNT(DISTINCT v.cliente_id)                        AS clientes_unicos,
    SUM(v.cantidad)                                     AS cantidad_total,
    SUM(v.importe)                                      AS importe_total,
    AVG(v.importe)                                      AS ticket_medio,

    -- YoY (requiere que dim_tiempo tenga datos de ambos años)
    SUM(v.importe)
        - ISNULL(SUM(SUM(v.importe)) OVER (
            PARTITION BY t.mes, t.dia_semana, p.categoria, e.provincia, v.canal
            ORDER BY t.anio
            ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING
          ), 0)                                         AS delta_importe_yoy

FROM dbo.fact_ventas     v
JOIN dbo.dim_tiempo      t ON t.fecha_id  = v.fecha_id
JOIN dbo.dim_producto    p ON p.producto_id = v.producto_id
JOIN dbo.dim_estacion    e ON e.estacion_id = v.estacion_id
GROUP BY
    t.fecha, t.anio, t.trimestre, t.mes, t.nombre_mes,
    t.dia_semana, t.es_festivo,
    p.categoria,
    e.provincia, e.comunidad, e.tipo,
    v.canal;
GO

-- Verificar
SELECT TOP 100 * FROM dbo.vw_kpi_ventas_diarias ORDER BY fecha DESC;