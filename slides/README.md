# Slides · Curso Microsoft Fabric

Slides modernas para las dos jornadas del curso, construidas con [**Marp**](https://marp.app) (Markdown Presentation Ecosystem).

## Decks

| Archivo | Jornada | Duración | Contenido |
|---|---|---|---|
| [`jornada-1-fabric.md`](jornada-1-fabric.md) | **J1** | 4 h | Fundamentos · OneLake · Lakehouse · Warehouse · Ingesta · Spark · Real-Time · Power BI Direct Lake |
| [`jornada-2-purview-fabriciq.md`](jornada-2-purview-fabriciq.md) | **J2** | 4 h | Purview · Data Map · Catalog · Information Protection · DLP · Integración con Fabric · **Fabric IQ** · Data Agents |

Hilo conductor: el operador ficticio **Aurora Energía** (estaciones de servicio + comercializadora eléctrica + logística). El repositorio es **público** y reutilizable: no contiene referencias a clientes reales.

## Diseño

Tema personalizado en [`themes/intelequia.css`](themes/intelequia.css):

- Tipografía **Inter** + **JetBrains Mono** (Google Fonts).
- Paleta brand **indigo → púrpura → cian** (`#6366F1 → #8B5CF6 → #06B6D4`).
- Layouts vía clase de slide:
  - `lead` · portada y cierres
  - `section` · separadores de módulo
  - `key` · "para llevarse a casa"
  - `tight` · slides con tabla larga o código
  - `bare` · ocultar paginación
- Bloques de código estilo terminal (con dots de tráfico).
- Pills, tags y módulos como elementos visuales reutilizables.

Cambia los colores en las variables CSS del bloque `:root` del tema y todo el deck se reestilará automáticamente.

## Requisitos

- **Node.js 18+** instalado.
- (Opcional) Extensión [**Marp for VS Code**](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode) para previsualizar en vivo.

Instalación de Marp CLI:

```bash
# Global (recomendado)
npm install -g @marp-team/marp-cli

# o con scripts del proyecto
cd "slides"
npm install
```

## Renderizar

Desde esta carpeta `slides/`:

### HTML (single-file, ideal para presentar)

```bash
marp jornada-1-fabric.md           --theme themes/intelequia.css --html --allow-local-files -o dist/jornada-1-fabric.html
marp jornada-2-purview-fabriciq.md --theme themes/intelequia.css --html --allow-local-files -o dist/jornada-2-purview-fabriciq.html
```

### PDF (entrega a alumnos)

```bash
marp jornada-1-fabric.md           --theme themes/intelequia.css --pdf  --allow-local-files -o dist/jornada-1-fabric.pdf
marp jornada-2-purview-fabriciq.md --theme themes/intelequia.css --pdf  --allow-local-files -o dist/jornada-2-purview-fabriciq.pdf
```

### PowerPoint (.pptx)

```bash
marp jornada-1-fabric.md           --theme themes/intelequia.css --pptx --allow-local-files -o dist/jornada-1-fabric.pptx
marp jornada-2-purview-fabriciq.md --theme themes/intelequia.css --pptx --allow-local-files -o dist/jornada-2-purview-fabriciq.pptx
```

> En PPTX el render aproxima la maquetación (algunas capas decorativas pueden simplificarse). Para máxima fidelidad, usa el HTML proyectado a pantalla completa.

### Atajos npm

```bash
npm run j1:html     # → dist/jornada-1-fabric.html
npm run j2:pdf      # → dist/jornada-2-purview-fabriciq.pdf
npm run all:pdf     # ambos PDFs
npm run watch:j1    # live server con recarga
```

## Previsualizar en VS Code

1. Instala la extensión **Marp for VS Code**.
2. Abre cualquier `jornada-*.md`.
3. Pulsa el icono de previsualización Marp (esquina superior derecha del editor).
4. La extensión detecta `theme: intelequia` automáticamente si añades en *Settings*:

   ```json
   "markdown.marp.themes": [
     "./slides/themes/intelequia.css"
   ]
   ```

## Estructura

```text
slides/
├── README.md                          ← este archivo
├── package.json                       ← scripts de render
├── jornada-1-fabric.md                ← deck Jornada 1
├── jornada-2-purview-fabriciq.md      ← deck Jornada 2
├── themes/
│   └── intelequia.css                 ← tema visual
└── dist/                              ← (generado) HTML/PDF/PPTX
```

## Convenciones del Markdown

- `---` separa slides.
- `<!-- _class: lead -->` aplica una clase **solo a esa slide**.
- `<!-- _class: lead bare -->` combina varias clases.
- Math con KaTeX entre `$...$` (inline) y `$$...$$` (bloque).
- Bloques de código triple backtick · resaltados como terminal.
- Tablas Markdown estándar.
- Para insertar imágenes: `![bg](path/al/png)` o `![w:600 h:400](url)`.

## Licencia / reutilización

Este material está pensado para reutilizarse internamente en Intelequia y con clientes. **No incluye datos ni nombres de clientes reales** — todo el caso "Aurora Energía" es ficticio.
