# FID SDK · Documentación de personalización

Referencia para el equipo de desarrollo: contrato de configuración, tokens, componentes, ilustraciones, íconos y accesibilidad.

- **`index.html`**: versión interactiva (playground, buscador, catálogo de tokens). Funciona abriéndola en el navegador.
- **`FID-SDK-Documentacion-viva.pdf`**: misma documentación en PDF, con índice y links clickeables.
- **`fuente/`**: plantilla y script para regenerar `index.html` desde el paquete de assets.

Fuente de verdad: archivo de Figma "FID SDK — Variables". Si algo contradice a Figma, gana Figma.

## Regenerar

Requiere el paquete `FID SDK - Assets` (CSS, SVG, Lotties, `tokens.json`, `DESIGN.md`) en la carpeta hermana, o pasar su ruta:

```bash
python3 fuente/build.py "ruta/a/FID SDK - Assets"
```
