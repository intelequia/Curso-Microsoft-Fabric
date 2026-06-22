# Preparación del entorno

Reserva entre 30 y 45 minutos antes de la primera jornada.

## 1. Crear el grupo de recursos

1. Entra en [Azure Portal](https://portal.azure.com).
2. Crea un resource group:
   - Nombre: `rg-ia-ml-azure-aurora`
   - Región sugerida: una región donde tengas cuota para modelos Foundry, Azure OpenAI y Azure Machine Learning.
3. Verifica que tu usuario tiene rol **Contributor** sobre el grupo.

## 2. Entrar en Microsoft Foundry

1. Abre [https://ai.azure.com](https://ai.azure.com).
2. Activa la experiencia nueva de Foundry si aparece el conmutador **New Foundry**.
3. Crea o selecciona un recurso/proyecto:
   - Recurso: `foundry-aurora`
   - Proyecto: `foundry-aurora-curso`
4. Anota el endpoint del proyecto, con forma:

```text
https://<resource-name>.services.ai.azure.com/api/projects/<project-name>
```

## 3. Desplegar un modelo

1. En Foundry, abre el catálogo de modelos.
2. Selecciona un modelo disponible en tu región.
3. Despliégalo con un nombre simple, por ejemplo:
   - `gpt-4.1-mini`
   - `gpt-5.1-mini`, si está disponible en tu tenant y región
4. Guarda el nombre exacto del despliegue: se usará en los ejercicios.

## 4. Preparar Azure AI Search

1. Crea un servicio Azure AI Search en el mismo grupo de recursos:
   - Nombre: `srch-aurora-foundry-<iniciales>`
   - Tier: Free o Basic para laboratorio.
2. En Foundry, crea una conexión al servicio de búsqueda.
3. Usaremos este servicio para knowledge bases y grounding.

## 5. Preparar observabilidad

1. Crea un recurso Application Insights:
   - Nombre: `appi-aurora-foundry`
2. Enlázalo al proyecto Foundry si la opción está disponible.
3. Si el portal no permite enlazarlo aún, se mostrará en demo y se usará como referencia arquitectónica.

## 6. Preparar local

```bash
az login
python --version
pip install azure-identity azure-ai-projects openai pandas
pip install azure-ai-ml mlflow scikit-learn matplotlib
```

Crea variables de entorno para los ejemplos:

```bash
export FOUNDRY_PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
export FOUNDRY_MODEL_DEPLOYMENT="<deployment-name>"
export AZURE_ML_WORKSPACE="<workspace-name>"
export AZURE_ML_RESOURCE_GROUP="rg-ia-ml-azure-aurora"
```

En Windows PowerShell:

```powershell
$env:FOUNDRY_PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
$env:FOUNDRY_MODEL_DEPLOYMENT="<deployment-name>"
$env:AZURE_ML_WORKSPACE="<workspace-name>"
$env:AZURE_ML_RESOURCE_GROUP="rg-ia-ml-azure-aurora"
```

## 7. Preparar Azure Machine Learning Studio

1. Abre [https://ml.azure.com](https://ml.azure.com).
2. Crea o selecciona un workspace:
   - Workspace: `mlw-aurora-curso`
   - Storage account: creado automáticamente o reutilizado del grupo.
   - Key Vault y Application Insights: creados automáticamente para laboratorio.
3. Crea una compute instance pequeña para notebooks:
   - Nombre: `ci-aurora-<iniciales>`
   - Tamaño sugerido: CPU económico disponible en tu región.
4. Crea un compute cluster con escalado a cero:
   - Nombre: `cpu-cluster`
   - Min nodes: `0`
   - Max nodes: `2`
5. Comprueba que puedes abrir Notebooks y ver Jobs, Models y Endpoints.

## 8. Verificación

Antes del curso deberías poder:

- Entrar en el proyecto Foundry.
- Entrar en Azure Machine Learning Studio.
- Ver al menos un modelo desplegado.
- Ver el workspace `mlw-aurora-curso`.
- Arrancar o seleccionar una compute instance.
- Abrir el playground y enviar una pregunta.
- Ejecutar `az account show`.
- Abrir los documentos de `assets/docs`.

## Problemas habituales

| Síntoma | Causa probable | Solución |
| --- | --- | --- |
| No puedo crear modelos | Falta cuota o región no compatible | Cambia de región o solicita cuota. |
| El endpoint no funciona | Estás usando el endpoint de recurso equivocado | Usa el endpoint del proyecto para Foundry SDK y Agent Service. |
| Error 401 local | `az login` usa otro tenant | Ejecuta `az login --tenant <tenant-id>`. |
| No aparece una herramienta | Preview no habilitada o región no compatible | Usa la alternativa indicada por el formador. |
| La compute de Azure ML no arranca | Cuota insuficiente o tamaño no disponible | Cambia el tamaño de VM o solicita cuota. |
