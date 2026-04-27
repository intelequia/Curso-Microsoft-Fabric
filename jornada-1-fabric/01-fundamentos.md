# J1-M1 · Fundamentos de Microsoft Fabric

**Duración:** 30 min · **Formato:** explicación + demo en vivo · **Pre-requisito:** [00-preparacion-entorno.md](../00-preparacion-entorno.md)

## Objetivos

Al terminar el bloque, el alumno debe ser capaz de:

1. Explicar **qué es Fabric** y por qué Microsoft lo ha posicionado como su plataforma analítica unificada.
2. Reconocer las **experiencias** o "workloads" de Fabric (Data Engineering, Data Warehouse, Data Science, Real-Time Intelligence, Power BI, Data Factory, Industry Solutions, Databases).
3. Entender el modelo de **capacidad** (SKUs F, equivalencia con Power BI Premium P) y de **licencias** de usuario.
4. Saber qué es **OneLake** y por qué es el "OneDrive de los datos".

## Hilo narrativo (cómo lo cuento en clase)

> "Imagina que en Aurora Energía tenemos hoy un Data Lake Gen2, un Synapse, un Power BI Premium, un Stream Analytics y un Purview. Cinco productos, cinco modelos de seguridad, cinco facturas. Fabric es la respuesta de Microsoft a ese caos: **una sola plataforma SaaS, una sola capacidad de cómputo y un único almacenamiento (OneLake) compartido por todos los workloads**."

Insistir en tres ideas que se repiten todo el curso:

- **SaaS-first**: no se aprovisiona infraestructura. Creas un workspace y empiezas.
- **OneLake = un almacenamiento, un formato (Delta-Parquet), un permiso**.
- **Una capacidad de cómputo unificada (F-SKUs)** que sirve para Spark, T-SQL, KQL y Power BI.

## Contenido

### 1. Qué es Microsoft Fabric

- Plataforma SaaS de **analítica unificada** lanzada en GA en noviembre de 2023.
- Reúne en un único producto: ingesta (Data Factory), data engineering (Spark), data warehouse (T-SQL), real-time (KQL/Eventstream), data science (notebooks + ML), Power BI y, desde 2024–2026, **Fabric Databases** y **Fabric IQ**.
- Construido sobre tres pilares: **OneLake**, **capacidades F** y **experiencias por rol**.

### 2. OneLake — el OneDrive de los datos

- Un único Data Lake **lógico por tenant**, multi-cloud, basado en ADLS Gen2.
- Se organiza así: `Tenant > Workspace > Item (Lakehouse / Warehouse / Eventhouse / etc.) > Files & Tables`.
- Todo se almacena como **Delta-Parquet** (formato abierto). Cualquier motor que lea Delta puede leer OneLake (Spark externo, Databricks, DuckDB, Snowflake con Iceberg vía mirroring, etc.).
- **Shortcuts**: punteros virtuales a datos que viven fuera de OneLake (ADLS, S3, Google Cloud Storage, otro workspace) o dentro. Evitan duplicar.
- **Mirroring**: réplica casi en tiempo real de Cosmos DB, Azure SQL DB, Snowflake, Fabric SQL Database, etc., en OneLake como tablas Delta.

### 3. Workloads / Experiencias

Fabric expone "lentes" diferentes sobre el mismo workspace según el perfil:

- **Data Factory** → ingesta (Pipelines, Dataflow Gen2, Copy Job).
- **Data Engineering** → Lakehouse, Notebooks, Spark Job Definitions, Environments.
- **Data Warehouse** → Warehouse T-SQL nativo.
- **Data Science** → notebooks, experimentos MLflow, modelos.
- **Real-Time Intelligence** → Eventstream, Eventhouse (KQL DB), Activator (alertas).
- **Power BI** → semantic models, reports, dashboards, apps.
- **Industry Solutions** (Healthcare, Sustainability, Retail, etc.).
- **Databases** (Fabric SQL Database, GA reciente).

### 4. Capacidad y licencias

| Concepto | Qué es | Equivalencia |
| --- | --- | --- |
| **F-SKU** (F2 → F2048) | Unidad de cómputo de Fabric, facturada por hora, pausable | F64 ≈ P1 de Power BI Premium |
| **Power BI Free** | Solo consumir reportes en mi área personal | — |
| **Power BI Pro** | Compartir reportes en workspaces que no estén en F64+ | Incluido en M365 E5 |
| **Power BI PPU** (Premium per user) | Funcionalidades premium por usuario, sin necesidad de capacidad | — |
| **Fabric capacity** | Imprescindible para crear cualquier item Fabric (Lakehouse, Warehouse…) | Por workspace |

> **Regla de oro comercial**: si quieres **distribuir reportes a usuarios Free**, necesitas mínimo **F64**. Por debajo, los consumidores deben tener Pro/PPU.

### 5. Licencia trial

- 60 días.
- Equivalente a una FT1 (similar a F64 en algunos límites).
- No requiere tarjeta. Una por cuenta de usuario.

### 6. Roles y permisos por workspace

- **Admin / Member / Contributor / Viewer** — clásico de Power BI, ahora aplicado a todos los items Fabric.
- Permisos finos por item (p. ej., compartir un Lakehouse en lectura sin compartir el workspace).
- **OneLake Data Access roles** y **RLS/CLS/OLS** los veremos en el bloque de Warehouse y en Jornada 2 con Purview.

## Demo en vivo (8 min)

1. Abrir el portal Fabric, mostrar el **app switcher** abajo a la izquierda.
2. Mostrar el **workspace** `aurora-curso-fabric` y los items que ya tenemos.
3. Entrar a OneLake desde el **OneLake Catalog** (botón en la barra lateral) y mostrar la jerarquía `Tenant → Workspace → Lakehouse → Tables/Files`.
4. Mostrar un **Shortcut** a una carpeta externa (puede ser otro workspace de demo). Explicar diferencia entre shortcut interno y externo.
5. Entrar a la administración del workspace y mostrar dónde se asigna la **capacidad** (Trial vs F-SKU).

## Mensajes clave para llevarse

- "Fabric no reemplaza a Azure, lo simplifica para casos analíticos."
- "OneLake es la pieza realmente disruptiva: un único almacenamiento, una única gobernanza."
- "Si en tu organización ya tienes Power BI Premium P1, **migrar a F64 es gratis y te da Fabric**."
- "La unidad de coste no es por workload, es **una sola capacidad** que ejecuta todo."

## Materiales

- Diapositivas: `assets/slides/J1-M1-fundamentos.pptx` (no incluido en repo público — el formador las proyecta).
- Diagrama de arquitectura: `assets/diagramas/onelake-overview.png` (genérico, hecho a mano en clase si no existe).
- Lectura recomendada: enlaces oficiales en [recursos.md](../recursos.md).
