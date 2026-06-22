# Ejercicio 2 (Jornada 1) · Primera llamada desde SDK

**Tiempo estimado:** 45 min · **Modalidad:** casa

## Objetivo

Ejecutar una llamada autenticada desde Python contra el modelo desplegado.

## Pasos

1. Instala dependencias:

   ```bash
   pip install azure-identity openai
   ```

2. Exporta variables:

   ```bash
   export AZURE_OPENAI_ENDPOINT="https://<resource>.openai.azure.com/"
   export FOUNDRY_MODEL_DEPLOYMENT="<deployment-name>"
   ```

3. Ejecuta:

   ```bash
   python assets/code/first_response.py
   ```

4. Cambia el prompt para pedir una respuesta en formato JSON.
5. Guarda la salida.

## Entregable

Salida del script y breve comentario sobre latencia, modelo usado y errores encontrados.

## Validación

- [ ] `az login` usa el tenant correcto.
- [ ] El script devuelve texto.
- [ ] El deployment usado coincide con el del ejercicio 1.
