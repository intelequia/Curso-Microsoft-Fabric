import os

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI


endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["FOUNDRY_MODEL_DEPLOYMENT"]

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default",
)

client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version="preview",
)

response = client.responses.create(
    model=deployment,
    input="Resume en una frase que aporta Microsoft Foundry a una empresa.",
)

print(response.output_text)
