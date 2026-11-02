"""
Piezas compartidas de la tienda: rutas, marca, estilo común de las fichas y el
motor que convierte HTML en PDF (tamaño Letter, el de EE. UU.) y en imágenes.
"""

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

RAIZ = Path(__file__).parent
FUENTES = RAIZ / "fuentes"
CONTENIDO = RAIZ / "contenido"
SALIDA = Path(os.environ.get("SALIDA_DIR", RAIZ / "salida"))

# Nombre de la tienda: elígelo tú y ponlo en la variable MARCA (aparece en cada página).
MARCA = os.environ.get("MARCA", "Sunny Desk Studio")
LICENCIA = f"© {MARCA} · For use in one classroom or home. Please don't share or post online."

CSS_BASE = """
@font-face{font-family:Fredoka;font-weight:500;src:url('file://%(f)s/Fredoka-Medium.ttf')}
@font-face{font-family:Fredoka;font-weight:600;src:url('file://%(f)s/Fredoka-SemiBold.ttf')}
@font-face{font-family:Lexend;font-weight:400;src:url('file://%(f)s/Lexend-Regular.ttf')}
@font-face{font-family:Lexend;font-weight:600;src:url('file://%(f)s/Lexend-SemiBold.ttf')}
@page{size:8.5in 11in;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:Lexend,sans-serif;color:#1f2a37}
.hoja{width:8.5in;height:11in;padding:.55in .6in .5in;position:relative;page-break-after:always;overflow:hidden}
.hoja:last-child{page-break-after:auto}
.borde{position:absolute;inset:.3in;border:3px solid var(--acento,#f4a259);border-radius:22px;pointer-events:none}
.cab{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;margin-bottom:14px;position:relative}
.nombre{font-size:13pt;white-space:nowrap}
.nombre span{display:inline-block;border-bottom:1.5px solid #1f2a37;width:2.3in;margin-left:6px}
.fecha span{width:1.2in}
h1{font-family:Fredoka,sans-serif;font-weight:600;font-size:26pt;margin:6px 0 2px;color:var(--titulo,#264653);line-height:1.1}
h2{font-family:Fredoka,sans-serif;font-weight:600;font-size:17pt;margin:0 0 8px;color:var(--titulo,#264653)}
.sub{font-size:11.5pt;color:#4b5563;margin:0 0 14px}
.pie{position:absolute;left:.6in;right:.6in;bottom:.42in;font-size:7.5pt;color:#6b7280;display:flex;justify-content:space-between}
.etiqueta{display:inline-block;background:var(--suave,#fde8d4);color:var(--titulo,#264653);font-family:Fredoka;font-weight:600;
  border-radius:999px;padding:3px 12px;font-size:10.5pt}
.solucion{color:#c0392b;font-weight:600}
"""


def css():
    return CSS_BASE % {"f": FUENTES.resolve()}


def documento(hojas, acento="#f4a259", titulo="#264653", suave="#fde8d4", extra_css=""):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{css()}
:root{{--acento:{acento};--titulo:{titulo};--suave:{suave}}}{extra_css}</style></head>
<body>{''.join(hojas)}</body></html>"""


def hoja(contenido, pagina=None, borde=True, clase=""):
    pie = f'<div class="pie"><span>{LICENCIA}</span><span>{pagina or ""}</span></div>'
    return f'<section class="hoja {clase}">{"<div class=borde></div>" if borde else ""}{contenido}{pie}</section>'


def cabecera_alumno():
    return ('<div class="cab"><div class="nombre">Name:<span></span></div>'
            '<div class="nombre fecha">Date:<span></span></div></div>')


# --------------------------------------------------------------------------
# HTML → PDF / PNG. Usa Playwright de Python si está; si no, el de Node.
# --------------------------------------------------------------------------

_JS = r"""
const {chromium}=require('playwright');
(async()=>{const [,,modo,html,salida,ancho,alto]=process.argv;
const b=await chromium.launch();const p=await b.newPage({viewport:{width:+ancho||816,height:+alto||1056},deviceScaleFactor:+(process.argv[8]||1)});
await p.goto('file://'+html,{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
if(modo==='pdf'){await p.pdf({path:salida,width:'8.5in',height:'11in',printBackground:true,preferCSSPageSize:true});}
else if(modo==='paginas'){const idx=JSON.parse(process.argv[7]);const hs=await p.$$('section.hoja');
 for(const i of idx){if(hs[i]) await hs[i].screenshot({path:salida.replace('%d',String(i+1))});}}
else{await p.screenshot({path:salida,fullPage:false});}
await b.close();})().catch(e=>{console.error(e);process.exit(1)});
"""


def _renderizar(modo, html, salida, ancho=816, alto=1056, indices=None, escala=1):
    salida = Path(salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        fichero = Path(tmp) / "pagina.html"
        fichero.write_text(html, encoding="utf-8")
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as pw:
                b = pw.chromium.launch()
                p = b.new_page(viewport={"width": ancho, "height": alto}, device_scale_factor=escala)
                p.goto(fichero.as_uri(), wait_until="networkidle")
                p.evaluate("document.fonts.ready")
                if modo == "pdf":
                    p.pdf(path=str(salida), width="8.5in", height="11in", print_background=True,
                          prefer_css_page_size=True)
                elif modo == "paginas":
                    hojas = p.query_selector_all("section.hoja")
                    for i in indices:
                        if i < len(hojas):
                            hojas[i].screenshot(path=str(salida).replace("%d", str(i + 1)))
                else:
                    p.screenshot(path=str(salida))
                b.close()
            return salida
        except ImportError:
            pass
        js = Path(tmp) / "render.js"
        js.write_text(_JS, encoding="utf-8")
        if not shutil.which("node"):
            raise SystemExit("Falta Playwright: pip install playwright && python -m playwright install chromium")
        subprocess.run(["node", str(js), modo, str(fichero), str(salida.resolve()), str(ancho), str(alto),
                        json.dumps(indices or []), str(escala)],
                       check=True, cwd=tmp, env={**os.environ, "NODE_PATH": _node_path()})
    return salida


def _node_path():
    raiz = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    return os.pathsep.join(filter(None, [os.environ.get("NODE_PATH"), raiz]))


def paginas_png(html, indices, patron, escala=2):
    """Foto de páginas sueltas del documento. patron lleva %d (nº de página)."""
    return _renderizar("paginas", html, patron, indices=list(indices), escala=escala)


def pdf(html, salida):
    return _renderizar("pdf", html, salida)


def png(html, salida, ancho, alto):
    return _renderizar("png", html, salida, ancho, alto)


def leer_json(ruta):
    return json.loads(Path(ruta).read_text(encoding="utf-8"))


def escribir_json(ruta, datos):
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    Path(ruta).write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
