# Ejercicio 6 (Jornada 3) · Deployment Pipeline Dev → Test → Prod

**Tiempo estimado:** 45 min · **Modalidad:** fuera de aula

## Objetivo

Propagar el modelo de forecast entre tres workspaces con aprobación humana y herencia de etiquetas Purview.

## Requisitos previos

- Modelo champion en `aurora-ml-dev-<iniciales>`.
- Permisos para crear 2 workspaces adicionales con la misma capacidad.

## Pasos

1. Crea los workspaces `aurora-ml-test-<iniciales>` y `aurora-ml-prod-<iniciales>`.
2. En `aurora-ml-dev-...` → **Workspace settings → Deployment pipelines → Create pipeline**:
   - Nombre `dp_aurora_ml`.
   - Tres stages: Dev, Test, Prod.
   - Asocia cada workspace a su stage.
3. Configura **Deployment rules** para parametrizar:
   - Nombre del Lakehouse (`lh_aurora_ml` en todos pero con shortcuts a distintos workspaces).
   - Alias del modelo (`challenger` en Test, `champion` sólo en Prod).
4. Promueve los items: notebook de scoring, pipeline, modelo, environment.
5. Antes de promover a **Prod**, verifica el checklist Responsible AI mínimo del módulo M6:
   - [ ] MAPE Test < umbral.
   - [ ] Model card escrita (puedes usar markdown en el item).
   - [ ] Etiqueta de sensibilidad propagada (revisa en Purview).
   - [ ] Owner identificado.
6. Solicita aprobación de otro alumno (o del instructor) y aprueba la promoción.

## Entregable

- Captura del Deployment Pipeline con los 3 stages en verde.
- Captura del histórico de aprobaciones.

## Validación

- ✅ Modelo presente en los 3 workspaces.
- ✅ Alias correcto por entorno.
- ✅ Reglas de despliegue activas.
- ✅ Etiquetas de sensibilidad visibles en Prod (vía Purview).
