# Slides · IA y ML en Azure

Slides modernas para las jornadas del curso, construidas con [Marp](https://marp.app).

## Decks

| Archivo | Jornada | Duración | Contenido |
| --- | --- | --- | --- |
| `jornada-1-foundry.md` | J1 | 4 h | Fundamentos, modelos, SDKs, Responses API, RAG, Foundry IQ, evaluación y costes |
| `jornada-2-foundry-agents-governance.md` | J2 | 4 h | Agent Service, tools, MCP, A2A, seguridad, observabilidad y producción |
| `jornada-azure-ml-studio.md` | AML | 4 h | Workspace, datos, compute, experimentos, AutoML, endpoints, MLOps e integración |

## Renderizar

```bash
npm install
npm run all:pdf
npm run all:pptx
```

## HTML

```bash
npm run all:html
```

## Convenciones

- `---` separa slides.
- `<!-- _class: lead -->` define portadas.
- `<!-- _class: section -->` define separadores de módulo.
- `<!-- _class: key -->` define slides de mensajes clave.
- Las notas de ponente van en comentarios HTML.
