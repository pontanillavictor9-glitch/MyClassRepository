"""
Agente DISEÑADOR. Prepara lo que se ve en la tienda:
  - portada.png       2000×2000, la primera imagen del anuncio (TPT y Etsy)
  - muestra-N.png     páginas de muestra con marca de agua «PREVIEW»
  - vista_previa.pdf  esas mismas muestras en un PDF (TPT lo pide como «Preview»)

Las muestras llevan marca de agua para que nadie se quede el producto gratis.
"""

from html import escape
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import comun


def marca_agua(origen, destino):
    im = Image.open(origen).convert("RGBA")
    capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    fuente = ImageFont.truetype(str(comun.FUENTES / "Fredoka-SemiBold.ttf"), int(im.width * 0.07))
    texto = f"PREVIEW · {comun.MARCA}"
    paso = int(im.width * 0.42)
    for y in range(-im.height, im.height * 2, paso):
        for x in range(-im.width, im.width * 2, int(paso * 2.2)):
            d.text((x, y), texto, font=fuente, fill=(120, 120, 120, 60))
    capa = capa.rotate(30, center=(im.width / 2, im.height / 2))
    Image.alpha_composite(im, capa).convert("RGB").save(destino, quality=92)
    return destino


def muestras(html, indices, carpeta):
    carpeta = Path(carpeta)
    tmp = carpeta / "_paginas"
    tmp.mkdir(parents=True, exist_ok=True)
    comun.paginas_png(html, indices, str(tmp / "p%d.png"), escala=2)
    salida = []
    for n, i in enumerate(indices, 1):
        origen = tmp / f"p{i + 1}.png"
        if origen.exists():
            salida.append(marca_agua(origen, carpeta / f"muestra-{n}.png"))
    if salida:
        imgs = [Image.open(s).convert("RGB") for s in salida]
        imgs[0].save(carpeta / "vista_previa.pdf", save_all=True, append_images=imgs[1:], resolution=192)
    return salida, tmp


def portada(ficha, paginas, carpeta, colores):
    """Portada cuadrada: título grande, insignias y 3 páginas en abanico."""
    p = ficha["portada"]
    imgs = "".join(
        f'<img src="{Path(x).resolve().as_uri()}" style="--r:{r}deg;--x:{dx}px;--y:{dy}px;z-index:{z}">'
        for x, r, dx, dy, z in zip(paginas, (-8, 8, 0), (-330, 330, 0), (50, 50, 0), (1, 2, 3)))
    insignias = "".join(f"<span>{escape(t)}</span>" for t in ficha.get("insignias", []))
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{comun.css()}
body{{margin:0;width:2000px;height:2000px;background:{colores['suave']};font-family:Fredoka;overflow:hidden;position:relative}}
.marco{{position:absolute;inset:40px;border:14px solid {colores['acento']};border-radius:80px}}
.arriba{{position:absolute;top:120px;left:0;right:0;text-align:center;color:{colores['titulo']}}}
.grado{{display:inline-block;background:{colores['acento']};color:#fff;font-weight:600;font-size:64px;border-radius:999px;padding:14px 56px}}
h1{{font-size:150px;line-height:1.02;margin:34px 80px 0;color:{colores['titulo']}}}
.det{{font-family:Lexend;font-size:52px;margin-top:22px;color:#334155}}
.pags{{position:absolute;left:50%;top:700px;width:0}}
.pags img{{position:absolute;width:760px;left:-380px;top:0;border-radius:18px;
  box-shadow:0 30px 60px rgba(0,0,0,.25);transform:translate(var(--x),var(--y)) rotate(var(--r))}}
.ins{{position:absolute;z-index:10;bottom:95px;left:0;right:0;display:flex;justify-content:center;gap:24px}}
.ins span{{background:#fff;border:5px solid {colores['acento']};color:{colores['titulo']};font-weight:600;font-size:46px;border-radius:999px;padding:10px 36px}}
</style></head><body><div class="marco"></div>
<div class="arriba"><span class="grado">{escape(p['grado'])}</span><h1>{escape(p['linea1'])}<br>{escape(p['linea2'])}</h1>
<div class="det">{escape(p['detalle'])}</div></div>
<div class="pags">{imgs}</div><div class="ins">{insignias}</div></body></html>"""
    return comun.png(html, Path(carpeta) / "portada.png", 2000, 2000)
