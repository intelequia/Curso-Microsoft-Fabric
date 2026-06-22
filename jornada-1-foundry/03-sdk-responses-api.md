# J1-M3 · Primera aplicación con SDKs y Responses API

**Duración:** 40 min · **Formato:** explicación + coding demo

## Objetivos

1. Entender qué SDK conviene usar según el escenario.
2. Hacer una primera llamada autenticada desde código.
3. Distinguir llamada directa a modelo, llamada al proyecto y agente publicado.

## Contenido

Foundry ofrece varias superficies de desarrollo:

| SDK/API | Cuándo usarlo |
| --- | --- |
| **Foundry SDK** | Acceso al proyecto: modelos, herramientas, agentes, archivos y evaluaciones. |
| **OpenAI SDK** | Máxima compatibilidad con modelos OpenAI y `/openai/v1`. |
| **Agent Framework** | Agentes code-first, hosted agents y multi-agent systems. |
| **REST** | Integraciones ligeras, pipelines y pruebas controladas. |

La autenticación recomendada para empresa es **Microsoft Entra ID** con `DefaultAzureCredential`. Las API keys son útiles en laboratorio, pero no deberían ser la base de producción.

## Snippet de referencia

```python
import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["FOUNDRY_MODEL_DEPLOYMENT"]

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version="preview"
)

response = client.responses.create(
    model=deployment,
    input="Resume en una frase qué aporta Microsoft Foundry."
)

print(response.output_text)
```

## Demo en vivo

1. Configurar variables de entorno.
2. Ejecutar una llamada simple.
3. Cambiar modelo y comparar latencia/respuesta.
4. Mostrar error típico de autenticación y cómo leerlo.
5. Guardar el snippet como base para ejercicios.

## Mensajes clave

- El endpoint del proyecto y el endpoint OpenAI no son intercambiables.
- Usa Entra ID por defecto en entornos reales.
- La primera integración debe medir latencia, coste aproximado y errores, no solo "funciona".
