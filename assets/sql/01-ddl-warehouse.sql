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
    es_festivo  BIT  NOT NULL DEFAULT 0
);

-- ============================================================================
-- Hechos
-- ============================================================================

CREATE TABLE dbo.fact_ventas (
    transaccion_id  BIGINT NOT NULL,
    fecha_id        INT    NOT NULL,
    fecha_venta     DATETIME2 NOT NULL,
    cliente_id      INT    NULL,         -- ventas anónimas permitidas
    producto_id     INT    NOT NULL,
    estacion_id     INT    NOT NULL,
    cantidad        DECIMAL(12,3) NOT NULL,
    precio_unitario DECIMAL(10,4) NOT NULL,
    importe         DECIMAL(14,2) NOT NULL,
    canal           VARCHAR(20) NOT NULL  -- pos / app / web
);

-- ============================================================================
-- Procedimientos auxiliares
-- ============================================================================

CREATE OR ALTER PROCEDURE dbo.sp_refresh_dim_tiempo
    @anio_desde INT = 2023,
    @anio_hasta INT = 2027
AS
BEGIN
    DELETE FROM dbo.dim_tiempo;

    ;WITH dias AS (
        SELECT CAST(CONCAT(@anio_desde, '-01-01') AS DATE) AS d
        UNION ALL
        SELECT DATEADD(DAY, 1, d) FROM dias
        WHERE d < CAST(CONCAT(@anio_hasta, '-12-31') AS DATE)
    )
    INSERT INTO dbo.dim_tiempo (fecha_id, fecha, anio, trimestre, mes, nombre_mes, semana, dia_semana, es_festivo)
    SELECT
        CAST(CONVERT(VARCHAR(8), d, 112) AS INT),
        d,
        YEAR(d),
        DATEPART(QUARTER, d),
        MONTH(d),
        DATENAME(MONTH, d),
        DATEPART(WEEK, d),
        DATENAME(WEEKDAY, d),
        0
    FROM dias
    OPTION (MAXRECURSION 32767);
END;
GO

EXEC dbo.sp_refresh_dim_tiempo;
GO
