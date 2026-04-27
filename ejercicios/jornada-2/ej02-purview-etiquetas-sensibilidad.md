# Ejercicio 2 (Jornada 2) · Etiquetas de sensibilidad y DLP en Fabric

**Tiempo estimado:** 45 min · **Modalidad:** fuera de aula

## Objetivo

Aplicar etiquetas de sensibilidad a los items de Fabric y crear una regla DLP que bloquee la exportación de datos sensibles.

## Pasos

1. Comprueba que las etiquetas (publicadas en clase) están disponibles en tu cuenta:
   - `Aurora — Interno`
   - `Aurora — Confidencial`
   - `Aurora — Restringido PII`
2. En Fabric, aplica `Aurora — Confidencial` a:
   - `lh_aurora`
   - `wh_aurora`
   - `sm_aurora_ventas`
   - `rpt_aurora_ejecutivo`
3. Comprueba que **el reporte hereda la etiqueta** desde el modelo.
4. Exporta el reporte a Excel y abre el fichero. Verifica:
   - Cabecera con la etiqueta.
   - Encriptación activa (al abrir desde otro usuario sin permiso, debe denegar).
5. Crea una **regla DLP** en el Compliance Portal:
   - Ámbito: Fabric / Power BI.
   - Condición: items con etiqueta `Aurora — Restringido PII`.
   - Acción: bloquear export a CSV/Excel + notificar al usuario.
6. Aplica la etiqueta `Aurora — Restringido PII` a `dim_cliente`.
7. Intenta exportar un visual basado en `dim_cliente` y verifica el bloqueo.
8. Revisa **Activity Explorer** y localiza el evento.

## Entregable

- Captura de cada item con su etiqueta aplicada.
- Captura del Excel exportado mostrando cabecera y encriptación.
- Captura del bloqueo DLP.
- Captura del evento en Activity Explorer.

## Validación

- ✅ Etiqueta heredada por el reporte.
- ✅ Bloqueo DLP funcional.
- ✅ Evento auditado.
