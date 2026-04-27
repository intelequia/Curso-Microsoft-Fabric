# J1-M6 · Real-Time Intelligence: Eventhouse y KQL

**Duración:** 25 min · **Formato:** explicación + demo en vivo

## Objetivos

1. Entender la **Real-Time Intelligence** de Fabric: Eventstream, Eventhouse, KQL DB, Activator y Real-Time Dashboard.
2. Crear un Eventhouse con la telemetría de surtidores de Aurora Energía.
3. Conocer la sintaxis básica de **KQL** (Kusto Query Language).
4. Identificar cuándo usar Real-Time vs Lakehouse/Warehouse.

## Contenido

### 1. Mapa de la Real-Time Intelligence

```
[Origen: IoT Hub, Event Hub, Kafka, sample]
            ↓
       Eventstream
            ↓
   ┌────────┼─────────┐
   ↓        ↓         ↓
Eventhouse  Lakehouse  Activator
 (KQL DB)   (Delta)    (alertas)
```

- **Eventstream**: ingesta de streaming, no-code, transformaciones simples (filtro, agregación, JOIN con tabla de referencia).
- **Eventhouse / KQL Database**: motor analítico orientado a series temporales y logs. La estrella es **KQL**.
- **Activator**: motor de reglas → dispara acciones (correo, Teams, Power Automate, llamada a Pipeline) cuando se cumple una condición sobre el stream o sobre Power BI.
- **Real-Time Dashboard**: dashboard tipo Grafana/Kusto Explorer integrado en Fabric.

### 2. Eventhouse vs Lakehouse para series temporales

| Caso | Mejor opción |
| --- | --- |
| Telemetría de IoT, logs, eventos clickstream, security events | Eventhouse / KQL |
| Histórico analítico de negocio (ventas, finanzas) | Lakehouse / Warehouse |
| Necesito query en milisegundos sobre miles de millones de eventos | Eventhouse |
| Necesito unión a un modelo dimensional de negocio | Lakehouse / Warehouse |

### 3. KQL en 5 minutos

Sintaxis pipe-based (`|`), parecida a `pandas` o a un SQL más legible:

```kql
// Top 10 estaciones por número de eventos en las últimas 24h
TelemetriaSurtidor
| where Timestamp > ago(24h)
| summarize Eventos = count() by EstacionId
| top 10 by Eventos desc

// Detección de surtidores con caudal anómalo
TelemetriaSurtidor
| where Timestamp > ago(1h)
| summarize CaudalMedio = avg(Caudal) by EstacionId, SurtidorId, bin(Timestamp, 5m)
| where CaudalMedio < 0.5 or CaudalMedio > 80

// Time series con make-series y series_decompose_anomalies
TelemetriaSurtidor
| where Timestamp > ago(7d)
| make-series Caudal = avg(Caudal) default=0 on Timestamp step 10m by EstacionId
| extend anomalies = series_decompose_anomalies(Caudal, 1.5)
```

### 4. Caso Aurora Energía

- 250 estaciones × 6 surtidores × eventos cada 30s.
- Eventstream desde Event Hub (simulado en aula con **Sample Data → Stocks** o **Bicycle rentals** y rebautizado).
- Tabla `TelemetriaSurtidor` con columnas: `Timestamp`, `EstacionId`, `SurtidorId`, `Producto`, `Caudal`, `Temperatura`, `Estado`.
- Dashboard con tiles: eventos/min, caudal medio, top alertas, mapa.

### 5. Activator (mención breve)

- Definir reglas como: "Si `Temperatura > 65 °C` en una estación durante > 3 min, enviar correo al jefe de estación".
- En Aurora Energía: alertas predictivas de mantenimiento.

## Demo en vivo (10 min)

1. Crear `eh_aurora_telemetria` (Eventhouse) en el workspace.
2. Crear un **Eventstream** y agregar **Sample data → Bicycle rentals** (o similar) como origen.
3. Agregar **destination → Eventhouse**, mapear a tabla `TelemetriaSurtidor` (renombrar columnas para que encaje con el caso).
4. Esperar 30s y abrir KQL Queryset.
5. Lanzar las 3 queries del apartado 3 (adaptadas al esquema generado).
6. Crear un **Real-Time Dashboard** con un par de tiles.
7. Crear un **Activator** simple (regla `Caudal > X`) y enseñar el panel de actions.

## Mensajes clave

- "KQL no asusta — para un SQL-ero se aprende en una tarde."
- "Eventhouse no reemplaza al Warehouse: convive con él."
- "Activator es la pieza que cierra el círculo: del dato al acto."
