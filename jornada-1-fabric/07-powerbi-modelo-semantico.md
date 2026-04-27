# J1-M7 · Power BI sobre Fabric: modelo semántico y reportes

**Duración:** 25 min · **Formato:** demo en vivo + cierre

## Objetivos

1. Crear un **modelo semántico Direct Lake** sobre `wh_aurora`.
2. Construir un **reporte Power BI** básico publicado en Fabric.
3. Conocer **Power BI Desktop developer mode (PBIP)** y **Git integration**.
4. Mencionar **Apps**, **Subscriptions** y **Embed**.

## Contenido

### 1. Modelo semántico

- **Default semantic model** del Lakehouse → tablas detectadas automáticamente, sin relaciones definidas.
- **Custom semantic model** → recomendado para producción: defines relaciones, jerarquías, medidas DAX, perspectivas, RLS.
- Se crea desde el item Lakehouse/Warehouse o vía Power BI Desktop conectando a Fabric.

### 2. Medidas DAX típicas para Aurora Energía

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

### 3. Reportes y publicación

- Reporte web directo en Fabric (Power BI experience), o desde Power BI Desktop publicando.
- **Apps** para empaquetar reportes y distribuirlos a colectivos (lectores Free necesitan F64+).
- **Subscriptions** programadas, **Subscribe to data alert**, **Comments**, **Workspace OneLake hub**.

### 4. PBIP y Git

- Power BI Desktop guarda en formato **.pbip** (carpeta + JSON/TMDL/PBIR), versionable en Git.
- Workspaces de Fabric tienen **Source control** integrado (Git en Azure DevOps o GitHub).
- Permite revisar PRs sobre el modelo semántico y los reportes.

### 5. Direct Lake — recordatorio de buenas prácticas

- Que las tablas Delta tengan tipos correctos (no `STRING` para fechas).
- Particionar columnas grandes ayuda al **column store** del modelo.
- Evitar **calculated columns** complejas en el modelo: muévelas al Lakehouse/Warehouse.
- Vigilar el **fallback to DirectQuery** en el indicador del modelo.

## Demo en vivo (12 min)

1. Desde `wh_aurora` → **Nuevo modelo semántico** → marcar las 5 tablas + vistas.
2. Renombrar al modelo `sm_aurora_ventas`. Crear relaciones (estrella).
3. Añadir las medidas DAX del apartado 2.
4. **+ Nuevo reporte** sobre el modelo.
5. Construir página: KPI `Importe Total`, gráfico de barras por categoría, mapa por provincia, tabla top 10 clientes.
6. Publicar y mostrar al alumno cómo aparece en el workspace.
7. Mostrar **App** vacía y cómo se publicaría.
8. Mostrar **Source control** del workspace conectado a un repo Git de demo (capturas si no hay tiempo).

## Cierre de Jornada 1

Recapitulación visual:

```
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

### Deberes para casa antes de la Jornada 2

- Completar todos los ejercicios de [ejercicios/jornada-1/](../ejercicios/jornada-1/).
- Tener su workspace `aurora-curso-fabric` con: Lakehouse, Warehouse, Notebook ejecutado, Pipeline programado y Reporte publicado.
- Lectura ligera: índice de [ejercicios/jornada-2/](../ejercicios/jornada-2/) para llegar contextualizado al gobierno y a Fabric IQ.
