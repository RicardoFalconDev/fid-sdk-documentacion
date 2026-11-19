# FID SDK · Documentación de personalización

Referencia para el equipo de desarrollo: contrato de configuración, tokens, componentes, ilustraciones, íconos y accesibilidad.

**[Abrir la documentación →](https://ricardofalcondev.github.io/fid-sdk-documentacion/)**

## Qué hay en este repo

| Archivo | Para qué |
|---|---|
| `index.html` | Versión interactiva: playground, buscador (⌘K), catálogo de tokens y checklist. Es la que publica GitHub Pages. |
| `FID-SDK-Documentacion-viva.pdf` | La misma documentación en PDF, con índice, marcadores y links clickeables. |
| `fuente/` | Plantilla y script para regenerar `index.html` desde el paquete de assets. |

## Fuente de verdad

Archivo de Figma "FID SDK — Variables". Si algo contradice a Figma, gana Figma.

## Regenerar

Requiere el paquete `FID SDK - Assets` (CSS, SVG, Lotties, `tokens.json`, `DESIGN.md`) en la carpeta hermana, o pasar su ruta:

```bash
python3 fuente/build.py "ruta/a/FID SDK - Assets"
```
