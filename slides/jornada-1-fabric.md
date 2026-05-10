---
marp: true
theme: intelequia
paginate: true
size: 16:9
title: "Jornada 1 · Microsoft Fabric"
description: "Master class de 4 horas: arquitectura, OneLake, Lakehouse, Warehouse, ingesta, Spark, Real-Time y Power BI Direct Lake"
author: Intelequia
math: katex
---

<!-- _class: lead bare -->

<span class="tag">Curso · Jornada 1 de 2</span>

# Microsoft **Fabric**
## La plataforma analítica unificada de Microsoft

### 4 horas · master class · caso *Aurora Energía*

<!--
Bienvenida. Presentaros brevemente: quién sois y vuestra relación con Fabric. Preguntar a la sala: ¿quién tiene experiencia con Power BI Premium? ¿con Azure Data Factory? Eso os sitúa en el punto de partida. El hilo conductor de todo el día es Aurora Energía: un operador ficticio con 250 estaciones de servicio, comercializadora eléctrica y división logística. En 4 horas construimos juntos un flujo de datos end-to-end real. Recordar la dinámica: bloque teórico + demo en vivo + ejercicios para casa.
-->

---

<!-- _class: tight -->

## ¿Qué nos llevaremos hoy?

<div>

- Entender **qué es Fabric** y dónde encaja en el ecosistema Microsoft.
- Comprender **OneLake** y por qué es la pieza disruptiva.
- Distinguir **Lakehouse**, **Warehouse**, **Eventhouse** y **Semantic Model**.
- Construir un flujo *end-to-end*: **CSV → Lakehouse → Spark → Warehouse → Power BI**.
- Tocar **Real-Time Intelligence** con KQL.
- Salir con un **workspace funcional** sobre el que practicar en casa.

</div>

> **Hilo conductor**: Aurora Energía — operador ficticio con red de estaciones de servicio, comercializadora eléctrica y división de logística.

<!--
Leer los objetivos en voz alta y pedir que los apunten. Avisar: al final de cada bloque habrá una slide '¿Qué me llevo?' — eso es lo mínimo que debe quedar claro. Si algo no queda claro, es el momento de preguntar ahí. Presentar el caso Aurora Energía brevemente: empresa real-ficticia, datos de ventas de carburante y electricidad, datos de telemetría de surtidores, datos de clientes con GDPR.
-->

---

## Agenda · 4 h con descanso de 15 min

| Bloque | Min | Tema |
|---|---|---|
| **M0** | 15 | Bienvenida y contexto |
| **M1** | 30 | Fundamentos · arquitectura · OneLake · licencias |
| **M2** | 35 | Lakehouse, Warehouse y SQL Endpoint |
| **M3** | 40 | Ingesta · Dataflow Gen2 + Pipelines |
| ☕ | 15 | **Descanso** |
| **M4** | 35 | Notebooks y Spark |
| **M5** | 30 | Warehouse en profundidad + Direct Lake |
| **M6** | 25 | Real-Time Intelligence · Eventhouse + KQL |
| **M7** | 25 | Power BI · modelo semántico Direct Lake |
| **M8** | 10 | Cierre y deberes |

<!--
Recorrer la agenda módulo a módulo. Descanso fijo a mitad: aproximadamente a las 2h de empezar. Las demos son en vivo — si algo falla en producción hay capturas de pantalla de respaldo. Los ejercicios para casa están en la carpeta ejercicios/jornada-1/. Preguntar: ¿hay algún bloque que les interese especialmente para hacer hincapié?
-->
---
## Antes de empezar

Todo el contenido del curso está en https://github.com/intelequia/Curso-Microsoft-Fabric

1. Lee [requisitos.md](requisitos.md) y prepara tu equipo con todo lo indicado **antes** de la primera jornada.
2. Sigue [00-preparacion-entorno.md](00-preparacion-entorno.md) para crear tu trial de Microsoft Fabric. Si tu organización ya dispone de capacidad Fabric, hablamos en el primer bloque sobre cómo solicitarte un workspace propio.
3. Descarga la carpeta [assets/data](assets/data) en local: la usarás en varios ejercicios.

*NOTA*: para los que no les haya dado tiempo, hemos preparado un tenant auroraenergiasl.onmicrosoft.com, con credenciales para todos.

---

<!-- _class: section -->

<span class="module">M1 · 30 min</span>

# Fundamentos
## Arquitectura, OneLake, capacidades y licencias

<!--
Transición al primer bloque. Avisar que M1 es el más conceptual del día, pero que cuanto mejor quede OneLake en la cabeza, más fácil será entender todo lo demás. Duración estimada: 25 minutos incluyendo preguntas.
-->

---

## ¿Qué es Microsoft Fabric?

- Plataforma **SaaS** de analítica unificada · GA noviembre 2023.
- Reúne en un único producto: **ingesta**, **data engineering**, **data warehouse**, **real-time**, **data science**, **Power BI** y, desde 2024–2026, **Fabric Databases** y **Fabric IQ**.
- Construido sobre tres pilares:
  - **OneLake** · un único almacenamiento por tenant.
  - **Capacidades F** · una sola unidad de cómputo para todo.
  - **Experiencias por rol** · "lentes" sobre el mismo workspace.

> *Fabric no reemplaza a Azure: lo simplifica para casos analíticos.*

<!--
Fabric GA en noviembre 2023 — menos de 2 años de vida, pero ya en uso en miles de empresas. El mensaje clave: no es una herramienta más, es una plataforma SaaS que reúne Synapse, ADF, Power BI Premium, Data Science y Real-Time Intelligence bajo un único paraguas de capacidad. El precio ya no es por motor, sino por capacidad unificada (F-SKU). Preguntar: ¿alguien usa todavía Synapse Analytics clásico o Azure Data Factory independiente?
-->

---

## OneLake · *el OneDrive de los datos*

- Data Lake **lógico por tenant**, multi-cloud, sobre ADLS Gen2.
- Jerarquía: `Tenant > Workspace > Item > Files & Tables`.
- Todo se almacena en **Delta-Parquet** (formato abierto).
- Cualquier motor que lea Delta puede leer OneLake.
- Dos primitivas clave:
  - <span class="pill">Shortcuts</span> punteros virtuales a datos externos (ADLS, S3, GCS) o internos.
  - <span class="pill">Mirroring</span> réplica casi en tiempo real desde Cosmos DB, Azure SQL, Snowflake, Fabric SQL DB.

<!--
OneLake es LA pieza disruptiva. Un storage, un formato Delta-Parquet, un permiso. Analogía: como OneDrive pero para datos analíticos. Todos los items Fabric (Lakehouses, Warehouses, etc.) almacenan sus datos en OneLake automáticamente — sin configuración. Los Shortcuts son accesos directos que apuntan a datos en ADLS, S3 o GCS sin moverlos. El Mirroring replica casi en tiempo real desde Azure SQL, Cosmos DB o Snowflake sin ETL. Dar el ejemplo: si tenéis una base de datos operacional en Azure SQL, en minutos tenéis los datos en OneLake.
-->

---

## Workloads · una plataforma, muchas lentes

| Experiencia | Para qué |
|---|---|
| **Data Factory** | Pipelines, Dataflow Gen2, Copy Job |
| **Data Engineering** | Lakehouse, Notebooks, Spark Job Definitions |
| **Data Warehouse** | T-SQL nativo lectura/escritura |
| **Data Science** | Notebooks, MLflow, modelos |
| **Real-Time Intelligence** | Eventstream, Eventhouse, Activator |
| **Power BI** | Semantic models, reports, dashboards, apps |
| **Databases** | Fabric SQL Database |
| **Industry Solutions** | Healthcare, Sustainability, Retail |

<!--
Esta tabla se puede leer rápido — lo importante es que hay una 'lente' por rol. Un ingeniero de datos trabaja en Data Engineering. Un analista en Power BI. Un científico de datos en Data Science. Un ingeniero de datos en tiempo real en Real-Time Intelligence. Todos comparten el mismo workspace y los mismos datos en OneLake: no hay silos.
-->

---

<!-- _class: tight -->

## Capacidad y licencias

| Concepto | Qué es | Equivalencia |
|---|---|---|
| **F-SKU** (F2 → F2048) | Unidad de cómputo de Fabric, facturada por hora, **pausable** | F64 ≈ P1 de Power BI Premium |
| **Power BI Free** | Solo consumir reportes en el área personal | — |
| **Power BI Pro** | Compartir reportes en workspaces que no estén en F64+ | Incluido en M365 E5 |
| **Power BI PPU** | Funcionalidades premium por usuario, sin capacidad | — |
| **Fabric capacity** | Imprescindible para crear cualquier item Fabric | Por workspace |

> **Regla de oro:** para distribuir reportes a usuarios *Free* necesitas **F64+**. Por debajo, los consumidores deben tener Pro/PPU.

<!--
Esta slide es la que genera más dudas. La regla de oro: necesitáis F64 si queréis que usuarios con licencia Free (sin Pro) puedan consumir reportes en el workspace. Por debajo de F64, los consumidores necesitan licencia Pro o PPU. El trial de 60 días equivale a F64 — aprovecharlos para validar el caso de uso antes de comprar. Para la mayoría de pymes, F8 o F16 son suficientes para empezar.
-->

---

## Trial y roles

- **Trial Fabric**: 60 días, equivalente a una FT1 (~F64 en muchos límites). Sin tarjeta, una por usuario.
- **Roles de workspace** (heredados de Power BI, ahora aplicados a *todos* los items Fabric):
  - **Admin** · gobierna el workspace.
  - **Member** · gestiona y publica.
  - **Contributor** · crea y edita.
  - **Viewer** · sólo lectura.
- Permisos finos por item (compartir un Lakehouse en lectura sin compartir el workspace).
- **OneLake Data Access roles** + **RLS / CLS / OLS** se ven en M5 y en Jornada 2 con Purview.

<!--
El trial se activa desde la configuración del tenant — cualquier admin puede hacerlo en 5 minutos. Los roles de workspace (Viewer, Contributor, Member, Admin) son los mismos que en Power BI pero ahora aplican a todos los items Fabric del workspace. Recordar: los permisos también se pueden dar a nivel de item individual — puedo compartir solo el Lakehouse sin dar acceso al workspace completo.
-->

---

<!-- _class: key -->

## Tres ideas que se repiten todo el curso

- **SaaS-first** · creas un workspace y empiezas. Cero infraestructura.
- **OneLake** · un almacenamiento, un formato (Delta), un permiso.
- **Una capacidad** · mismos *Capacity Units* para Spark, T-SQL, KQL y Power BI.

<!--
Hacer pausa y preguntar: ¿alguien puede explicar con sus propias palabras qué diferencia hay entre F-SKU y Power BI Premium P-SKU? Respuesta esperada: antes se pagaba por motor (Premium era solo para Power BI), ahora una sola capacidad da acceso a todos los workloads Fabric. La unificación de billing es el argumento más potente para el CFO.
-->

---

<!-- _class: section -->

<span class="module">M2 · 35 min</span>

# Lakehouse vs Warehouse
## Y el famoso *SQL Endpoint*

<!--
Transición. En este bloque respondemos la pregunta más frecuente en proyectos Fabric: ¿Lakehouse o Warehouse? La respuesta corta: depende del equipo y del tipo de carga. Duración estimada: 30 minutos incluyendo demo.
-->

---

## Lakehouse

- Estructura física: **Files** (cualquier formato) + **Tables** (Delta-Parquet, descubribles).
- Ingesta multi-modo: portal, OneLake File Explorer, Spark, Dataflow, Pipeline, shortcut.
- **Gratis** trae:
  - **SQL Analytics Endpoint** (sólo lectura).
  - **Default semantic model** para Power BI.
- Encaje natural: data lake moderno, ingesta cruda + curado, ML, Spark, datos no estructurados.

<!--
El Lakehouse es el depósito universal. Acepta cualquier formato en la sección Files (CSV, Parquet, JSON, imágenes, binarios...) y expone tablas Delta para consultas SQL. Lo más importante: incluye gratis el SQL Analytics Endpoint (para consultas T-SQL de solo lectura) y el Default Semantic Model (para conectar Power BI directamente). Preguntar: ¿en vuestro proyecto actual, dónde aterriza la ingesta — ADLS, Azure SQL, archivos CSV?
-->

---

## Warehouse

- **T-SQL nativo, lectura/escritura** · DML completo: `INSERT`, `UPDATE`, `DELETE`, `MERGE`.
- Almacenamiento debajo: **Delta-Parquet en OneLake** (mismo formato que Lakehouse).
- Soporta:
  - **Vistas, procedimientos, funciones**.
  - **Transacciones cross-table**.
  - **OLS, CLS, RLS, Dynamic Data Masking**.
- Encaje natural: equipo SQL, modelo en estrella servido a BI, lógica con DML/transacciones.

<!--
El Warehouse es para el equipo SQL clásico. DML completo: INSERT, UPDATE, DELETE, MERGE. Stored procedures, funciones, vistas, transacciones multi-tabla. La sorpresa que suele sorprender: por debajo también es Delta-Parquet sobre OneLake. No es un silo: comparte el mismo storage que el Lakehouse del mismo workspace. Desde el Warehouse puedes hacer queries cross-database directamente al Lakehouse — sin ETL.
-->

---

<!-- _class: tight -->

## Comparativa cara a cara

| Característica | Lakehouse + SQL endpoint | Warehouse |
|---|---|---|
| Lenguaje principal | PySpark / Spark SQL | T-SQL |
| Escritura SQL | ❌ (endpoint solo lectura) | ✅ |
| Datos no estructurados | ✅ (carpeta Files) | ❌ |
| DML T-SQL | ❌ | ✅ |
| Transacciones multi-tabla | Limitado (Delta) | ✅ ACID |
| RLS / CLS / OLS | Parcial | Completo |
| Dynamic Data Masking | Limitado | ✅ |
| Stored procs / funciones | ❌ | ✅ |
| Direct Lake en Power BI | ✅ | ✅ |

<!--
Las diferencias clave a remarcar: 1) El SQL endpoint del Lakehouse es solo lectura — no se puede hacer INSERT ni MERGE. 2) El Warehouse soporta DML completo, stored procs y transacciones. 3) Para datos no estructurados (JSON crudo, imágenes, PDFs), solo el Lakehouse. 4) Para código T-SQL heredado con stored procedures, el Warehouse. Preguntar: ¿en vuestro equipo predomina el perfil PySpark/Python o el perfil T-SQL?
-->

---

## ¿Cuándo cada uno?

- **Lakehouse** → ingesto fuentes heterogéneas, necesito *raw* y *curated*, hago ciencia de datos, no requiero DML SQL.
- **Warehouse** → equipo SQL puro, DML/MERGE, transacciones multi-tabla, gobierno fino sobre tablas SQL.
- **Patrón habitual:**
  - **Lakehouse** para *bronze* y *silver*.
  - **Warehouse** para *gold* (modelo dimensional servido a Power BI).

> En Aurora Energía: `lh_aurora` aterriza la materia prima, `wh_aurora` sirve el modelo certificado.

<!--
El patrón más habitual en proyectos grandes: Lakehouse para las capas bronze (datos crudos) y silver (datos limpios), Warehouse para la capa gold (modelo dimensional servido a Power BI). En Aurora: lh_aurora aterriza la materia prima desde los sistemas operacionales, wh_aurora sirve el modelo dimensional certificado a Power BI con Direct Lake. Este patrón cubre el 80% de los proyectos de datos que veréis en clientes.
-->

---

## Demo en vivo · 10 min

1. Crear `lh_aurora` desde **+ Nuevo elemento → Lakehouse**.
2. Subir `clientes.csv` a `Files/landing/`.
3. *Cargar a tablas* → `clientes_raw`.
4. Cambiar al **SQL Endpoint** y `SELECT TOP 10 * FROM clientes_raw;`.
5. Crear `wh_aurora` y ejecutar:
   ```sql
   CREATE TABLE dim_cliente_demo (id INT, nombre VARCHAR(100));
   INSERT INTO dim_cliente_demo VALUES (1, 'Demo');
   ```
6. Comparar con el SQL Endpoint del Lakehouse (que **no** permitiría esto).

<!--
Demo en vivo. Tiempo estimado: 10 minutos. Puntos clave a mostrar: 1) Diferencia visual entre Lakehouse y Warehouse en la interfaz del portal. 2) El SQL Endpoint del Lakehouse y que al intentar INSERT da error. 3) El Warehouse con el editor T-SQL y la cross-database query al Lakehouse. Si hay problemas de conectividad en el aula, mostrar las capturas de respaldo de la demo. Subir el CSV clientes.csv al Lakehouse y mostrar cómo se convierte en tabla Delta automáticamente.
-->

---

<!-- _class: key -->

## Para llevarse a casa

- Lakehouse y Warehouse **comparten OneLake** — no son silos.
- Si dudas, empieza por **Lakehouse** y crea Warehouse cuando necesites DML.
- El **SQL endpoint** es la puerta de entrada a tu Lakehouse para todo el mundo SQL.

<!--
Pregunta de verificación: ¿puedo hacer un MERGE en el SQL endpoint de un Lakehouse? Respuesta: no, es solo lectura. ¿Y en el Warehouse? Sí, con el patrón MERGE estándar T-SQL. Segundo punto: el shared storage significa que si cargo datos en el Lakehouse vía Spark, ya son accesibles desde el Warehouse sin mover nada — ambos ven el mismo Delta en OneLake.
-->

---

<!-- _class: section -->

<span class="module">M3 · 40 min</span>

# Ingesta
## Dataflow Gen2, Pipelines, Copy Job, Mirroring

<!--
Transición al bloque de ingesta — el más práctico de la mañana. Regla de tres para elegir la herramienta: Dataflow Gen2 para transformar, Pipeline para orquestar, Copy Job para incremental masivo, Mirroring para replicación operacional en tiempo real. Duración estimada: 35 minutos incluyendo demo.
-->

---

<!-- _class: tight -->

## Opciones de ingesta · cuándo usar cada una

| Opción | Cuándo encaja | Lenguaje |
|---|---|---|
| **Dataflow Gen2** | Ingesta + transformación con Power Query, low-code, batch | M / sin código |
| **Data Pipeline** | Orquestación, control de flujo, copia masiva | UI / JSON |
| **Copy Job** | Copia incremental gestionada (CDC + watermark) | UI |
| **Eventstream** | Streaming continuo (IoT Hub, Event Hub, Kafka) | UI |
| **Mirroring** | Réplica casi en tiempo real desde Azure SQL, Cosmos, Snowflake | UI |
| **Notebook Spark** | Ingesta programática con `spark.read` | PySpark |

> *Dataflow para transformar, Pipeline para orquestar.*

<!--
Recorrer la tabla fila a fila. El punto de confusión habitual: ¿cuándo Pipeline vs Dataflow Gen2? Dataflow Gen2 es la transformación en sí (interfaz Power Query). Pipeline es el orquestador que llama a varios Dataflows, Notebooks, Stored Procs, etc. con control de flujo, dependencias y notificaciones. Otra confusión: Copy Job vs Copy activity dentro de Pipeline — Copy Job es un item independiente para cargas incrementales programadas; Copy activity es una actividad dentro de un Pipeline más complejo.
-->

---

## Dataflow Gen2 al detalle

- Heredero del Dataflow clásico de Power BI · multi-destino, motor mejorado (**Fast Copy**).
- UX = **Power Query Online** · vista previa, *Applied Steps*, editor M.
- Destinos: Lakehouse, Warehouse, KQL DB, Azure SQL DB, Synapse SQL, ADX.
- **Refresco** programable, identidades de servicio y service principal.
- **Plantillas .pqt** importables y exportables.
- **Fast Copy** se activa automáticamente para conectores y cargas grandes.

<!--
Dataflow Gen2 tiene una mejora importante respecto al clásico (Gen1): Fast Copy. Para conectores como ADLS, Azure SQL o SharePoint, en lugar de ir fila a fila usa la ruta de copia masiva nativa. Resultado: hasta 25x más rápido para grandes volúmenes. Y el destino puede ser Lakehouse, Warehouse, Azure SQL, Synapse SQL, etc. La interfaz es Power Query Online — si tu equipo ya conoce Power Query de Excel o Power BI Desktop, la curva de aprendizaje es mínima.
-->

---

## Data Pipeline al detalle

- Orquestador heredero de **Azure Data Factory v2**, integrado en Fabric.
- **Actividades**: Copy data, Dataflow, Notebook, Spark Job, Stored Procedure, Lookup, ForEach, If/Switch, Wait, Web, Office365, Teams.
- **Eventos** entre actividades:
  - 🟢 éxito · 🔴 fallo · 🟠 omisión · 🔵 al completar.
- **Programación**: cron, eventos (*file arrived*), manual.
- **Monitoring Hub**: vista cross-workspace de ejecuciones.

<!--
Heredero directo de Azure Data Factory v2. Si venís de ADF, todo os resultará familiar: mismas actividades (Copy, ForEach, If, Wait, Lookup...), mismos conectores, mismos triggers. Si no venís de ADF, el punto de entrada es la actividad Copy data para cargas simples. El Monitoring Hub es la pieza que más agradece la operaciones: todas las ejecuciones de Pipelines, Dataflows, Notebooks y Spark Jobs quedan registradas en un único lugar con estado, duración y errores.
-->

---

<!-- _class: tight -->

## Patrón habitual · Pipeline llama a Dataflow

```text
[Pipeline pl_aurora_ingesta]
  ├── Dataflow → df_clientes        (carga clientes_raw)
  ├── Dataflow → df_ventas          (carga ventas_raw)
  ├── Notebook → nb_silver_clean    (raw → silver)
  ├── Stored Proc (Warehouse) → sp_load_dim_cliente
  ├── On success: Office365 Outlook → correo OK
  └── On failure: Teams → mensaje al canal de soporte
```

> Empieza siempre con un Pipeline madre que oriente todo el flujo: te dará trazabilidad y errores controlados.

<!--
Este patrón Pipeline madre + actividades hijo es el que replicaréis en el 80% de proyectos. La secuencia: Pipeline dispara Dataflow de clientes → si tiene éxito, Dataflow de ventas → si todo va bien, ejecuta el Notebook de limpieza silver → notifica al equipo por email/Teams. El beneficio principal: trazabilidad completa en el Monitoring Hub y reintentos automáticos en caso de error parcial.
-->

---

## Mirroring · ETL cero

- Workspace → **+ Nuevo → Mirrored database**.
- Selecciona origen: Azure SQL DB, Cosmos DB, Snowflake, Fabric SQL DB.
- En segundos aparece como base **espejo** sobre OneLake en Delta.
- Cualquier item Fabric puede leerla.

> En Aurora Energía: replicamos el ERP (Azure SQL) **sin construir ETL** para análisis. Coste: capacidad consumida + storage marginal.

<!--
Mirroring es lo más cercano a magia en Fabric para equipos que vienen de ETL tradicional. Sin construir un pipeline de réplica, en minutos tenéis una copia casi en tiempo real de vuestro Azure SQL, Cosmos DB o Snowflake sobre OneLake. El coste es marginal: capacidad consumida por la sincronización + storage en OneLake. Ideal para análisis sobre sistemas operacionales sin afectarlos. Limitación: solo para los orígenes soportados — consultar la lista actualizada en docs.
-->

---

## Demo en vivo · 15 min

**Parte 1 · Dataflow Gen2**
1. **+ Nuevo → Dataflow Gen2** → `df_clientes`.
2. *Get data → Text/CSV* → `clientes.csv`. Tipos correctos.
3. Destino: `lh_aurora.clientes`, modo **Replace**.
4. *Publish* y ejecutar.

**Parte 2 · Data Pipeline**
1. **+ Nuevo → Data pipeline** → `pl_aurora_ingesta`.
2. Actividad **Dataflow** → `df_clientes`.
3. Actividad **Copy data** → `productos.csv` → tabla `productos`.
4. Validar, ejecutar, abrir **Monitoring Hub**.

<!--
Demo en vivo. Tiempo estimado: 15 minutos. Parte 1 (8 min): Crear Dataflow Gen2, conectar a una fuente de ejemplo, aplicar una transformación básica, configurar destino al Lakehouse. Parte 2 (7 min): Crear Pipeline que invoca el Dataflow + una actividad de notificación. Mostrar el Monitoring Hub al final con la ejecución completada. Si el Dataflow tarda más de 2 min en el aula, pasar al siguiente paso y volver al resultado.
-->

---

<!-- _class: key -->

## Mensajes clave del bloque

- **Dataflow** transforma, **Pipeline** orquesta.
- Si tu origen es **operacional**, no construyas ETL: usa **Mirroring**.
- **Monitoring Hub es tu amigo** · úsalo siempre antes de pedir ayuda.

<!--
Pregunta: ¿qué usaríais para cargar datos desde un ERP on-premise al Lakehouse? Respuesta: si el ERP tiene API REST, un Dataflow Gen2 con el conector web. Si tiene base de datos SQL accesible, un Pipeline con Self-Hosted IR. Si es replicación continua y el origen lo soporta, Mirroring. El Monitoring Hub es obligatorio en producción — si no puedes ver qué falló, no puedes operar.
-->

---

<!-- _class: lead bare -->

# ☕ Descanso · 15 min
### Volvemos para Spark, Warehouse y Real-Time

<!--
Descanso de 15 minutos. Dejar el workspace abierto en el portal para que quienes quieran puedan explorar por su cuenta. Recordar que a la vuelta empezamos con Notebooks y Spark — el bloque más hands-on del día. Aprovechar el descanso para resetear la sesión de demo si es necesario.
-->

---

<!-- _class: section -->

<span class="module">M4 · 35 min</span>

# Notebooks y Spark
## La herramienta de transformación más potente

<!--
Transición a Notebooks y Spark. Spark en Fabric es diferente al Spark que muchos conocéis de Databricks o HDInsight: no hay cluster que aprovisionar, no se espera 5-10 minutos para el arranque. El Starter Pool arranca en ~15 segundos. Los Environments versionan las librerías junto con el código. Duración estimada: 30 minutos incluyendo demo.
-->

---

## Notebooks en Fabric

- Editor estilo **Jupyter** con celdas de código y markdown.
- Lenguajes: **PySpark**, **Spark SQL**, **Scala**, **SparkR / sparklyr**.
- Conexión nativa a uno o varios **Lakehouses** desde el panel *Explorer*.
- Ejecución sobre **Apache Spark gestionado** · sin provisionar cluster.

> En Fabric el Spark **ya está**. No esperas 5 minutos al pool: en segundos tienes sesión.

<!--
El Notebook es la herramienta de transformación más potente pero no la más rápida de configurar. Para transformaciones simples ya establecidas, usad Dataflow Gen2. Para lógica Python compleja, ML, o volúmenes donde Spark se amortiza (>1M filas), usad Notebook. La integración nativa con el Lakehouse adjunto es clave: no hay cadenas de conexión, no hay credenciales — el Notebook ve las tablas y ficheros directamente.
-->

---

## Spark gestionado · pools, environments, sessions

- **Starter Pool** · pool predeterminado, listo en segundos.
- **Custom pools** · tamaño, autoscale, librerías propias.
- **Environments** · paquetes Python/Java + configuración Spark + recursos. *Versionables y compartibles*.
- **Sessions** · ejecución activa. Pueden quedar **calientes** (high concurrency) entre celdas y notebooks.

<!--
El Starter Pool: listo en ~15 segundos, sin coste de arranque extra, se apaga automáticamente tras el tiempo de inactividad configurado. Los Custom Pools permiten escalar verticalmente para cargas ML pesadas o joins muy grandes. Los Environments son el equivalente a un requirements.txt + imagen Docker versionada: reproducibles, compartibles entre notebooks, y pinneables a una versión de Spark concreta. Preguntar: ¿alguien ha gestionado clusters Spark en el pasado? ¿cuánto tardaba el aprovisionamiento?
-->

---

## APIs que vas a usar

- **PySpark** · `spark.read.format("csv")`, `df.write.format("delta").saveAsTable(...)`.
- **Spark SQL** · celdas con `%%sql`. Ideal para perfil SQL puro.
- **NotebookUtils** (`notebookutils`) · OneLake, secretos, fs, jobs encadenados.
- **Pandas API on Spark** + **fabric-data-functions** · DataFrame *pandas-like* sobre Lakehouse.

<!--
Las tres APIs que usaréis el 90% del tiempo: spark.read/write para leer y escribir datos, %%sql (magic cell) para SQL puro en el notebook, y notebookutils para gestión de ficheros en OneLake y acceso a secretos de Key Vault. La Pandas API on Spark (pandas-on-Spark) permite usar código pandas casi igual que en local, con el motor Spark debajo — muy útil para migrar notebooks de pandas a Fabric sin reescribir todo. Preguntar: ¿alguien ha usado PySpark fuera de Fabric?
-->

---

## Acceso a OneLake desde Spark

```python
# Lectura de tabla del Lakehouse adjunto
df = spark.read.table("lh_aurora.clientes")

# Lectura de fichero en Files/
df_raw = (spark.read
              .option("header", True)
              .csv("Files/landing/ventas.csv"))

# Escritura como tabla Delta gestionada
(df_silver.write
          .mode("overwrite")
          .format("delta")
          .saveAsTable("ventas_silver"))
```

<!--
Mostrar el código detenidamente. Puntos clave: 1) spark.read.table() accede directamente a la tabla Delta del Lakehouse adjunto sin path explícito. 2) Para ficheros en la sección Files/, se usa el path relativo con Files/. 3) Siempre escribir en formato Delta (saveAsTable o write.format('delta')) para que los datos sean accesibles desde el SQL Endpoint y el modelo semántico. Avisar: si escribís en Parquet sin registrar la tabla, el SQL Endpoint no la verá.
-->

---

## Caso Aurora · de *bronze* a *silver*

Notebook **`nb_aurora_lab`** que:

1. Lee `clientes`, `productos`, `estaciones`, `ventas_raw`.
2. Limpia `ventas_raw` · descarta `importe <= 0`, normaliza fechas, deriva `año`, `mes`, `día_semana`.
3. *Join* con `productos` para añadir `categoria`, `unidad_medida`.
4. Escribe `ventas_silver` como tabla Delta.

<!--
Este es exactamente el notebook que haréis en el ejercicio de casa. Bronze: datos crudos con posibles errores de formato, valores nulos, duplicados. Silver: datos limpios, tipados correctamente, enriquecidos con joins. El paso crítico: filtrar ventas con importe <= 0 (datos de prueba del ERP que se cuelan). Normalizar fechas a formato DATE — esto es crítico para Direct Lake más adelante. El join entre las 4 tablas produce la tabla ventas_silver que alimentará el Warehouse.
-->

---

## Buenas prácticas

- Cabecera **markdown** en cada notebook: objetivo, inputs, outputs.
- `display(df)` en lugar de `df.show()` · visuales interactivos.
- Habilitar **Git integration** del workspace.
- Notebooks estables → **Spark Job Definition** invocable desde Pipeline.
- Para grandes volúmenes, **particionar Delta** por columna de baja cardinalidad (ej. `año`).

<!--
Tres recomendaciones que marcan la diferencia entre un proyecto amateur y uno profesional: 1) Cabecera markdown clara en cada notebook: ¿qué hace, qué consume, qué produce, quién lo mantiene? 2) Cuando el notebook esté estabilizado, convertirlo en Spark Job Definition para poder invocarlo desde Pipeline con parámetros y sin sesión interactiva. 3) Particionar las tablas Delta por fecha si superan los 10-20M de filas — mejora el rendimiento de lecturas filtradas por rango de fechas.
-->

---

<!-- _class: key -->

## Para llevarse a casa

- Spark en Fabric es **gestionado** y de pago **por uso real**.
- Notebook es la transformación más potente — **pero no la única**.
- Convierte notebooks estables en **Spark Job Definitions** y orquéstalos con Pipeline.

<!--
Pregunta: ¿cuándo usaría Notebook en lugar de Dataflow Gen2? Respuesta: cuando necesito lógica Python compleja (ML, NLP, custom transformations), cuando proceso volúmenes donde Spark se amortiza (normalmente >1 millón de filas), o cuando necesito integraciones que Dataflow no tiene como conector. El Spark Job Definition + Pipeline es el combo correcto para producción.
-->

---

<!-- _class: section -->

<span class="module">M5 · 30 min</span>

# Warehouse en profundidad
## Y el modo *Direct Lake* de Power BI

<!--
El Warehouse lo hemos visto en M2, pero ahora profundizamos en dos cosas: el modelado SQL para la capa gold y Direct Lake, que es la razón por la que Power BI brilla sobre Fabric de una manera que antes era imposible. Duración estimada: 35 minutos incluyendo demo.
-->

---

## Warehouse · refresco rápido

- T-SQL completo · DDL, DML, vistas, procs, funciones, transacciones multi-tabla.
- Almacena en **Delta-Parquet sobre OneLake** (visible desde el Lakehouse vía cross-DB).
- Soporta:
  - `CREATE TABLE AS SELECT` (CTAS) y `SELECT INTO`.
  - `MERGE` (vía pattern).
  - **Cross-database queries** a Lakehouse y a otros Warehouses.

<!--
Novedad clave que a menudo se pasa por alto: cross-database queries. Desde el Warehouse puedo hacer SELECT sobre tablas del Lakehouse del mismo workspace usando la notación de 3 partes: lakehouse_name.dbo.table_name. No hay copia, no hay ETL previo: lee directamente el Delta del Lakehouse en OneLake. Esto permite tener el Lakehouse como staging y el Warehouse como capa de servicio sin mover datos entre ellos — solo referencias.
-->

---

<!-- _class: tight -->

## Modelando el `gold` de Aurora

```sql
CREATE TABLE dim_cliente   (cliente_id INT, nombre NVARCHAR(150),
                            segmento NVARCHAR(20), pais NVARCHAR(50),
                            fecha_alta DATE);

CREATE TABLE dim_producto  (producto_id INT, nombre NVARCHAR(150),
                            categoria NVARCHAR(50), unidad NVARCHAR(20));

CREATE TABLE dim_estacion  (estacion_id INT, nombre NVARCHAR(150),
                            provincia NVARCHAR(50), tipo NVARCHAR(30));

CREATE TABLE dim_tiempo    (fecha DATE, anio INT, mes INT, dia INT,
                            trimestre INT, dia_semana INT);

CREATE TABLE fact_ventas   (venta_id BIGINT, fecha DATE,
                            cliente_id INT, producto_id INT, estacion_id INT,
                            cantidad DECIMAL(12,3), importe DECIMAL(12,2));
```

<!--
Este es el modelo en estrella de Aurora: 4 dimensiones + 1 tabla de hechos. El modelo Kimball clásico que el 90% de los clientes puede adoptar directamente. Si alguien pregunta por SCD (Slowly Changing Dimensions): se puede implementar con MERGE, pero para el curso usamos truncate-and-load para simplificar. Las claves sustitutas (surrogate keys) son enteros autoincrementales — más eficientes en Direct Lake que GUIDs.
-->

---

## Carga, vistas y seguridad

```sql
CREATE OR ALTER PROCEDURE sp_load_dim_cliente AS
BEGIN
  TRUNCATE TABLE dim_cliente;
  INSERT INTO dim_cliente
  SELECT cliente_id, nombre, segmento, pais, fecha_alta
  FROM lh_aurora.dbo.clientes;     -- cross-DB al Lakehouse
END;
```

- **RLS** · política basada en `USER_NAME()` o claim de Entra.
- **CLS** · `GRANT SELECT` sólo sobre columnas concretas.
- **OLS** · ocultar tablas / columnas a roles.
- **Dynamic Data Masking** · enmascarar DNI, email, teléfono.

<!--
El stored procedure de carga usa cross-DB para leer del Lakehouse — notar la notación lh_aurora.dbo.clientes. Row-Level Security (RLS): el comercial de Madrid solo ve las ventas de las estaciones de Madrid. Column-Level Security (CLS): el analista junior no ve la columna margen_neto. Object-Level Security (OLS): el rol externo no ve ni la tabla dim_cliente. Dynamic Data Masking (DDM): el teléfono del cliente aparece como XXXX-XXX-XXX para ciertos roles. Recomendación: empezad siempre por RLS, que es el más maduro y soportado en Power BI.
-->

---

## Direct Lake · *el santo grial* del modelo semántico

- Power BI lee **directamente las tablas Delta** del Lakehouse / Warehouse.
- **Velocidad de Import + frescura de DirectQuery, sin coste de refresh.**
- **Fallback automático a DirectQuery** si la consulta excede límites.
- Requisitos:
  - Capacidad **F-SKU** (Trial vale).
  - Modelo creado desde el item Lakehouse / Warehouse.
  - Columnas tipadas correctamente.
  - Sin transformaciones complejas en el modelo.

<!--
Direct Lake es el cambio de paradigma de Power BI en Fabric. El dilema clásico: Import era rápido pero con datos fríos (refresh programado). DirectQuery era datos frescos pero lento (query a la BD por cada visual). Direct Lake es rápido Y fresco: lee directamente el Delta-Parquet de OneLake en modo columnar. El fallback a DirectQuery existe como safety net, pero con un buen modelo Delta bien mantenido raramente se activa. Condición: los datos deben estar en formato Delta en OneLake.
-->

---

## Direct Lake on OneLake (DLOL)

- PBIP "vacío" desde Power BI Desktop apunta al Lakehouse vía DLOL.
- **Independiente del Lakehouse origen** → mejor para *multi-tenant* y para mover el modelo entre workspaces sin recrearlo.
- Encaje natural: ISVs, productos data, plantillas reutilizables.

<!--
DLOL es la variante avanzada para ISVs y escenarios multi-tenant. En lugar de referenciar el Lakehouse del mismo workspace, el modelo semántico apunta al OneLake path via URL directa. Esto permite tener un modelo semántico maestro que apunta a los datos del cliente A, B, C sin tener que crear un modelo por cliente. Todavía en preview — revisar la documentación para la disponibilidad actual.
-->

---

## Demo en vivo · 12 min

1. En `wh_aurora` ejecutar el DDL de las 5 tablas + `sp_load_dim_cliente`.
2. Cross-DB al Lakehouse para llenar `fact_ventas`.
3. Crear vista `vw_kpi_ventas_diarias`.
4. **+ Nuevo modelo semántico** desde el Warehouse · 5 tablas + vista. Relaciones.
5. Reporte nuevo · matriz **año / categoría / SUM(importe)**. Comentar tiempos.
6. Verificar en propiedades del modelo que está en **Direct Lake**.

<!--
Demo en vivo. Tiempo estimado: 12 minutos. Secuencia: ejecutar el DDL de las 5 tablas → ejecutar el stored proc de carga → crear la vista de producto → crear el modelo semántico y verificar que está en modo Direct Lake (en las propiedades del modelo debe aparecer 'Direct Lake'). Crear un reporte rápido para demostrar el tiempo de respuesta. Si hay tiempo, simular el fallback generando una query muy compleja.
-->

---

<!-- _class: key -->

## Mensajes clave

- Warehouse es la pieza para el equipo SQL clásico — pero **comparte storage** con Lakehouse.
- **Direct Lake** elimina el dilema clásico *Import vs DirectQuery*.
- Cuanto más limpio el Delta, mejor el rendimiento de Direct Lake.

<!--
Pregunta: ¿qué ventaja tiene Direct Lake sobre Import para un reporte que se actualiza cada hora con datos del ERP? Respuesta: eliminas el coste y la latencia del refresh (que en Import puede tomar 20-30 minutos). Con Direct Lake, los datos son frescos siempre que el Delta se actualiza, y el rendimiento es comparable a Import gracias al column store nativo en OneLake.
-->

---

<!-- _class: section -->

<span class="module">M6 · 25 min</span>

# Real-Time Intelligence
## Eventstream, Eventhouse y KQL

<!--
Real-Time Intelligence es el componente más diferencial de Fabric respecto a Power BI Premium clásico o Databricks. Eventhouse + KQL es el motor ideal para series temporales, logs de máquinas e IoT. Activator cierra el círculo: del dato al acto sin necesidad de código extra. Duración estimada: 25 minutos incluyendo demo.
-->

---

<!-- _class: tight -->

## Mapa de la Real-Time Intelligence

```text
[Origen: IoT Hub, Event Hub, Kafka, sample]
            ↓
       Eventstream
            ↓
   ┌────────┼─────────┐
   ↓        ↓         ↓
Eventhouse  Lakehouse  Activator
 (KQL DB)   (Delta)    (alertas)
```

- **Eventstream** · ingesta no-code, transformaciones simples.
- **Eventhouse / KQL DB** · motor analítico para series temporales y logs.
- **Activator** · motor de reglas → correo, Teams, Power Automate, Pipeline.
- **Real-Time Dashboard** · estilo Grafana / Kusto Explorer integrado.

<!--
Recorrer el diagrama de izquierda a derecha. Eventstream recoge datos del origen (Event Hub, IoT Hub, Kafka, CDC de base de datos) y los enruta al destino: Eventhouse para análisis en tiempo real, Lakehouse para histórico en Delta, Activator para reaccionar automáticamente. El KQL Queryset es el editor de queries sobre el Eventhouse. El Real-Time Dashboard es el reporte de baja latencia sobre el Eventhouse.
-->

---

## ¿Eventhouse o Lakehouse?

| Caso | Mejor opción |
|---|---|
| Telemetría IoT, logs, clickstream, security events | **Eventhouse / KQL** |
| Histórico analítico de negocio (ventas, finanzas) | **Lakehouse / Warehouse** |
| Query en milisegundos sobre miles de millones de eventos | **Eventhouse** |
| Unión a un modelo dimensional de negocio | **Lakehouse / Warehouse** |

<!--
La regla de oro para decidir: Si la pregunta tiene 'en los últimos N minutos/horas' o 'cuántos eventos por segundo', es Eventhouse. Si la pregunta es sobre análisis histórico de negocio (ventas del año pasado, tendencias mensuales), es Lakehouse/Warehouse. En Aurora: la telemetría de surtidores (temperatura, caudal, errores en tiempo real) va al Eventhouse; los datos de ventas consolidados del ERP van al Lakehouse.
-->

---

## KQL en 5 minutos

```kql
// Top 10 estaciones por número de eventos en las últimas 24 h
TelemetriaSurtidor
| where Timestamp > ago(24h)
| summarize Eventos = count() by EstacionId
| top 10 by Eventos desc

// Detección de surtidores con caudal anómalo
TelemetriaSurtidor
| where Timestamp > ago(1h)
| summarize CaudalMedio = avg(Caudal)
            by EstacionId, SurtidorId, bin(Timestamp, 5m)
| where CaudalMedio < 0.5 or CaudalMedio > 80
```

> Sintaxis *pipe-based* · si vienes de SQL, lo aprendes en una tarde.

<!--
KQL (Kusto Query Language) tiene una sintaxis de pipeline con el operador | que es muy intuitiva para quien viene de UNIX o de pandas. summarize es el GROUP BY, where es el WHERE, project es el SELECT. Para quien viene de SQL, en 30 minutos se aprende lo básico para ser productivo. Las dos queries mostradas son exactamente las que usaréis en el ejercicio de la demo. Remarcar: KQL está optimizado para rangos de tiempo — las queries sobre series temporales son 10-100x más rápidas que el SQL equivalente sobre datos del mismo volumen.
-->

---

## Caso Aurora · telemetría de surtidores

- 250 estaciones × 6 surtidores · evento cada 30 s.
- Eventstream desde Event Hub (en aula simulamos con **Sample data**).
- Tabla `TelemetriaSurtidor` con `Timestamp`, `EstacionId`, `SurtidorId`, `Producto`, `Caudal`, `Temperatura`, `Estado`.
- Dashboard · eventos/min, caudal medio, top alertas, mapa.
- **Activator** · *si `Temperatura > 65 °C` durante > 3 min, avisar al jefe de estación*.

<!--
250 estaciones × 6 surtidores × un evento cada 30 segundos = 3.000 eventos/minuto = 180.000 eventos/hora. Eso es imposible de gestionar con Power BI clásico en DirectQuery sobre SQL. Con Eventhouse, es trivial: ingesta en milisegundos, queries en segundos sobre millones de filas. El Activator: si la temperatura supera 65°C en cualquier surtidor, se dispara automáticamente una alerta al responsable de operaciones sin código adicional.
-->

---

## Demo en vivo · 10 min

1. Crear `eh_aurora_telemetria` (Eventhouse).
2. Crear **Eventstream** + *Sample data → Bicycle rentals*.
3. *Destination → Eventhouse*, mapear a `TelemetriaSurtidor`.
4. Esperar 30 s y abrir **KQL Queryset**.
5. Lanzar las 3 queries adaptadas al esquema generado.
6. Crear un **Real-Time Dashboard** con un par de tiles.
7. Crear un **Activator** simple sobre `Caudal`.

<!--
Demo en vivo. Tiempo estimado: 10 minutos. Como no tenemos un Event Hub real en el aula, usamos los sample data del portal de Fabric (Bicycle Rentals o Automotive). Adaptar los nombres de columnas en las queries. Puntos a mostrar: 1) Creación del Eventhouse y del KQL Database. 2) Creación del Real-Time Dashboard con 2-3 tiles. 3) Creación de una regla básica en Activator. Este último paso suele impresionar mucho a la audiencia — la reacción automática sin código.
-->

---

<!-- _class: key -->

## Mensajes clave

- **KQL no asusta** · para un SQL-ero se aprende en una tarde.
- Eventhouse **no reemplaza** al Warehouse: convive con él.
- **Activator** cierra el círculo · del dato al **acto**.

<!--
Pregunta: ¿Activator puede enviar un mensaje a un canal de Teams? Respuesta: sí, es una de las acciones disponibles de fábrica. También puede enviar email, llamar a un webhook de Power Automate, o invocar un Pipeline de Fabric para desencadenar un proceso más complejo. Segundo punto: KQL y SQL conviven en el mismo workspace — el analista de negocio usa el reporte de Power BI, el ingeniero usa KQL Queryset.
-->

---

<!-- _class: section -->

<span class="module">M7 · 25 min</span>

# Power BI sobre Fabric
## Modelo semántico Direct Lake y publicación

<!--
Ya tenemos el dato ingerido, limpio, modelado y con capacidad real-time. Ahora lo consumimos. Power BI en Fabric es más potente que nunca gracias a Direct Lake y al versionado del modelo con PBIP. Duración estimada: 30 minutos incluyendo demo.
-->

---

## Tipos de modelo semántico

- **Default semantic model** del Lakehouse → tablas detectadas automáticamente, sin relaciones.
- **Custom semantic model** → recomendado para producción:
  - Relaciones, jerarquías, medidas DAX, perspectivas, **RLS**.
- Se crea desde el item Lakehouse/Warehouse o desde **Power BI Desktop** apuntando a Fabric.

<!--
El Default Semantic Model que genera automáticamente el Lakehouse o el Warehouse es un buen punto de partida para exploración, pero NO lo uses en producción. Motivos: incluye todas las tablas sin relaciones, sin medidas DAX, sin jerarquías. El Custom Semantic Model es donde añades relaciones, medidas DAX, perspectivas y RLS. Regla: siempre crear un Custom Semantic Model para los reportes que van a usuarios finales.
-->

---

<!-- _class: tight -->

## DAX típico para Aurora

```dax
Importe Total = SUM(fact_ventas[importe])

Litros Vendidos = SUM(fact_ventas[cantidad])

Importe Año Anterior =
CALCULATE([Importe Total], SAMEPERIODLASTYEAR(dim_tiempo[fecha]))

Variación % =
DIVIDE([Importe Total] - [Importe Año Anterior], [Importe Año Anterior])

Top 5 Estaciones =
CALCULATE([Importe Total], TOPN(5, dim_estacion, [Importe Total]))
```

<!--
Leer las medidas una a una. Puntos a destacar: 1) DIVIDE(numerador, denominador, 0) evita el error de división por cero. 2) CALCULATE + SAMEPERIODLASTYEAR es el patrón estándar para comparar con el año anterior. 3) TOPN sobre la dimensión de estaciones usa filter context — este tipo de query en DirectQuery era lento; con Direct Lake es instantáneo. Preguntar: ¿alguien tiene experiencia con DAX? ¿cuáles son las medidas más complejas que habéis escrito?
-->

---

## Publicación, apps y subscriptions

- Reportes web directos en Fabric, o publicados desde Power BI Desktop.
- **Apps** · empaquetan reportes para colectivos (lectores Free necesitan F64+).
- **Subscriptions** programadas, **data alerts**, **comments**.
- **OneLake hub** del workspace · catálogo de items por workspace.

<!--
Las Apps de Power BI siguen siendo la forma estándar de distribuir reportes en organizaciones grandes. El beneficio: el consumidor no ve el workspace, solo la App — más limpio y controlado. Con F64+: los usuarios Free pueden consumir la App sin licencia Pro. Las subscriptions permiten enviar capturas del reporte por email de forma programada — muy útil para directivos que prefieren recibir el resumen diario en el correo.
-->

---

## PBIP y Git

- Power BI Desktop guarda en formato **.pbip** (carpeta + JSON / TMDL / PBIR).
- Workspaces de Fabric con **Source control** integrado (Azure DevOps o GitHub).
- Permite **revisar PRs** sobre el modelo semántico y los reportes.

> En 2026 ya no hay excusa: el modelo y el reporte son **código versionable**.

<!--
PBIP (Power BI Project) es el formato de archivo que convierte el modelo y el reporte en texto plano versionable con Git. En Fabric, la integración Git está en el workspace: conectáis el workspace a Azure DevOps o GitHub y los cambios se sincronizan automáticamente. Esto permite code review de modelos DAX, branching, y deployment pipelines entre dev/test/prod. Si el equipo usa Azure DevOps, la integración es nativa — no necesitáis plugins externos.
-->

---

## Direct Lake · buenas prácticas

- Tablas Delta con **tipos correctos** (no `STRING` para fechas).
- **Particionar** columnas grandes ayuda al *column store*.
- Evitar **calculated columns** complejas en el modelo · llévalas al Lakehouse / Warehouse.
- Vigilar el **fallback to DirectQuery** en el indicador del modelo.

<!--
El error más común que veo en proyectos: columnas de fecha guardadas como STRING en Delta. Direct Lake no puede construir el column store correctamente sobre strings que representan fechas. Aseguraos de que todas las fechas son DATE o DATETIME en la tabla Delta antes de crear el modelo. Segundo error frecuente: columnas calculadas en DAX sobre tablas grandes con Direct Lake — prefieran siempre calcular en el Notebook o en el Warehouse y almacenar la columna calculada en Delta.
-->

---

## Demo en vivo · 12 min

1. Desde `wh_aurora` → **Nuevo modelo semántico** → 5 tablas + vistas.
2. Renombrar a `sm_aurora_ventas`. Crear relaciones (estrella).
3. Añadir las medidas DAX.
4. **+ Nuevo reporte** · KPI *Importe Total*, barras por categoría, mapa por provincia, tabla top 10 clientes.
5. Publicar y mostrar el item en el workspace.
6. Mostrar **App** vacía y cómo se publicaría.
7. Mostrar **Source control** del workspace conectado a un repo Git de demo.

<!--
Demo en vivo. Tiempo estimado: 12 minutos. El modelo semántico sm_aurora_ventas es el mismo que vimos en M5 pero ahora añadimos las 5 medidas DAX y las relaciones entre tablas. Verificar que el modo es Direct Lake (propiedades del modelo semántico en el portal). Crear el reporte con 3-4 visualizaciones: ventas por estación, evolución mensual, top 5 productos. Si hay tiempo, mostrar la conexión del workspace a Azure DevOps y la sincronización Git.
-->

---

<!-- _class: tight -->

## Cierre · todo lo de hoy en una imagen

```text
CSV/Excel → Dataflow Gen2 → Lakehouse (bronze)
                                ↓
                         Notebook Spark
                                ↓
                        Lakehouse (silver)
                                ↓
                  Stored Proc Warehouse
                                ↓
                         Warehouse (gold)
                                ↓
                Direct Lake → Semantic Model
                                ↓
                          Reporte Power BI

(en paralelo)
Event Hub → Eventstream → Eventhouse → KQL Dashboard / Activator
```

<!--
Este diagrama es el resumen de todo lo que hemos construido hoy. Guardadlo o haced una foto: es la referencia del patrón Fabric estándar que lleváis a vuestros proyectos. El flujo vertical (batch): CSV → Dataflow/Pipeline → Lakehouse bronze → Notebook silver → Warehouse gold → Direct Lake → Power BI. El flujo en paralelo (real-time): Eventstream → Eventhouse → KQL Dashboard + Activator. Ambos flujos comparten OneLake como storage único — esa es la magia de la plataforma.
-->

---

## Deberes para casa antes de la Jornada 2

- Completa los **ejercicios** de `ejercicios/jornada-1/`.
- Tu workspace `aurora-curso-fabric` debe tener:
  - Lakehouse + Warehouse poblados.
  - Notebook ejecutado.
  - Pipeline programado.
  - Reporte Power BI publicado.
- Lectura ligera del índice de `ejercicios/jornada-2/` para llegar contextualizado a **Purview** y **Fabric IQ**.

<!--
Los ejercicios están en la carpeta ejercicios/jornada-1/ del repositorio del curso. Son progresivos: primero el workspace, luego la ingesta, luego el notebook, luego el warehouse, luego el reporte Direct Lake. Cada ejercicio tiene su README con instrucciones paso a paso. Si os quedáis atascados, el canal de Teams del curso está disponible durante 2 semanas. El objetivo: llegar a la Jornada 2 con el workspace aurora-curso-fabric construido y los datos cargados.
-->

---

<!-- _class: lead bare -->

# ¡Hasta la **Jornada 2**!
## *Purview · Fabric IQ · gobierno y agentes de datos*

### Si te atascas, abre un issue en el repo del curso o pásate por el canal de Teams del curso.

<!--
Preguntas finales — dar 5-10 minutos. Si hay preguntas específicas de proyectos de los asistentes, responder brevemente o dejar para el canal. Recordar la fecha de la Jornada 2: Purview + Fabric IQ. Invitar a explorar el workspace durante las próximas semanas y a traer dudas al canal de Teams. Agradecimiento al equipo organizador e Intelequia.
-->
