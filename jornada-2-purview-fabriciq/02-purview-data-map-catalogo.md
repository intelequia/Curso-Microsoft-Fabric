# J2-M2 · Purview Data Map y Unified Catalog

**Duración:** 40 min · **Formato:** explicación + demo en vivo + ejercicio corto

## Objetivos

1. Entender el **Data Map** (inventario técnico) y el **Unified Catalog** (capa de negocio).
2. Conocer **glossary terms, data products, OKRs y critical data elements**.
3. Saber cómo **escanear** una fuente externa (ej. Azure SQL, ADLS) y conectarla con Fabric.
4. Aprender a publicar **Data Products** en el Catalog con dueño, descripción y términos asociados.

## Contenido

### 1. Data Map — capa técnica

- Inventario de assets de datos: tablas, ficheros, modelos, dashboards, columnas.
- Se alimenta de **conexiones**:
  - Cloud nativo: Fabric (automático), Azure SQL, Synapse, ADLS Gen2, Databricks, Snowflake, Power BI, etc.
  - On-prem: SQL Server, Oracle, Teradata, ficheros (vía **Self-Hosted Integration Runtime**).
  - SaaS: Salesforce, ServiceNow, Workday, etc.
- Cada conexión tiene **scans** programables que descubren esquemas y aplican **classifications** automáticas (ej. "EU Passport Number", "Credit Card Number").

### 2. Unified Catalog — capa de negocio

- Vista para usuarios funcionales (analistas, owners de dato).
- Estructura por **Business Domain → Data Product → Data Asset**.
- Conceptos clave:
  - **Glossary terms**: vocabulario común ("Cliente Comercial", "Volumen Vendido", "PII").
  - **Critical Data Elements (CDE)**: las columnas/atributos que la organización ha decretado críticos.
  - **OKRs / Goals**: objetivos asociados a Data Products.
  - **Health controls**: indicadores automatizados de calidad, uso, propiedad.
  - **Endorsements**: Promoted ✅, Certified ⭐.

### 3. Data Quality

- Reglas DQ (rule templates) sobre tablas Delta, Lakehouse, Warehouse, etc.
- Tipos: completeness, uniqueness, validity, accuracy, freshness.
- Resultado: **score** numérico por dataset, evolución histórica, alertas.

### 4. Data Lineage

- Automático para Fabric (Lakehouse → Notebook → Warehouse → Semantic Model → Report).
- Manual / programático con APIs / OpenLineage para fuera de Fabric.
- Vista visual con drill-down.

### 5. Data Access Policies

- Permite **conceder acceso a un dato desde Purview** sin entrar a la herramienta origen.
- Federa: ADLS Gen2, Azure SQL DB, Fabric (preview/GA según fecha).

### 6. Caso Aurora Energía

Vamos a publicar un **Data Product** llamado **"Ventas Aurora — Gold"** que agrupa el Warehouse `wh_aurora` y el modelo semántico `sm_aurora_ventas`. Le asociaremos:

- **Dominio**: "Comercial".
- **Glossary terms**: "Importe de Venta", "Estación de Servicio", "Cliente Comercial".
- **Critical Data Element**: `cliente_id`, `importe`.
- **Owner**: usuario "Marisa Ledesma" (ficticio).
- **Endorsement**: Certified.

## Demo en vivo (15 min)

1. Abrir Purview → **Unified Catalog → Governance domains**. Crear `Comercial`.
2. Crear los glossary terms necesarios.
3. Crear el **Data Product** `Ventas Aurora — Gold` y enlazar `wh_aurora` y `sm_aurora_ventas`.
4. Asignar owner, términos, endorsement.
5. Mostrar **lineage** del Data Product (debería pintar el flujo de Jornada 1).
6. Crear una **DQ rule** simple sobre `fact_ventas`: `importe IS NOT NULL`.
7. Mostrar el dashboard del Data Product.

## Ejercicio corto en aula (8 min)

Cada alumno crea su propio **Glossary term** "Importe de Venta" y lo asocia a su `wh_aurora.fact_ventas[importe]`.

## Mensajes clave

- "Data Map es el inventario, Catalog es la tienda."
- "Sin owners, no hay gobierno — empieza por asignar dueños."
- "El lineage automático es la mejor demostración del valor inmediato de Purview."
