# J2-M1 · Por qué gobierno: panorama de Microsoft Purview y Fabric

**Duración:** 30 min · **Formato:** explicación + benchmark + demo corta

## Objetivos

1. Entender por qué el gobierno del dato es el "tema serio" cuando una organización adopta Fabric.
2. Conocer la suite **Microsoft Purview** y todos sus módulos (no solo Data Map).
3. Diferenciar **Purview Data Governance** vs **Purview Information Protection** vs **Purview Compliance / Risk Management**.
4. Mapear cada necesidad típica de gobierno con el módulo de Purview que la cubre.

## Hilo narrativo

> "En Aurora Energía hemos montado en una mañana un Lakehouse, un Warehouse y un par de modelos semánticos. Buenísimo. ¿Pero quién sabe **qué hay**, **quién accede**, **qué es PII** y **qué pasa si alguien se descarga un Excel con DNIs**? Para esto existe Purview. Y para que el alumno no se pierda: Purview ha cambiado de nombre y de ámbito **dos veces** en los últimos cinco años. Hoy es un paraguas con varios productos."

## Contenido

### 1. Mapa de Microsoft Purview (2026)

Microsoft Purview se organiza en torno a tres grandes áreas:

| Área | Capacidades clave | Portal |
| --- | --- | --- |
| **Data Governance** | Data Map, Unified Catalog (incl. Data Quality y Lineage como features), Estate Insights, Data Products, Data Access Policies | `purview.microsoft.com` |
| **Information Protection** | Sensitivity labels, Auto-labeling, Encryption, Rights Management | `purview.microsoft.com` |
| **Risk & Compliance** | DLP (Data Loss Prevention), Insider Risk, Communication Compliance, eDiscovery, Audit, Records Management, Compliance Manager | `purview.microsoft.com` |

> **Cambio de marca clave**: lo que antes se llamaba "Microsoft 365 Compliance Center" hoy es **Microsoft Purview Compliance Portal**. Lo que antes era "Azure Purview" hoy es **Microsoft Purview Data Governance**. Es el mismo portal, dos áreas.

### 2. Por qué gobernar Fabric

- Fabric centraliza datos antes dispersos → el riesgo de exposición sube.
- OneLake permite que cualquier workspace lea/escriba → **disciplina o caos**.
- **Compliance** (GDPR, esquema nacional de seguridad, ISO 27001, NIS2) exige clasificar, rastrear y proteger.
- El negocio **necesita encontrar** los datos: un Catálogo es la única forma escalable.

### 3. Diferenciación clave

| Necesidad | Módulo Purview |
| --- | --- |
| ¿Qué datos tengo y dónde? | Data Map + Unified Catalog |
| ¿Quién tiene acceso? | Data Access Policies + integración Fabric |
| ¿Cómo encuentro el dato que busco? | Unified Catalog + Búsqueda |
| ¿Cómo sé si un dataset es de calidad? | **Unified Catalog** → Data Quality *(feature integrada)* |
| ¿De dónde viene esta tabla? | **Data Map + Unified Catalog** → Lineage *(feature integrada)* |
| ¿Qué columnas son PII / financieras? | **Information Protection** (sensitivity labels + Classifiers) |
| ¿Cómo evito que alguien pegue un DNI en Teams? | DLP + Communication Compliance |
| ¿Cómo cumplo GDPR / borrado? | **Data Lifecycle Management + Records Management + eDiscovery** |
| ¿Quién está descargando datasets sensibles? | Insider Risk + Audit + Activity Explorer |
| ¿Qué tan maduro estoy en compliance? | Compliance Manager |

### 4. La novedad: gobierno **federado** sobre Fabric

Desde 2024, todo lo que ocurre dentro de Fabric (workspaces, Lakehouses, Warehouses, semantic models, reports) **se ve y se gobierna desde Purview** sin necesidad de scan tradicional. Esto se llama **Microsoft Purview hub for Fabric** y se accede desde:

- El propio portal de Fabric (icono Purview hub).
- El portal de Purview Data Governance (Fabric aparece como source nativa).

Esta integración permite:

- Catalogación automática de items de Fabric.
- Aplicación de **sensitivity labels** a Lakehouse, Warehouse, semantic model y report (heredado de M365).
- **Data lineage** automático entre items Fabric (Lakehouse → Notebook → Warehouse → Semantic Model → Report).
- **Endorsements** (Promoted, Certified) y **Data Quality scores**.

### 5. Entorno mínimo para Jornada 2

| Item | ¿Imprescindible? |
| --- | --- |
| Tenant M365 con licencia E5 / E5 Compliance (trial vale) | Recomendado para Information Protection y DLP |
| Acceso a `purview.microsoft.com` | ✅ |
| Workspace Fabric con items reales (de Jornada 1) | ✅ |
| Sensitivity labels publicadas en el tenant | ✅ — incluido en E5 |
| Cuenta admin del tenant (al menos uno por equipo) | ✅ |

## Demo en vivo (8 min)

1. Abrir `purview.microsoft.com` → mostrar la home y los **solution areas** (Data Map, Unified Catalog, Information Protection, Data Loss Prevention, Insider Risk, etc.).
2. Entrar a **Unified Catalog** → mostrar que ya aparecen los items del workspace `aurora-curso-fabric` (gracias a la integración nativa).
3. Abrir uno (ej. `lh_aurora`) y mostrar **lineage**, **schema**, **sensitivity label** (vacía aún).
4. Volver a Fabric, abrir el mismo Lakehouse y mostrar el icono **Microsoft Purview** en la barra superior.

## Mensajes clave

- "Purview es un paraguas. No te quedes solo con Data Map."
- "Para Fabric, no necesitas hacer scan: la integración nativa publica todo automáticamente."
- "Sin gobierno, Fabric escala como cualquier data lake: hacia el caos."
