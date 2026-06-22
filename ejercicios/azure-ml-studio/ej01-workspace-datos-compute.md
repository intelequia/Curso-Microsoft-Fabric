# Ejercicio 1 (Azure ML Studio) · Workspace, datos y compute

**Tiempo estimado:** 45 min · **Modalidad:** aula / casa

## Objetivo

Crear o revisar un workspace de Azure Machine Learning, preparar compute y registrar un primer data asset para el caso Aurora Energía.

## Prerequisitos

- Suscripción Azure activa.
- Permiso para crear recursos.
- Acceso a `https://ml.azure.com`.
- Fichero `assets/data/incidencias.json` disponible localmente.

## Pasos

1. Crea o selecciona el resource group `rg-ia-ml-azure-aurora`.
2. Entra en Azure Machine Learning Studio.
3. Crea el workspace `mlw-aurora-curso` si no existe.
4. Revisa los recursos asociados: Storage, Key Vault y Application Insights.
5. Crea una compute instance:
   - Nombre: `ci-aurora-<iniciales>`
   - Tipo: CPU económico disponible.
6. Crea un compute cluster:
   - Nombre: `cpu-cluster`
   - Min nodes: `0`
   - Max nodes: `2`
7. Sube o referencia `assets/data/incidencias.json`.
8. Registra un data asset llamado `aurora-incidencias`.
9. Abre la vista previa y valida que se entiende el esquema.

## Entregable

Captura del workspace con compute creado y data asset registrado.

## Validación

- [ ] El workspace `mlw-aurora-curso` existe.
- [ ] La compute instance está creada.
- [ ] El cluster `cpu-cluster` escala a cero.
- [ ] El data asset `aurora-incidencias` aparece en Azure ML Studio.
