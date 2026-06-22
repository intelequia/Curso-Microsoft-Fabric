# Requisitos del curso IA y ML en Azure

Este documento recoge lo necesario para seguir las demos y completar los ejercicios.

> Si tu equipo corporativo bloquea instalaciones o acceso a Azure, avisa al formador con antelación para usar una alternativa cloud-only.

## 1. Cuentas y permisos

| Recurso | Obligatorio | Notas |
| --- | --- | --- |
| Cuenta Microsoft Entra ID | Si | No sirve una cuenta personal `@outlook.com` para todos los escenarios. |
| Suscripción Azure | Si | Puede ser una trial. Revisa cuotas y regiones antes del curso. |
| Permiso para crear recursos | Si | Resource group, Microsoft Foundry, Azure Machine Learning, Azure AI Search, Storage y Application Insights. |
| Acceso a `https://ai.azure.com` | Si | Usaremos la experiencia nueva de Microsoft Foundry. |
| Acceso a `https://ml.azure.com` | Si | Usaremos Azure Machine Learning Studio para la jornada ML. |
| Permiso para registrar aplicaciones o usar managed identity | Recomendado | Necesario para escenarios de producción y herramientas seguras. |

## 2. Herramientas locales

| Herramienta | Versión | Uso |
| --- | --- | --- |
| Microsoft Edge o Google Chrome | Ultima estable | Portales de Foundry, Azure ML Studio y Azure. |
| Visual Studio Code | Ultima estable | Editar código, prompts y documentos. |
| Git | 2.40+ | Clonar el repositorio. |
| Python | 3.11+ | Ejemplos con SDK, evaluación y scripts. |
| Node.js | 18+ | Renderizar slides Marp. |
| Azure CLI | Ultima estable | Login, variables y validaciones. |

Extensiones recomendadas de VS Code:

- Python.
- Jupyter.
- Azure Resources.
- Microsoft Foundry for VS Code, si está disponible en tu entorno.
- Azure Machine Learning, si está disponible en tu entorno.

## 3. Paquetes Python

Los ejercicios usan principalmente:

```bash
pip install azure-identity azure-ai-projects openai pandas
```

Para la jornada de Azure ML Studio se añadirán paquetes habituales de ciencia de datos y MLOps:

```bash
pip install azure-ai-ml mlflow scikit-learn matplotlib
```

Según la región y las capacidades habilitadas, algunos ejemplos pueden requerir paquetes adicionales indicados en cada ejercicio.

## 4. Red y dominios

Solicita acceso sin inspección SSL agresiva a:

- `*.azure.com`
- `*.microsoft.com`
- `*.services.ai.azure.com`
- `*.openai.azure.com`
- `*.search.windows.net`
- `*.applicationinsights.azure.com`
- `*.blob.core.windows.net`
- `*.cognitiveservices.azure.com`
- `*.ml.azure.com`
- `*.notebooks.azure.net`

## 5. Conocimientos previos

El curso no exige ser científico de datos, pero ayuda tener:

- Conceptos básicos de APIs REST y JSON.
- Python básico.
- Nociones de autenticación con Entra ID.
- Conocimiento general de Azure: resource groups, regiones, RBAC y managed identities.
- Familiaridad con prompts, RAG o Azure OpenAI, aunque no es imprescindible.

## 6. Checklist del alumno

- [ ] Tengo una suscripción Azure activa.
- [ ] Puedo entrar en `https://ai.azure.com`.
- [ ] Puedo entrar en `https://ml.azure.com`.
- [ ] Puedo crear un resource group.
- [ ] Tengo Python 3.11+ y VS Code instalados.
- [ ] Tengo Azure CLI instalado y `az login` funciona.
- [ ] He clonado o descargado este repositorio.
- [ ] He revisado los assets del curso.

## 7. Nota sobre previews

Microsoft Foundry, Azure Machine Learning y Fabric evolucionan muy rápido. Algunas capacidades como A2A, hosted agents, toolboxes, voice agents, routines, Work IQ, conectores de Fabric, datastores OneLake o ciertos endpoints pueden estar en preview o variar por región. Los ejercicios principales se diseñan para depender de capacidades base de Foundry, Agent Service, modelos, Azure AI Search, Azure ML Studio y evaluaciones.
