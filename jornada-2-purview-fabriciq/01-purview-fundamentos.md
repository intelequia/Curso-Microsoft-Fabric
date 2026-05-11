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
| **Data Governance** | Data Map, Unified Catalog (incl. Data Quality, Lineage y Health Management como features), Data Products, Data Access Policies | `purview.microsoft.com` |
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

### 4. Gobierno federado sobre Fabric · dos capas

Existen dos formas complementarias de gobernar Fabric desde Purview, con requisitos distintos:

#### Purview Hub for Fabric (sin scan, integrado en Fabric)

Accesible desde el workspace **Admin monitoring** de Fabric (solo Fabric Admins). Es un informe de monitoring que proporciona insights sobre:

- **Sensitivity labels** aplicadas a items del tenant.
- **Endorsements** (Promoted, Certified) y dominios.
- Exposición de datos sensibles y actividad de clasificación.

No requiere configuración de scan en Purview. No realiza catalogación completa en el Data Map.

#### Purview Data Map — scan de Fabric (Purview Enterprise, requiere configuración)

Para que los items de Fabric aparezcan en el **Purview Data Map** con metadatos, esquemas, clasificaciones automáticas y lineage completo, hay que:

1. Registrar el tenant de Fabric como fuente en Purview Data Map.
2. Configurar autenticación (Managed Identity o Service Principal) y habilitar las Admin APIs de Fabric.
3. Crear y ejecutar scans (programados o puntuales).

Lo que **sí funciona de forma nativa** sin scan en Purview:

- Aplicación de **sensitivity labels** directamente en Fabric (Lakehouse, Warehouse, modelo semántico, report).
- **Endorsements** (Promoted, Certified) gestionados desde el portal de Fabric.
- **Data Quality scores** en el Unified Catalog (requieren definir reglas DQ, no scan de Data Map).

### 5. Microsoft Fabric Capacity Metrics App

Herramienta de monitorización del consumo de capacidad (CU — Capacity Units) para Fabric y Power BI Premium.

**Prerequisitos:**
- Ser **Capacity admin** de al menos una capacidad Fabric/Power BI Premium.
- Licencia **Power BI Pro, PPU** o trial individual de Power BI.

**Instalación primera vez:**
1. Ir a [AppSource → Microsoft Fabric Capacity Metrics](https://go.microsoft.com/fwlink/?linkid=2219875) y seleccionar *Get it now*. Alternativamente: en el servicio Power BI → Apps → Get apps → buscar "Microsoft Fabric" → seleccionar la app.
2. Completar el registro en AppSource y seleccionar **Install** en la ventana de Fabric.
3. En Fabric (cambiar a experiencia Power BI) → **Apps** → seleccionar *Microsoft Fabric Capacity Metrics* → **Connect**.
4. Configurar parámetros:
   - `UTC_offset`: desplazamiento UTC de la organización (p.ej. `1` para CET, `5.5` para IST).
   - `Advanced` (opcional): deshabilita la actualización automática a medianoche.
5. Seleccionar método de autenticación **OAuth2** y nivel de privacidad **Organizational** → *Sign in and continue*.
6. Seleccionar la capacidad en el desplegable → la primera carga puede tardar unos minutos.

**Actualización:** no hay que borrar la versión anterior; reinstalar desde AppSource actualiza la app en el mismo workspace.

**Entornos Government Cloud:**
- GCC: <https://aka.ms/FabricUSGovCapacityUsageReport>
- GCC High: <https://aka.ms/FabricUSGovHighCapacityUsageReport>
- DoD: <https://aka.ms/FabricUSGovDodCapacityUsageReport>

> ⚠️ Instalar la app en un workspace con licencia **Pro** para evitar que su propio consumo impacte la capacidad que monitoriza.

> Ref: <https://learn.microsoft.com/en-us/fabric/enterprise/metrics-app-install>

### 6. Entorno mínimo para Jornada 2

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
- "El **Purview Hub for Fabric** da visibilidad de gobierno sin configurar scans; la **catalogación completa en Purview Data Map sí requiere configurar el scan** del tenant de Fabric."
- "Sin gobierno, Fabric escala como cualquier data lake: hacia el caos."
