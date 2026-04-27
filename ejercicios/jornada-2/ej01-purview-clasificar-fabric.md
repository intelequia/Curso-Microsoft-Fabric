# Ejercicio 1 (Jornada 2) · Clasificar y catalogar Fabric desde Purview

**Tiempo estimado:** 60 min · **Modalidad:** fuera de aula

## Objetivo

Publicar tu Lakehouse y Warehouse de Aurora como **Data Product certificado** en el Unified Catalog de Purview, con dominio, glossary y owner.

## Pasos

1. Entra a `https://purview.microsoft.com`.
2. Verifica que tu workspace `aurora-curso-fabric-<iniciales>` aparece en el **Microsoft Purview hub for Fabric**.
3. **Unified Catalog → Governance domains** → crea (si no existe) `Comercial`.
4. Crea 3 **glossary terms** dentro del dominio:
   - `Importe de Venta`
   - `Estación de Servicio`
   - `Cliente Comercial`
5. **+ New → Data Product** → `Ventas Aurora — Gold`:
   - Owner: tú.
   - Sensitivity label: `Aurora — Confidencial`.
   - Endorsement: Certified.
   - Datasets enlazados: `wh_aurora.fact_ventas`, `wh_aurora.dim_*`, `sm_aurora_ventas`.
   - Glossary terms: los 3 anteriores.
6. Asigna **Critical Data Element** a `cliente_id` e `importe` en `fact_ventas`.
7. Define una **regla de calidad** (Data Quality):
   - Tipo: completeness.
   - Tabla: `fact_ventas`.
   - Columna: `importe`.
   - Umbral: 100% no nulos.
8. Comprueba la pestaña **Lineage** del Data Product. Debe mostrar el flujo Lakehouse → Warehouse → Semantic Model.

## Entregable

- Captura del Data Product `Ventas Aurora — Gold` con todos sus metadatos.
- Captura del lineage.
- Captura del DQ score tras ejecutar la regla.

## Validación

- ✅ Data Product aparece en el Unified Catalog con badge Certified.
- ✅ Glossary terms enlazados.
- ✅ Lineage visible.
