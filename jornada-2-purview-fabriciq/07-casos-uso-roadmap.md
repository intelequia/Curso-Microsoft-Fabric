# J2-M7 · Casos de uso, hoja de ruta de adopción y cierre

**Duración:** 30 min · **Formato:** taller participativo + cierre

## Objetivos

1. Conectar todo lo aprendido con casos de uso reales aplicables a una organización energética.
2. Proponer una **hoja de ruta de adopción** Fabric + Purview + Data agents realista.
3. Definir **roles y responsabilidades** mínimos.
4. Cerrar con **deberes para casa** (ejercicios pendientes) y los **siguientes pasos**.

## Contenido

### 1. Catálogo de casos de uso para Aurora Energía

| Área | Caso | Componentes |
| --- | --- | --- |
| Comercial | Cuadro de mando ventas multicanal (gasolinera, EV, electricidad, gas) | Lakehouse + Warehouse + Semantic Model + Power BI |
| Comercial | Asistente conversacional para responsables de zona | Data agent + Teams |
| Operaciones | Mantenimiento predictivo de surtidores | Eventstream + Eventhouse + Notebook ML + Activator |
| Operaciones | Alertas en tiempo real sobre anomalías de caudal | Eventstream + KQL + Activator → Teams/SMS |
| Finanzas | P&L por estación con drill-down | Warehouse + Direct Lake + Power BI |
| RR.HH. | Búsqueda interna sobre políticas y convenios | Data agent (con OneLake Files) + Sensitivity labels |
| Compliance | Cumplimiento GDPR sobre datasets de cliente | Purview Catalog + DLP + Insider Risk |
| Sostenibilidad | Reporting CSRD/ESG | Mirroring ERP + Warehouse + Power BI + Sensitivity labels |

### 2. Hoja de ruta sugerida (90 días)

**Días 0–30 — Fundamentos**

- Diseñar **dominios** (3–5) y **glossary maestro** (≤30 términos).
- Definir **5 sensitivity labels** y publicarlas.
- Crear capacidad Fabric definitiva (F-SKU según uso) + 3 workspaces (`-dev`, `-test`, `-prod`).
- Establecer convención de naming.
- Activar Purview hub en Fabric.

**Días 30–60 — Primer Data Product gobernado**

- Elegir **un caso de negocio claro** (ej. ventas multicanal).
- Construir Lakehouse + Warehouse + Semantic Model + Reporte.
- Aplicar etiquetas, glossary, owner, calidad.
- Publicar como **Data Product Certified** en Unified Catalog.
- Documentar el patrón.

**Días 60–90 — Escala + IA**

- Replicar el patrón a **2 dominios más**.
- Construir el **primer Data agent** sobre el dominio piloto (capacidad GA dentro de Fabric).
- Evaluar el **workload Fabric IQ (preview)** — Ontology, Graph, Plan, Operations agent — cuando esté disponible en el tenant.
- Habilitar DLP en Fabric/Power BI con 1–2 reglas críticas.
- KPIs operativos: % datasets con owner, % con label, % con DQ rule, nº usuarios activos del agente.
- Plan de formación al resto del equipo.

### 3. Roles mínimos

| Rol | Responsabilidad | ¿Quién? |
| --- | --- | --- |
| **Data Owner** (por dominio) | Negocio. Decide qué dato es bueno y quién accede | Director de área |
| **Data Steward** | Operativiza el gobierno: glossary, calidad, etiquetas | Analista senior / TI |
| **Fabric Capacity Admin** | Gestiona la capacidad, monitoreo CU, regiones | Plataforma cloud |
| **Fabric Workspace Admin** | Permisos a nivel workspace y deployment pipelines | Lead de cada equipo |
| **AI Steward** | Diseña, publica y evalúa los agentes (Data agents y, cuando proceda, otros agentes del workload Fabric IQ) | Data scientist / ingeniero IA |
| **Compliance Officer** | DLP, Insider Risk, auditorías | Seguridad / Legal |

### 4. Anti-patrones que evitar

- "Un workspace para todo" → ingobernable.
- "Etiquetas a posteriori" → nunca llegan.
- "Agente IA sin RLS" → fuga de información.
- "Power BI Pro como única licencia" → no aprovechas Direct Lake / OneLake.
- "Mirroring de todo" → costes de capacidad disparados.

### 5. Cierre y deberes

Repaso del **dossier de ejercicios fuera de aula** (ver carpeta `ejercicios/`):

- Jornada 1: workspace, ingesta, pipeline, notebook bronze→silver, warehouse SQL, modelo semántico Direct Lake.
- Jornada 2: clasificar y etiquetar Fabric desde Purview, construir tu propio Data agent.

Plan de soporte:

- Canal Teams del curso para dudas durante 2 semanas.
- 1 sesión de office hours opcional a los 15 días.
- Bibliografía oficial → ver `recursos.md`.

## Mensajes clave

- "Fabric + Purview + Data agents es una **plataforma**, no una herramienta. Tratada como plataforma, escala. Tratada como herramienta, fracasa. Y el workload **Fabric IQ (preview)** es lo siguiente que vendrá sobre esa plataforma."
- "Empieza pequeño, gobierna desde el día 1, escala con patrones replicables."
- "El ROI de la IA en datos depende del **gobierno previo**, no del modelo."
