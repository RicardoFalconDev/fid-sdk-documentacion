#!/usr/bin/env python3
"""Arma index.html (documentación viva, un solo archivo) desde el paquete FID SDK - Assets.
Uso: python3 build.py [ruta/al/paquete FID SDK - Assets]
"""
import html, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent.parent / 'FID SDK - Assets'
OUT = HERE.parent / 'index.html'
LOTTIE_LIB = HERE / 'lottie.min.js'

LINKS = {
    'LINK_FIGMA_DOCS': 'https://www.figma.com/design/o5RhfPgp35VOEXuybrIL9W/FID-SDK-%E2%80%94-Variables--dev---refactor-?node-id=51-2936',
    'LINK_FIGMA_HANDOFF': 'https://www.figma.com/design/HhP97fjZ3FT8xG1AG411Qj/-Handoff--Portal-Integradores?node-id=847-26060',
    'LINK_DRIVE': 'https://drive.google.com/drive/folders/1ErW-_ImyoMbPjmgqAmvuWtwEqSEJ39Cj',
}

read = lambda p: Path(p).read_text(encoding='utf-8')
md = read(PKG / 'DESIGN.md')
tokens = json.loads(read(PKG / 'tokens.json'))


def section(title_start, until=None):
    i = md.index(title_start)
    j = md.index(until, i + 1) if until else len(md)
    return md[i:j]


def code_blocks(text, lang):
    return re.findall(r'```' + lang + r'\n(.*?)```', text, re.S)


def hl(code):
    """Resaltado mínimo (comentarios y cadenas) sobre texto ya escapado."""
    out = html.escape(code, quote=False)
    out = re.sub(r'(/\*.*?\*/)', r'<span class="tk-c">\1</span>', out, flags=re.S)
    out = re.sub(r'(?m)(^|\s)(//.*)$', r'\1<span class="tk-c">\2</span>', out)
    out = re.sub(r'(&lt;!--.*?--&gt;)', r'<span class="tk-c">\1</span>', out, flags=re.S)
    return out.rstrip('\n')


# ── usos desde las tablas de DESIGN.md ──
uso = {}
for line in section('## 5 · Catálogo', '## 6 ·').splitlines():
    m = re.match(r'\|\s*`(--[a-z0-9-]+)`\s*\|(.*)\|\s*$', line)
    if m:
        cells = [c.strip() for c in m.group(2).split('|')]
        if cells and cells[-1] and not cells[-1] in ('sí', 'no', '**sí**'):
            uso[m.group(1)] = cells[-1].replace('`', '')

STATE_ES = {'error': 'error', 'success': 'éxito', 'warning': 'advertencia', 'info': 'información'}
PART_ES = {'bg': 'fondo', 'border': 'borde', 'text': 'texto', 'icon': 'ícono', 'surface': 'superficie'}
BTN_ES = {'primary': 'primario', 'secondary': 'secundario', 'tertiary': 'terciario', 'danger': 'de peligro', 'disabled': 'deshabilitado'}


def make_uso(name):
    if name in uso:
        return uso[name]
    m = re.match(r'--feedback-(\w+)-(\w+)', name)
    if m:
        return f'Estado de {STATE_ES.get(m.group(1), m.group(1))}: {PART_ES.get(m.group(2), m.group(2))}'
    m = re.match(r'--button-(\w+)-(.+)', name)
    if m:
        part = m.group(2).replace('bg-hover', 'fondo en hover').replace('-hover', ' en hover').replace('bg', 'fondo').replace('border', 'borde').replace('text', 'texto')
        return f'Botón {BTN_ES.get(m.group(1), m.group(1))}: {part}'
    m = re.match(r'--accent-(\d+)', name)
    if m:
        return f'Escala de marca, paso {m.group(1)}'
    return ''


semantic = []
for name, t in tokens['semantic'].items():
    ref = t.get('ref') or ''
    brand = ('accent-' in ref) or name.startswith('--accent-') or name == '--button-primary-text'
    semantic.append({'name': name, 'value': t['value'], 'ref': ref, 'uso': make_uso(name), 'brand': brand})

# estilos de texto
text_styles = []
for line in section('Estilos de texto, de mayor', '## 6 ·').splitlines():
    m = re.match(r'\|\s*`(text/[^`]+)`\s*\|\s*([\d]+\s*/\s*[\d]+)\s*\|\s*(.+?)\s*\|', line)
    if m:
        text_styles.append({'name': m.group(1), 'px': m.group(2), 'peso': m.group(3)})

# checklist
def inline_md(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)

checklist = [inline_md(l[6:].strip()) for l in section('## 10 ·').splitlines() if l.startswith('- [ ] ')]

# código
apply_js = code_blocks(section('## 4 ·', '## 5 ·'), 'js')[0]
recetas = code_blocks(section('## 6 ·', '## 7 ·'), 'css')[0]
def cut(a, b=None):
    i = recetas.index(a)
    j = recetas.index(b) if b else len(recetas)
    return recetas[i:j].strip('\n')
code_btn = cut('.sdk-btn {', '.sdk-checkbox')
code_form = cut('.sdk-checkbox', '.sdk-link')
code_misc = cut('.sdk-link')
icons_snip = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,100..700,0..1,0&display=swap">\n\n'
              + read(PKG / 'css/icons.css').split('*/', 1)[1].strip()
              + '\n\n<span class="icon" aria-hidden="true">info</span>             <!-- sin relleno (por defecto) -->\n<span class="icon icon--filled" aria-hidden="true">error</span> <!-- relleno -->')
a11y_js = apply_js.split('function applyBranding')[0].strip()
tint_js = read(PKG / 'js/tint-lottie.js')

# paquete css (orden de carga)
package_css = '\n'.join(read(PKG / 'css' / f) for f in ('tokens.css', 'accent-from-primary.css', 'illustrations.css', 'icons.css'))

svgs = {n: read(PKG / 'illustrations' / f'{n}.svg') for n in ('ill-onboarding', 'ill-sms', 'ill-email', 'error-x')}
lotties = {n: json.loads(read(PKG / 'lottie' / f'{n}.json')) for n in ('face-scan', 'card-skeleton', 'verification', 'success-check')}
logo = read(PKG / 'fixed/logo-fid.svg').strip()
logo_sm = re.sub(r'width="46" height="32"', 'width="22" height="15"', logo, count=1)

def js(o):
    return json.dumps(o, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

scale_cap = ''.join(f'<span>{p}</span>' for p in ['3%', '5%', '10%', '15%', '22%', '29%', '39%', '54%', '100%', '97%', '87%', '46%'])

repl = {
    'PACKAGE_CSS': package_css,
    'LOGO_FID_SM': logo_sm,
    'LOGO_FID': logo,
    'SCALE_CAP': scale_cap,
    'CODE_APPLY': hl(apply_js),
    'CODE_BTN': hl(code_btn),
    'CODE_FORM': hl(code_form),
    'CODE_MISC': hl(code_misc),
    'CODE_TINT': hl(tint_js),
    'CODE_ICONS': hl(icons_snip),
    'CODE_A11Y': hl(a11y_js),
    'LOTTIE_LIB': read(LOTTIE_LIB).replace('</script', '<\\/script'),
    'DATA_JSON': js({'semantic': semantic, 'textStyles': text_styles, 'checklist': checklist}),
    'LOTTIES_JSON': js(lotties),
    'SVGS_JSON': js(svgs),
    'LOGO_JSON': js({'full': logo, 'sm': logo_sm}),
    **LINKS,
}

out = read(HERE / 'plantilla.html')
# Los marcadores largos van primero para que LOGO_FID no pise a LOGO_FID_SM
for k in sorted(repl, key=len, reverse=True):
    out = out.replace('{{' + k + '}}', repl[k])
left = re.findall(r'\{\{[A-Z_]+\}\}', out)
assert not left, left
OUT.write_text(out, encoding='utf-8')
print(f'OK → {OUT}  ({OUT.stat().st_size/1024:.0f} KB) · tokens {len(semantic)} · estilos {len(text_styles)} · checklist {len(checklist)}')
