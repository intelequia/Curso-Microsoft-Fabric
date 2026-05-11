# J2-M4 · Integración Purview ↔ Fabric: gobierno extremo a extremo

**Duración:** 25 min · **Formato:** demo en vivo y conversación

## Objetivos

1. Ver cómo se ven los items de Fabric desde Purview y viceversa.
2. Entender el **OneLake Catalog** dentro de Fabric y su relación con el Unified Catalog.
3. Configurar **Data Access Policies** para que Purview otorgue acceso sobre Fabric.
4. Diseñar un **modelo de dominios** para Aurora Energía.

## Contenido

### 1. Donde se ve qué

| Vista | Qué muestra | Audiencia |
| --- | --- | --- |
| **Workspace de Fabric** | Items técnicos del proyecto | Equipo técnico |
| **OneLake Catalog (en Fabric)** | Items del tenant filtrables, búsqueda, endorsements, etiquetas | Analistas, data engineers |
| **Purview Unified Catalog** | Data Products, glossary, dominios, calidad, lineage | Negocio + gobierno |
| **Purview Data Map** | Inventario crudo + scans | Data stewards / arquitectos |

### 2. OneLake Catalog en Fabric

- Acceso desde la barra lateral del portal Fabric.
- Filtro por: tipo, endorsement, sensitivity label, owner, dominio.
- Atajo a **explorar** el item: schema, sample, ABFS path, copy code.
- Crear shortcuts directamente desde el catálogo.

### 3. Data Access Policies

- Desde Purview, defines: "**Cualquiera del grupo Analistas Comercial** puede **leer** el data product **Ventas Aurora — Gold**".
- Purview se encarga de propagar el permiso en Fabric (sobre el Lakehouse / Warehouse / semantic model).
- Modelo recomendado: **roles/grupos en Entra ID + dominios en Purview + workspaces en Fabric**, no permisos individuales.

### 4. Modelo de dominios para Aurora Energía

Propuesta para usar como punto de partida en el cliente real (lo dibujamos en pizarra):

```
Aurora Energía
 ├── Comercial
 │    ├── Data Product: Ventas Aurora — Gold
 │    ├── Data Product: Clientes (PII)
 │    └── Data Product: Campañas Marketing
 ├── Operaciones
 │    ├── Data Product: Telemetría Surtidores
 │    └── Data Product: Mantenimiento Predictivo
 ├── Finanzas
 │    └── Data Product: P&L Estación
 └── Gobierno (transversal)
      ├── Glossary maestro
      ├── Reglas DQ globales
      └── Sensitivity labels
```

Cada dominio tiene **1 owner** (rol negocio) y **1 steward** (rol técnico).

### 5. Health Management (Unified Catalog)

- Sección de **Unified Catalog** con reportes listos (*ready-made reports*) sobre el estado del data estate: nº de assets gobernados, % con owner, % con etiqueta, evolución de DQ score.
- **Health Controls**: miden el grado de cumplimiento con los estándares de gobierno y generan un score.
- **Health Actions**: lista de acciones concretas para mejorar la puntuación.
- Útil para reporting ejecutivo al CDO o CISO.

## Demo en vivo (12 min)

1. OneLake Catalog en Fabric → buscar "ventas" → ver `wh_aurora` con la etiqueta de Jornada anterior.
2. Filtrar por endorsement Certified → mostrar el Data Product `Ventas Aurora — Gold`.
3. Volver a Purview → **Unified Catalog → Health Management** → mostrar reportes de gobierno.
4. Crear una **Data Access Policy** que conceda lectura del Data Product al usuario "carlos.lopez@aurora-test.com" (cuenta ficticia/de prueba).
5. Comprobar en Fabric que el usuario aparece con permiso de lectura sobre el Warehouse.

## Mensajes clave

- "Fabric te da el dato, Purview te da la disciplina."
- "El gobierno no es la suma de mil tareas: es decidir 5 dominios y 5 etiquetas y aplicarlos en serio."
- "**Health Management** (Unified Catalog) es el dashboard que enseñas al CISO/CDO el primer mes."
