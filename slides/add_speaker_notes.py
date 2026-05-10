"""
Script para añadir notas de speaker a los slides Marp de las jornadas del curso Fabric.
Las notas se insertan como comentarios HTML (<!-- ... -->) justo antes de cada separador ---.
"""

# ============================================================
# NOTAS JORNADA 1
# ============================================================
notes_j1 = [
    # Slide 1 — Cover lead
    (
        "Bienvenida. Presentaros brevemente: quién sois y vuestra relación con Fabric. "
        "Preguntar a la sala: ¿quién tiene experiencia con Power BI Premium? ¿con Azure Data Factory? "
        "Eso os sitúa en el punto de partida. El hilo conductor de todo el día es Aurora Energía: "
        "un operador ficticio con 250 estaciones de servicio, comercializadora eléctrica y división logística. "
        "En 4 horas construimos juntos un flujo de datos end-to-end real. "
        "Recordar la dinámica: bloque teórico + demo en vivo + ejercicios para casa."
    ),

    # Slide 2 — ¿Qué nos llevaremos hoy?
    (
        "Leer los objetivos en voz alta y pedir que los apunten. "
        "Avisar: al final de cada bloque habrá una slide '¿Qué me llevo?' — eso es lo mínimo que debe quedar claro. "
        "Si algo no queda claro, es el momento de preguntar ahí. "
        "Presentar el caso Aurora Energía brevemente: empresa real-ficticia, datos de ventas de carburante y electricidad, "
        "datos de telemetría de surtidores, datos de clientes con GDPR."
    ),

    # Slide 3 — Agenda
    (
        "Recorrer la agenda módulo a módulo. "
        "Descanso fijo a mitad: aproximadamente a las 2h de empezar. "
        "Las demos son en vivo — si algo falla en producción hay capturas de pantalla de respaldo. "
        "Los ejercicios para casa están en la carpeta ejercicios/jornada-1/. "
        "Preguntar: ¿hay algún bloque que les interese especialmente para hacer hincapié?"
    ),

    # Slide 4 — Section M1
    (
        "Transición al primer bloque. Avisar que M1 es el más conceptual del día, "
        "pero que cuanto mejor quede OneLake en la cabeza, más fácil será entender todo lo demás. "
        "Duración estimada: 25 minutos incluyendo preguntas."
    ),

    # Slide 5 — ¿Qué es Microsoft Fabric?
    (
        "Fabric GA en noviembre 2023 — menos de 2 años de vida, pero ya en uso en miles de empresas. "
        "El mensaje clave: no es una herramienta más, es una plataforma SaaS que reúne Synapse, ADF, Power BI Premium, "
        "Data Science y Real-Time Intelligence bajo un único paraguas de capacidad. "
        "El precio ya no es por motor, sino por capacidad unificada (F-SKU). "
        "Preguntar: ¿alguien usa todavía Synapse Analytics clásico o Azure Data Factory independiente?"
    ),

    # Slide 6 — OneLake
    (
        "OneLake es LA pieza disruptiva. Un storage, un formato Delta-Parquet, un permiso. "
        "Analogía: como OneDrive pero para datos analíticos. Todos los items Fabric (Lakehouses, Warehouses, etc.) "
        "almacenan sus datos en OneLake automáticamente — sin configuración. "
        "Los Shortcuts son accesos directos que apuntan a datos en ADLS, S3 o GCS sin moverlos. "
        "El Mirroring replica casi en tiempo real desde Azure SQL, Cosmos DB o Snowflake sin ETL. "
        "Dar el ejemplo: si tenéis una base de datos operacional en Azure SQL, en minutos tenéis los datos en OneLake."
    ),

    # Slide 7 — Workloads
    (
        "Esta tabla se puede leer rápido — lo importante es que hay una 'lente' por rol. "
        "Un ingeniero de datos trabaja en Data Engineering. Un analista en Power BI. "
        "Un científico de datos en Data Science. Un ingeniero de datos en tiempo real en Real-Time Intelligence. "
        "Todos comparten el mismo workspace y los mismos datos en OneLake: no hay silos."
    ),

    # Slide 8 — Capacidad y licencias
    (
        "Esta slide es la que genera más dudas. La regla de oro: necesitáis F64 "
        "si queréis que usuarios con licencia Free (sin Pro) puedan consumir reportes en el workspace. "
        "Por debajo de F64, los consumidores necesitan licencia Pro o PPU. "
        "El trial de 60 días equivale a F64 — aprovecharlos para validar el caso de uso antes de comprar. "
        "Para la mayoría de pymes, F8 o F16 son suficientes para empezar."
    ),

    # Slide 9 — Trial y roles
    (
        "El trial se activa desde la configuración del tenant — cualquier admin puede hacerlo en 5 minutos. "
        "Los roles de workspace (Viewer, Contributor, Member, Admin) son los mismos que en Power BI "
        "pero ahora aplican a todos los items Fabric del workspace. "
        "Recordar: los permisos también se pueden dar a nivel de item individual — "
        "puedo compartir solo el Lakehouse sin dar acceso al workspace completo."
    ),

    # Slide 10 — Key M1
    (
        "Hacer pausa y preguntar: ¿alguien puede explicar con sus propias palabras "
        "qué diferencia hay entre F-SKU y Power BI Premium P-SKU? "
        "Respuesta esperada: antes se pagaba por motor (Premium era solo para Power BI), "
        "ahora una sola capacidad da acceso a todos los workloads Fabric. "
        "La unificación de billing es el argumento más potente para el CFO."
    ),

    # Slide 11 — Section M2
    (
        "Transición. En este bloque respondemos la pregunta más frecuente en proyectos Fabric: "
        "¿Lakehouse o Warehouse? La respuesta corta: depende del equipo y del tipo de carga. "
        "Duración estimada: 30 minutos incluyendo demo."
    ),

    # Slide 12 — Lakehouse
    (
        "El Lakehouse es el depósito universal. Acepta cualquier formato en la sección Files "
        "(CSV, Parquet, JSON, imágenes, binarios...) y expone tablas Delta para consultas SQL. "
        "Lo más importante: incluye gratis el SQL Analytics Endpoint (para consultas T-SQL de solo lectura) "
        "y el Default Semantic Model (para conectar Power BI directamente). "
        "Preguntar: ¿en vuestro proyecto actual, dónde aterriza la ingesta — ADLS, Azure SQL, archivos CSV?"
    ),

    # Slide 13 — Warehouse
    (
        "El Warehouse es para el equipo SQL clásico. DML completo: INSERT, UPDATE, DELETE, MERGE. "
        "Stored procedures, funciones, vistas, transacciones multi-tabla. "
        "La sorpresa que suele sorprender: por debajo también es Delta-Parquet sobre OneLake. "
        "No es un silo: comparte el mismo storage que el Lakehouse del mismo workspace. "
        "Desde el Warehouse puedes hacer queries cross-database directamente al Lakehouse — sin ETL."
    ),

    # Slide 14 — Comparativa cara a cara
    (
        "Las diferencias clave a remarcar: "
        "1) El SQL endpoint del Lakehouse es solo lectura — no se puede hacer INSERT ni MERGE. "
        "2) El Warehouse soporta DML completo, stored procs y transacciones. "
        "3) Para datos no estructurados (JSON crudo, imágenes, PDFs), solo el Lakehouse. "
        "4) Para código T-SQL heredado con stored procedures, el Warehouse. "
        "Preguntar: ¿en vuestro equipo predomina el perfil PySpark/Python o el perfil T-SQL?"
    ),

    # Slide 15 — ¿Cuándo cada uno?
    (
        "El patrón más habitual en proyectos grandes: "
        "Lakehouse para las capas bronze (datos crudos) y silver (datos limpios), "
        "Warehouse para la capa gold (modelo dimensional servido a Power BI). "
        "En Aurora: lh_aurora aterriza la materia prima desde los sistemas operacionales, "
        "wh_aurora sirve el modelo dimensional certificado a Power BI con Direct Lake. "
        "Este patrón cubre el 80% de los proyectos de datos que veréis en clientes."
    ),

    # Slide 16 — Demo M2
    (
        "Demo en vivo. Tiempo estimado: 10 minutos. "
        "Puntos clave a mostrar: "
        "1) Diferencia visual entre Lakehouse y Warehouse en la interfaz del portal. "
        "2) El SQL Endpoint del Lakehouse y que al intentar INSERT da error. "
        "3) El Warehouse con el editor T-SQL y la cross-database query al Lakehouse. "
        "Si hay problemas de conectividad en el aula, mostrar las capturas de respaldo de la demo. "
        "Subir el CSV clientes.csv al Lakehouse y mostrar cómo se convierte en tabla Delta automáticamente."
    ),

    # Slide 17 — Key M2
    (
        "Pregunta de verificación: ¿puedo hacer un MERGE en el SQL endpoint de un Lakehouse? "
        "Respuesta: no, es solo lectura. ¿Y en el Warehouse? Sí, con el patrón MERGE estándar T-SQL. "
        "Segundo punto: el shared storage significa que si cargo datos en el Lakehouse vía Spark, "
        "ya son accesibles desde el Warehouse sin mover nada — ambos ven el mismo Delta en OneLake."
    ),

    # Slide 18 — Section M3
    (
        "Transición al bloque de ingesta — el más práctico de la mañana. "
        "Regla de tres para elegir la herramienta: "
        "Dataflow Gen2 para transformar, Pipeline para orquestar, "
        "Copy Job para incremental masivo, Mirroring para replicación operacional en tiempo real. "
        "Duración estimada: 35 minutos incluyendo demo."
    ),

    # Slide 19 — Opciones de ingesta
    (
        "Recorrer la tabla fila a fila. "
        "El punto de confusión habitual: ¿cuándo Pipeline vs Dataflow Gen2? "
        "Dataflow Gen2 es la transformación en sí (interfaz Power Query). "
        "Pipeline es el orquestador que llama a varios Dataflows, Notebooks, Stored Procs, etc. "
        "con control de flujo, dependencias y notificaciones. "
        "Otra confusión: Copy Job vs Copy activity dentro de Pipeline — "
        "Copy Job es un item independiente para cargas incrementales programadas; "
        "Copy activity es una actividad dentro de un Pipeline más complejo."
    ),

    # Slide 20 — Dataflow Gen2
    (
        "Dataflow Gen2 tiene una mejora importante respecto al clásico (Gen1): Fast Copy. "
        "Para conectores como ADLS, Azure SQL o SharePoint, en lugar de ir fila a fila "
        "usa la ruta de copia masiva nativa. Resultado: hasta 25x más rápido para grandes volúmenes. "
        "Y el destino puede ser Lakehouse, Warehouse, Azure SQL, Synapse SQL, etc. "
        "La interfaz es Power Query Online — si tu equipo ya conoce Power Query de Excel o Power BI Desktop, "
        "la curva de aprendizaje es mínima."
    ),

    # Slide 21 — Data Pipeline
    (
        "Heredero directo de Azure Data Factory v2. Si venís de ADF, todo os resultará familiar: "
        "mismas actividades (Copy, ForEach, If, Wait, Lookup...), mismos conectores, mismos triggers. "
        "Si no venís de ADF, el punto de entrada es la actividad Copy data para cargas simples. "
        "El Monitoring Hub es la pieza que más agradece la operaciones: "
        "todas las ejecuciones de Pipelines, Dataflows, Notebooks y Spark Jobs "
        "quedan registradas en un único lugar con estado, duración y errores."
    ),

    # Slide 22 — Patrón Pipeline→Dataflow
    (
        "Este patrón Pipeline madre + actividades hijo es el que replicaréis en el 80% de proyectos. "
        "La secuencia: Pipeline dispara Dataflow de clientes → si tiene éxito, Dataflow de ventas → "
        "si todo va bien, ejecuta el Notebook de limpieza silver → notifica al equipo por email/Teams. "
        "El beneficio principal: trazabilidad completa en el Monitoring Hub y "
        "reintentos automáticos en caso de error parcial."
    ),

    # Slide 23 — Mirroring
    (
        "Mirroring es lo más cercano a magia en Fabric para equipos que vienen de ETL tradicional. "
        "Sin construir un pipeline de réplica, en minutos tenéis una copia casi en tiempo real "
        "de vuestro Azure SQL, Cosmos DB o Snowflake sobre OneLake. "
        "El coste es marginal: capacidad consumida por la sincronización + storage en OneLake. "
        "Ideal para análisis sobre sistemas operacionales sin afectarlos. "
        "Limitación: solo para los orígenes soportados — consultar la lista actualizada en docs."
    ),

    # Slide 24 — Demo M3
    (
        "Demo en vivo. Tiempo estimado: 15 minutos. "
        "Parte 1 (8 min): Crear Dataflow Gen2, conectar a una fuente de ejemplo, "
        "aplicar una transformación básica, configurar destino al Lakehouse. "
        "Parte 2 (7 min): Crear Pipeline que invoca el Dataflow + una actividad de notificación. "
        "Mostrar el Monitoring Hub al final con la ejecución completada. "
        "Si el Dataflow tarda más de 2 min en el aula, pasar al siguiente paso y volver al resultado."
    ),

    # Slide 25 — Key M3
    (
        "Pregunta: ¿qué usaríais para cargar datos desde un ERP on-premise al Lakehouse? "
        "Respuesta: si el ERP tiene API REST, un Dataflow Gen2 con el conector web. "
        "Si tiene base de datos SQL accesible, un Pipeline con Self-Hosted IR. "
        "Si es replicación continua y el origen lo soporta, Mirroring. "
        "El Monitoring Hub es obligatorio en producción — si no puedes ver qué falló, no puedes operar."
    ),

    # Slide 26 — Break lead
    (
        "Descanso de 15 minutos. "
        "Dejar el workspace abierto en el portal para que quienes quieran puedan explorar por su cuenta. "
        "Recordar que a la vuelta empezamos con Notebooks y Spark — el bloque más hands-on del día. "
        "Aprovechar el descanso para resetear la sesión de demo si es necesario."
    ),

    # Slide 27 — Section M4
    (
        "Transición a Notebooks y Spark. "
        "Spark en Fabric es diferente al Spark que muchos conocéis de Databricks o HDInsight: "
        "no hay cluster que aprovisionar, no se espera 5-10 minutos para el arranque. "
        "El Starter Pool arranca en ~15 segundos. Los Environments versionan las librerías junto con el código. "
        "Duración estimada: 30 minutos incluyendo demo."
    ),

    # Slide 28 — Notebooks en Fabric
    (
        "El Notebook es la herramienta de transformación más potente pero no la más rápida de configurar. "
        "Para transformaciones simples ya establecidas, usad Dataflow Gen2. "
        "Para lógica Python compleja, ML, o volúmenes donde Spark se amortiza (>1M filas), usad Notebook. "
        "La integración nativa con el Lakehouse adjunto es clave: "
        "no hay cadenas de conexión, no hay credenciales — el Notebook ve las tablas y ficheros directamente."
    ),

    # Slide 29 — Spark gestionado
    (
        "El Starter Pool: listo en ~15 segundos, sin coste de arranque extra, "
        "se apaga automáticamente tras el tiempo de inactividad configurado. "
        "Los Custom Pools permiten escalar verticalmente para cargas ML pesadas o joins muy grandes. "
        "Los Environments son el equivalente a un requirements.txt + imagen Docker versionada: "
        "reproducibles, compartibles entre notebooks, y pinneables a una versión de Spark concreta. "
        "Preguntar: ¿alguien ha gestionado clusters Spark en el pasado? ¿cuánto tardaba el aprovisionamiento?"
    ),

    # Slide 30 — APIs
    (
        "Las tres APIs que usaréis el 90% del tiempo: "
        "spark.read/write para leer y escribir datos, "
        "%%sql (magic cell) para SQL puro en el notebook, "
        "y notebookutils para gestión de ficheros en OneLake y acceso a secretos de Key Vault. "
        "La Pandas API on Spark (pandas-on-Spark) permite usar código pandas casi igual que en local, "
        "con el motor Spark debajo — muy útil para migrar notebooks de pandas a Fabric sin reescribir todo. "
        "Preguntar: ¿alguien ha usado PySpark fuera de Fabric?"
    ),

    # Slide 31 — Acceso a OneLake desde Spark
    (
        "Mostrar el código detenidamente. Puntos clave: "
        "1) spark.read.table() accede directamente a la tabla Delta del Lakehouse adjunto sin path explícito. "
        "2) Para ficheros en la sección Files/, se usa el path relativo con Files/. "
        "3) Siempre escribir en formato Delta (saveAsTable o write.format('delta')) "
        "para que los datos sean accesibles desde el SQL Endpoint y el modelo semántico. "
        "Avisar: si escribís en Parquet sin registrar la tabla, el SQL Endpoint no la verá."
    ),

    # Slide 32 — Caso Aurora bronze→silver
    (
        "Este es exactamente el notebook que haréis en el ejercicio de casa. "
        "Bronze: datos crudos con posibles errores de formato, valores nulos, duplicados. "
        "Silver: datos limpios, tipados correctamente, enriquecidos con joins. "
        "El paso crítico: filtrar ventas con importe <= 0 (datos de prueba del ERP que se cuelan). "
        "Normalizar fechas a formato DATE — esto es crítico para Direct Lake más adelante. "
        "El join entre las 4 tablas produce la tabla ventas_silver que alimentará el Warehouse."
    ),

    # Slide 33 — Buenas prácticas Spark
    (
        "Tres recomendaciones que marcan la diferencia entre un proyecto amateur y uno profesional: "
        "1) Cabecera markdown clara en cada notebook: ¿qué hace, qué consume, qué produce, quién lo mantiene? "
        "2) Cuando el notebook esté estabilizado, convertirlo en Spark Job Definition "
        "para poder invocarlo desde Pipeline con parámetros y sin sesión interactiva. "
        "3) Particionar las tablas Delta por fecha si superan los 10-20M de filas — "
        "mejora el rendimiento de lecturas filtradas por rango de fechas."
    ),

    # Slide 34 — Key M4
    (
        "Pregunta: ¿cuándo usaría Notebook en lugar de Dataflow Gen2? "
        "Respuesta: cuando necesito lógica Python compleja (ML, NLP, custom transformations), "
        "cuando proceso volúmenes donde Spark se amortiza (normalmente >1 millón de filas), "
        "o cuando necesito integraciones que Dataflow no tiene como conector. "
        "El Spark Job Definition + Pipeline es el combo correcto para producción."
    ),

    # Slide 35 — Section M5
    (
        "El Warehouse lo hemos visto en M2, pero ahora profundizamos en dos cosas: "
        "el modelado SQL para la capa gold y Direct Lake, "
        "que es la razón por la que Power BI brilla sobre Fabric de una manera que antes era imposible. "
        "Duración estimada: 35 minutos incluyendo demo."
    ),

    # Slide 36 — Warehouse refresco rápido
    (
        "Novedad clave que a menudo se pasa por alto: cross-database queries. "
        "Desde el Warehouse puedo hacer SELECT sobre tablas del Lakehouse del mismo workspace "
        "usando la notación de 3 partes: lakehouse_name.dbo.table_name. "
        "No hay copia, no hay ETL previo: lee directamente el Delta del Lakehouse en OneLake. "
        "Esto permite tener el Lakehouse como staging y el Warehouse como capa de servicio "
        "sin mover datos entre ellos — solo referencias."
    ),

    # Slide 37 — DDL Aurora gold
    (
        "Este es el modelo en estrella de Aurora: 4 dimensiones + 1 tabla de hechos. "
        "El modelo Kimball clásico que el 90% de los clientes puede adoptar directamente. "
        "Si alguien pregunta por SCD (Slowly Changing Dimensions): "
        "se puede implementar con MERGE, pero para el curso usamos truncate-and-load para simplificar. "
        "Las claves sustitutas (surrogate keys) son enteros autoincrementales — "
        "más eficientes en Direct Lake que GUIDs."
    ),

    # Slide 38 — Carga, vistas y seguridad
    (
        "El stored procedure de carga usa cross-DB para leer del Lakehouse — notar la notación lh_aurora.dbo.clientes. "
        "Row-Level Security (RLS): el comercial de Madrid solo ve las ventas de las estaciones de Madrid. "
        "Column-Level Security (CLS): el analista junior no ve la columna margen_neto. "
        "Object-Level Security (OLS): el rol externo no ve ni la tabla dim_cliente. "
        "Dynamic Data Masking (DDM): el teléfono del cliente aparece como XXXX-XXX-XXX para ciertos roles. "
        "Recomendación: empezad siempre por RLS, que es el más maduro y soportado en Power BI."
    ),

    # Slide 39 — Direct Lake
    (
        "Direct Lake es el cambio de paradigma de Power BI en Fabric. "
        "El dilema clásico: Import era rápido pero con datos fríos (refresh programado). "
        "DirectQuery era datos frescos pero lento (query a la BD por cada visual). "
        "Direct Lake es rápido Y fresco: lee directamente el Delta-Parquet de OneLake en modo columnar. "
        "El fallback a DirectQuery existe como safety net, pero con un buen modelo Delta bien mantenido "
        "raramente se activa. Condición: los datos deben estar en formato Delta en OneLake."
    ),

    # Slide 40 — Direct Lake on OneLake (DLOL)
    (
        "DLOL es la variante avanzada para ISVs y escenarios multi-tenant. "
        "En lugar de referenciar el Lakehouse del mismo workspace, "
        "el modelo semántico apunta al OneLake path via URL directa. "
        "Esto permite tener un modelo semántico maestro que apunta a los datos del cliente A, B, C "
        "sin tener que crear un modelo por cliente. "
        "Todavía en preview — revisar la documentación para la disponibilidad actual."
    ),

    # Slide 41 — Demo M5
    (
        "Demo en vivo. Tiempo estimado: 12 minutos. "
        "Secuencia: ejecutar el DDL de las 5 tablas → ejecutar el stored proc de carga → "
        "crear la vista de producto → crear el modelo semántico y verificar que está en modo Direct Lake "
        "(en las propiedades del modelo debe aparecer 'Direct Lake'). "
        "Crear un reporte rápido para demostrar el tiempo de respuesta. "
        "Si hay tiempo, simular el fallback generando una query muy compleja."
    ),

    # Slide 42 — Key M5
    (
        "Pregunta: ¿qué ventaja tiene Direct Lake sobre Import para un reporte "
        "que se actualiza cada hora con datos del ERP? "
        "Respuesta: eliminas el coste y la latencia del refresh (que en Import puede tomar 20-30 minutos). "
        "Con Direct Lake, los datos son frescos siempre que el Delta se actualiza, "
        "y el rendimiento es comparable a Import gracias al column store nativo en OneLake."
    ),

    # Slide 43 — Section M6
    (
        "Real-Time Intelligence es el componente más diferencial de Fabric "
        "respecto a Power BI Premium clásico o Databricks. "
        "Eventhouse + KQL es el motor ideal para series temporales, logs de máquinas e IoT. "
        "Activator cierra el círculo: del dato al acto sin necesidad de código extra. "
        "Duración estimada: 25 minutos incluyendo demo."
    ),

    # Slide 44 — Mapa RTI
    (
        "Recorrer el diagrama de izquierda a derecha. "
        "Eventstream recoge datos del origen (Event Hub, IoT Hub, Kafka, CDC de base de datos) "
        "y los enruta al destino: Eventhouse para análisis en tiempo real, "
        "Lakehouse para histórico en Delta, Activator para reaccionar automáticamente. "
        "El KQL Queryset es el editor de queries sobre el Eventhouse. "
        "El Real-Time Dashboard es el reporte de baja latencia sobre el Eventhouse."
    ),

    # Slide 45 — ¿Eventhouse o Lakehouse?
    (
        "La regla de oro para decidir: "
        "Si la pregunta tiene 'en los últimos N minutos/horas' o 'cuántos eventos por segundo', es Eventhouse. "
        "Si la pregunta es sobre análisis histórico de negocio (ventas del año pasado, tendencias mensuales), "
        "es Lakehouse/Warehouse. "
        "En Aurora: la telemetría de surtidores (temperatura, caudal, errores en tiempo real) va al Eventhouse; "
        "los datos de ventas consolidados del ERP van al Lakehouse."
    ),

    # Slide 46 — KQL en 5 minutos
    (
        "KQL (Kusto Query Language) tiene una sintaxis de pipeline con el operador | "
        "que es muy intuitiva para quien viene de UNIX o de pandas. "
        "summarize es el GROUP BY, where es el WHERE, project es el SELECT. "
        "Para quien viene de SQL, en 30 minutos se aprende lo básico para ser productivo. "
        "Las dos queries mostradas son exactamente las que usaréis en el ejercicio de la demo. "
        "Remarcar: KQL está optimizado para rangos de tiempo — las queries sobre series temporales "
        "son 10-100x más rápidas que el SQL equivalente sobre datos del mismo volumen."
    ),

    # Slide 47 — Caso Aurora telemetría
    (
        "250 estaciones × 6 surtidores × un evento cada 30 segundos = 3.000 eventos/minuto = 180.000 eventos/hora. "
        "Eso es imposible de gestionar con Power BI clásico en DirectQuery sobre SQL. "
        "Con Eventhouse, es trivial: ingesta en milisegundos, queries en segundos sobre millones de filas. "
        "El Activator: si la temperatura supera 65°C en cualquier surtidor, "
        "se dispara automáticamente una alerta al responsable de operaciones sin código adicional."
    ),

    # Slide 48 — Demo M6
    (
        "Demo en vivo. Tiempo estimado: 10 minutos. "
        "Como no tenemos un Event Hub real en el aula, usamos los sample data del portal de Fabric "
        "(Bicycle Rentals o Automotive). Adaptar los nombres de columnas en las queries. "
        "Puntos a mostrar: "
        "1) Creación del Eventhouse y del KQL Database. "
        "2) Creación del Real-Time Dashboard con 2-3 tiles. "
        "3) Creación de una regla básica en Activator. "
        "Este último paso suele impresionar mucho a la audiencia — la reacción automática sin código."
    ),

    # Slide 49 — Key M6
    (
        "Pregunta: ¿Activator puede enviar un mensaje a un canal de Teams? "
        "Respuesta: sí, es una de las acciones disponibles de fábrica. "
        "También puede enviar email, llamar a un webhook de Power Automate, "
        "o invocar un Pipeline de Fabric para desencadenar un proceso más complejo. "
        "Segundo punto: KQL y SQL conviven en el mismo workspace — "
        "el analista de negocio usa el reporte de Power BI, el ingeniero usa KQL Queryset."
    ),

    # Slide 50 — Section M7
    (
        "Ya tenemos el dato ingerido, limpio, modelado y con capacidad real-time. "
        "Ahora lo consumimos. Power BI en Fabric es más potente que nunca gracias a Direct Lake "
        "y al versionado del modelo con PBIP. "
        "Duración estimada: 30 minutos incluyendo demo."
    ),

    # Slide 51 — Tipos de modelo semántico
    (
        "El Default Semantic Model que genera automáticamente el Lakehouse o el Warehouse "
        "es un buen punto de partida para exploración, pero NO lo uses en producción. "
        "Motivos: incluye todas las tablas sin relaciones, sin medidas DAX, sin jerarquías. "
        "El Custom Semantic Model es donde añades relaciones, medidas DAX, perspectivas y RLS. "
        "Regla: siempre crear un Custom Semantic Model para los reportes que van a usuarios finales."
    ),

    # Slide 52 — DAX típico Aurora
    (
        "Leer las medidas una a una. Puntos a destacar: "
        "1) DIVIDE(numerador, denominador, 0) evita el error de división por cero. "
        "2) CALCULATE + SAMEPERIODLASTYEAR es el patrón estándar para comparar con el año anterior. "
        "3) TOPN sobre la dimensión de estaciones usa filter context — "
        "este tipo de query en DirectQuery era lento; con Direct Lake es instantáneo. "
        "Preguntar: ¿alguien tiene experiencia con DAX? ¿cuáles son las medidas más complejas que habéis escrito?"
    ),

    # Slide 53 — Publicación, apps y subscriptions
    (
        "Las Apps de Power BI siguen siendo la forma estándar de distribuir reportes en organizaciones grandes. "
        "El beneficio: el consumidor no ve el workspace, solo la App — más limpio y controlado. "
        "Con F64+: los usuarios Free pueden consumir la App sin licencia Pro. "
        "Las subscriptions permiten enviar capturas del reporte por email de forma programada — "
        "muy útil para directivos que prefieren recibir el resumen diario en el correo."
    ),

    # Slide 54 — PBIP y Git
    (
        "PBIP (Power BI Project) es el formato de archivo que convierte el modelo y el reporte "
        "en texto plano versionable con Git. "
        "En Fabric, la integración Git está en el workspace: conectáis el workspace a Azure DevOps o GitHub "
        "y los cambios se sincronizan automáticamente. "
        "Esto permite code review de modelos DAX, branching, y deployment pipelines entre dev/test/prod. "
        "Si el equipo usa Azure DevOps, la integración es nativa — no necesitáis plugins externos."
    ),

    # Slide 55 — Direct Lake buenas prácticas
    (
        "El error más común que veo en proyectos: columnas de fecha guardadas como STRING en Delta. "
        "Direct Lake no puede construir el column store correctamente sobre strings que representan fechas. "
        "Aseguraos de que todas las fechas son DATE o DATETIME en la tabla Delta antes de crear el modelo. "
        "Segundo error frecuente: columnas calculadas en DAX sobre tablas grandes con Direct Lake — "
        "prefieran siempre calcular en el Notebook o en el Warehouse y almacenar la columna calculada en Delta."
    ),

    # Slide 56 — Demo M7
    (
        "Demo en vivo. Tiempo estimado: 12 minutos. "
        "El modelo semántico sm_aurora_ventas es el mismo que vimos en M5 pero ahora añadimos "
        "las 5 medidas DAX y las relaciones entre tablas. "
        "Verificar que el modo es Direct Lake (propiedades del modelo semántico en el portal). "
        "Crear el reporte con 3-4 visualizaciones: ventas por estación, evolución mensual, top 5 productos. "
        "Si hay tiempo, mostrar la conexión del workspace a Azure DevOps y la sincronización Git."
    ),

    # Slide 57 — Cierre diagrama
    (
        "Este diagrama es el resumen de todo lo que hemos construido hoy. "
        "Guardadlo o haced una foto: es la referencia del patrón Fabric estándar que lleváis a vuestros proyectos. "
        "El flujo vertical (batch): CSV → Dataflow/Pipeline → Lakehouse bronze → Notebook silver → Warehouse gold "
        "→ Direct Lake → Power BI. "
        "El flujo en paralelo (real-time): Eventstream → Eventhouse → KQL Dashboard + Activator. "
        "Ambos flujos comparten OneLake como storage único — esa es la magia de la plataforma."
    ),

    # Slide 58 — Deberes para casa
    (
        "Los ejercicios están en la carpeta ejercicios/jornada-1/ del repositorio del curso. "
        "Son progresivos: primero el workspace, luego la ingesta, luego el notebook, "
        "luego el warehouse, luego el reporte Direct Lake. "
        "Cada ejercicio tiene su README con instrucciones paso a paso. "
        "Si os quedáis atascados, el canal de Teams del curso está disponible durante 2 semanas. "
        "El objetivo: llegar a la Jornada 2 con el workspace aurora-curso-fabric construido y los datos cargados."
    ),

    # Slide 59 — Farewell lead
    (
        "Preguntas finales — dar 5-10 minutos. "
        "Si hay preguntas específicas de proyectos de los asistentes, responder brevemente o dejar para el canal. "
        "Recordar la fecha de la Jornada 2: Purview + Fabric IQ. "
        "Invitar a explorar el workspace durante las próximas semanas y a traer dudas al canal de Teams. "
        "Agradecimiento al equipo organizador e Intelequia."
    ),
]

# ============================================================
# NOTAS JORNADA 2
# ============================================================
notes_j2 = [
    # Slide 1 — Cover lead J2
    (
        "Bienvenida a la Jornada 2. Preguntar: ¿quién completó los ejercicios de Jornada 1? "
        "¿Alguien se quedó atascado en algún punto? "
        "Recordar que hoy el foco es el gobierno del dato (Purview) y la capa de inteligencia (Fabric IQ). "
        "Sin lo de hoy, Fabric es potente pero no controlable ni escalable en una organización real. "
        "El hilo conductor sigue siendo Aurora Energía — usamos el mismo workspace de ayer."
    ),

    # Slide 2 — Repaso exprés J1
    (
        "Recorrer el flujo rápidamente. Las preguntas incómodas son el hilo conductor de la jornada de hoy: "
        "¿quién sabe exactamente qué hay en OneLake? ¿quién accede a qué datos y con qué permisos? "
        "¿qué pasa si un empleado descarga datos de clientes con DNI? "
        "Esas tres preguntas las respondemos con Purview en los bloques M1-M4. "
        "Preguntar si alguien tiene ya Purview en su organización o si es la primera vez que lo ven."
    ),

    # Slide 3 — Agenda J2
    (
        "Misma estructura que J1: bloques teóricos + demos en vivo + descanso a mitad. "
        "M1-M3 es Purview (gobierno, catalogo, protección). "
        "M4 es la integración bidireccional Purview↔Fabric. "
        "M5-M6 es Fabric IQ y Data Agents — la parte más novedosa. "
        "M7 es la hoja de ruta para llevarlo a vuestra organización. "
        "Preguntar si el foco de interés está más en governance/compliance o en IA."
    ),

    # Slide 4 — Section M1
    (
        "Transición. Purview es enorme — tiene 40+ módulos. "
        "Hoy cubrimos lo que os va a ser útil en los primeros 90 días de un proyecto Fabric real: "
        "Data Map, Unified Catalog, Sensitivity Labels y DLP. "
        "Duración estimada: 30 minutos incluyendo demo."
    ),

    # Slide 5 — Purview tres grandes áreas
    (
        "La confusión más frecuente con Purview: tiene dos portales. "
        "El portal de gobierno del dato (purview.microsoft.com) es donde trabajamos hoy. "
        "El portal de compliance (compliance.microsoft.com) es para el equipo legal y de seguridad. "
        "En 2024 Microsoft unificó ambos bajo el mismo paraguas de marca 'Microsoft Purview', "
        "pero siguen siendo superficies distintas. "
        "Hoy trabajamos con las tres áreas: un poco de Data Governance, un poco de Information Protection "
        "y el escenario de DLP que aplica a Fabric."
    ),

    # Slide 6 — ¿Por qué gobernar Fabric?
    (
        "El argumento de venta interno para convencer al CIO o al CISO: "
        "si construís Fabric sin gobierno, en 12 meses tendréis el mismo problema que tenéis "
        "con el data lake actual, pero a mayor escala. "
        "Fabric centraliza datos de múltiples orígenes — el riesgo de exposición inadvertida sube proporcionalmente. "
        "GDPR, ENS (Esquema Nacional de Seguridad), ISO 27001, NIS2 son regulaciones reales "
        "que aplican a la mayoría de las organizaciones en España. "
        "Sin gobierno documentado, una auditoría es un infierno."
    ),

    # Slide 7 — Cada necesidad, su módulo
    (
        "Esta tabla es la hoja de ruta de adopción de Purview. "
        "No intentéis implementar todo a la vez — os paralizaréis. "
        "El mínimo viable para empezar: "
        "Data Map + Unified Catalog (inventario y contexto de negocio) + "
        "5 sensitivity labels publicadas (clasificación). "
        "Con eso ya tenéis valor inmediato y demostrable. "
        "El resto se añade en fases posteriores según la madurez del equipo."
    ),

    # Slide 8 — Gobierno federado sobre Fabric
    (
        "Esta es la novedad más importante de Purview para equipos Fabric desde 2024: "
        "ya no necesitáis configurar un scan de los items Fabric en el Data Map. "
        "La integración nativa publica automáticamente Lakehouses, Warehouses, "
        "modelos semánticos, pipelines y reportes en el Data Map. "
        "El lineage (quién consume qué de quién) se construye solo. "
        "Es casi mágico comparado con cómo funcionaba Purview clásico hace 2 años."
    ),

    # Slide 9 — Entorno mínimo
    (
        "Verificar que todos tienen acceso al tenant del curso. "
        "Necesitamos al menos una licencia E5 trial o el add-on de Purview Compliance "
        "para las features de sensitivity labels y DLP. "
        "El acceso a purview.microsoft.com es con la cuenta del tenant — no hay portal separado. "
        "Si alguien no tiene acceso, que trabaje con el compañero del lado durante las demos. "
        "Recordar que el admin del tenant ya ha habilitado la integración de Purview hub en Fabric."
    ),

    # Slide 10 — Demo M1
    (
        "Demo en vivo. Tiempo estimado: 8 minutos. "
        "El primer 'momento wow' del día: abrir purview.microsoft.com → Unified Catalog "
        "y mostrar que ya aparecen los items del workspace de la Jornada 1 sin ninguna configuración adicional. "
        "Sin scan, sin setup previo. "
        "Mostrar el lineage automático de lh_aurora: de dónde vienen los datos, qué consume qué. "
        "Si hay delay en la aparición de los items (puede ser hasta 24h en tenants nuevos), "
        "usar la captura de pantalla de respaldo."
    ),

    # Slide 11 — Key M1
    (
        "Pregunta: ¿necesito configurar un scan de Fabric en el Data Map de Purview? "
        "Respuesta: no para los items Fabric nativos — la integración es automática. "
        "Sí necesitáis configurar conexiones y scans para fuentes externas "
        "(Azure SQL, ADLS externo, Oracle, SAP, etc.). "
        "Segundo punto clave: sin gobierno desde el día 1, el inventario nunca estará limpio. "
        "Es mucho más fácil clasificar 10 tablas que 1.000."
    ),

    # Slide 12 — Section M2
    (
        "Transición. Data Map es el inventario técnico automático. "
        "Unified Catalog es la tienda donde el negocio encuentra los datos con contexto de negocio. "
        "Son dos vistas del mismo grafo de conocimiento subyacente. "
        "Duración estimada: 35 minutos incluyendo demo."
    ),

    # Slide 13 — Data Map capa técnica
    (
        "Las connections son los conectores que alimentan el Data Map. "
        "Para Fabric, la conexión es automática. "
        "Para Oracle, Teradata o SAP on-premise, necesitáis el Self-Hosted Integration Runtime "
        "(el mismo que en Azure Data Factory). "
        "Las classifications son etiquetas automáticas basadas en el contenido (DNI, IBAN, email...) "
        "que Purview aplica durante el scan. "
        "Diferencia importante: classifications ≠ sensitivity labels — "
        "las primeras son técnicas y automáticas, las segundas son de negocio y se aplican manualmente o con recomendación."
    ),

    # Slide 14 — Unified Catalog capa negocio
    (
        "La jerarquía a recordar: "
        "Business Domain (área de negocio: Comercial, Finanzas...) → "
        "Data Product (conjunto de datos con propósito, owner y certificación) → "
        "Data Asset (la tabla o fichero concreto). "
        "El Glossary vincula términos de negocio ('Importe Neto') con columnas técnicas ('net_amount'). "
        "Los Certified Data Elements (CDEs) son las columnas críticas del negocio que requieren gestión especial. "
        "Esto es el puente entre el lenguaje técnico y el lenguaje de negocio."
    ),

    # Slide 15 — Data Quality
    (
        "Los DQ scores son el indicador que el analista mira antes de confiar en un dataset. "
        "Si la completeness de la columna 'importe' es del 60%, "
        "el analista ya sabe que ese campo tiene problemas antes de usarlo en un reporte. "
        "Esto da confianza al consumidor del dato y reduce el tiempo perdido en validaciones manuales. "
        "Las reglas de DQ se definen una vez y se ejecutan automáticamente en cada scan. "
        "Las alertas notifican al Data Steward cuando el score baja del umbral configurado."
    ),

    # Slide 16 — Lineage y Access Policies
    (
        "El lineage automático en Fabric es una de las mayores ventajas competitivas. "
        "En Azure Purview clásico (pre-2023), construir el lineage era un proyecto en sí mismo: "
        "había que instrumentar cada pipeline, cada notebook. "
        "Ahora en Fabric viene de fábrica para todos los items nativos. "
        "Las Access Policies desde Purview permiten gestionar permisos de Fabric "
        "centralizadamente sin entrar en cada workspace — "
        "el compliance officer puede ver y revocar accesos sin depender del equipo técnico."
    ),

    # Slide 17 — Caso Aurora: Data Product Ventas Gold
    (
        "Publicar el Data Product 'Ventas Aurora — Gold' es el ejercicio práctico de este bloque. "
        "El owner es una persona de negocio (Marisa Ledesma, directora comercial ficticia) — "
        "no del IT. Esto es fundamental: el ownership del dato debe estar en el negocio. "
        "El Endorsement 'Certified' significa que alguien ha verificado formalmente "
        "la calidad, la documentación y el gobierno del producto. "
        "Un consumer que ve 'Certified' sabe que puede confiar en esos datos."
    ),

    # Slide 18 — Demo M2
    (
        "Demo en vivo. Tiempo estimado: 15 minutos. "
        "Secuencia: crear el Governance Domain 'Comercial' → "
        "crear 3 glossary terms (Importe Neto, Litros Vendidos, Estación) → "
        "crear el Data Product 'Ventas Aurora — Gold' con wh_aurora y sm_aurora_ventas → "
        "aplicar Endorsement Certified → "
        "navegar al lineage automático (puede tardar 30-60 segundos en actualizarse). "
        "Ir despacio en la creación del Domain y el Glossary — es la parte más conceptualmente nueva. "
        "El lineage suele ser el momento más impactante visualmente."
    ),

    # Slide 19 — Key M2
    (
        "Pregunta: ¿quién debería ser el Data Owner de un Data Product en vuestra organización? "
        "Respuesta correcta: alguien del negocio, no del IT. "
        "El IT es el Data Steward (operativiza el gobierno, mantiene el glossary y las reglas de calidad). "
        "El Owner toma decisiones estratégicas: qué dato es bueno, quién accede, cuándo se retira. "
        "Si el negocio no asume el ownership, el programa de gobierno muere en 6 meses."
    ),

    # Slide 20 — Section M3
    (
        "Transición al bloque de protección de la información. "
        "Las etiquetas de sensibilidad son la pieza que viaja con el dato. "
        "Si alguien exporta a Excel un dataset con etiqueta Restringido-PII, "
        "el Excel hereda la encriptación MIP automáticamente. "
        "Eso es lo que diferencia a un sistema de gobierno real de uno puramente cosmético. "
        "Duración estimada: 25 minutos incluyendo demo."
    ),

    # Slide 21 — Sensitivity labels
    (
        "Las sensitivity labels se configuran a nivel de tenant en Microsoft Purview "
        "y están disponibles en todos los servicios M365: "
        "Exchange, SharePoint, Teams, Power BI, Fabric, Office apps. "
        "La herencia en Fabric es automática: "
        "si etiquetáis el Lakehouse, los modelos semánticos y reportes derivados heredan la etiqueta. "
        "Esto es un multiplicador enorme: un solo acto de clasificación se propaga hacia arriba en la cadena. "
        "La encriptación MIP (Microsoft Information Protection) viaja con el fichero — "
        "incluso si alguien lo envía por email o lo copia en un USB."
    ),

    # Slide 22 — Sensitive Information Types
    (
        "Los SIT (Sensitive Information Types) out-of-the-box de Microsoft "
        "incluyen más de 200 patrones predefinidos: DNI español, IBAN, tarjetas de crédito, "
        "número de Seguridad Social, pasaporte, etc. "
        "Para datos propios del negocio (ej. código de contrato interno de Aurora), "
        "usáis SIT personalizado con regex. "
        "EDM (Exact Data Match) es para comparar contra vuestra base de datos de clientes real — "
        "el más preciso pero el más complejo de configurar. "
        "Trainable classifiers usan ML para reconocer contenido sensible por contexto, no por patrón."
    ),

    # Slide 23 — Etiquetas recomendadas Aurora
    (
        "Esta tabla de 5 etiquetas es el mínimo viable para empezar un programa de gobierno real. "
        "La regla de oro: menos es más. "
        "20 etiquetas no las aplica nadie — la gente elige al azar o no clasifica. "
        "5 etiquetas bien diseñadas, con criterios claros y aplicadas de forma consistente tienen impacto real. "
        "La etiqueta 'Público' también es importante: marca los datos que SÍ se pueden compartir libremente, "
        "lo que elimina la duda sobre qué se puede publicar en la web o en informes externos."
    ),

    # Slide 24 — DLP
    (
        "DLP (Data Loss Prevention) es la red de seguridad que actúa donde las etiquetas clasifican. "
        "Donde las etiquetas identifican, DLP actúa. "
        "La acción más usada en la práctica: aviso al usuario + justificación obligatoria registrada. "
        "El bloqueo total se reserva para los casos más críticos (ej. datos financieros sin autorizar) "
        "porque genera fricción y tickets de soporte. "
        "Las políticas DLP se diseñan ANTES de que los datos estén en producción — "
        "aplicarlas a posteriori es posible pero mucho más difícil."
    ),

    # Slide 25 — DLP en Fabric ejemplo
    (
        "El ejemplo del DNI en el semantic model es un escenario real. "
        "Si el modelo semántico sm_aurora_ventas contiene la columna dni_cliente sin enmascarar "
        "y alguien lo exporta a CSV, la regla DLP puede bloquear la exportación y registrar el intento. "
        "Combinado con Activity Explorer tenéis la pista de auditoría completa: "
        "quién intentó exportar qué, cuándo, desde qué dispositivo, y qué acción tomó DLP. "
        "Esto es lo que necesita el Compliance Officer para responder a una auditoría GDPR."
    ),

    # Slide 26 — Demo M3
    (
        "Demo en vivo. Tiempo estimado: 10 minutos. "
        "Secuencia: "
        "1) Crear las 5 etiquetas en purview.microsoft.com (o mostrar las ya creadas). "
        "2) Crear una DLP policy básica para Fabric/Power BI que detecte la etiqueta Restringido-PII. "
        "3) Aplicar la etiqueta Restringido-PII al Lakehouse wh_aurora. "
        "4) Verificar la herencia en el modelo semántico. "
        "5) Intentar exportar a CSV desde Power BI — mostrar el bloqueo o el aviso. "
        "6) Activity Explorer: mostrar el evento registrado. "
        "IMPORTANTE: Las reglas DLP pueden tardar hasta 30 minutos en propagarse. "
        "Si no se activa en el aula, mostrar la captura de pantalla de respaldo del resultado."
    ),

    # Slide 27 — Key M3
    (
        "Pregunta: ¿qué pasa si alguien descarga un Excel con datos Restringido-PII "
        "desde casa, en un dispositivo no gestionado por la empresa? "
        "Respuesta: con encriptación MIP + DLP de endpoint + Conditional Access de Entra ID, "
        "el archivo llega encriptado y solo puede abrirse en dispositivos que cumplan la política. "
        "Sin la clave MIP, el archivo es ilegible. "
        "Esto requiere que todos los elementos estén configurados — "
        "MIP solo sin DLP no es suficiente para un escenario completo."
    ),

    # Slide 28 — Break lead
    (
        "Descanso de 15 minutos. "
        "La segunda parte del día es la más novedosa y la que más preguntas va a generar: "
        "Fabric IQ y los Data Agents. "
        "Aprovechar el descanso para abrir el portal de Fabric IQ en el tenant y verificar que está habilitado. "
        "Si hay algún problema de configuración, es el momento de resolverlo antes de la demo."
    ),

    # Slide 29 — Section M4
    (
        "Transición al bloque de integración. "
        "Purview y Fabric no son dos herramientas separadas que hay que conectar manualmente — "
        "están integradas de fábrica. "
        "Purview ve los items de Fabric, Fabric respeta los permisos y etiquetas de Purview. "
        "Duración estimada: 30 minutos incluyendo demo."
    ),

    # Slide 30 — ¿Dónde se ve qué?
    (
        "Esta tabla aclara la confusión más frecuente entre Fabric y Purview. "
        "Cada persona tiene su vista optimizada: "
        "El técnico (ingeniero de datos) vive en el workspace de Fabric — crea, transforma, depura. "
        "El analista semi-técnico vive en el OneLake Catalog dentro de Fabric — busca y descubre datos. "
        "El analista de negocio y el Data Owner viven en Purview Unified Catalog — "
        "ven el contexto de negocio, el lineage, la calidad. "
        "El CISO/CDO vive en Estate Insights — visión ejecutiva del estado del gobierno."
    ),

    # Slide 31 — OneLake Catalog en Fabric
    (
        "El OneLake Catalog es la interfaz de descubrimiento para los consumidores técnicos y semi-técnicos. "
        "Pueden filtrar por endorsement (solo datos Certified o Promoted), "
        "por sensitivity label (solo datos Público o Interno), "
        "por tipo de item (solo Warehouses, solo modelos semánticos...). "
        "También pueden copiar el ABFS path del Lakehouse para acceder programáticamente desde un notebook. "
        "Los shortcuts se pueden crear directamente desde el catálogo — "
        "esto facilita el self-service de los analistas sin depender del equipo de datos."
    ),

    # Slide 32 — Data Access Policies
    (
        "Las Data Access Policies son el gobierno de acceso federado desde Purview. "
        "En lugar de ir a cada workspace de Fabric a dar permisos individualmente, "
        "los gestionáis centralizadamente desde Purview. "
        "El grupo de Entra ID 'Analistas Comercial' recibe acceso al Data Product 'Ventas Aurora — Gold', "
        "y Purview propaga automáticamente el permiso de lectura al Lakehouse, Warehouse y modelo semántico "
        "que forman parte de ese Data Product. "
        "Esto es el gobierno de acceso real en una organización grande."
    ),

    # Slide 33 — Modelo dominios Aurora
    (
        "Este diagrama es el target architecture de gobierno para Aurora. "
        "Cuatro dominios: Comercial, Operaciones, Finanzas y Gobierno (transversal). "
        "Cada dominio tiene su Data Owner (negocio) y su Data Steward (IT/analítica). "
        "El dominio Gobierno es transversal — gestiona las políticas que aplican a todos los dominios. "
        "Empezad siempre por el dominio con más valor de negocio — en Aurora, sería Comercial, "
        "porque ahí están los datos de ventas que ya tenemos en el Warehouse. "
        "Esto demuestra valor rápido y construye momentum para los siguientes dominios."
    ),

    # Slide 34 — Estate Insights
    (
        "Estate Insights es el cuadro de mando que enseñáis al CISO o al CDO en la reunión del primer mes. "
        "Muestra el nivel de madurez de gobierno en números concretos: "
        "% de assets con owner asignado, % con sensitivity label, evolución del DQ score, "
        "número de incidentes DLP, accesos a datos sensibles. "
        "Es la prueba de que el programa de gobierno está funcionando y tiene impacto medible. "
        "Preguntar: ¿vuestro CDO o CISO pide este tipo de reporting actualmente? "
        "Si no, Estate Insights puede ser el argumento para empezar el proyecto."
    ),

    # Slide 35 — Demo M4
    (
        "Demo en vivo. Tiempo estimado: 12 minutos. "
        "Secuencia: "
        "1) OneLake Catalog: buscar 'ventas', filtrar por Certified, mostrar shortcuts. "
        "2) Estate Insights: mostrar el dashboard ejecutivo (puede estar vacío en tenant nuevo — usar captura). "
        "3) Data Access Policy: crear una policy que da acceso a 'Analistas Comercial' al Data Product. "
        "4) Verificar en Fabric que el miembro del grupo puede acceder. "
        "NOTA: La propagación de Access Policies puede tardar varios minutos. "
        "Si no aparece inmediatamente, refrescar el workspace y esperar."
    ),

    # Slide 36 — Key M4
    (
        "Las tres frases del bloque. Hacerlas leer en voz alta o preguntar si alguien las puede completar: "
        "1) Fabric da el dato, Purview da la... (disciplina). "
        "2) Cinco dominios bien definidos valen más que... (20 mal definidos). "
        "3) Estate Insights es el informe que le enseñas al... (CISO/CDO para demostrar valor). "
        "Estos son los argumentos para vender el programa de gobierno internamente."
    ),

    # Slide 37 — Section M5
    (
        "Transición a Fabric IQ — la novedad más grande de 2025-2026 en el ecosistema Fabric. "
        "Es lo que convierte Fabric de una plataforma de datos en una plataforma de conocimiento accionable. "
        "Data Agents son el componente estrella: permiten hacer preguntas en lenguaje natural "
        "sobre los datos gobernados y obtener respuestas con trazabilidad. "
        "Duración estimada: 30 minutos incluyendo demo."
    ),

    # Slide 38 — ¿Qué es Fabric IQ?
    (
        "Fabric IQ no es un chatbot sobre vuestros datos — eso es lo que ya existe con Power BI Q&A. "
        "Fabric IQ es una capa de razonamiento que: "
        "1) Entiende el significado de los datos gracias al modelo semántico y al glossary de Purview. "
        "2) Respeta automáticamente los permisos RLS y las sensitivity labels. "
        "3) Puede ejecutar múltiples herramientas (SQL sobre Warehouse, KQL sobre Eventhouse, "
        "búsqueda en documentos de OneLake) para responder preguntas complejas. "
        "4) Incluye trazabilidad completa: qué datasets consultó, qué SQL/DAX ejecutó, qué filas usó. "
        "Preguntar: ¿alguien ha probado ya Q&A en Power BI? ¿qué limitaciones habéis encontrado?"
    ),

    # Slide 39 — Arquitectura conceptual
    (
        "Leer el diagrama de abajo a arriba — eso es el flujo de trabajo del agente: "
        "La base es OneLake (los datos físicos). "
        "Encima, la capa semántica (modelos DAX, glossary Purview, metadatos). "
        "Encima, los Data Agents que razonan usando las herramientas disponibles. "
        "Encima, las aplicaciones de consumo (Teams, web, API REST). "
        "Purview atraviesa toda la arquitectura de forma transversal — "
        "el gobierno no es una capa opcional, es la base que hace el sistema confiable."
    ),

    # Slide 40 — Tres ideas Fabric IQ
    (
        "Estas tres ideas son el resumen ejecutivo de Fabric IQ para una audiencia de negocio. "
        "Si tuvierais que vender Fabric IQ a un director de área en 30 segundos, usad estas tres. "
        "La capa semántica es el por qué: sin ella, el agente no entiende qué significa 'importe neto'. "
        "Los Data Agents son el qué: entidades que razonan y ejecutan. "
        "El gobierno integrado es el cómo: Purview hace que el agente sea seguro y auditable."
    ),

    # Slide 41 — Diferencias con productos previos
    (
        "La pregunta más frecuente: '¿esto es Power BI Q&A pero más potente?' "
        "No exactamente. Q&A es para un solo semantic model, sin razonamiento multi-paso. "
        "Fabric IQ Data Agent es multi-fuente (Warehouse + Eventhouse + docs), razona en múltiples pasos "
        "y tiene gobierno automático de Purview. "
        "Respecto a Azure AI Foundry Agents: son más potentes y configurables, "
        "pero requieren integrar manualmente tu data estate. "
        "Fabric IQ tiene cero plumbing — los datos ya están conectados."
    ),

    # Slide 42 — Capacidad de razonamiento
    (
        "El reasoning loop es lo que diferencia al agente de una búsqueda simple. "
        "El agente planifica: ¿qué herramienta necesito para responder esto? "
        "La ejecuta, evalúa el resultado, y decide si necesita ejecutar otra herramienta o si ya tiene la respuesta. "
        "Esto permite responder preguntas complejas que requieren varias consultas coordinadas. "
        "Las citas de trazabilidad son críticas para la confianza: "
        "el analista puede verificar de qué tabla y de qué filas viene cada número de la respuesta."
    ),

    # Slide 43 — Requisitos
    (
        "F4 para experimentar, F64 para producción — esto es orientativo, puede variar. "
        "El LLM lo provee Microsoft en la región de la capacidad de Fabric: "
        "no necesitáis configurar una clave de Azure OpenAI ni pagar por separado el modelo. "
        "Eso simplifica enormemente el compliance, porque los datos no salen de vuestra región de capacidad. "
        "Importante: los items origen deben tener etiquetas Purview y permisos configurados "
        "ANTES de conectarlos al agente — el agente hereda el gobierno, no lo crea."
    ),

    # Slide 44 — Tipos de Data Agent
    (
        "Los cuatro tipos cubren los cuatro casos de uso más comunes. "
        "En Aurora empezamos con el Analytical (ventas y KPIs comerciales) "
        "porque es el más claro y el que más impacto inmediato tiene para la audiencia de negocio. "
        "El Operational (alertas de surtidores) es el siguiente paso natural — "
        "conecta con el Eventhouse que montamos en la Jornada 1. "
        "Search/Knowledge (políticas RR.HH.) y Workflow (consolidación de informes) "
        "son más complejos y se dejan para proyectos avanzados. "
        "Preguntar: ¿cuál de estos tipos sería más útil en vuestro contexto actual?"
    ),

    # Slide 45 — Demo M5
    (
        "Demo en vivo. Tiempo estimado: 12 minutos. "
        "Secuencia: "
        "1) Abrir el área Fabric IQ en el workspace (debe estar habilitado por el admin). "
        "2) Crear el Data Agent 'agente-ventas-aurora'. "
        "3) Asociar wh_aurora y sm_aurora_ventas como fuentes. "
        "4) Añadir 2-3 instrucciones básicas de sistema. "
        "5) Probar las 3 preguntas de la slide — mostrar la respuesta y la pestaña Trace. "
        "6) Mostrar la publicación como endpoint. "
        "Si hay problemas con el tenant, usar el agente pre-configurado de respaldo. "
        "La pestaña Trace es la más importante: demuestra que el agente no 'inventa' — "
        "muestra el SQL exacto que ejecutó para llegar a la respuesta."
    ),

    # Slide 46 — Key M5
    (
        "El punto más crítico del bloque: sin gobierno previo, el agente expone lo que no debe. "
        "Esto no es una exageración teórica: si no hay RLS sobre dim_cliente, "
        "el agente podría responder preguntas con DNI y datos personales de clientes. "
        "El gobierno (Purview + labels + RLS) es la condición necesaria y previa "
        "para publicar un agente de IA sobre datos reales en una organización. "
        "Hacer esta conexión explícita: todo lo que hemos hecho en M1-M4 hoy "
        "es exactamente lo que hace que M5-M6 sea seguro."
    ),

    # Slide 47 — Section M6
    (
        "Transición al bloque más hands-on de la jornada. "
        "En M5 creamos el agente rápido y lo probamos. "
        "En M6 vamos paso a paso por todas las decisiones de diseño que hacen que un agente "
        "sea robusto, seguro y evaluable en producción. "
        "Si hay tiempo, los asistentes pueden seguir los pasos en paralelo en su propio tenant. "
        "Duración estimada: 30 minutos incluyendo el ejercicio en aula."
    ),

    # Slide 48 — Pre-requisitos M6
    (
        "Verificar que el workspace tiene todos los items necesarios de la Jornada 1. "
        "Si alguien no completó los ejercicios de J1, puede usar el workspace de demo compartido. "
        "El Fabric IQ debe estar habilitado por el admin del tenant — esto se hace en el Admin Portal. "
        "La sensitivity label ya está aplicada a wh_aurora si completamos la demo de M3. "
        "El RLS de Comercial debe estar configurado en el modelo semántico sm_aurora_ventas."
    ),

    # Slide 49 — 1 - Definir rol e instrucciones
    (
        "El system prompt del agente es lo más importante que escribiréis para su comportamiento. "
        "Las 6 reglas del ejemplo son el mínimo: "
        "idioma y tono, fuentes autorizadas, comportamiento ante datos faltantes, "
        "formato de importes, y — la más crítica — la prohibición explícita de exponer PII. "
        "La última regla (nunca DNI ni teléfonos) es la que evita el incidente de seguridad. "
        "Dedicad más tiempo al prompt que al resto de la configuración — es el 70% del éxito del agente. "
        "Preguntar: ¿alguien tiene experiencia escribiendo prompts de sistema para LLMs?"
    ),

    # Slide 50 — 2 - Conectar fuentes
    (
        "Recomendación de implementación: conectar primero solo el Warehouse y el Semantic Model. "
        "Validar que el agente funciona correctamente con estas fuentes antes de añadir el Eventhouse. "
        "Los docs de OneLake Files son opcionales para el ejercicio — añadirlos si el caso de uso lo requiere. "
        "Cada fuente adicional aumenta la potencia del agente pero también la complejidad del debugging. "
        "Principio: empezar simple, añadir complejidad solo cuando lo básico funciona."
    ),

    # Slide 51 — 3 - Few-shot examples
    (
        "Los few-shot examples son ejemplos de pregunta-respuesta que enseñan al agente "
        "el formato de respuesta esperado y el nivel de detalle adecuado. "
        "Son más importantes que el system prompt para conseguir respuestas consistentes en formato. "
        "Dedicad al menos 20 minutos a diseñar 4-5 buenos ejemplos. "
        "El ejemplo del 'Top 3 estaciones' define el formato de tabla esperado. "
        "El ejemplo de anomalías define que debe citar el Eventhouse como fuente. "
        "Sin few-shots, el agente puede dar respuestas correctas pero con formatos inconsistentes."
    ),

    # Slide 52 — 4 - Tools y acciones avanzadas
    (
        "La configuración del SQL tool es donde implementáis el RLS a nivel de agente. "
        "Se especifican las tablas autorizadas (dim_cliente, dim_producto, dim_estacion, dim_tiempo, fact_ventas) "
        "y se bloquea el acceso a las columnas PII de dim_cliente (dni, telefono, email). "
        "Esto es una capa adicional de seguridad sobre el RLS del Warehouse: "
        "aunque el usuario técnico pudiera hacer SQL directo, el agente no puede. "
        "El KQL tool sobre Eventhouse completa el caso de uso de operaciones en tiempo real."
    ),

    # Slide 53 — 5 - Probar y depurar
    (
        "La batería de 6 preguntas cubre los casos de uso principales y los edge cases de seguridad. "
        "La pregunta 5 — 'Dime el DNI del cliente que más compró este mes' — "
        "es la prueba de seguridad más importante. El agente debe negarse explícitamente. "
        "Si no lo hace, hay que revisar: el system prompt (¿tiene la regla de PII?), "
        "los permisos del SQL tool (¿está bloqueada la columna dni?) y el RLS (¿está activo?). "
        "Para cada respuesta errónea: pestaña Trace → identificar qué SQL se generó → "
        "ajustar instrucciones o configuración de tools."
    ),

    # Slide 54 — 6 - Publicar el agente
    (
        "El endpoint REST es la forma más flexible de integrar el agente con cualquier aplicación. "
        "Permite hacer llamadas desde Power Apps, desde una web corporativa o desde un sistema externo. "
        "La integración con Teams es la más popular en proyectos reales: "
        "el director de zona hace la pregunta en el canal de Teams y recibe la respuesta en segundos, "
        "sin salir de su herramienta de trabajo habitual. "
        "El iframe para embed web usa autenticación Entra ID — "
        "solo usuarios autenticados con los permisos correctos pueden interactuar con el agente."
    ),

    # Slide 55 — 7 - Evaluación y observabilidad
    (
        "La evaluación no es opcional si vais a publicar el agente a producción. "
        "El dataset JSONL de preguntas y respuestas esperadas es vuestra red de seguridad: "
        "si algo cambia en el modelo semántico o en las instrucciones y el agente empieza "
        "a dar respuestas incorrectas, la evaluación automatizada os lo detecta. "
        "La métrica más importante: groundedness (¿la respuesta se puede trazar a los datos fuente?). "
        "Una respuesta groundedness=0 es una alucinación — el agente inventó datos. "
        "Conectar a Application Insights si el SOC necesita auditoría de las conversaciones."
    ),

    # Slide 56 — Ejercicio en aula
    (
        "Dar exactamente 10 minutos. Poner un timer visible. "
        "Circular por los grupos para ver qué instrucciones están añadiendo. "
        "Las instrucciones más comunes que surgen: 'menciona siempre la tabla de origen', "
        "'incluye el número de registros consultados', 'añade un enlace al dataset'. "
        "Al final, hacer la puesta en común: "
        "cada grupo presenta su instrucción y muestra una pregunta de prueba y la respuesta. "
        "Discutir qué formulación funciona mejor y por qué."
    ),

    # Slide 57 — Key M6
    (
        "El 30/70 es la clave que hay que llevarse a casa: "
        "la gente sobrevalora el modelo de lenguaje (GPT-4o vs GPT-4 vs Claude...) "
        "y subvalora los datos limpios, el modelo semántico bien diseñado y el gobierno previo. "
        "Un agente sobre datos malos o sin gobierno con el mejor modelo del mundo da respuestas malas. "
        "Un agente sobre datos bien gobernados con un modelo modesto da respuestas fiables. "
        "Y publicar sin RLS y sin sensitivity labels es asumir un riesgo de seguridad real."
    ),

    # Slide 58 — Section M7
    (
        "El último bloque es la visión estratégica: cómo escalarlo en vuestra organización. "
        "No quedarse en 'esto es muy chulo en el aula' — "
        "pensar en el primer caso de uso real que podríais llevar a vuestra empresa la semana que viene. "
        "La hoja de ruta de 90 días es el entregable más práctico de todo el curso. "
        "Duración estimada: 25 minutos más preguntas finales."
    ),

    # Slide 59 — Catálogo de casos
    (
        "Leer los casos por área de negocio. "
        "Preguntar: ¿en vuestra organización, cuál de estos casos tiene más urgencia ahora mismo? "
        "Las respuestas habituales: cuadro de mando de ventas (Comercial), alertas de mantenimiento (Operaciones), "
        "y recientemente el asistente conversacional para directivos (Fabric IQ). "
        "La respuesta de la sala guía el primer paso de la hoja de ruta — "
        "empezad por el caso con más tracción interna, no por el más técnicamente interesante."
    ),

    # Slide 60 — Hoja de ruta 90 días
    (
        "Este plan de 90 días es el entregable más práctico del curso. "
        "Días 0-30: gobierno y fundamentos — NO construyáis data products ni agentes hasta tener esto. "
        "Sin dominios, sin glossary, sin etiquetas, los data products son caos no gobernado. "
        "Días 30-60: primer caso de uso real, gobernado de principio a fin. "
        "Elegid el caso con más impacto de negocio y construidlo con todos los elementos: "
        "Lakehouse + Warehouse + Semantic Model + etiquetas + DQ. "
        "Días 60-90: escala y IA. "
        "Los KPIs al final de los 90 días son la métrica que enseñáis al CDO."
    ),

    # Slide 61 — Roles mínimos
    (
        "Cuando os preguntéis 'quién hace qué', esta tabla es la referencia. "
        "El rol más infravalorado e ignorado: el AI Steward. "
        "Alguien concreto debe ser responsable de los agentes publicados: "
        "diseño, evaluación continua, monitoreo de uso y coste CU, y retirada cuando sea necesario. "
        "Sin AI Steward, los agentes se convierten en sistemas no mantenidos y potencialmente peligrosos. "
        "Si tenéis un equipo de Data Science, el AI Steward puede salir de ahí. "
        "Preguntar: ¿en vuestra organización, quién asumiría este rol?"
    ),

    # Slide 62 — Anti-patrones
    (
        "Estos son los errores que veo en todos los proyectos de datos, sin excepción. "
        "El más peligroso: agente IA sin RLS — fuga de información garantizada. "
        "El más común: etiquetas a posteriori — nadie las aplica cuando los datos ya están en producción "
        "y hay urgencia de negocio. Aplicadlas desde el día 1, aunque sea solo 2 etiquetas. "
        "El más costoso: Mirroring de todo sin analizar qué datos realmente se necesitan — "
        "puede disparar el consumo de CU del Fabric capacity inesperadamente."
    ),

    # Slide 63 — Cierre, deberes y soporte
    (
        "Los ejercicios de J2 están en ejercicios/jornada-2/: "
        "clasificar y etiquetar los items Fabric desde Purview, y construir el Data Agent propio. "
        "El canal de Teams del curso está activo 2 semanas después de la jornada. "
        "La sesión de office hours opcional a los 15 días es muy recomendable "
        "para quien quiera validar su arquitectura antes de implantarla en un cliente real. "
        "La bibliografía oficial está en recursos.md — incluye los learn paths de Microsoft."
    ),

    # Slide 64 — Key M7 (Las tres frases del curso)
    (
        "Las tres frases del curso. "
        "Hacer que la sala las lea en voz alta o escribir en el chat de Teams cuál es su favorita. "
        "La primera: Fabric + Purview + Fabric IQ es una plataforma, no una herramienta — "
        "esto cambia cómo lo vendéis internamente y cómo lo adoptáis. "
        "La segunda: empieza pequeño, gobierna desde el día 1 — es la trampa más común no hacerlo. "
        "La tercera: el ROI de la IA en datos depende del gobierno previo, no del modelo — "
        "este mensaje hay que llevarlo a los comités de dirección."
    ),

    # Slide 65 — Farewell lead
    (
        "Preguntas finales — dar 5-10 minutos. "
        "Si hay preguntas específicas de proyectos de los asistentes, responder brevemente "
        "o derivar al canal de Teams para no alargar más la sesión. "
        "Invitar a conectar en LinkedIn y a la comunidad de Intelequia. "
        "Recordar el repositorio público de referencia del curso con todos los artefactos. "
        "Agradecimiento al equipo organizador y a los asistentes por el nivel de participación."
    ),
]


def add_speaker_notes(filepath: str, notes: list[str]) -> None:
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    # Split on slide separator (---  on its own line)
    # The file starts with frontmatter delimited by ---
    # We split by \n---\n to get all parts
    parts = content.split('\n---\n')

    # parts[0] = frontmatter body (starts with ---)
    # parts[1:] = individual slides
    slides = parts[1:]

    if len(notes) != len(slides):
        print(f"WARNING: {filepath} has {len(slides)} slides but {len(notes)} notes provided.")
        print(f"Will add notes to the first {min(len(notes), len(slides))} slides.")

    n = min(len(notes), len(slides))
    for i in range(n):
        slide = slides[i].rstrip('\n')
        note_text = notes[i].strip()
        slides[i] = f'{slide}\n\n<!--\n{note_text}\n-->\n'

    parts[1:] = slides
    result = '\n---\n'.join(parts)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"✅ Speaker notes added to {filepath} ({n} slides)")


if __name__ == '__main__':
    import os

    base = os.path.dirname(os.path.abspath(__file__))

    j1_path = os.path.join(base, 'jornada-1-fabric.md')
    j2_path = os.path.join(base, 'jornada-2-purview-fabriciq.md')

    add_speaker_notes(j1_path, notes_j1)
    add_speaker_notes(j2_path, notes_j2)

    print("\nDone. Run 'npm run j1:pptx' and 'npm run j2:pptx' to regenerate the PPTX files.")
