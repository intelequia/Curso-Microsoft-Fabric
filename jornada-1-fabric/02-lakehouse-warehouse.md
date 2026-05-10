# J1-M2 · Lakehouse, Warehouse y SQL Endpoint

**Duración:** 35 min · **Formato:** explicación + demo + ejercicio corto en aula

## Objetivos

1. Entender la diferencia conceptual y técnica entre **Lakehouse** y **Warehouse**.
2. Conocer el **SQL Analytics Endpoint** que genera automáticamente todo Lakehouse.
3. Decidir cuándo usar uno u otro en función del caso.
4. Crear el `lh_aurora` y el `wh_aurora` que se usarán durante todo el curso.

## Contenido

### 1. Lakehouse en Fabric

- **Estructura física**: dos zonas — `Files` (cualquier formato: CSV, JSON, imágenes, PDF…) y `Tables` (Delta-Parquet, descubribles).
- **Ingesta multi-modo**: subir desde el portal, OneLake File Explorer, Spark, Dataflow, Pipeline, shortcut.
- Cada Lakehouse trae **gratis** un **SQL Analytics Endpoint** (de solo lectura) y un **Default semantic model** para Power BI.
- Buen encaje para: data lake moderno, ingesta cruda + curado, ML, Spark, datos no estructurados, equipos data engineer.

### 2. Warehouse en Fabric

- **T-SQL nativo, lectura/escritura** (DML completo: INSERT, UPDATE, DELETE, MERGE).
- Almacenamiento bajo el capó: Delta-Parquet en OneLake (mismo formato que el Lakehouse).
- Soporta **vistas, procedimientos almacenados, funciones, transacciones cross-table**, **Object-Level Security**, **column-level masking**, **RLS**.
- Buen encaje para: equipos SQL, modelos en estrella servidos a BI, lógica que requiere DML/transacciones.

### 3. SQL Endpoint del Lakehouse

- Aparece automáticamente como un "primo" del Lakehouse en el workspace.
- **Solo lectura**: las tablas se mantienen escribiendo desde Spark/Dataflow/Pipeline.
- Permite: SELECT, CREATE VIEW, GRANT, gestionar **OLS/CLS/RLS**, aplicar **Dynamic Data Masking** (con limitaciones).
- Conexión vía cadena T-SQL desde SSMS, Azure Data Studio, Power BI, herramientas BI.

### 4. Tabla comparativa

| Característica | Lakehouse (+ SQL endpoint) | Warehouse |
| --- | --- | --- |
| Lenguaje principal | PySpark / Spark SQL | T-SQL |
| Escritura SQL | ❌ (endpoint solo lectura) | ✅ |
| Datos no estructurados | ✅ (carpeta Files) | ❌ |
| DML T-SQL | ❌ | ✅ |
| Transacciones multi-tabla | Limitado (Delta) | ✅ ACID |
| RLS / CLS / OLS | Parcial | Completo |
| Dynamic Data Masking | Limitado | ✅ |
| Stored procs / funciones | ❌ | ✅ |
| Visible para Power BI Direct Lake | ✅ | ✅ |

### 5. Cuándo elegir cuál

- **Lakehouse** si: ingesto de fuentes heterogéneas, necesito un "raw" y "curated", uso ciencia de datos, no requiero DML SQL.
- **Warehouse** si: equipo SQL puro, necesito DML/MERGE, transacciones multi-tabla, gobierno fino sobre tablas SQL.
- **Patrón habitual**: Lakehouse para `bronze`/`silver` (datos crudos y limpios) + Warehouse para `gold` (modelo dimensional servido a Power BI).

### 6. Caso Aurora Energía

- `lh_aurora` será el **landing zone**: aquí caen `clientes`, `productos`, `estaciones`, `ventas` desde Dataflows y Pipelines.
- `wh_aurora` será el **modelo curado**: `dim_cliente`, `dim_producto`, `dim_estacion`, `fact_ventas`, vistas y procs.
- El **modelo semántico Direct Lake** apuntará al Warehouse (jornada bloque M7).

## Demo en vivo (10 min)

1. Crear `lh_aurora` desde **+ Nuevo elemento → Lakehouse**.
2. Subir `assets/data/clientes.csv` a la carpeta `Files/landing/`.
3. Click derecho en el CSV → **Cargar a tablas** → tabla `clientes_raw`.
4. Cambiar al **SQL Endpoint** y lanzar `SELECT TOP 10 * FROM clientes_raw;`.
5. Crear `wh_aurora` desde **+ Nuevo elemento → Warehouse**.
6. Editor SQL: ejecutar `CREATE TABLE dim_cliente_demo (id INT, nombre VARCHAR(100));` e `INSERT` un par de filas. Comparar con el SQL Endpoint del Lakehouse (que no permitiría esto).

## Ejercicio corto en aula (10 min)

Cada alumno, en su workspace personal:

1. Crear `lh_aurora` y `wh_aurora`.
2. Subir `clientes.csv` al Lakehouse en `Files/landing/`.
3. Cargar el CSV como tabla `clientes_raw`.
4. Conectarse al SQL endpoint y devolver el `COUNT(*)`.
5. En el Warehouse, crear una tabla vacía `dim_cliente` con columnas `id INT`, `nombre VARCHAR(150)`, `segmento VARCHAR(20)`.

> **Validación**: que el formador (o el compañero de al lado) pueda ver los dos artefactos en el workspace.

## Errores frecuentes

- "No veo el SQL endpoint" → está al lado del Lakehouse, mismo nombre con sufijo. Hay que cambiar el desplegable arriba a la derecha.
- "Cargar a tabla falla" → cabecera con caracteres extraños o tipos no inferidos. Forzar todo como `STRING` y limpiar después.
- "Mi Warehouse no aparece como destino en Power BI Direct Lake" → asegúrate de que el workspace está en capacidad **Trial / F-SKU**.

## Mensajes clave

- "Lakehouse y Warehouse comparten OneLake — no son silos."
- "Si dudas, empieza con Lakehouse y crea Warehouse cuando necesites DML / gobierno SQL fuerte."
- "El SQL endpoint es la puerta de entrada a tu Lakehouse para todo el mundo SQL."
