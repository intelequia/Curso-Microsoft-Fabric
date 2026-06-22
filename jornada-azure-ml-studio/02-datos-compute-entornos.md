# AML-M2 · Datos, compute y entornos

**Duración:** 35 min · **Formato:** explicación + demo guiada

## Objetivos

1. Preparar datos reutilizables para experimentos y pipelines.
2. Elegir compute instance, compute cluster o serverless según el trabajo.
3. Entender environments como base de reproducibilidad.

## Hilo narrativo

> "Antes de entrenar modelos hay que estabilizar tres cosas: de dónde salen los datos, dónde se ejecuta el trabajo y con qué dependencias."

## Contenido

En Azure ML, los datos se consumen mediante datastores y data assets. El datastore apunta a almacenamiento físico; el data asset da nombre, versión y semántica a un conjunto de datos. Esta separación evita copiar datos innecesariamente y permite que notebooks, jobs y pipelines usen la misma referencia.

### Datos

| Elemento | Uso |
| --- | --- |
| **Datastore** | Conexión a Storage, ADLS Gen2 u otros orígenes soportados. |
| **Data asset** | Dataset versionado para entrenamiento, validación o scoring. |
| **MLTable** | Definición estructurada para leer datos tabulares con transformaciones básicas. |
| **OneLake / Fabric** | Origen o destino de datos cuando la organización trabaja en Fabric. |

Con Fabric, el patrón recomendado es evitar duplicados: acceder al mismo almacenamiento cuando sea posible, usar shortcuts o datastores compatibles y documentar qué plataforma es dueña del dato.

### Compute

| Compute | Cuándo usarlo |
| --- | --- |
| **Compute instance** | Exploración, notebooks y debugging. |
| **Compute cluster** | Entrenamiento repetible, AutoML, pipelines y jobs escalables. |
| **Serverless compute** | Pruebas rápidas cuando está disponible y encaja con las políticas del tenant. |
| **Managed online endpoint** | Inferencia online con baja latencia. |
| **Batch endpoint** | Scoring masivo o programado sobre ficheros/tablas. |

### Entornos

Un environment define imagen base, paquetes Conda/pip y configuración de ejecución. El objetivo no es solo que el notebook funcione hoy, sino que el entrenamiento se pueda repetir mañana en otro compute.

## Demo en vivo

1. Crear o revisar el datastore por defecto del workspace.
2. Registrar un data asset tabular con datos de incidencias de Aurora.
3. Mostrar compute instance y compute cluster `cpu-cluster`.
4. Revisar un environment gestionado y explicar cuándo crear uno propio.
5. Abrir una vista de datos y validar columnas clave.

## Mensajes clave

- El notebook no debería depender de rutas locales frágiles.
- El compute cluster debe escalar a cero para controlar coste.
- Los environments son parte del producto, no un detalle técnico.
