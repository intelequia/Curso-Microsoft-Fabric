# Requisitos del curso

Este documento detalla **todo lo que necesita tener instalado y configurado el alumno** antes de la primera jornada para poder seguir las demostraciones y ejecutar los ejercicios prácticos en casa.

> Si en tu equipo no puedes instalar software por restricciones corporativas, avísanos al menos **48 horas antes** de la primera jornada para coordinar alternativas (entorno cloud-only o máquina virtual).

## 1. Requisitos de cuenta

| Recurso | Obligatorio | Notas |
| --- | --- | --- |
| Cuenta **Microsoft Entra ID** (corporativa o de pruebas) con permiso para iniciar trials | ✅ | Imprescindible. Una cuenta `@outlook.com` o `@gmail.com` **no sirve** para Fabric. Si tu tenant no permite trials, crea uno gratuito siguiendo [00-preparacion-entorno.md](00-preparacion-entorno.md). |
| **Trial de Microsoft Fabric** activa (60 días) | ✅ | Se activa el primer día de curso o antes. Instrucciones detalladas en [00-preparacion-entorno.md](00-preparacion-entorno.md). |
| Suscripción de **Azure** (puede ser trial gratuita con 200 USD) | ➕ Opcional | Solo necesaria si quieres practicar capacidades Fabric F-SKU desde Azure. Para el curso no es obligatoria. |
| Cuenta **Microsoft 365** con licencia E5 / E5 Compliance o trial equivalente | ✅ recomendada para Jornada 2 | Necesaria para ver Purview en su forma completa (Information Protection, DLP). Si no la tienes, el formador hará la demo y aún así podrás seguir los conceptos. |

> **Sobre Data agents y workload Fabric IQ.** El curso construye un **Data agent** real (capacidad disponible). El **workload Fabric IQ** y sus capacidades **Ontology**, **Graph**, **Plan** y **Operations agent** están en **preview** y su disponibilidad depende del tenant y la región. En este curso se tratan como visión y roadmap; los ejercicios no dependen de ellas.

## 2. Navegador y red

- **Microsoft Edge** o **Google Chrome** en su última versión estable.
- Conexión estable (mínimo 10 Mbps).
- **Acceso sin proxy/SSL inspection** a los siguientes dominios (verifica con tu IT si es un equipo corporativo):
  - `*.fabric.microsoft.com`
  - `*.powerbi.com`
  - `*.microsoft.com`
  - `*.azure.com`
  - `*.onelake.fabric.microsoft.com`
  - `*.dfs.fabric.microsoft.com`
  - `*.purview.microsoft.com`
  - `*.compliance.microsoft.com`
  - `*.cognitiveservices.azure.com` (para Fabric IQ)
  - `*.openai.azure.com`

## 3. Software a preinstalar

### Imprescindible

| Herramienta | Versión | Para qué se usa |
| --- | --- | --- |
| **Power BI Desktop** | Última versión (release mensual) | Construir modelos semánticos, conectarse a Direct Lake, publicar reportes. [Descarga](https://powerbi.microsoft.com/desktop/). |
| **Visual Studio Code** | Última | Editar SQL, KQL, notebooks, ver/modificar los assets del curso. [Descarga](https://code.visualstudio.com/). |
| Extensiones de VS Code | — | `ms-mssql.mssql` (T-SQL), `ms-toolsai.jupyter` (notebooks), `fabric.vscode-fabric` (Microsoft Fabric),  `SynapseVSCode.synapse` (Fabric Data Engineering VS Code), `ms-python.python`. |
| **Git** | 2.40+ | Clonar este repositorio. [Descarga](https://git-scm.com/downloads). |
| **OneLake File Explorer** (Windows) | Última | Acceder a OneLake como si fuera OneDrive. [Descarga](https://www.microsoft.com/en-us/download/details.aspx?id=105222). En macOS no está disponible: usaremos la web. |

### Recomendado

| Herramienta | Para qué se usa |
| --- | --- |
| **Azure Storage Explorer** | Inspeccionar OneLake vía endpoint ABFS si quieres profundizar. |
| **Azure Data Studio** o **SQL Server Management Studio (SSMS)** | Clientes alternativos para conectarse al SQL endpoint de Lakehouse/Warehouse. Azure Data Studio ha sido descontinuado el 28 febrero 2026 en favor de VS Code con la extensión de MSSQL.  |
| **Microsoft Purview Data Map cliente** (web) | Solo navegador, sin instalación. |
| **Python 3.11+** local con `pandas`, `pyarrow`, `azure-identity` | Si quieres ejecutar notebooks fuera de Fabric. No imprescindible. |
| **Microsoft Teams** | Canal de soporte entre jornadas (si el formador lo habilita). |

## 4. Datos

Descarga la carpeta [assets/data](assets/data) de este repositorio en una ruta local que recuerdes (por ejemplo `~/data`). Verás los siguientes ficheros:

- `clientes.csv` — Maestro de clientes ficticios de Aurora Energía.
- `productos.csv` — Catálogo de productos (combustibles, electricidad, gas, lubricantes).
- `estaciones.csv` — Red de estaciones de servicio y puntos de recarga.
- `ventas.csv` — Hechos de venta por estación y producto (≈ 50.000 filas).
- `telemetria_eventos.json` — Eventos sintéticos de surtidores para el bloque de Real-Time / KQL.

> Todos los datos son **sintéticos**. Cualquier parecido con clientes, estaciones o productos reales es pura coincidencia.

## 5. Conocimientos previos

No es un curso introductorio a base de datos ni a SQL. Para aprovecharlo al máximo, conviene que el alumno tenga:

- Conocimientos **básicos de SQL** (SELECT, JOIN, GROUP BY).
- Familiaridad con conceptos de **modelado de datos** (hechos vs dimensiones, claves).
- Experiencia previa con **Power BI** a nivel usuario o desarrollador (lectura de modelos, conexión a fuentes).
- Nociones de **Python** son útiles para los notebooks, pero no imprescindibles.
- Para Jornada 2: nociones de **gobierno del dato y compliance** (qué es DLP, qué es una etiqueta de sensibilidad, qué significa GDPR).

## 6. Checklist final del alumno

Antes del primer día marca todas estas casillas:

- [ ] Tengo cuenta corporativa o de tenant de pruebas con permisos para activar trial Fabric.
- [ ] He activado mi trial de Microsoft Fabric siguiendo [00-preparacion-entorno.md](00-preparacion-entorno.md).
- [ ] Veo el portal de Fabric en `https://app.fabric.microsoft.com` y puedo crear un workspace.
- [ ] Tengo Power BI Desktop instalado y abre correctamente.
- [ ] Tengo VS Code con las extensiones recomendadas.
- [ ] He clonado o descargado este repositorio.
- [ ] He copiado la carpeta `assets/data/` a una ruta local.
- [ ] He probado abrir un CSV en VS Code y un PBIX en Power BI Desktop.

Si alguna casilla no se marca, contacta con el formador antes de la sesión.
