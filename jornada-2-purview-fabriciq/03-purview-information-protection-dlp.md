# J2-M3 · Information Protection, etiquetas de sensibilidad y DLP

**Duración:** 30 min · **Formato:** explicación + demo en vivo

## Objetivos

1. Manejar el ciclo de **Sensitivity labels** (creación, publicación, aplicación, herencia, encriptación).
2. Conocer **Auto-labeling** y los **Sensitive Information Types (SIT)** + **Trainable classifiers**.
3. Entender qué hace **Data Loss Prevention (DLP)** dentro y fuera de Fabric.
4. Aplicar etiquetas a items de Fabric y verificar la protección heredada.

## Contenido

### 1. Sensitivity labels

- Definidas a nivel **tenant** desde el Purview Compliance Portal.
- Pueden:
  - Etiquetar visualmente (cabecera, pie, watermark).
  - Aplicar **encriptación** (Microsoft Information Protection / Azure Rights Management).
  - Restringir acciones (no copiar, no imprimir, no reenviar).
  - Aplicarse a Office, Outlook, Teams, SharePoint, OneDrive, **Fabric items, archivos en OneLake, Power BI reports**.
- Aplicación: manual por usuario, **auto-label** por contenido, auto-label por contenedor.
- **Herencia en Fabric**: si un Lakehouse tiene la etiqueta `Confidencial`, todo modelo o reporte derivado la hereda. Si exporto a Excel/PDF, **se exporta la etiqueta y la encriptación**.

### 2. Sensitive Information Types

- Catálogo enorme out-of-the-box (DNI España, NIF, IBAN, tarjetas de crédito, pasaportes, números SSN, etc.).
- Personalizables (regex + keywords + función + nivel de confianza).
- **EDM (Exact Data Match)**: comparar contra una tabla maestra propia (ej. lista de DNIs de empleados).
- **Trainable classifiers**: ML para clasificar contenidos por categoría (CV, contratos, código fuente, etc.).

### 3. Etiquetas recomendadas para Aurora Energía

| Etiqueta | Marca | Encriptación | Caso |
| --- | --- | --- | --- |
| Público | — | No | Materiales de marketing |
| Interno | "Aurora — Interno" | No | Documentación operativa |
| Confidencial — Comercial | "Aurora — Confidencial" | Sí, lectura para grupo Ventas | Datos de cliente comercial |
| Restringido — PII | "Aurora — Restringido PII" | Sí, lectura solo Owner del Data Product | Datasets con PII de cliente |
| Restringido — Financiero | "Aurora — Restringido Financiero" | Sí, lectura para grupo Finanzas | Datasets económicos clave |

### 4. Data Loss Prevention (DLP)

- Reglas que **detectan, alertan o bloquean** contenidos sensibles en:
  - Endpoints (Windows, macOS) → **Endpoint DLP**.
  - Exchange, Teams, SharePoint, OneDrive.
  - **Fabric items y Power BI** → DLP for Power BI / Fabric.
  - Servicios de terceros vía **Defender for Cloud Apps**.
- Acciones: aviso al usuario, justificación obligatoria, bloqueo, override con auditoría.

### 5. DLP en Fabric

- Reglas tipo: "Si un semantic model contiene >X registros con DNI → bloquea la exportación a CSV".
- Disponible para Lakehouse, semantic models y reports.

### 6. Activity Explorer y Audit

- Visor cronológico de eventos de etiquetado y DLP.
- Útil para auditoría e investigación.

## Demo en vivo (10 min)

1. Compliance Portal → **Information Protection → Labels**. Mostrar las 5 etiquetas (si no existen, crear `Aurora — Confidencial`).
2. Publicar un **Label policy** al grupo "Curso Fabric".
3. En Fabric, abrir `wh_aurora` → menú **Sensitivity** → aplicar `Aurora — Confidencial`.
4. Mostrar que el **modelo semántico y los reportes derivados** heredan la etiqueta.
5. Exportar el reporte a Excel y mostrar la cabecera y la encriptación.
6. Crear una regla DLP: "Si reporte tiene etiqueta `Restringido — PII`, bloquear exportación a Excel". Probarla.
7. Activity Explorer → ver el intento bloqueado.

## Mensajes clave

- "La etiqueta viaja con el dato — incluso cuando sale de Fabric."
- "DLP no se inventa el día del incidente. Se diseña antes."
- "Empieza con 4–5 etiquetas. Más es ingobernable."
