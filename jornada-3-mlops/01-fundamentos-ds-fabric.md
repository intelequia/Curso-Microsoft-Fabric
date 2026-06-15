# J3-M1 · Fundamentos de Data Science en Microsoft Fabric

**Duración:** 25 min · **Formato:** explicación + demo en vivo · **Pre-requisito:** haber completado Jornada 1 (Lakehouse `lh_aurora` operativo)

## Objetivos

1. Conocer la experiencia **Data Science** de Fabric y dónde encaja respecto a Data Engineering.
2. Distinguir los **runtimes** disponibles (Python puro, PySpark, R) y los **Environments** como mecanismo de paquetes y configuración.
3. Saber qué librerías vienen **preinstaladas** (scikit-learn, statsmodels, Prophet, LightGBM, XGBoost, PyTorch, MLflow, SynapseML) y cómo añadir las propias.
4. Entender el papel de **Copilot for Data Science** y **Data Wrangler**.

## Hilo narrativo

> "En Aurora Energía ya tenemos los datos limpios en el Lakehouse y publicados en el Warehouse. Pero el negocio quiere ir más allá del *qué pasó* y entrar en el *qué va a pasar* (forecast) y el *qué es raro* (anomalías). Para eso necesitamos el segundo músculo de Fabric: **Data Science**."

Tres ideas que se repiten:

- **Mismo workspace, mismo OneLake**: el científico de datos no copia datos, los **lee directamente** de las tablas Delta del Lakehouse.
- **MLflow es ciudadano de primera clase**: Fabric expone `Experiments` y `ML Models` como items nativos del workspace, con UI propia.
- **`PREDICT` cierra el círculo**: el modelo entrenado se invoca en T-SQL o en PySpark sin desplegar endpoint.

## Contenido

### 1. La experiencia Data Science

- Acceso desde el *app switcher* → **Data Science**.
- Items específicos: **Notebook**, **Experiment**, **ML Model**, **Environment**.
- Comparte capacidad y permisos con el resto de items del workspace (no hay billing aparte).

### 2. Runtimes y pools

| Runtime | Cuándo usarlo |
| --- | --- |
| **Spark (PySpark / Spark SQL)** | Datasets grandes, joins entre tablas Delta, feature engineering distribuido |
| **Python "puro" (pandas / single-node)** | Prototipado, datasets que caben en memoria, entrenamientos de scikit-learn / Prophet |
| **R** | Estadística clásica, equipos con código heredado en R |
| **GPU pools** (opcionales según SKU) | Entrenamiento PyTorch / TensorFlow, transformers |

> Los notebooks de Fabric soportan **High Concurrency Mode** y **session sharing**: varios notebooks pueden compartir la misma sesión Spark caliente.

### 3. Environments

- Un **Environment** es un artefacto del workspace que define:
  - **Runtime de Spark** (versión).
  - **Paquetes Python/R** extra (`requirements.txt` o subida de `.whl`).
  - **Spark properties** y configuración de pool.
- Se **adjunta a notebooks y Spark Job Definitions**.
- Permite reproducibilidad: el mismo Environment en Dev / Test / Prod.

### 4. Librerías preinstaladas relevantes para esta jornada

- **scikit-learn**, **statsmodels**, **prophet**, **LightGBM**, **XGBoost**, **CatBoost**.
- **PyTorch**, **TensorFlow** (CPU; GPU según SKU).
- **MLflow** (cliente integrado contra el tracking server gestionado por Fabric).
- **SynapseML** — librería de Microsoft Research con LightGBM distribuido, Cognitive Services y modelos de anomalías sobre Spark.
- **Pandas**, **Polars**, **PyArrow**, **Delta-Spark**.

### 5. Data Wrangler

- IDE visual dentro del notebook para **explorar y transformar DataFrames** (pandas o Spark) con clicks.
- Cada paso genera código Python equivalente que se inserta en el notebook → ideal para enseñar y para que el científico no parta de cero.

### 6. Copilot for Data Science

- Disponible en notebooks de Fabric (sujeto a habilitación de tenant y región).
- Genera celdas a partir de prompts: *"crea features de calendario"*, *"entrena un LightGBM y registra el experimento en MLflow"*.
- Útil pedagógicamente para enseñar buenas prácticas; **siempre revisar** el código antes de ejecutarlo.

### 7. Los dos casos de Aurora Energía que articulan la jornada

| Caso | Tipo | Datos de partida |
| --- | --- | --- |
| **Forecast demanda eléctrica horaria** por estación | Regresión / series temporales | `fact_ventas` + `clima_historico` |
| **Predicción de demanda de bicicletas** Caso tiempo real | Forecast/real tiem | `transacciones_fidelizacion` + `dim_cliente` |

## Demo en vivo (6 min)

1. Cambiar el *workload* a **Data Science** y mostrar los items disponibles.
2. Crear un **Environment** `env_aurora_ml` con `prophet` y `lightgbm`.
3. Crear un Notebook nuevo, adjuntar `env_aurora_ml` y `lh_aurora`, leer `spark.read.table("fact_ventas")` y abrir **Data Wrangler** sobre el DataFrame.
4. Mostrar la pestaña **Experiments** vacía del workspace — la llenaremos en M3.

## Mensajes clave

- "Data Science en Fabric **no es Azure ML**: vive dentro del mismo workspace, comparte OneLake y se factura contra la misma capacidad."
- "El **Environment** es la pieza clave de MLOps reproducible — no instales paquetes con `%pip install` en producción."
- "Copilot y Data Wrangler aceleran, pero **el gobierno y el registro de modelos no son negociables**."
