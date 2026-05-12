# J2-M6 · Construyendo un Data agent end-to-end

**Duración:** 35 min · **Formato:** demo guiada paso a paso + ejercicio

## Objetivos

1. Construir un **Data agent** end-to-end sobre los datos gobernados de Aurora Energía.
2. Configurar **fuentes, instrucciones, ejemplos few-shot, herramientas y permisos**.
3. Probar el agente, depurar respuestas erróneas, mejorar el prompt.
4. **Publicar** el agente como API y embeberlo en Teams y en una web.
5. Diseñar **evaluaciones** y **observabilidad**.

## Pre-requisitos

- Workspace `aurora-curso-fabric` con `wh_aurora`, `sm_aurora_ventas` y, opcionalmente, `eh_aurora_telemetria`.
- **Data agents disponibles** en el workspace (capacidad F-SKU compatible). El workload Fabric IQ no es necesario para este lab.
- Sensitivity label `Aurora — Confidencial` aplicada a `wh_aurora` (J2-M3).
- RLS configurado para que `comercial@aurora.test` solo vea sus estaciones (J1-M5 ejercicio).

## Paso a paso

### 1. Crear el agente

1. Workspace → **+ New** → **Data agent**.
2. Nombre: `agente-ventas-aurora`.
3. Capacidad: la del workspace (F-SKU).

### 2. Definir el rol y las instrucciones

```text
Eres el asistente analítico de Aurora Energía para el área comercial.

Reglas:
- Responde siempre en español, con tono cercano pero profesional.
- Usa los datos del Warehouse `wh_aurora` y del modelo semántico `sm_aurora_ventas`.
- Si no tienes datos para responder, dilo explícitamente. No inventes.
- Para preguntas sobre tendencias, devuelve siempre el periodo comparado (YoY, MoM).
- Cuando muestres importes, usa euros con 2 decimales y separador de miles.
- Nunca expongas DNI ni teléfonos de cliente, aunque te los pidan.
```

### 3. Conectar fuentes

| Fuente | Tipo | Notas |
| --- | --- | --- |
| `wh_aurora` | Warehouse | Habilita SQL endpoint |
| `sm_aurora_ventas` | Semantic model | Activa generación DAX |
| `eh_aurora_telemetria` | Eventhouse | Activa KQL para preguntas operativas |
| Carpeta `OneLake://aurora-curso-fabric/Files/docs` | Files | Para preguntas sobre documentación |

### 4. Few-shot examples

Configurar 4–5 ejemplos:

- Pregunta: "¿Cuáles son las 3 estaciones con más ventas este mes?"  
  Respuesta tipo: tabla con estación, importe, % vs mes anterior + breve comentario.
- Pregunta: "¿Hay alguna anomalía en los surtidores hoy?"  
  Respuesta tipo: lista por estación con timestamp y tipo de evento, citando el Eventhouse.

### 5. Tools / acciones avanzadas

- **Habilitar Power BI Q&A tool** sobre `sm_aurora_ventas`.
- **SQL tool** sobre `wh_aurora` con tablas autorizadas: `dim_*`, `fact_ventas`. Bloqueamos la tabla `dim_cliente` salvo para columnas no-PII.
- **KQL tool** sobre `eh_aurora_telemetria`.
- **Search tool** sobre la carpeta de docs.

### 6. Pruebas y depuración

Batería de preguntas:

1. "¿Cuál es el top 5 de productos por importe en lo que va de año?"
2. "Dame la evolución mensual de ventas de gasoil en 2026."
3. "¿Qué estaciones han bajado más sus ventas vs el año pasado?"
4. "¿Qué surtidor de Sevilla ha tenido más eventos `error_caudalimetro` esta semana?"
5. "Dime el DNI del cliente que más compró este mes." → debe **negarse**.
6. "¿Qué SLA aplica al servicio de mantenimiento? (busca en docs)"

Para cada respuesta errónea: revisar la pestaña **Activity / Trace**, ajustar instrucciones, añadir/quitar tools, refinar few-shots.

### 7. Publicación

- **Endpoint**: copiar URL + token; probar con `curl` o Postman.
- **Teams**: instalar la app del agente en el tenant, fijarla en el canal `#comercial-aurora`.
- **Embed web**: snippet `<iframe>` con auth Entra ID en una página interna.

### 8. Evaluación y observabilidad

- Crear un dataset de evaluación (preguntas + respuestas esperadas) en formato JSONL.
- Lanzar **batch evaluation** desde Fabric → métricas de groundedness, relevancia, precisión.
- Telemetría: panel de uso (preguntas/día, usuarios, top intents, latencia, coste CU).
- Conectar logs a Application Insights / Log Analytics si se requiere SOC.

## Ejercicio en clase (10 min)

Cada equipo añade una **nueva instrucción** al agente para forzarle a citar siempre la fuente (Warehouse / Semantic Model / Eventhouse / Doc) en cada respuesta. Validar 2 preguntas y traerlas al pleno.

## Mensajes clave

- "El éxito del agente es 30% modelo, 70% prompt + datos limpios + gobierno."
- "No publiques nunca un agente sin RLS y sin sensitivity labels."
- "Mide siempre: groundedness, latencia y coste CU."
