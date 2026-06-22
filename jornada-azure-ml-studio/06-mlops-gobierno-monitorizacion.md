# AML-M6 · MLOps, gobierno y monitorización

**Duración:** 30 min · **Formato:** explicación + discusión técnica

## Objetivos

1. Entender el ciclo MLOps mínimo para Azure ML.
2. Identificar controles de seguridad, coste y gobierno.
3. Preparar criterios de operación para modelos en producción.

## Hilo narrativo

> "MLOps es convertir ciencia de datos en un servicio mantenible: versionado, automatización, control, monitorización y retirada."

## Contenido

Un modelo productivo necesita más que una métrica alta. Debe poder reproducirse, aprobarse, desplegarse, monitorizarse y retirarse cuando deje de cumplir criterios.

### Ciclo MLOps mínimo

1. Versionar datos, código y configuración.
2. Ejecutar entrenamiento como job o pipeline.
3. Registrar métricas, artefactos y modelo.
4. Aplicar validaciones antes de registrar o promocionar.
5. Desplegar en endpoint controlado.
6. Monitorizar calidad, latencia, errores y coste.
7. Reentrenar o retirar según señales.

### Controles

| Área | Control |
| --- | --- |
| Identidad | Entra ID, RBAC, managed identity. |
| Red | Private endpoints, bloqueo de acceso público si aplica. |
| Datos | Datastores con permisos mínimos, Purview/Fabric governance cuando exista. |
| Coste | Clusters con min nodes 0, cuotas, apagado de compute instances. |
| Calidad | Métricas de validación, drift, pruebas de regresión. |
| Auditoría | MLflow, logs de endpoints, Azure Monitor y Application Insights. |

## Demo en vivo

1. Revisar Jobs y Models como evidencia del ciclo.
2. Mostrar logs de un endpoint o job.
3. Revisar coste operativo esperado: compute, storage, endpoints y logging.
4. Diseñar una checklist de promoción dev -> test -> prod.
5. Conectar con Responsible AI y revisión humana.

## Mensajes clave

- La reproducibilidad debe estar antes del despliegue.
- El coste de compute se controla con escalado, apagado y límites.
- Un modelo sin monitorización se degrada sin avisar.
