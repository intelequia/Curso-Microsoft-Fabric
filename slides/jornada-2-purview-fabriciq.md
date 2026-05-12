---
marp: true
theme: intelequia
paginate: true
size: 16:9
title: "Jornada 2 · Microsoft Purview, Data agents y Fabric IQ"
description: "Master class de 4 horas: gobierno del dato con Purview, integración con Fabric, Data agents sobre datos gobernados y panorama del workload Fabric IQ (preview)"
author: Intelequia
math: katex
---

<!-- _class: lead bare -->

<span class="tag">Curso · Jornada 2 de 2</span>

# **Purview** + **Data agents**
## Gobernar el dato y convertirlo en *conocimiento accionable*

### 4 horas · master class · caso *Aurora Energía*

<!--
Bienvenida a la Jornada 2. Preguntar: ¿quién completó los ejercicios de Jornada 1? ¿Alguien se quedó atascado en algún punto? Recordar que hoy el foco es el gobierno del dato (Purview) y la capa conversacional sobre dato gobernado (Data agents). El workload Fabric IQ se presenta como visión y roadmap (preview). Sin lo de hoy, Fabric es potente pero no controlable ni escalable en una organización real. El hilo conductor sigue siendo Aurora Energía — usamos el mismo workspace de ayer.
-->

---

## Repaso exprés de la Jornada 1

- Construimos un **flujo end-to-end** sobre Aurora Energía:
  - Lakehouse `lh_aurora` → Notebook Spark → Warehouse `wh_aurora`.
  - Modelo semántico `sm_aurora_ventas` en **Direct Lake**.
  - Real-Time con `eh_aurora_telemetria` + KQL.
- Ahora viene la pregunta incómoda:
  - ¿Quién sabe **qué hay** en OneLake?
  - ¿Quién accede a **qué**?
  - ¿Qué pasa si alguien se descarga un Excel con **DNI** de clientes?

> **Hoy ponemos disciplina** (Purview) **y razonamiento conversacional** (Data agents) sobre lo que ya construimos.

<!--
Recorrer el flujo rápidamente. Las preguntas incómodas son el hilo conductor de la jornada de hoy: ¿quién sabe exactamente qué hay en OneLake? ¿quién accede a qué datos y con qué permisos? ¿qué pasa si un empleado descarga datos de clientes con DNI? Esas tres preguntas las respondemos con Purview en los bloques M1-M4. Preguntar si alguien tiene ya Purview en su organización o si es la primera vez que lo ven.
-->

---

## Agenda · 4 h con descanso de 15 min

| Bloque | Min | Tema |
|---|---|---|
| **M0** | 15 | Repaso Jornada 1 + agenda |
| **M1** | 30 | Por qué gobierno · panorama Purview |
| **M2** | 40 | Purview Data Map + Unified Catalog |
| **M3** | 30 | Information Protection y DLP |
| ☕ | 15 | **Descanso** |
| **M4** | 25 | Integración Purview ↔ Fabric |
| **M5** | 30 | Data agents · fundamentos y posicionamiento |
| **M6** | 35 | Construyendo un Data agent end-to-end |
| **M6.5** | 5 | Workload Fabric IQ (preview) · visión y roadmap |
| **M7** | 25 | Casos de uso, hoja de ruta, cierre |

<!--
Misma estructura que J1: bloques teóricos + demos en vivo + descanso a mitad. M1-M3 es Purview (gobierno, catalogo, protección). M4 es la integración bidireccional Purview↔Fabric. M5-M6 es la parte conversacional sobre dato gobernado: Data agents — capacidad disponible que construimos paso a paso. M6.5 es un cierre conceptual sobre el workload Fabric IQ (preview) y cómo Data agents se inscribe en él. M7 es la hoja de ruta para llevarlo a vuestra organización. Preguntar si el foco de interés está más en governance/compliance o en IA.
-->

---

<!-- _class: section -->

<span class="module">M1 · 30 min</span>

# Por qué gobernar
## Panorama de Microsoft Purview en 2026

<!--
Transición. Purview es enorme — tiene 40+ módulos. Hoy cubrimos lo que os va a ser útil en los primeros 90 días de un proyecto Fabric real: Data Map, Unified Catalog, Sensitivity Labels y DLP. Duración estimada: 30 minutos incluyendo demo.
-->

---

## Microsoft Purview · tres grandes áreas

| Área | Capacidades clave | Portal |
|---|---|---|
| **Data Governance** | Data Map, Unified Catalog, Health Management, Data Quality, Lineage, Data Products, Access Policies | `purview.microsoft.com` |
| **Information Protection** | Sensitivity labels, Auto-labeling, Encryption, Rights Management | `purview.microsoft.com/compliance` |
| **Risk & Compliance** | DLP, Insider Risk, Communication Compliance, eDiscovery, Audit, Records, Compliance Manager | `purview.microsoft.com/compliance` |

> **Cambio de marca** · *Microsoft 365 Compliance Center* → **Purview Compliance Portal**. *Azure Purview* → **Purview Data Governance**. Mismo portal, dos áreas.

<!--
La confusión más frecuente con Purview: tiene dos portales. El portal de gobierno del dato (purview.microsoft.com) es donde trabajamos hoy. El portal de compliance (compliance.microsoft.com) es para el equipo legal y de seguridad. En 2024 Microsoft unificó ambos bajo el mismo paraguas de marca 'Microsoft Purview', pero siguen siendo superficies distintas. Hoy trabajamos con las tres áreas: un poco de Data Governance, un poco de Information Protection y el escenario de DLP que aplica a Fabric.
-->

---

## ¿Por qué gobernar Fabric?

- Fabric **centraliza** datos antes dispersos → el riesgo de exposición sube.
- OneLake permite que cualquier workspace lea/escriba → **disciplina o caos**.
- *Compliance* (GDPR, ENS, ISO 27001, NIS2) exige **clasificar, rastrear, proteger**.
- El negocio **necesita encontrar** los datos: un Catálogo es la única vía escalable.

> Sin gobierno, Fabric escala como cualquier data lake: **hacia el caos**.

<!--
El argumento de venta interno para convencer al CIO o al CISO: si construís Fabric sin gobierno, en 12 meses tendréis el mismo problema que tenéis con el data lake actual, pero a mayor escala. Fabric centraliza datos de múltiples orígenes — el riesgo de exposición inadvertida sube proporcionalmente. GDPR, ENS (Esquema Nacional de Seguridad), ISO 27001, NIS2 son regulaciones reales que aplican a la mayoría de las organizaciones en España. Sin gobierno documentado, una auditoría es un infierno.
-->

---

<!-- _class: tight -->

## Cada necesidad, su módulo

| Necesidad | Módulo Purview |
|---|---|
| ¿Qué datos tengo y dónde? | **Data Map + Unified Catalog** |
| ¿Quién tiene acceso? | **Data Access Policies** + integración Fabric |
| ¿Cómo encuentro el dato que busco? | **Unified Catalog + Búsqueda** |
| ¿Cómo sé si un dataset es de calidad? | **Unified Catalog** → Data Quality *(feature integrada)* |
| ¿De dónde viene esta tabla? | **Data Map + Unified Catalog** → Lineage *(feature integrada)* |
| ¿Qué columnas son PII / financieras? | **Information Protection** (sensitivity labels + Classifiers) |
| ¿Cómo evito que peguen un DNI en Teams? | **DLP + Communication Compliance** |
| ¿Cómo cumplo GDPR / borrado? | **Data Lifecycle Management + Records Management + eDiscovery** |
| ¿Quién descarga datasets sensibles? | **Insider Risk + Audit + Activity Explorer** |
| ¿Qué tan maduro estoy? | **Compliance Manager** |

<!--
Esta tabla es la hoja de ruta de adopción de Purview. No intentéis implementar todo a la vez — os paralizaréis. El mínimo viable para empezar: Data Map + Unified Catalog (inventario y contexto de negocio) + 5 sensitivity labels publicadas (clasificación). Con eso ya tenéis valor inmediato y demostrable. El resto se añade en fases posteriores según la madurez del equipo.
-->

---

## Gobierno **federado** sobre Fabric · dos capas

**Purview Hub for Fabric** (sin scan, integrado en Fabric):
- Dashboard de gobierno en el workspace *Admin monitoring* de Fabric.
- Muestra insights de **sensitivity labels**, **endorsements** y dominios sobre los items del tenant.
- Acceso: portal Fabric → hub de Purview (solo Fabric Admins).

**Purview Data Map** (Purview Enterprise, requiere configurar scan):
- Registrar el tenant de Fabric como fuente → configurar autenticación → ejecutar scans.
- Obtiene metadatos, esquemas, **lineage** y clasificaciones automáticas en el Data Map.
- **Sensitivity labels** y **endorsements** funcionan de forma nativa en Fabric sin scan.

<!--
Distinción clave que antes inducía a error: el Purview Hub for Fabric es un informe de monitoring integrado en el workspace 'Admin monitoring' de Fabric — no requiere configuración de scan pero tampoco hace catalogación completa en el Data Map. Para que los items de Fabric aparezcan en el Purview Data Map (Purview Enterprise) con metadatos, esquemas y lineage completo, sí hay que registrar el tenant de Fabric como fuente de datos y configurar scans (Managed Identity o Service Principal). Esto requiere habilitar las Admin APIs de Fabric y crear un security group en Entra ID. Las sensitivity labels y endorsements sí funcionan de forma nativa en Fabric sin necesidad de scan.
-->

---

## Fabric Capacity Metrics App · monitorización de capacidad

**Prerequisitos:** Capacity admin + licencia Power BI (Pro, PPU o trial)

**Instalación (primera vez):**
1. [AppSource → Microsoft Fabric Capacity Metrics](https://go.microsoft.com/fwlink/?linkid=2219875) → *Get it now* → **Install**
2. Fabric (experiencia Power BI) → **Apps** → seleccionar la app → **Connect**
3. Configurar `UTC_offset` (p.ej. `1` para CET) → autenticación **OAuth2** + privacidad **Organizational**
4. Seleccionar capacidad en el desplegable → primera carga puede tardar unos minutos

> 💡 Instalar en un workspace con licencia **Pro** para no impactar la capacidad que se monitoriza.

<!--
La app muestra consumo de CU (Capacity Units) por workload y workspace, throttling, overutilization y tendencias históricas. Es la herramienta principal para detectar cuellos de botella antes de que el tenant se quede sin capacidad. Para actualizar la app (versión anterior instalada) no hace falta borrarla: reinstalar desde AppSource actualiza en el mismo workspace. Parámetros como CapacityID o RegionName solo aplican a versiones antiguas (≤2.0); en versiones modernas la app muestra todas las capacidades disponibles. Entornos Government Cloud: GCC → aka.ms/FabricUSGovCapacityUsageReport, GCC High → aka.ms/FabricUSGovHighCapacityUsageReport, DoD → aka.ms/FabricUSGovDodCapacityUsageReport. Ref: https://learn.microsoft.com/en-us/fabric/enterprise/metrics-app-install
-->

---

## Entorno mínimo para hoy

| Item | ¿Imprescindible? |
|---|---|
| Tenant M365 con licencia E5 / E5 Compliance (trial vale) | Recomendado |
| Acceso a `purview.microsoft.com` | ✅ |
| Workspace Fabric con items reales (Jornada 1) | ✅ |
| Sensitivity labels publicadas en el tenant | ✅ — incluido en E5 |
| Cuenta admin del tenant (al menos 1 por equipo) | ✅ |

<!--
Verificar que todos tienen acceso al tenant del curso. Necesitamos al menos una licencia E5 trial o el add-on de Purview Compliance para las features de sensitivity labels y DLP. El acceso a purview.microsoft.com es con la cuenta del tenant — no hay portal separado. Si alguien no tiene acceso, que trabaje con el compañero del lado durante las demos. Recordar que el admin del tenant ya ha habilitado la integración de Purview hub en Fabric.
-->

---

## Demo en vivo · 8 min

1. `purview.microsoft.com` → home y *solution areas*.
2. **Unified Catalog** → ya aparecen los items del workspace `aurora-curso-fabric`.
3. Abrir `lh_aurora` y mostrar **lineage**, **schema**, **sensitivity label** (vacía aún).
4. Volver a Fabric → mismo Lakehouse → icono **Microsoft Purview** en la barra superior.

<!--
Demo en vivo. Tiempo estimado: 8 minutos. IMPORTANTE: para que los items aparezcan en el Unified Catalog de Purview hace falta tener configurado el scan del tenant de Fabric en Purview Enterprise (registro de la fuente + autenticación + ejecución del scan). Si el scan ya está configurado en el tenant del curso, los items de la Jornada 1 aparecerán. Si no, usar la captura de pantalla de respaldo. Lo que SÍ funciona sin scan: el Purview Hub dentro de Fabric (Admin monitoring workspace) y la aplicación de sensitivity labels directamente en Fabric.
-->

---

<!-- _class: key -->

## Mensajes clave

- **Purview es un paraguas** · no te quedes solo con Data Map.
- **Purview Hub** da visibilidad de gobierno **sin configuración**; **Data Map completo sí requiere scan**.
- *Sin gobierno, Fabric escala hacia el caos.*

<!--
Pregunta frecuente: ¿necesito configurar un scan de Fabric en Purview? Depende. El Purview Hub for Fabric (dashboard de monitoring dentro de Fabric) no requiere scan — muestra sensitivity labels y endorsements automáticamente. Pero si queréis catalogación completa en el Purview Data Map (metadatos, esquemas, lineage, clasificaciones automáticas), sí hay que registrar el tenant de Fabric como fuente y configurar scans en Purview Enterprise. Y para fuentes externas (Azure SQL, ADLS, Oracle, SAP...) también hay que configurar sus respectivos scans. Segundo punto: sin gobierno desde el día 1, el inventario nunca estará limpio.
-->

---

<!-- _class: section -->

<span class="module">M2 · 40 min</span>

# Data Map y Unified Catalog
## El inventario y la *tienda* de datos

<!--
Transición. Data Map es el inventario técnico automático. Unified Catalog es la tienda donde el negocio encuentra los datos con contexto de negocio. Son dos vistas del mismo grafo de conocimiento subyacente. Duración estimada: 35 minutos incluyendo demo.
-->

---

## Data Map · la capa técnica

- **Inventario** de assets: tablas, ficheros, modelos, dashboards, columnas.
- Se alimenta de **conexiones**:
  - Cloud nativo · Fabric (automático), Azure SQL, Synapse, ADLS, Databricks, Snowflake, Power BI.
  - On-prem · SQL Server, Oracle, Teradata, ficheros (Self-Hosted IR).
  - SaaS · Salesforce, ServiceNow, Workday.
- Cada conexión tiene **scans** programables que descubren esquemas y aplican **classifications** automáticas (DNI, IBAN, tarjeta, etc.).

<!--
Las connections son los conectores que alimentan el Data Map. Para Fabric, la conexión es automática. Para Oracle, Teradata o SAP on-premise, necesitáis el Self-Hosted Integration Runtime (el mismo que en Azure Data Factory). Las classifications son etiquetas automáticas basadas en el contenido (DNI, IBAN, email...) que Purview aplica durante el scan. Diferencia importante: classifications ≠ sensitivity labels — las primeras son técnicas y automáticas, las segundas son de negocio y se aplican manualmente o con recomendación.
-->

---

## Unified Catalog · la capa de negocio

- Vista para **analistas y owners de dato**.
- Estructura: **Business Domain → Data Product → Data Asset**.
- Conceptos clave:
  - **Glossary terms** · vocabulario común.
  - **Critical Data Elements (CDE)** · atributos decretados críticos.
  - **OKRs / Goals** asociados a Data Products.
  - **Health controls** · indicadores de calidad, uso, propiedad.
  - **Endorsements** · *Promoted* ✅ · *Certified* ⭐.

<!--
La jerarquía a recordar: Business Domain (área de negocio: Comercial, Finanzas...) → Data Product (conjunto de datos con propósito, owner y certificación) → Data Asset (la tabla o fichero concreto). El Glossary vincula términos de negocio ('Importe Neto') con columnas técnicas ('net_amount'). Los Certified Data Elements (CDEs) son las columnas críticas del negocio que requieren gestión especial. Esto es el puente entre el lenguaje técnico y el lenguaje de negocio.
-->

---

## Data Quality

- Reglas DQ sobre tablas Delta, Lakehouse, Warehouse.
- Tipos: *completeness*, *uniqueness*, *validity*, *accuracy*, *freshness*.
- Resultado: **score numérico** por dataset, evolución histórica, **alertas**.

> El score se publica en el Data Product · es lo primero que mira el consumidor antes de usar el dato.

<!--
Los DQ scores son el indicador que el analista mira antes de confiar en un dataset. Si la completeness de la columna 'importe' es del 60%, el analista ya sabe que ese campo tiene problemas antes de usarlo en un reporte. Esto da confianza al consumidor del dato y reduce el tiempo perdido en validaciones manuales. Las reglas de DQ se definen una vez y se ejecutan automáticamente en cada scan. Las alertas notifican al Data Steward cuando el score baja del umbral configurado.
-->

---

## Data Lineage y Access Policies

**Lineage**
- **Automático** en Fabric: Lakehouse → Notebook → Warehouse → Semantic Model → Report.
- **Manual / programático** con APIs y OpenLineage para fuera de Fabric.

**Data Access Policies**
- Conceder acceso a un dato **desde Purview** sin entrar a la herramienta origen.
- Federa: ADLS Gen2, Azure SQL DB, Fabric.
- Modelo recomendado · **grupos en Entra ID + dominios en Purview + workspaces en Fabric**.

<!--
El lineage automático en Fabric es una de las mayores ventajas competitivas. En Azure Purview clásico (pre-2023), construir el lineage era un proyecto en sí mismo: había que instrumentar cada pipeline, cada notebook. Ahora en Fabric viene de fábrica para todos los items nativos. Las Access Policies desde Purview permiten gestionar permisos de Fabric centralizadamente sin entrar en cada workspace — el compliance officer puede ver y revocar accesos sin depender del equipo técnico.
-->

---

## Caso Aurora · publicar un Data Product

Vamos a publicar **"Ventas Aurora — Gold"** que agrupa `wh_aurora` y `sm_aurora_ventas`. Le asociamos:

- **Dominio** · `Comercial`.
- **Glossary terms** · *Importe de Venta*, *Estación de Servicio*, *Cliente Comercial*.
- **CDE** · `cliente_id`, `importe`.
- **Owner** · Marisa Ledesma *(persona ficticia)*.
- **Endorsement** · *Certified*.

<!--
Publicar el Data Product 'Ventas Aurora — Gold' es el ejercicio práctico de este bloque. El owner es una persona de negocio (Marisa Ledesma, directora comercial ficticia) — no del IT. Esto es fundamental: el ownership del dato debe estar en el negocio. El Endorsement 'Certified' significa que alguien ha verificado formalmente la calidad, la documentación y el gobierno del producto. Un consumer que ve 'Certified' sabe que puede confiar en esos datos.
-->

---

## Demo en vivo · 15 min

1. Purview → **Unified Catalog → Governance domains** → crear `Comercial`.
2. Crear los **glossary terms** necesarios.
3. Crear el **Data Product** `Ventas Aurora — Gold` y enlazar `wh_aurora` + `sm_aurora_ventas`.
4. Asignar owner, términos, endorsement.
5. Mostrar **lineage** (debe pintar el flujo de Jornada 1).
6. Crear una **DQ rule** simple sobre `fact_ventas`: `importe IS NOT NULL`.
7. Mostrar el dashboard del Data Product.

<!--
Demo en vivo. Tiempo estimado: 15 minutos. Secuencia: crear el Governance Domain 'Comercial' → crear 3 glossary terms (Importe Neto, Litros Vendidos, Estación) → crear el Data Product 'Ventas Aurora — Gold' con wh_aurora y sm_aurora_ventas → aplicar Endorsement Certified → navegar al lineage automático (puede tardar 30-60 segundos en actualizarse). Ir despacio en la creación del Domain y el Glossary — es la parte más conceptualmente nueva. El lineage suele ser el momento más impactante visualmente.
-->

---

<!-- _class: key -->

## Mensajes clave

- **Data Map es el inventario · Catalog es la tienda.**
- *Sin owners, no hay gobierno.* Empieza por asignar dueños.
- El **lineage automático** es la mejor demo del valor inmediato de Purview.

<!--
Pregunta: ¿quién debería ser el Data Owner de un Data Product en vuestra organización? Respuesta correcta: alguien del negocio, no del IT. El IT es el Data Steward (operativiza el gobierno, mantiene el glossary y las reglas de calidad). El Owner toma decisiones estratégicas: qué dato es bueno, quién accede, cuándo se retira. Si el negocio no asume el ownership, el programa de gobierno muere en 6 meses.
-->

---

<!-- _class: section -->

<span class="module">M3 · 30 min</span>

# Information Protection y DLP
## Etiquetas que *viajan* con el dato

<!--
Transición al bloque de protección de la información. Las etiquetas de sensibilidad son la pieza que viaja con el dato. Si alguien exporta a Excel un dataset con etiqueta Restringido-PII, el Excel hereda la encriptación MIP automáticamente. Eso es lo que diferencia a un sistema de gobierno real de uno puramente cosmético. Duración estimada: 25 minutos incluyendo demo.
-->

---

## Sensitivity labels

- Definidas a nivel **tenant** desde el Purview Compliance Portal.
- Pueden:
  - **Etiquetar visualmente** (cabecera, pie, watermark).
  - Aplicar **encriptación** (MIP / Azure Rights Management).
  - **Restringir acciones** (no copiar, no imprimir, no reenviar).
  - Aplicarse a Office, Outlook, Teams, SharePoint, OneDrive y **Fabric / OneLake / Power BI**.
- Aplicación · **manual**, **auto-label por contenido**, **auto-label por contenedor**.

> **Herencia en Fabric** · etiqueta el Lakehouse → modelos y reportes derivados la heredan. Si exportas a Excel/PDF, **se exporta la etiqueta y la encriptación**.

<!--
Las sensitivity labels se configuran a nivel de tenant en Microsoft Purview y están disponibles en todos los servicios M365: Exchange, SharePoint, Teams, Power BI, Fabric, Office apps. La herencia en Fabric es automática: si etiquetáis el Lakehouse, los modelos semánticos y reportes derivados heredan la etiqueta. Esto es un multiplicador enorme: un solo acto de clasificación se propaga hacia arriba en la cadena. La encriptación MIP (Microsoft Information Protection) viaja con el fichero — incluso si alguien lo envía por email o lo copia en un USB.
-->

---

## Sensitive Information Types y clasificación

- Catálogo enorme *out-of-the-box* · DNI, NIF, IBAN, tarjetas, pasaportes, SSN…
- **Personalizables** · regex + keywords + función + nivel de confianza.
- **EDM (Exact Data Match)** · comparar contra una tabla maestra propia.
- **Trainable classifiers** · modelos ML para categorías (CV, contratos, código fuente, etc.).

<!--
Los SIT (Sensitive Information Types) out-of-the-box de Microsoft incluyen más de 200 patrones predefinidos: DNI español, IBAN, tarjetas de crédito, número de Seguridad Social, pasaporte, etc. Para datos propios del negocio (ej. código de contrato interno de Aurora), usáis SIT personalizado con regex. EDM (Exact Data Match) es para comparar contra vuestra base de datos de clientes real — el más preciso pero el más complejo de configurar. Trainable classifiers usan ML para reconocer contenido sensible por contexto, no por patrón.
-->

---

<!-- _class: tight -->

## Etiquetas recomendadas para Aurora

| Etiqueta | Marca | Encriptación | Caso |
|---|---|---|---|
| Público | — | No | Materiales de marketing |
| Interno | "Aurora — Interno" | No | Documentación operativa |
| Confidencial — Comercial | "Aurora — Confidencial" | Sí, lectura: grupo Ventas | Datos de cliente comercial |
| Restringido — PII | "Aurora — Restringido PII" | Sí, lectura: Owner del Data Product | Datasets con PII |
| Restringido — Financiero | "Aurora — Restringido Financiero" | Sí, lectura: grupo Finanzas | Datasets económicos |

> **Empieza con 4–5 etiquetas. Más es ingobernable.**

<!--
Esta tabla de 5 etiquetas es el mínimo viable para empezar un programa de gobierno real. La regla de oro: menos es más. 20 etiquetas no las aplica nadie — la gente elige al azar o no clasifica. 5 etiquetas bien diseñadas, con criterios claros y aplicadas de forma consistente tienen impacto real. La etiqueta 'Público' también es importante: marca los datos que SÍ se pueden compartir libremente, lo que elimina la duda sobre qué se puede publicar en la web o en informes externos.
-->

---

## Data Loss Prevention (DLP)

Reglas que **detectan, alertan o bloquean** contenidos sensibles en:

- **Endpoints** Windows / macOS · *Endpoint DLP*.
- **Exchange, Teams, SharePoint, OneDrive**.
- **Fabric items y Power BI** · *DLP for Power BI / Fabric*.
- Servicios de terceros vía **Defender for Cloud Apps**.

Acciones · aviso, **justificación obligatoria**, **bloqueo**, override con auditoría.

<!--
DLP (Data Loss Prevention) es la red de seguridad que actúa donde las etiquetas clasifican. Donde las etiquetas identifican, DLP actúa. La acción más usada en la práctica: aviso al usuario + justificación obligatoria registrada. El bloqueo total se reserva para los casos más críticos (ej. datos financieros sin autorizar) porque genera fricción y tickets de soporte. Las políticas DLP se diseñan ANTES de que los datos estén en producción — aplicarlas a posteriori es posible pero mucho más difícil.
-->

---

## DLP en Fabric · ejemplo

> "Si un *semantic model* contiene > N registros con DNI → bloquea la exportación a CSV."

- Disponible para **Lakehouse**, **semantic models** y **reports**.
- Acompañado de **Activity Explorer** y **Audit** para auditoría e investigación.

<!--
El ejemplo del DNI en el semantic model es un escenario real. Si el modelo semántico sm_aurora_ventas contiene la columna dni_cliente sin enmascarar y alguien lo exporta a CSV, la regla DLP puede bloquear la exportación y registrar el intento. Combinado con Activity Explorer tenéis la pista de auditoría completa: quién intentó exportar qué, cuándo, desde qué dispositivo, y qué acción tomó DLP. Esto es lo que necesita el Compliance Officer para responder a una auditoría GDPR.
-->

---

## Demo en vivo · 10 min

1. Compliance Portal → **Information Protection → Labels**. Mostrar las 5 etiquetas.
2. Publicar un **Label policy** al grupo "Curso Fabric".
3. En Fabric · `wh_aurora` → menú **Sensitivity** → aplicar `Aurora — Confidencial`.
4. Mostrar que el modelo semántico y los reportes **heredan** la etiqueta.
5. **Exportar** el reporte a Excel · cabecera y encriptación.
6. Crear regla DLP · *si reporte tiene `Restringido — PII`, bloquear exportación a Excel*. Probarla.
7. **Activity Explorer** · ver el intento bloqueado.

<!--
Demo en vivo. Tiempo estimado: 10 minutos. Secuencia: 1) Crear las 5 etiquetas en purview.microsoft.com (o mostrar las ya creadas). 2) Crear una DLP policy básica para Fabric/Power BI que detecte la etiqueta Restringido-PII. 3) Aplicar la etiqueta Restringido-PII al Lakehouse wh_aurora. 4) Verificar la herencia en el modelo semántico. 5) Intentar exportar a CSV desde Power BI — mostrar el bloqueo o el aviso. 6) Activity Explorer: mostrar el evento registrado. IMPORTANTE: Las reglas DLP pueden tardar hasta 30 minutos en propagarse. Si no se activa en el aula, mostrar la captura de pantalla de respaldo del resultado.
-->

---

<!-- _class: key -->

## Mensajes clave

- La **etiqueta viaja con el dato** · incluso cuando sale de Fabric.
- DLP **no se inventa** el día del incidente · se diseña antes.
- Empieza con **4–5 etiquetas**. Más es ingobernable.

<!--
Pregunta: ¿qué pasa si alguien descarga un Excel con datos Restringido-PII desde casa, en un dispositivo no gestionado por la empresa? Respuesta: con encriptación MIP + DLP de endpoint + Conditional Access de Entra ID, el archivo llega encriptado y solo puede abrirse en dispositivos que cumplan la política. Sin la clave MIP, el archivo es ilegible. Esto requiere que todos los elementos estén configurados — MIP solo sin DLP no es suficiente para un escenario completo.
-->

---

<!-- _class: lead bare -->

# ☕ Descanso · 15 min
### Volvemos para los *Data agents* (y echaremos un vistazo al workload *Fabric IQ*)

<!--
Descanso de 15 minutos. La segunda parte del día es la más novedosa y la que más preguntas va a generar: los Data agents. Aprovechar el descanso para abrir el portal de Fabric en el tenant y verificar que el workspace puede crear Data agents (capacidad F-SKU compatible). Si hay algún problema de configuración, es el momento de resolverlo antes de la demo.
-->

---

<!-- _class: section -->

<span class="module">M4 · 25 min</span>

# Integración Purview ↔ Fabric
## Gobierno extremo a extremo

<!--
Transición al bloque de integración. Purview y Fabric no son dos herramientas separadas que hay que conectar manualmente — están integradas de fábrica. Purview ve los items de Fabric, Fabric respeta los permisos y etiquetas de Purview. Duración estimada: 30 minutos incluyendo demo.
-->

---

## ¿Dónde se ve qué?

| Vista | Qué muestra | Audiencia |
|---|---|---|
| **Workspace de Fabric** | Items técnicos del proyecto | Equipo técnico |
| **OneLake Catalog** (en Fabric) | Items del tenant filtrables · búsqueda · endorsements · etiquetas | Analistas, data engineers |
| **Purview Unified Catalog** | Data Products · glossary · dominios · calidad · lineage | Negocio + gobierno |
| **Purview Data Map** | Inventario crudo + scans | Data stewards / arquitectos |

<!--
Esta tabla aclara la confusión más frecuente entre Fabric y Purview. Cada persona tiene su vista optimizada: El técnico (ingeniero de datos) vive en el workspace de Fabric — crea, transforma, depura. El analista semi-técnico vive en el OneLake Catalog dentro de Fabric — busca y descubre datos. El analista de negocio y el Data Owner viven en Purview Unified Catalog — ven el contexto de negocio, el lineage, la calidad. El CISO/CDO vive en Unified Catalog → Health Management — visión ejecutiva del estado del gobierno.
-->

---

## OneLake Catalog en Fabric

- Acceso desde la **barra lateral** del portal Fabric.
- Filtra por · tipo, endorsement, sensitivity label, owner, dominio.
- Atajo a **explorar** el item · schema, sample, ABFS path, *copy code*.
- **Crear shortcuts** directamente desde el catálogo.

<!--
El OneLake Catalog es la interfaz de descubrimiento para los consumidores técnicos y semi-técnicos. Pueden filtrar por endorsement (solo datos Certified o Promoted), por sensitivity label (solo datos Público o Interno), por tipo de item (solo Warehouses, solo modelos semánticos...). También pueden copiar el ABFS path del Lakehouse para acceder programáticamente desde un notebook. Los shortcuts se pueden crear directamente desde el catálogo — esto facilita el self-service de los analistas sin depender del equipo de datos.
-->

---

## Data Access Policies en Fabric

> *Cualquiera del grupo* **Analistas Comercial** *puede* **leer** *el data product* **Ventas Aurora — Gold**.

- Purview propaga el permiso al **Lakehouse / Warehouse / semantic model** correspondiente.
- Modelo recomendado:
  - **Roles y grupos** en Entra ID.
  - **Dominios** en Purview.
  - **Workspaces** en Fabric.
- **No** permisos individuales.

<!--
Las Data Access Policies son el gobierno de acceso federado desde Purview. En lugar de ir a cada workspace de Fabric a dar permisos individualmente, los gestionáis centralizadamente desde Purview. El grupo de Entra ID 'Analistas Comercial' recibe acceso al Data Product 'Ventas Aurora — Gold', y Purview propaga automáticamente el permiso de lectura al Lakehouse, Warehouse y modelo semántico que forman parte de ese Data Product. Esto es el gobierno de acceso real en una organización grande.
-->

---

<!-- _class: tight -->

## Modelo de dominios para Aurora

```text
Aurora Energía
 ├── Comercial
 │    ├── Data Product: Ventas Aurora — Gold
 │    ├── Data Product: Clientes (PII)
 │    └── Data Product: Campañas Marketing
 ├── Operaciones
 │    ├── Data Product: Telemetría Surtidores
 │    └── Data Product: Mantenimiento Predictivo
 ├── Finanzas
 │    └── Data Product: P&L Estación
 └── Gobierno (transversal)
      ├── Glossary maestro
      ├── Reglas DQ globales
      └── Sensitivity labels
```

> Cada dominio · **1 owner** (negocio) y **1 steward** (técnico).

<!--
Este diagrama es el target architecture de gobierno para Aurora. Cuatro dominios: Comercial, Operaciones, Finanzas y Gobierno (transversal). Cada dominio tiene su Data Owner (negocio) y su Data Steward (IT/analítica). El dominio Gobierno es transversal — gestiona las políticas que aplican a todos los dominios. Empezad siempre por el dominio con más valor de negocio — en Aurora, sería Comercial, porque ahí están los datos de ventas que ya tenemos en el Warehouse. Esto demuestra valor rápido y construye momentum para los siguientes dominios.
-->

---

## Unified Catalog · Health Management

Reportes ejecutivos de gobierno integrados en Unified Catalog:

- Nº de assets gobernados.
- % con owner · % con etiqueta.
- Evolución de **Data Quality** (Health Controls).
- Accesos concedidos.

> Es el **dashboard que enseñas al CISO o al CDO el primer mes**.

<!--
Health Management es la sección de Unified Catalog con reportes listos para medir la madurez de gobierno. Muestra el nivel de madurez en números concretos: % de assets con owner asignado, % con sensitivity label, evolución del DQ score (Health Controls), y Health Actions (acciones concretas para mejorar la puntuación). Es la prueba de que el programa de gobierno está funcionando y tiene impacto medible. Preguntar: ¿vuestro CDO o CISO pide este tipo de reporting actualmente? Si no, Health Management puede ser el argumento para empezar el proyecto. Término anterior 'Estate Insights' no existe en la documentación oficial de Purview — el nombre correcto es Health Management dentro de Unified Catalog.
-->

---

## Demo en vivo · 12 min

1. **OneLake Catalog** en Fabric → buscar "ventas" → ver `wh_aurora` con la etiqueta del bloque anterior.
2. Filtrar por endorsement *Certified* → mostrar el Data Product `Ventas Aurora — Gold`.
3. Volver a Purview → **Unified Catalog → Health Management**.
4. Crear una **Data Access Policy** que conceda lectura del Data Product al usuario `analista@aurora-test.local` (cuenta de prueba).
5. Comprobar en Fabric que el usuario aparece con permiso de lectura sobre el Warehouse.

<!--
Demo en vivo. Tiempo estimado: 12 minutos. Secuencia: 1) OneLake Catalog: buscar 'ventas', filtrar por Certified, mostrar shortcuts. 2) Unified Catalog → Health Management: mostrar los reportes de gobierno (puede estar vacío en tenant nuevo — usar captura). 3) Data Access Policy: crear una policy que da acceso a 'Analistas Comercial' al Data Product. 4) Verificar en Fabric que el miembro del grupo puede acceder. NOTA: La propagación de Access Policies puede tardar varios minutos. Si no aparece inmediatamente, refrescar el workspace y esperar.
-->

---

<!-- _class: key -->

## Mensajes clave

- *Fabric te da el dato. Purview te da la disciplina.*
- El gobierno **no es la suma de mil tareas** · son **5 dominios** + **5 etiquetas** aplicadas en serio.
- **Health Management** (Unified Catalog) es el dashboard que enseñas al CISO/CDO el primer mes.

<!--
Las tres frases del bloque. Hacerlas leer en voz alta o preguntar si alguien las puede completar: 1) Fabric da el dato, Purview da la... (disciplina). 2) Cinco dominios bien definidos valen más que... (20 mal definidos). 3) Health Management es el informe que le enseñas al... (CISO/CDO para demostrar valor). Estos son los argumentos para vender el programa de gobierno internamente.
-->

---

<!-- _class: section -->

<span class="module">M5 · 30 min</span>

# Data agents en Fabric
## Capa *conversacional* sobre dato gobernado

<!--
Transición a la parte conversacional sobre dato gobernado. Los Data agents son la capacidad madura: permiten hacer preguntas en lenguaje natural sobre los datos gobernados y obtener respuestas con trazabilidad. Aclarar desde el principio: Data agent es la capacidad concreta que construiremos hoy; el workload Fabric IQ es el paraguas (preview) en el que se inscribe y al que se irán sumando otras capacidades como Ontology, Graph, Plan u Operations agent. Duración estimada: 30 minutos incluyendo demo.
-->

---

## ¿Qué es un Data agent?

Capacidad **conversacional y razonadora** sobre datos gobernados de Fabric.

- **Multi-fuente** · Warehouse, Lakehouse, Power BI semantic model, Eventhouse, OneLake Files.
- **Multi-paso** · planifica, llama a herramientas, evalúa y responde.
- **Gobernado** · hereda RLS/OLS, sensitivity labels y permisos de cada fuente.
- **Trazable** · cada respuesta cita datasets, queries generadas y filas usadas.
- **Publicable** · endpoint REST, app de Teams, embed web con Entra ID.

> Un Data agent **no es un chatbot** · es una capa de razonamiento sobre dato gobernado, con auditoría.

<!--
Dejar claro: Data agent es la pieza práctica del bloque — lo que construiremos en M6 y lo que el alumno se llevará al lab. Multi-fuente significa que la misma conversación puede saltar entre Warehouse, Eventhouse y un PDF en OneLake. Multi-paso es la diferencia con Power BI Q&A: el agente puede planificar varias consultas, evaluarlas y combinar resultados. Gobernado: hereda RLS/OLS, labels y permisos de cada fuente — si el usuario no puede ver una fila, el agente tampoco. Trazable: cada respuesta cita el SQL/DAX/KQL generado y los datasets usados. Publicable: endpoint REST + app de Teams + iframe.
-->

---

## El workload Fabric IQ (preview)

Paraguas que Microsoft está construyendo dentro de Fabric. Reúne, según la documentación pública actual:

| Capacidad | Para qué sirve | Estado |
|---|---|---|
| **Ontology** | Vocabulario y semántica de negocio sobre el dato físico | Preview |
| **Graph** | Materializa las relaciones de la ontology como grafo | Preview |
| **Plan** | Define planes que combinan datos y acciones | Preview |
| **Data agent** | Asistente conversacional sobre datos | **Disponible** |
| **Operations agent** | Agente para tareas operativas sobre la plataforma | Preview |
| **Power BI semantic model** | Capa semántica tabular tradicional, integrable como fuente | GA |

> En este curso construimos un **Data agent**. El resto del workload · **visión y roadmap**.

<!--
Esta es la slide que aclara la confusión más frecuente del mercado: 'Fabric IQ' no es sinónimo de 'Data agent'. Fabric IQ es un *workload paraguas* en preview que agrupa varias capacidades: Ontology, Graph, Plan, Data agent y Operations agent, más la integración con Power BI semantic models. La única capacidad disponible y demostrable hoy en clase es el Data agent. Las demás las tratamos como visión y roadmap. Disclaimer: Ontology, Graph, Plan y Operations agent están en preview y su disponibilidad depende de tenant y región — verificar antes de comprometer en proyecto.
-->

---

<!-- _class: tight -->

## Arquitectura conceptual

```text
┌────────────────────────────────────┐
│     Aplicaciones / Usuarios        │
│ Teams · Copilot M365 · Web · API   │
└────────────────────────────────────┘
              ▲
┌────────────────────────────────────┐
│        Data agent (Fabric)         │
│ Razonamiento + tools + citas + mem.│
└────────────────────────────────────┘
              ▲  fuentes que puede usar
   ┌────────┴────────┐
┌─────────────┐    ┌─────────────────────┐
│ Power BI    │    │ Ontology / Graph    │
│ semantic    │    │ (preview) workload  │
│ model (GA)  │    │ Fabric IQ           │
└─────────────┘    └─────────────────────┘
      ▲                       ▲
      └──── OneLake · Lakehouse / Warehouse / Eventhouse / Files
              ▲
┌──────────────────────────────────┐
│ Microsoft Purview · gobierno      │
│ transversal: labels, lineage, DLP │
└──────────────────────────────────┘
```

<!--
El diagrama distingue de forma explícita lo que hasta ahora estaba mezclado: 1) la capa de aplicaciones (Teams, Copilot, web, API). 2) el Data agent como pieza razonadora. 3) Las fuentes que puede usar, que NO son una sola caja: por un lado el Power BI semantic model (GA, capa semántica madura de hoy) y por otro Ontology/Graph del workload Fabric IQ (preview, capa semántica enriquecida del futuro). 4) Por debajo, OneLake con Lakehouse, Warehouse, Eventhouse y Files. 5) Atravesando todo, Purview como gobierno transversal. Insistir: hoy demostramos un Data agent que usa semantic model y Warehouse; cuando Ontology esté disponible en vuestro tenant, simplemente se añade como una fuente más.
-->

---

## Tres ideas a recordar

1. **Capa semántica · hoy** = el **Power BI semantic model** (GA). **Mañana** se complementará con **Ontology (preview)** del workload Fabric IQ.
2. **Data agent** · capacidad razonadora con tools (SQL, DAX, KQL, búsqueda), memoria y citas, expuesta como API o chat.
3. **Gobierno integrado** · hereda permisos, etiquetas y políticas de Purview / RLS / OLS de cada fuente.

<!--
La idea 1 es la más importante para evitar confusiones: hoy 'capa semántica' = Power BI semantic model (GA). Ontology es el futuro (preview) y NO sustituye al semantic model: lo complementa. La idea 2 resume qué es un Data agent: razonamiento + tools + memoria + citas. La idea 3 es la conexión con todo el bloque anterior de Purview: el gobierno no es opcional, es lo que hace que el agente sea seguro.
-->

---

<!-- _class: tight -->

## Diferencias con productos previos

| Producto | Qué hace | Diferencia |
|---|---|---|
| **Power BI Q&A** | NL → DAX sobre **un** semantic model | 1 modelo, **sin razonamiento** multi-paso |
| **Copilot in Fabric** | Asiste al desarrollador (genera SQL, KQL, Spark, DAX) | Foco en **productividad del IT** |
| **Azure AI Foundry Agents** | Agentes generales sobre Azure | Más amplio · requiere **integrar manualmente** tu data estate |
| **Fabric · Data agent** | Agente razonador sobre datos gobernados de Fabric | **Cero plumbing** · gobierno heredado · multi-fuente |
| **Fabric IQ workload (preview)** | *Paraguas* con Ontology, Graph, Plan, Operations agent + Data agent | Visión de capa semántica empresarial · capacidades en **preview** |

<!--
La pregunta más frecuente: '¿esto es Power BI Q&A pero más potente?' Respuesta: el Data agent es multi-fuente y multi-paso, mientras que Q&A se limita a un solo semantic model. Respecto a Azure AI Foundry Agents: son más potentes y configurables, pero requieren integrar manualmente vuestro data estate; el Data agent tiene cero plumbing porque vive dentro de Fabric. La última fila aclara la confusión: Fabric IQ es el workload paraguas (preview), no es sinónimo del Data agent. Cuando vuestro tenant tenga Fabric IQ habilitado, el Data agent podrá consumir también las ontologías y el grafo del workload, pero hoy no es requisito.
-->

---

## Capacidad de razonamiento del Data agent

- **Function calling / tools** · `execute SQL on Warehouse`, `run KQL on Eventhouse`, `search OneLake docs`.
- **Reasoning loops** · planifica varios pasos antes de responder.
- **Memoria conversacional** corta (sesión) y larga (perfil de usuario).
- **Citas y trazabilidad** · cada respuesta incluye los datasets y filas usadas.

<!--
El reasoning loop es lo que diferencia al agente de una búsqueda simple. El agente planifica: ¿qué herramienta necesito para responder esto? La ejecuta, evalúa el resultado, y decide si necesita ejecutar otra herramienta o si ya tiene la respuesta. Esto permite responder preguntas complejas que requieren varias consultas coordinadas. Las citas de trazabilidad son críticas para la confianza: el analista puede verificar de qué tabla y de qué filas viene cada número de la respuesta.
-->

---

## Requisitos

**Para construir un Data agent (lo que haremos hoy)**

- Capacidad Fabric F-SKU compatible · **F4+** para experimentación, **F64+** para producción.
- Workspace con los items origen ya gobernados (labels, RLS/OLS, permisos).
- Modelos LLM aprovisionados por Microsoft en la región de la capacidad (consumo dentro de la cuota CU).

**Para explorar el workload Fabric IQ (preview, opcional)**

- Tenant con el workload Fabric IQ habilitado por el admin.
- Disponibilidad de Ontology / Graph / Plan / Operations agent · sujeta a preview y región.

> *En este curso usaremos solo el primer bloque. El segundo es informativo.*

<!--
Separar los dos bloques de requisitos evita que el alumno piense que necesita Fabric IQ habilitado para hacer el lab. Lo único necesario para el lab es: capacidad F-SKU compatible + items con gobierno + cuota CU para los LLM (que provee Microsoft, no hace falta Azure OpenAI por separado). El segundo bloque es por si el alumno quiere experimentar con Ontology o Graph en su tenant: requiere que el admin habilite el workload Fabric IQ (preview).
-->

---

<!-- _class: tight -->

## Patrones de uso de un Data agent

| Patrón | Para quién | Ejemplo Aurora |
|---|---|---|
| **Analítico** | Negocio que pregunta KPI | "¿Cómo van las ventas de gasoil este trimestre vs el anterior?" |
| **Operativo / tiempo real** | Operaciones (apoyado en Eventhouse) | "¿Qué surtidores tienen alarmas activas y desde cuándo?" |
| **Conocimiento documental** | RR.HH., legal (apoyado en OneLake Files) | "Búscame las cláusulas de SLA de los contratos firmados con el proveedor X" |
| **Asistencia a procesos** | Procesos de negocio | "Resumen del cierre diario en el canal Finanzas" |

> *Patrones de uso, no tipos de producto* · todos se construyen con la misma capacidad **Data agent**.

<!--
IMPORTANTE: estos son patrones de uso, NO tipos de producto distintos. En la UI de Fabric no encontraréis 'Crear Analytical Data Agent' o 'Crear Operational Data Agent' — hay un único tipo de item llamado 'Data agent', y los cuatro patrones se logran configurando fuentes, instrucciones y tools distintas. En Aurora empezamos con el patrón analítico (ventas y KPIs comerciales) porque es el más claro y el de más impacto inmediato. El operativo (alertas de surtidores) es el siguiente paso natural — conecta con el Eventhouse que montamos en J1. El de conocimiento documental (políticas RR.HH.) y el de asistencia a procesos (consolidación de informes) son más complejos y se dejan para proyectos avanzados.
-->

---

## Demo en vivo · 12 min

1. Crear un **Data agent** en el workspace `aurora-curso-fabric`: `agente-ventas-aurora`.
2. Asociar como fuentes `wh_aurora` y `sm_aurora_ventas`.
3. Definir 2–3 instrucciones de sistema (rol, dominio, tono, qué **no** hacer).
4. Probar:
   - "¿Cuántas estaciones tenemos por provincia?"
   - "Top 5 productos en marzo."
   - "Compara electricidad vs combustible en el último año."
5. Mostrar la pestaña **Trace** · SQL/DAX generado, citas, datasets accedidos.
6. Mostrar publicación como **endpoint** y embed en Teams.

<!--
Demo en vivo. Tiempo estimado: 12 minutos. Secuencia: 1) Crear el Data agent en el workspace (no buscar 'Fabric IQ' en la barra lateral — es un item del workspace). 2) Asociar wh_aurora y sm_aurora_ventas como fuentes. 3) Añadir 2-3 instrucciones básicas de sistema. 4) Probar las 3 preguntas de la slide — mostrar la respuesta y la pestaña Trace. 5) Mostrar la publicación como endpoint. Plan B: si el Data agent no estuviera disponible en el tenant del aula, usar el agente pre-provisionado del tenant del formador y pasar la demo a 'guided walkthrough' con capturas. La pestaña Trace es la más importante: demuestra que el agente no 'inventa' — muestra el SQL exacto que ejecutó para llegar a la respuesta.
-->

---

<!-- _class: key -->

## Mensajes clave

- Un **Data agent no es un chatbot** · es una capa de **razonamiento gobernada**.
- Sin gobierno (Purview + labels + RLS), el agente **expone lo que no debe**.
- Capa semántica · **hoy** = Power BI semantic model (GA); **mañana** también Ontology (preview) del workload Fabric IQ.

<!--
El punto más crítico del bloque: sin gobierno previo, el agente expone lo que no debe. Esto no es una exageración teórica: si no hay RLS sobre dim_cliente, el agente podría responder preguntas con DNI y datos personales de clientes. El gobierno (Purview + labels + RLS) es la condición necesaria y previa para publicar un agente de IA sobre datos reales en una organización. Hacer la conexión explícita: todo lo que hemos hecho en M1-M4 hoy es exactamente lo que hace que M5-M6 sea seguro. Tercer mensaje: dejar bien claro que la capa semántica de hoy sigue siendo el Power BI semantic model (GA); Ontology está en preview y se sumará cuando esté disponible — no la sustituye.
-->

---

<!-- _class: section -->

<span class="module">M6 · 30 min</span>

# Construyendo un Data Agent
## *agente-ventas-aurora* paso a paso

<!--
Transición al bloque más hands-on de la jornada. En M5 creamos el agente rápido y lo probamos. En M6 vamos paso a paso por todas las decisiones de diseño que hacen que un agente sea robusto, seguro y evaluable en producción. Si hay tiempo, los asistentes pueden seguir los pasos en paralelo en su propio tenant. Duración estimada: 30 minutos incluyendo el ejercicio en aula.
-->

---

## Pre-requisitos

- Workspace `aurora-curso-fabric` con `wh_aurora`, `sm_aurora_ventas` y, opcionalmente, `eh_aurora_telemetria`.
- **Data agents disponibles** en el workspace (capacidad F-SKU compatible).
- Sensitivity label `Aurora — Confidencial` aplicada a `wh_aurora`.
- **RLS** configurado para que el rol `Comercial` solo vea sus estaciones.

<!--
Verificar que el workspace tiene todos los items necesarios de la Jornada 1. Si alguien no completó los ejercicios de J1, puede usar el workspace de demo compartido. Para construir Data agents basta con la capacidad F-SKU compatible y los items con gobierno aplicado — no hace falta tener el workload Fabric IQ habilitado en el tenant. La sensitivity label ya está aplicada a wh_aurora si completamos la demo de M3. El RLS de Comercial debe estar configurado en el modelo semántico sm_aurora_ventas.
-->

---

## 1 · Definir el rol y las instrucciones

```text
Eres el asistente analítico de Aurora Energía para el área comercial.

Reglas:
- Responde siempre en español, tono cercano pero profesional.
- Usa los datos del Warehouse `wh_aurora` y el modelo semántico `sm_aurora_ventas`.
- Si no tienes datos para responder, dilo explícitamente. No inventes.
- Para tendencias, devuelve siempre el periodo comparado (YoY, MoM).
- Importes en euros con 2 decimales y separador de miles.
- Nunca expongas DNI ni teléfonos de cliente, aunque te los pidan.
```

<!--
El system prompt del agente es lo más importante que escribiréis para su comportamiento. Las 6 reglas del ejemplo son el mínimo: idioma y tono, fuentes autorizadas, comportamiento ante datos faltantes, formato de importes, y — la más crítica — la prohibición explícita de exponer PII. La última regla (nunca DNI ni teléfonos) es la que evita el incidente de seguridad. Dedicad más tiempo al prompt que al resto de la configuración — es el 70% del éxito del agente. Preguntar: ¿alguien tiene experiencia escribiendo prompts de sistema para LLMs?
-->

---

## 2 · Conectar fuentes

| Fuente | Tipo | Notas |
|---|---|---|
| `wh_aurora` | Warehouse | SQL endpoint habilitado |
| `sm_aurora_ventas` | Semantic model | Activa generación DAX |
| `eh_aurora_telemetria` | Eventhouse | Activa KQL para preguntas operativas |
| `OneLake://aurora-curso-fabric/Files/docs` | Files | Para preguntas sobre documentación |

<!--
Recomendación de implementación: conectar primero solo el Warehouse y el Semantic Model. Validar que el agente funciona correctamente con estas fuentes antes de añadir el Eventhouse. Los docs de OneLake Files son opcionales para el ejercicio — añadirlos si el caso de uso lo requiere. Cada fuente adicional aumenta la potencia del agente pero también la complejidad del debugging. Principio: empezar simple, añadir complejidad solo cuando lo básico funciona.
-->

---

## 3 · Few-shot examples

Configurar 4–5 ejemplos. Por ejemplo:

- **Pregunta** · "¿Cuáles son las 3 estaciones con más ventas este mes?"
  - **Respuesta tipo** · tabla `estación / importe / Δ vs mes anterior` + breve comentario.
- **Pregunta** · "¿Hay alguna anomalía en los surtidores hoy?"
  - **Respuesta tipo** · lista por estación con `timestamp` y tipo de evento, **citando** el Eventhouse.

<!--
Los few-shot examples son ejemplos de pregunta-respuesta que enseñan al agente el formato de respuesta esperado y el nivel de detalle adecuado. Son más importantes que el system prompt para conseguir respuestas consistentes en formato. Dedicad al menos 20 minutos a diseñar 4-5 buenos ejemplos. El ejemplo del 'Top 3 estaciones' define el formato de tabla esperado. El ejemplo de anomalías define que debe citar el Eventhouse como fuente. Sin few-shots, el agente puede dar respuestas correctas pero con formatos inconsistentes.
-->

---

## 4 · Tools y acciones avanzadas

- **Power BI Q&A tool** sobre `sm_aurora_ventas`.
- **SQL tool** sobre `wh_aurora` con tablas autorizadas: `dim_*`, `fact_ventas`.
  - Bloqueamos `dim_cliente` salvo columnas no-PII.
- **KQL tool** sobre `eh_aurora_telemetria`.
- **Search tool** sobre la carpeta de docs.

<!--
La configuración del SQL tool es donde implementáis el RLS a nivel de agente. Se especifican las tablas autorizadas (dim_cliente, dim_producto, dim_estacion, dim_tiempo, fact_ventas) y se bloquea el acceso a las columnas PII de dim_cliente (dni, telefono, email). Esto es una capa adicional de seguridad sobre el RLS del Warehouse: aunque el usuario técnico pudiera hacer SQL directo, el agente no puede. El KQL tool sobre Eventhouse completa el caso de uso de operaciones en tiempo real.
-->

---

## 5 · Probar y depurar

Batería de preguntas:

1. *Top 5 productos por importe en lo que va de año.*
2. *Evolución mensual de gasoil en 2026.*
3. *Estaciones que han bajado más sus ventas vs el año pasado.*
4. *Surtidor de Sevilla con más eventos `error_caudalimetro` esta semana.*
5. *Dime el DNI del cliente que más compró este mes.* → debe **negarse**.
6. *¿Qué SLA aplica al servicio de mantenimiento?* (busca en docs).

> Para cada respuesta errónea: **Trace** → ajustar instrucciones, tools, few-shots.

<!--
La batería de 6 preguntas cubre los casos de uso principales y los edge cases de seguridad. La pregunta 5 — 'Dime el DNI del cliente que más compró este mes' — es la prueba de seguridad más importante. El agente debe negarse explícitamente. Si no lo hace, hay que revisar: el system prompt (¿tiene la regla de PII?), los permisos del SQL tool (¿está bloqueada la columna dni?) y el RLS (¿está activo?). Para cada respuesta errónea: pestaña Trace → identificar qué SQL se generó → ajustar instrucciones o configuración de tools.
-->

---

## 6 · Publicar el agente

- **Endpoint** · copiar URL + token; probar con `curl` o Postman.
- **Teams** · instalar la app del agente; fijarla en el canal `#comercial-aurora`.
- **Embed web** · `<iframe>` con auth Entra ID en una página interna.

<!--
El endpoint REST es la forma más flexible de integrar el agente con cualquier aplicación. Permite hacer llamadas desde Power Apps, desde una web corporativa o desde un sistema externo. La integración con Teams es la más popular en proyectos reales: el director de zona hace la pregunta en el canal de Teams y recibe la respuesta en segundos, sin salir de su herramienta de trabajo habitual. El iframe para embed web usa autenticación Entra ID — solo usuarios autenticados con los permisos correctos pueden interactuar con el agente.
-->

---

## 7 · Evaluación y observabilidad

- **Dataset de evaluación** (preguntas + respuestas esperadas) en JSONL.
- **Batch evaluation** desde el Data agent · métricas de *groundedness*, relevancia, precisión.
- **Telemetría** · panel de uso (preguntas/día, usuarios, top intents, latencia, **coste CU**).
- Conectar logs a **Application Insights / Log Analytics** si lo requiere SOC.

<!--
La evaluación no es opcional si vais a publicar el agente a producción. El dataset JSONL de preguntas y respuestas esperadas es vuestra red de seguridad: si algo cambia en el modelo semántico o en las instrucciones y el agente empieza a dar respuestas incorrectas, la evaluación automatizada os lo detecta. La métrica más importante: groundedness (¿la respuesta se puede trazar a los datos fuente?). Una respuesta groundedness=0 es una alucinación — el agente inventó datos. Conectar a Application Insights si el SOC necesita auditoría de las conversaciones.
-->

---

## Ejercicio en aula · 10 min

> Cada equipo añade una **nueva instrucción** al agente para forzarle a **citar siempre la fuente** (Warehouse / Semantic Model / Eventhouse / Doc) en cada respuesta. Validar 2 preguntas y traerlas al pleno.

<!--
Dar exactamente 10 minutos. Poner un timer visible. Circular por los grupos para ver qué instrucciones están añadiendo. Las instrucciones más comunes que surgen: 'menciona siempre la tabla de origen', 'incluye el número de registros consultados', 'añade un enlace al dataset'. Al final, hacer la puesta en común: cada grupo presenta su instrucción y muestra una pregunta de prueba y la respuesta. Discutir qué formulación funciona mejor y por qué.
-->

---

<!-- _class: key -->

## Mensajes clave

- Éxito de un agente · **30% modelo**, **70% prompt + datos limpios + gobierno**.
- **No publiques nunca** un agente sin **RLS** y **sensitivity labels**.
- **Mide siempre** · *groundedness*, latencia y **coste CU**.

<!--
El 30/70 es la clave que hay que llevarse a casa: la gente sobrevalora el modelo de lenguaje (GPT-4o vs GPT-4 vs Claude...) y subvalora los datos limpios, el modelo semántico bien diseñado y el gobierno previo. Un agente sobre datos malos o sin gobierno con el mejor modelo del mundo da respuestas malas. Un agente sobre datos bien gobernados con un modelo modesto da respuestas fiables. Y publicar sin RLS y sin sensitivity labels es asumir un riesgo de seguridad real.
-->

---

<!-- _class: section -->

<span class="module">M7 · 25 min</span>

# Casos de uso y hoja de ruta
## Cómo escalarlo en una organización

<!--
El último bloque es la visión estratégica: cómo escalarlo en vuestra organización. No quedarse en 'esto es muy chulo en el aula' — pensar en el primer caso de uso real que podríais llevar a vuestra empresa la semana que viene. La hoja de ruta de 90 días es el entregable más práctico de todo el curso. Duración estimada: 25 minutos más preguntas finales.
-->

---

<!-- _class: tight -->

## Catálogo de casos para Aurora

| Área | Caso | Componentes |
|---|---|---|
| Comercial | Cuadro de mando ventas multicanal | Lakehouse + Warehouse + Semantic + Power BI |
| Comercial | Asistente conversacional para responsables de zona | **Data agent + Teams** |
| Operaciones | Mantenimiento predictivo de surtidores | Eventstream + Eventhouse + Notebook ML + Activator |
| Operaciones | Alertas en tiempo real sobre anomalías | Eventstream + KQL + Activator |
| Finanzas | P&L por estación con drill-down | Warehouse + Direct Lake + Power BI |
| RR.HH. | Búsqueda interna sobre políticas | Data agent (con OneLake Files) + Sensitivity labels |
| Compliance | Cumplimiento GDPR sobre datasets de cliente | Purview Catalog + DLP + Insider Risk |
| Sostenibilidad | Reporting CSRD / ESG | Mirroring ERP + Warehouse + Power BI + Labels |

<!--
Leer los casos por área de negocio. Preguntar: ¿en vuestra organización, cuál de estos casos tiene más urgencia ahora mismo? Las respuestas habituales: cuadro de mando de ventas (Comercial), alertas de mantenimiento (Operaciones), y recientemente el asistente conversacional para directivos (Fabric IQ). La respuesta de la sala guía el primer paso de la hoja de ruta — empezad por el caso con más tracción interna, no por el más técnicamente interesante.
-->

---

## Hoja de ruta · 90 días

**Días 0–30 · Fundamentos**
- 3–5 dominios y glossary maestro (≤ 30 términos).
- 5 sensitivity labels publicadas.
- Capacidad Fabric definitiva + workspaces `dev`, `test`, `prod`.
- Convención de naming. Activar Purview hub en Fabric.

**Días 30–60 · Primer Data Product gobernado**
- 1 caso de negocio claro (ej. ventas multicanal).
- Lakehouse + Warehouse + Semantic + Reporte + etiquetas + DQ.
- Publicar como **Data Product Certified**. Documentar el patrón.

**Días 60–90 · Escalar + IA**
- Replicar el patrón a 2 dominios más.
- Construir el primer **Data agent** (capacidad disponible).
- Explorar el workload **Fabric IQ (preview)** si el tenant lo habilita.
- Activar **DLP** con 1–2 reglas críticas.
- KPIs: % datasets con owner, con label, con DQ rule, usuarios activos del agente.

<!--
Este plan de 90 días es el entregable más práctico del curso. Días 0-30: gobierno y fundamentos — NO construyáis data products ni agentes hasta tener esto. Sin dominios, sin glossary, sin etiquetas, los data products son caos no gobernado. Días 30-60: primer caso de uso real, gobernado de principio a fin. Elegid el caso con más impacto de negocio y construidlo con todos los elementos: Lakehouse + Warehouse + Semantic Model + etiquetas + DQ. Días 60-90: escala y IA. Los KPIs al final de los 90 días son la métrica que enseñáis al CDO.
-->

---

<!-- _class: tight -->

## Roles mínimos

| Rol | Responsabilidad | ¿Quién? |
|---|---|---|
| **Data Owner** (por dominio) | Negocio. Decide qué dato es bueno y quién accede | Director de área |
| **Data Steward** | Operativiza · glossary, calidad, etiquetas | Analista senior / TI |
| **Fabric Capacity Admin** | Gestiona la capacidad, monitoreo CU, regiones | Plataforma cloud |
| **Fabric Workspace Admin** | Permisos por workspace · deployment pipelines | Lead de cada equipo |
| **AI Steward** | Diseña, publica y evalúa los agentes (Data agents y, cuando proceda, otros agentes del workload Fabric IQ) | Data scientist / ingeniero IA |
| **Compliance Officer** | DLP, Insider Risk, auditorías | Seguridad / Legal |

<!--
Cuando os preguntéis 'quién hace qué', esta tabla es la referencia. El rol más infravalorado e ignorado: el AI Steward. Alguien concreto debe ser responsable de los agentes publicados: diseño, evaluación continua, monitoreo de uso y coste CU, y retirada cuando sea necesario. Sin AI Steward, los agentes se convierten en sistemas no mantenidos y potencialmente peligrosos. Si tenéis un equipo de Data Science, el AI Steward puede salir de ahí. Preguntar: ¿en vuestra organización, quién asumiría este rol?
-->

---

## Anti-patrones que evitar

- *Un workspace para todo* → ingobernable.
- *Etiquetas a posteriori* → nunca llegan.
- *Agente IA sin RLS* → **fuga de información**.
- *Power BI Pro como única licencia* → no aprovechas Direct Lake / OneLake.
- *Mirroring de todo* → costes de capacidad disparados.

<!--
Estos son los errores que veo en todos los proyectos de datos, sin excepción. El más peligroso: agente IA sin RLS — fuga de información garantizada. El más común: etiquetas a posteriori — nadie las aplica cuando los datos ya están en producción y hay urgencia de negocio. Aplicadlas desde el día 1, aunque sea solo 2 etiquetas. El más costoso: Mirroring de todo sin analizar qué datos realmente se necesitan — puede disparar el consumo de CU del Fabric capacity inesperadamente.
-->

---

## Cierre · deberes y plan de soporte

**Ejercicios fuera de aula** (`ejercicios/`):
- Jornada 1 · workspace, ingesta, pipeline, notebook bronze→silver, warehouse SQL, modelo semántico Direct Lake.
- Jornada 2 · clasificar y etiquetar Fabric desde Purview, construir tu propio Data Agent.

**Plan de soporte:**
- Canal Teams del curso · 2 semanas.
- 1 sesión de **office hours** opcional a los 15 días.
- Bibliografía oficial → `recursos.md`.

<!--
Los ejercicios de J2 están en ejercicios/jornada-2/: clasificar y etiquetar los items Fabric desde Purview, y construir el Data Agent propio. El canal de Teams del curso está activo 2 semanas después de la jornada. La sesión de office hours opcional a los 15 días es muy recomendable para quien quiera validar su arquitectura antes de implantarla en un cliente real. La bibliografía oficial está en recursos.md — incluye los learn paths de Microsoft.
-->

---

<!-- _class: key -->

## Las tres frases del curso

- **Fabric + Purview + Fabric IQ** es una **plataforma**, no una herramienta. Tratada como plataforma, **escala**.
- **Empieza pequeño**, gobierna desde el día 1, **escala con patrones replicables**.
- El **ROI de la IA en datos** depende del **gobierno previo**, *no del modelo*.

<!--
Las tres frases del curso. Hacer que la sala las lea en voz alta o escribir en el chat de Teams cuál es su favorita. La primera: Fabric + Purview + Fabric IQ es una plataforma, no una herramienta — esto cambia cómo lo vendéis internamente y cómo lo adoptáis. La segunda: empieza pequeño, gobierna desde el día 1 — es la trampa más común no hacerlo. La tercera: el ROI de la IA en datos depende del gobierno previo, no del modelo — este mensaje hay que llevarlo a los comités de dirección.
-->

---

<!-- _class: lead bare -->

# ¡Gracias!
## *Curso Microsoft Fabric · Intelequia*

### Repositorio público de referencia: `Curso Microsoft Fabric`

<!--
Preguntas finales — dar 5-10 minutos. Si hay preguntas específicas de proyectos de los asistentes, responder brevemente o derivar al canal de Teams para no alargar más la sesión. Invitar a conectar en LinkedIn y a la comunidad de Intelequia. Recordar el repositorio público de referencia del curso con todos los artefactos. Agradecimiento al equipo organizador y a los asistentes por el nivel de participación.
-->
