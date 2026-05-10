# J1-M5 · Warehouse en profundidad y Direct Lake

**Duración:** 30 min · **Formato:** explicación + demo en vivo

## Objetivos

1. Manejar el **Warehouse** de Fabric con T-SQL.
2. Modelar `gold` (estrella) sobre Aurora Energía: `dim_cliente`, `dim_producto`, `dim_estacion`, `dim_tiempo`, `fact_ventas`.
3. Entender el modo **Direct Lake** de Power BI.
4. Conocer **mirroring** entre Lakehouse, Warehouse y Power BI semantic model.

## Contenido

### 1. Warehouse — refresco

- T-SQL completo: DDL, DML, vistas, procs, funciones, transacciones multi-tabla.
- Almacena en **Delta-Parquet** sobre OneLake (las tablas son visibles desde el Lakehouse vía shortcut o consulta cross-DB).
- Soporta **CREATE TABLE AS SELECT (CTAS)**, **SELECT INTO**, **MERGE** (vía pattern), **CROSS DATABASE QUERY** (a Lakehouse, otros Warehouses).

### 2. Modelado del `gold`

```sql
-- Dimensiones
CREATE TABLE dim_cliente (
  cliente_id   INT          NOT NULL,
  nombre_cliente       VARCHAR(150),
  email        VARCHAR(150),
  dominio_email VARCHAR(100),
  segmento     VARCHAR(20),
  fecha_alta   DATE
);

CREATE TABLE dim_producto (
  producto_id  INT          NOT NULL,
  nombre       VARCHAR(150),
  categoria    VARCHAR(50),
  unidad       VARCHAR(20)
);

CREATE TABLE dim_estacion (
  estacion_id  INT          NOT NULL,
  nombre_estacion       VARCHAR(150),
  provincia    VARCHAR(50),
  comunidad    VARCHAR(50),
  tipo         VARCHAR(30) -- "combustible" | "electrolinera" | "mixta"
  fecha_apertura DATE
);

CREATE TABLE dim_tiempo (
  fecha        DATE         NOT NULL,
  anio         INT,
  mes          INT,
  dia          INT,
  trimestre    INT,
  dia_semana   INT
);

CREATE TABLE dbo.fact_ventas (
    transaccion_id  BIGINT        NOT NULL,   -- CAST AS BIGINT
    fecha_id        INT           NOT NULL,   -- yyyymmdd derivado de fecha_venta
    fecha_venta     DATETIME2(6)     NOT NULL,   -- CAST AS DATETIME2
    cliente_id      INT           NULL,       -- TRY_CAST → NULL en ventas anónimas
    producto_id     INT           NOT NULL,
    estacion_id     INT           NOT NULL,
    cantidad        DECIMAL(12,3) NOT NULL,
    precio_unitario DECIMAL(10,4) NOT NULL,
    importe         DECIMAL(14,2) NOT NULL,
    canal           VARCHAR(20)   NOT NULL    -- 'pos' / 'app' / 'web'
);
```

Procedimiento de carga (ejemplo):

```sql
CREATE OR ALTER PROCEDURE sp_load_dim_cliente AS
BEGIN
  TRUNCATE TABLE dim_cliente;
  INSERT INTO dim_cliente
  SELECT cliente_id, nombre, segmento, pais, fecha_alta
  FROM lh_aurora.dbo.clientes;  -- cross-database al Lakehouse
END;
```

### 3. Vistas, funciones y seguridad

- `CREATE VIEW vw_ventas_por_estacion AS SELECT ... GROUP BY ...`
- **Row-Level Security (RLS)**: política basada en sesión (`USER_NAME()` o claim de Entra).
- **Column-Level Security (CLS)**: `GRANT SELECT ON ... TO role` solo sobre columnas concretas.
- **Object-Level Security (OLS)**: ocultar tablas o columnas a roles.
- **Dynamic Data Masking**: enmascarar columnas sensibles (DNI, email).

### 4. Direct Lake — el "santo grial" del modelo semántico

- Power BI puede leer **directamente las tablas Delta** del Lakehouse / Warehouse, sin cargar memoria, sin DirectQuery a SQL.
- Velocidad de **Import**, frescura de **DirectQuery**, sin coste de refresh.
- **Fallback automático a DirectQuery** si una consulta excede límites (cardinalidad, columnas calculadas en DAX, joins complejos no resolubles).
- Requisitos: capacidad F-SKU, modelo creado desde el item Lakehouse/Warehouse, columnas tipadas, sin transformaciones complejas en el modelo.

### 5. Modo Direct Lake on OneLake (preview/GA)

- Permite que un Power BI Desktop guarde un PBIP "vacío" que apunta al Lakehouse vía Direct Lake on OneLake (DLOL).
- Independiente del Lakehouse origen → mejor para multi-tenant y para llevar el modelo entre workspaces sin recrearlo.

### 6. Cross-database queries

```sql
SELECT v.fecha, c.nombre, SUM(v.importe)
FROM fact_ventas v
JOIN lh_aurora.dbo.clientes c ON c.cliente_id = v.cliente_id
GROUP BY v.fecha, c.nombre;
```

## Demo en vivo (12 min)

1. En `wh_aurora` ejecutar el DDL de las 5 tablas y el `sp_load_dim_cliente`.
2. Lanzar consulta cross-DB al Lakehouse para llenar `fact_ventas`.
3. Crear una vista `vw_kpi_ventas_diarias`.
4. **+ Nuevo modelo semántico** desde el Warehouse → seleccionar las 5 tablas y la vista. Crear relaciones.
5. Abrir Power BI report nuevo en línea, agregar matriz `año / categoría / SUM(importe)`. Mostrar tiempos.
6. Verificar en propiedades del modelo que está en modo **Direct Lake**.


Paso 2:
```sql
-- Paso 2a: cargar primero las dimensiones (si no existe un proc ya creado)
-- dim_cliente
TRUNCATE TABLE dbo.dim_cliente;
INSERT INTO dbo.dim_cliente
SELECT cliente_id, nombre_cliente, email, dominio_email, segmento, CAST(fecha_alta AS DATE)
FROM lh_aurora.dbo.clientes;

-- dim_producto
TRUNCATE TABLE dbo.dim_producto;
INSERT INTO dbo.dim_producto
SELECT producto_id, nombre_producto, categoria, unidad_medida
FROM lh_aurora.dbo.productos;

-- dim_estacion
TRUNCATE TABLE dbo.dim_estacion;
INSERT INTO dbo.dim_estacion
SELECT estacion_id, nombre_estacion, provincia, comunidad, tipo, fecha_apertura
FROM lh_aurora.dbo.estaciones;

-- Paso 2b: cargar fact_ventas (la cross-DB más vistosa para la demo)
TRUNCATE TABLE dbo.fact_ventas;
INSERT INTO dbo.fact_ventas
SELECT
    CAST(v.transaccion_id    AS BIGINT),
    CAST(CONVERT(VARCHAR(8), CAST(v.fecha_venta AS DATE), 112) AS INT) AS fecha_id,
    CAST(v.fecha_venta       AS DATETIME2),
    TRY_CAST(v.cliente_id    AS INT),          -- NULL en ventas anónimas
    CAST(v.producto_id       AS INT),
    CAST(v.estacion_id       AS INT),
    CAST(v.cantidad          AS DECIMAL(12,3)),
    CAST(v.precio_unitario   AS DECIMAL(10,4)),
    CAST(v.importe           AS DECIMAL(14,2)),
    v.canal
FROM lh_aurora.dbo.ventas v
WHERE v.fecha_venta IS NOT NULL
  AND v.producto_id IS NOT NULL
  AND v.estacion_id IS NOT NULL;

```

Puntos clave para el punto 2 de la demo:

* El fecha_id se calcula inline convirtiendo la fecha a INT yyyymmdd para hacer join con dim_tiempo.
* TRY_CAST en cliente_id para absorber las filas con cliente nulo (el CSV tiene filas con campo vacío).
* El WHERE filtra filas corruptas antes de insertar → buena práctica para mostrar en clase.
* Tras la carga, el SELECT COUNT(*) final es el "momento wow" que demuestra que se leen datos del Lakehouse sin moverlos.
  
```sql
-- Verificar
SELECT COUNT(*) AS n_ventas, MIN(fecha_venta) AS desde, MAX(fecha_venta) AS hasta
FROM dbo.fact_ventas;
```

Paso 3:
```sql
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

```

Por qué está así estructurada:

* Agrupa por fecha completa (no truncada al día) + dimensiones → una fila por día/categoría/provincia/canal, lo justo para que Direct Lake la trate como tabla de agregados sin explotar en cardinalidad.
* dim_tiempo como driver del tiempo en lugar de YEAR(fecha_venta): el modelo semántico puede hacer la jerarquía anio → trimestre → mes → fecha directamente desde la vista sin columnas calculadas DAX.
* delta_importe_yoy con window function: muestra en clase que el Warehouse soporta analítica avanzada en SQL, antes de que Power BI haga el YoY en DAX.
* clientes_unicos con COUNT(DISTINCT): sirve como métrica "premium" en el Power BI report del paso 5 junto con importe_total.
* cliente_id se excluye del GROUP BY intencionalmente (es NULL en ventas anónimas) → la vista queda limpia para Direct Lake.

```sql
-- Verificar
SELECT TOP 10 * FROM dbo.vw_kpi_ventas_diarias ORDER BY fecha DESC;
```

## Mensajes clave

- "Warehouse es la pieza para el equipo SQL clásico — pero comparte storage con Lakehouse."
- "Direct Lake elimina el dilema clásico Import vs DirectQuery."
- "Cuanto más limpio el Delta, mejor el rendimiento de Direct Lake."
