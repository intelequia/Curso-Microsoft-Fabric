# Ejercicio 2 (Jornada 1) · Ingesta con Dataflow Gen2

**Tiempo estimado:** 45 min · **Modalidad:** fuera de aula

## Objetivo

Crear un Dataflow Gen2 que lea un CSV remoto, lo limpie en Power Query y lo deposite en una tabla Delta del Lakehouse `lh_aurora`.

## Pasos

1. En el workspace, **+ New → Dataflow Gen2** → `df_aurora_clientes`.
2. **Get data → Web** → URL del CSV `clientes.csv` (puedes subirlo a un storage público o usar el del Lakehouse vía endpoint).
3. Aplica las siguientes transformaciones en Power Query:
   - Convierte `cliente_id` a entero.
   - Elimina filas con `email` nulo.
   - Crea columna `dominio_email` extrayendo lo que va tras la `@`.
   - Renombra `nombre` → `nombre_cliente`.
   - Cambia tipos: `fecha_alta` → date.
4. Configura el **destino** del Dataflow:
   - Lakehouse: `lh_aurora`.
   - Tabla destino: `dim_cliente`.
   - Modo: **Replace**.
5. Publica y ejecuta. Comprueba el historial de refresh.

## Bonus

Crea un segundo Dataflow `df_aurora_productos` que normalice los productos (`combustible`, `electricidad`, `gas`, `lubricante`) en una columna `categoria`.

## Entregable

- Captura del Dataflow con los pasos en Power Query.
- Captura del historial de ejecución correcta.
- `SELECT TOP 10 * FROM dim_cliente` desde el SQL endpoint.

## Validación

- ✅ Tabla `dim_cliente` con la columna `dominio_email` creada.
- ✅ Tipos correctos.
