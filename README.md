# Curso Microsoft Fabric + Purview + Fabric IQ

Master class de **8 horas**, distribuidas en **2 jornadas de 4 horas** (con un descanso de 15 minutos cada una). Pensado para grupos de hasta **25 alumnos** en formato **master class**, con demostraciones en vivo, ejercicios cortos en aula y un **bloque de práctica guiada** que el alumno completa fuera del horario de clase con los assets que se entregan en este repositorio.

> Repositorio público de referencia: **Curso Microsoft Fabric**.
>
> Todos los datos, nombres de empresa, esquemas y casos de uso de este material son **ficticios**. Usamos como hilo conductor una compañía inventada llamada **"Aurora Energía"** — un operador ficticio con red de estaciones de servicio, comercializadora eléctrica y una división de logística — para que las prácticas tengan continuidad sin referirse a ningún cliente real.

## Objetivos generales

Al finalizar el curso, el alumno será capaz de:

1. Entender la arquitectura de **Microsoft Fabric** (OneLake, capacidades, workspaces, artefactos) y elegir la pieza correcta para cada caso (Lakehouse vs Warehouse vs Eventhouse vs Power BI).
2. Construir un flujo end-to-end de **ingesta → transformación → modelo semántico → visualización** sobre Fabric.
3. Comprender el papel de **Microsoft Purview** como capa de gobierno: Data Map, catálogo, clasificación, etiquetas de sensibilidad y DLP, y cómo se integra con Fabric.
4. Conocer **Fabric IQ** (la nueva capa de inteligencia y razonamiento sobre datos en Fabric) y los escenarios donde aporta valor: Q&A en lenguaje natural, agentes de datos, semantic modeling asistido y observabilidad de uso.
5. Identificar el siguiente paso de adopción en su organización (qué workloads piloto tienen sentido, qué gobierno mínimo aplicar, dónde encaja Fabric IQ).

## Agenda

### Jornada 1 — Microsoft Fabric (4 h)

| Bloque | Duración | Tema |
| --- | --- | --- |
| J1-M0 | 15 min | Bienvenida, agenda, contexto del curso, presentación del caso ficticio Aurora Energía |
| J1-M1 | 30 min | [Fundamentos: arquitectura, capacidades, licencias, OneLake](jornada-1-fabric/01-fundamentos.md) |
| J1-M2 | 35 min | [Lakehouse, Warehouse y SQL endpoint](jornada-1-fabric/02-lakehouse-warehouse.md) |
| J1-M3 | 40 min | [Ingesta: Dataflow Gen2 y Data Pipelines](jornada-1-fabric/03-ingesta-dataflows-pipelines.md) |
| — | 15 min | **Descanso** |
| J1-M4 | 35 min | [Notebooks, Spark y procesamiento de datos](jornada-1-fabric/04-notebooks-spark.md) |
| J1-M5 | 30 min | [Warehouse en profundidad y Direct Lake](jornada-1-fabric/05-warehouse-directlake.md) |
| J1-M6 | 25 min | [Real-Time Intelligence: Eventhouse y KQL](jornada-1-fabric/06-realtime-eventhouse.md) |
| J1-M7 | 25 min | [Power BI sobre Fabric: modelo semántico y reportes](jornada-1-fabric/07-powerbi-modelo-semantico.md) |
| J1-M8 | 10 min | Cierre, preguntas y deberes (ejercicios para casa) |

### Jornada 2 — Microsoft Purview + Fabric IQ (4 h)

| Bloque | Duración | Tema |
| --- | --- | --- |
| J2-M0 | 15 min | Repaso de la jornada 1, agenda de hoy, dudas |
| J2-M1 | 30 min | [Por qué gobierno: panorama Purview y Fabric](jornada-2-purview-fabriciq/01-purview-fundamentos.md) |
| J2-M2 | 40 min | [Purview Data Map y Catálogo Unificado](jornada-2-purview-fabriciq/02-purview-data-map-catalogo.md) |
| J2-M3 | 30 min | [Information Protection, etiquetas de sensibilidad y DLP](jornada-2-purview-fabriciq/03-purview-information-protection-dlp.md) |
| — | 15 min | **Descanso** |
| J2-M4 | 25 min | [Integración Purview ↔ Fabric: gobierno extremo a extremo](jornada-2-purview-fabriciq/04-purview-fabric-integracion.md) |
| J2-M5 | 35 min | [Fabric IQ: qué es, arquitectura y posicionamiento](jornada-2-purview-fabriciq/05-fabric-iq-fundamentos.md) |
| J2-M6 | 30 min | [Fabric IQ en acción: Data Agents y Q&A en lenguaje natural](jornada-2-purview-fabriciq/06-fabric-iq-data-agents.md) |
| J2-M7 | 25 min | [Casos de uso, mejores prácticas y hoja de ruta](jornada-2-purview-fabriciq/07-casos-uso-roadmap.md) |
| J2-M8 | 15 min | Cierre, próximos pasos, recursos y Q&A |

## Estructura de este repositorio

```
contenidos/
├── README.md                       ← este fichero
├── requisitos.md                   ← qué necesita tener instalado el alumno
├── 00-preparacion-entorno.md       ← cómo crear la trial de Fabric paso a paso
├── jornada-1-fabric/               ← contenido teórico/demo de la jornada 1
├── jornada-2-purview-fabriciq/     ← contenido teórico/demo de la jornada 2
├── ejercicios/
│   ├── jornada-1/                  ← prácticas guiadas (mayoría para casa)
│   └── jornada-2/
├── assets/
│   ├── data/                       ← CSV/JSON de ejemplo (Aurora Energía)
│   ├── sql/                        ← scripts T-SQL para Warehouse
│   ├── kql/                        ← consultas KQL de ejemplo
│   └── notebooks/                  ← notebooks PySpark/Spark SQL
└── recursos.md                     ← enlaces oficiales y bibliografía
```

## Metodología

- **Master class** con explicación + demo en vivo del formador.
- **2 ejercicios cortos en aula** por jornada (10–15 min) para mantener el ritmo.
- **Pack de ejercicios para casa** por jornada (~3–4 h cada pack) totalmente guiados, con checklist de validación.
- **Caso unificado**: todos los ejercicios construyen incrementalmente el mismo entorno de Aurora Energía.
- **Canal de soporte asíncrono** entre las dos jornadas (recomendado: un canal de Teams o un repositorio de issues) para resolver dudas de los ejercicios para casa.

## Antes de empezar

1. Lee [requisitos.md](requisitos.md) y prepara tu equipo con todo lo indicado **antes** de la primera jornada.
2. Sigue [00-preparacion-entorno.md](00-preparacion-entorno.md) para crear tu trial de Microsoft Fabric. Si tu organización ya dispone de capacidad Fabric, hablamos en el primer bloque sobre cómo solicitarte un workspace propio.
3. Descarga la carpeta [assets/data](assets/data) en local: la usarás en varios ejercicios.

## Licencia y uso del material

Material elaborado por Intelequia para uso formativo. Puedes reutilizarlo internamente citando la fuente. Los datos sintéticos incluidos pueden modificarse y publicarse libremente.
