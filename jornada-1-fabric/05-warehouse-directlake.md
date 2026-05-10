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
  nombre       VARCHAR(150),
  provincia    VARCHAR(50),
  tipo         VARCHAR(30) -- "combustible" | "electrolinera" | "mixta"
);

CREATE TABLE dim_tiempo (
  fecha        DATE         NOT NULL,
  anio         INT,
  mes          INT,
  dia          INT,
  trimestre    INT,
  dia_semana   INT
);

-- Hechos
CREATE TABLE fact_ventas (
  venta_id     BIGINT       NOT NULL,
  fecha        DATE,
  cliente_id   INT,
  producto_id  INT,
  estacion_id  INT,
  cantidad     DECIMAL(12,3),
  importe      DECIMAL(12,2)
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

## Mensajes clave

- "Warehouse es la pieza para el equipo SQL clásico — pero comparte storage con Lakehouse."
- "Direct Lake elimina el dilema clásico Import vs DirectQuery."
- "Cuanto más limpio el Delta, mejor el rendimiento de Direct Lake."
