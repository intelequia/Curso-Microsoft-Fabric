# Preparación del entorno: Trial de Microsoft Fabric

Sigue estos pasos **antes de la primera jornada**. Reserva 15–20 minutos. Si no consigues completarlo, contacta con el formador.

## Opción A — Activar la trial de Fabric en tu tenant corporativo

Esta es la opción preferida si tu tenant lo permite.

1. Abre [https://app.fabric.microsoft.com](https://app.fabric.microsoft.com) e inicia sesión con tu cuenta de Entra ID corporativa.
2. En la esquina superior derecha pulsa el icono de **perfil** → **Iniciar prueba gratuita**.
3. Acepta los términos. Verás aparecer un badge **"Prueba"** en la barra superior con los días restantes (60 días por defecto).
4. Una vez activada, en la esquina inferior izquierda cambia el experience switcher al área que toque (Power BI, Data Engineering, Data Warehouse, Real-Time Intelligence, etc.). Todas usarán la misma capacidad de prueba (FT1 / Trial).

> **Si tu tenant tiene la opción deshabilitada** (ves un mensaje de "Tu administrador no permite las pruebas") salta a la **Opción B**.

## Opción B — Crear un tenant de Microsoft 365 Developer + activar Fabric

1. Regístrate en el **Microsoft 365 Developer Program** en [https://developer.microsoft.com/microsoft-365/dev-program](https://developer.microsoft.com/microsoft-365/dev-program). Necesitas una cuenta Microsoft personal para el alta, pero el tenant que se crea es independiente (`tu-alias.onmicrosoft.com`).
2. Crea el tenant de pruebas (instant sandbox o configurable). Te darán 25 licencias E5.
3. Inicia sesión en `https://admin.microsoft.com` y crea (o reutiliza) un usuario administrador.
4. Con esa cuenta, ve a [https://app.fabric.microsoft.com](https://app.fabric.microsoft.com) y sigue los pasos 2–4 de la Opción A.

## Opción C — Capacidad Fabric en Azure (solo si quieres ir más allá)

Si tu organización ya tiene una suscripción Azure y quieres ver una capacidad real:

1. Entra en [https://portal.azure.com](https://portal.azure.com).
2. Crea un recurso **Microsoft Fabric** (busca "Microsoft Fabric" en el marketplace).
3. Selecciona **F2** o **F4** para laboratorio (coste muy bajo si la pausas tras el curso).
4. Asigna la capacidad a un workspace creado en Fabric desde **Configuración del workspace → Premium → Fabric capacity**.

> **Importante**: Acuérdate de **pausar la capacidad** cuando no la uses (`Pause` en Azure Portal). Solo se factura el tiempo en el que está activa.

## Verificación

Cuando la trial esté activa deberías poder:

- Crear un nuevo **Workspace** (`+ Nuevo workspace`) y verlo en la lista.
- Dentro del workspace, pulsar **+ Nuevo elemento** y ver disponibles, al menos: Lakehouse, Warehouse, Notebook, Data pipeline, Eventhouse, Semantic model.
- Crear un Lakehouse vacío llamado `lh_aurora` y verlo aparecer.

Si las tres comprobaciones pasan, estás listo. Borra el Lakehouse de prueba si quieres, lo reharemos juntos en la primera práctica.

## Convención de nombres del curso

Para que todas las capturas y ejercicios encajen, usa estos nombres en tu workspace personal:

| Artefacto | Nombre |
| --- | --- |
| Workspace principal | `aurora-curso-fabric` |
| Workspace test (Jornada 1, ejercicio para casa de Deployment Pipeline) | `aurora-curso-fabric-test` |
| Workspace prod | `aurora-curso-fabric-prod` |
| Lakehouse | `lh_aurora` |
| Warehouse | `wh_aurora` |
| Notebook principal | `nb_aurora_lab` |
| Pipeline | `pl_aurora_ingesta` |
| Eventhouse | `eh_aurora_telemetria` |
| Semantic model | `sm_aurora_ventas` |

## Problemas habituales

| Síntoma | Causa probable | Solución |
| --- | --- | --- |
| No veo la opción "Iniciar prueba gratuita" | El admin del tenant la ha desactivado | Pide al admin que active "Trial users can start trials" en el centro de administración o usa la Opción B. |
| Aparece un error de licencia al crear un Lakehouse | No has asignado capacidad al workspace | Edita el workspace → asigna capacidad **Trial / Fabric capacity**. |
| No veo el Eventhouse en `+ Nuevo` | Estás en un workspace sin capacidad Fabric (solo Power BI Pro) | Reasigna el workspace a la capacidad Trial. |
| OneLake File Explorer no abre | Necesitas Windows + cuenta válida en Fabric | Usa la web mientras tanto, o instala desde [aquí](https://www.microsoft.com/en-us/download/details.aspx?id=105222). |
