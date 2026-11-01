"""
Agente 5 — ESCAPARATE

Genera la web pública (HTML estático) en datos/web/:
  - portada con el formulario de alta gratis y los precios
  - una página por sector y otra por sector + provincia, con las licitaciones
    abiertas DE VERDAD de hoy (es lo que Google enseña cuando alguien busca
    «licitaciones de limpieza en Sevilla»)
  - sitemap.xml y robots.txt para que Google las encuentre
  - privacidad y aviso legal (plantillas: hay que rellenar tus datos)

Uso:
    python escaparate.py
"""

import shutil
from collections import defaultdict
from html import escape

import comun

PROVINCIAS = [
    "A Coruña", "Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila", "Badajoz",
    "Barcelona", "Bizkaia", "Burgos", "Cáceres", "Cádiz", "Cantabria", "Castellón", "Ceuta",
    "Ciudad Real", "Córdoba", "Cuenca", "Gipuzkoa", "Girona", "Granada", "Guadalajara",
    "Huelva", "Huesca", "Illes Balears", "Jaén", "La Rioja", "Las Palmas", "León", "Lleida",
    "Lugo", "Madrid", "Málaga", "Melilla", "Murcia", "Navarra", "Ourense", "Palencia",
    "Pontevedra", "Salamanca", "Santa Cruz de Tenerife", "Segovia", "Sevilla", "Soria",
    "Tarragona", "Teruel", "Toledo", "Valencia", "Valladolid", "Zamora", "Zaragoza",
]

PRECIO_MES = "29 €/mes"

CSS = """
*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
color:#1f2933;background:#f7f8fa;line-height:1.55}a{color:#1d4ed8}
.wrap{max-width:960px;margin:0 auto;padding:0 16px}
header{background:#14213d;color:#fff}header .wrap{display:flex;justify-content:space-between;align-items:center;padding:14px 16px}
header a{color:#fff;text-decoration:none;font-weight:700}
.hero{background:#14213d;color:#fff;padding:40px 0 56px}.hero h1{font-size:clamp(28px,5vw,44px);line-height:1.15;margin:0 0 12px}
.hero p{font-size:18px;color:#cfd8e3;max-width:640px}
.card{background:#fff;border:1px solid #e3e6ea;border-radius:12px;padding:20px;margin:0 0 16px}
.grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
form label{display:block;font-size:14px;font-weight:600;margin:10px 0 4px}
input,select{width:100%;padding:11px;border:1px solid #cbd2d9;border-radius:8px;font-size:16px}
button,.btn{display:inline-block;background:#f59e0b;color:#14213d;border:0;border-radius:8px;padding:13px 20px;
font-size:16px;font-weight:700;cursor:pointer;text-decoration:none;margin-top:14px}
.lic h3{margin:0 0 4px;font-size:17px}.meta{color:#5b6573;font-size:14px}
.precio{font-size:30px;font-weight:800;color:#14213d}.chk{display:flex;gap:8px;align-items:flex-start;font-weight:400}
.chk input{width:auto;margin-top:4px}footer{color:#7b8794;font-size:13px;padding:30px 0}
ul.links{columns:2;padding-left:18px}@media(max-width:600px){ul.links{columns:1}}
"""


def pagina(titulo, cuerpo, descripcion="", nivel=0):
    base = "../" * nivel
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(titulo)}</title><meta name="description" content="{escape(descripcion)}">
<link rel="stylesheet" href="{base}estilo.css"></head><body>
<header><div class="wrap"><a href="{base}index.html">{escape(comun.NOMBRE_SERVICIO)}</a>
<a href="{base}index.html#alta" style="font-weight:600">Apúntate gratis</a></div></header>
{cuerpo}
<footer><div class="wrap">{escape(comun.NOMBRE_SERVICIO)} · {escape(comun.TITULAR)} ·
<a href="{base}privacidad.html">Privacidad</a> · <a href="{base}aviso-legal.html">Aviso legal</a><br>
Datos de la Plataforma de Contratación del Sector Público (datos abiertos del Gobierno de España).</div></footer>
</body></html>"""


def formulario():
    opciones = "".join(f'<option value="{k}">{escape(v)}</option>'
                       for k, v in sorted(comun.SECTORES.items(), key=lambda x: x[1]))
    provs = '<option value="">Toda España</option>' + "".join(
        f'<option>{escape(p)}</option>' for p in PROVINCIAS)
    return f"""<div class="card" id="alta"><h2 style="margin-top:0">Apúntate gratis</h2>
<p>Cada lunes, las 3 licitaciones abiertas que mejor te encajan. Sin tarjeta.</p>
<form method="post" action="/alta">
<label>Tu email</label><input type="email" name="email" required autocomplete="email">
<label>Tu nombre o el de tu empresa</label><input name="nombre" maxlength="80">
<label>¿A qué te dedicas?</label><select name="sector" required>{opciones}</select>
<label>Palabras clave (opcional, separadas por comas)</label><input name="palabras" placeholder="limpieza, colegios, oficinas">
<label>¿Dónde trabajas?</label><select name="provincia">{provs}</select>
<label class="chk"><input type="checkbox" name="acepto" value="1" required>
<span>Acepto recibir los avisos por email y la <a href="privacidad.html">política de privacidad</a>. Me puedo dar de baja con un clic.</span></label>
<input type="text" name="web" style="display:none" tabindex="-1" autocomplete="off">
<button type="submit">Quiero recibir licitaciones</button></form></div>"""


def tarjeta(lic):
    an = comun.analisis_de(lic) or {}
    plazo = (lic.get("fin_plazo") or "no indicado")[:10]
    return f"""<div class="card lic"><h3>{escape(lic.get('objeto') or lic.get('titulo') or '')}</h3>
<div class="meta">{escape(lic.get('organo') or '')} · {escape(lic.get('provincia') or 'España')} ·
<b>{escape(comun.euros(lic.get('importe_sin_iva')))}</b> · plazo {escape(plazo[8:10] + '/' + plazo[5:7] + '/' + plazo[:4] if len(plazo) == 10 else plazo)}</div>
{f"<p>{escape(an['resumen'])}</p>" if an.get('resumen') else ''}
{f'<a href="{escape(lic["enlace"])}" rel="nofollow">Ver en la plataforma oficial</a>' if lic.get('enlace') else ''}</div>"""


def generar():
    web = comun.WEB
    if web.exists():
        shutil.rmtree(web)
    (web / "licitaciones").mkdir(parents=True)
    (web / "estilo.css").write_text(CSS, encoding="utf-8")

    lics = comun.abiertas(comun.licitaciones_recientes())
    por_sector = defaultdict(list)
    por_sector_prov = defaultdict(list)
    for l in lics:
        for div in sorted({c[:2] for c in l.get("cpv", []) if c[:2] in comun.SECTORES}):
            por_sector[div].append(l)
            if l.get("provincia"):
                por_sector_prov[(div, l["provincia"])].append(l)

    urls = ["index.html"]

    def escribir(ruta, html):
        (web / ruta).parent.mkdir(parents=True, exist_ok=True)
        (web / ruta).write_text(html, encoding="utf-8")
        urls.append(ruta)

    enlaces = []
    for div, lista in sorted(por_sector.items(), key=lambda x: -len(x[1])):
        nombre = comun.SECTORES[div]
        ruta = f"licitaciones/{comun.slug(nombre)}.html"
        provs = sorted({l['provincia'] for l in lista if l.get('provincia')})
        sub = "".join(
            f'<li><a href="{comun.slug(nombre)}/{comun.slug(p)}.html">{escape(p)}</a> '
            f'({len(por_sector_prov[(div, p)])})</li>' for p in provs)
        cuerpo = f"""<div class="wrap" style="padding-top:24px">
<h1>Licitaciones de {escape(nombre.lower())} abiertas hoy</h1>
<p>{len(lista)} contratos públicos en plazo. Total: <b>{escape(comun.euros(sum(l.get('importe_sin_iva') or 0 for l in lista)))}</b> sin IVA.</p>
{f'<div class="card"><b>Por provincia</b><ul class="links">{sub}</ul></div>' if sub else ''}
{''.join(tarjeta(l) for l in lista[:30])}
{formulario().replace('href="privacidad.html"', 'href="../privacidad.html"')}</div>"""
        escribir(ruta, pagina(f"Licitaciones de {nombre.lower()} — {len(lista)} abiertas",
                              cuerpo, f"Contratos públicos de {nombre.lower()} en plazo, actualizados cada día.", 1))
        enlaces.append(f'<li><a href="{ruta}">{escape(nombre)}</a> ({len(lista)})</li>')

    for (div, prov), lista in por_sector_prov.items():
        nombre = comun.SECTORES[div]
        ruta = f"licitaciones/{comun.slug(nombre)}/{comun.slug(prov)}.html"
        cuerpo = f"""<div class="wrap" style="padding-top:24px">
<h1>Licitaciones de {escape(nombre.lower())} en {escape(prov)}</h1>
<p>{len(lista)} contrato{'s' if len(lista) != 1 else ''} en plazo hoy. <a href="../{comun.slug(nombre)}.html">Ver toda España</a></p>
{''.join(tarjeta(l) for l in lista[:30])}
{formulario().replace('href="privacidad.html"', 'href="../../privacidad.html"')}</div>"""
        escribir(ruta, pagina(f"Licitaciones de {nombre.lower()} en {prov}", cuerpo,
                              f"Contratos públicos de {nombre.lower()} en {prov}, en plazo y actualizados cada día.", 2))

    total = comun.euros(sum(l.get("importe_sin_iva") or 0 for l in lics))
    pago = (f'<a class="btn" href="{escape(comun.ENLACE_PAGO)}">Empezar plan completo</a>'
            if comun.ENLACE_PAGO else '<p class="meta">Muy pronto.</p>')
    portada = f"""<section class="hero"><div class="wrap">
<h1>Contratos públicos para tu empresa, cada mañana en tu email</h1>
<p>Leemos cada día las licitaciones de toda España y te mandamos solo las que encajan contigo,
resumidas en un minuto: qué piden, cuánto pagan y qué requisitos hay.</p>
<p><b>Hoy hay {len(lics)} licitaci{'ón abierta' if len(lics) == 1 else 'ones abiertas'} por {escape(total)}.</b></p>
<a class="btn" href="#alta">Apúntate gratis</a></div></section>
<div class="wrap" style="padding-top:28px">
<div class="grid">
<div class="card"><h3>1. Nos dices a qué te dedicas</h3>Sector, palabras clave y provincias.</div>
<div class="card"><h3>2. Leemos los pliegos por ti</h3>Cada día, todas las administraciones.</div>
<div class="card"><h3>3. Te llega lo que encaja</h3>Resumido: importe, plazo, requisitos y dificultad.</div>
</div>
<h2 id="precios">Precios</h2>
<div class="grid">
<div class="card"><h3>Gratis</h3><div class="precio">0 €</div><p>3 licitaciones a la semana, cada lunes.</p><a class="btn" href="#alta">Apuntarme</a></div>
<div class="card"><h3>Completo</h3><div class="precio">{PRECIO_MES}</div><p>Todas las que encajan, cada mañana, con requisitos, criterios y dificultad. Sin permanencia.</p>{pago}</div>
</div>
{formulario()}
<div class="card"><h2 style="margin-top:0">Licitaciones abiertas por sector</h2><ul class="links">{''.join(enlaces) or '<li>Hoy no hay datos todavía.</li>'}</ul></div>
</div>"""
    (web / "index.html").write_text(pagina(f"{comun.NOMBRE_SERVICIO} — contratos públicos en tu email",
                                           portada, "Alertas diarias de licitaciones públicas resumidas para autónomos y pymes."),
                                    encoding="utf-8")

    for ruta, titulo, texto in (
        ("privacidad.html", "Política de privacidad", f"""<p><b>Responsable:</b> {escape(comun.TITULAR)}.</p>
<p><b>Qué datos guardamos:</b> tu email, el nombre que nos des y tus preferencias (sector, palabras, provincias).</p>
<p><b>Para qué:</b> solo para mandarte los avisos que pediste y, si eres de pago, para facturarte.</p>
<p><b>Base legal:</b> tu consentimiento al apuntarte (art. 6.1.a RGPD). Lo puedes retirar cuando quieras con el enlace de baja de cada email.</p>
<p><b>Cuánto tiempo:</b> mientras sigas suscrito. Al darte de baja se borran tus preferencias.</p>
<p><b>Con quién se comparten:</b> con nadie, salvo el proveedor de envío de email y el de pagos, que actúan como encargados del tratamiento.</p>
<p><b>Tus derechos:</b> acceso, rectificación, supresión, oposición y portabilidad escribiendo a {escape(comun.EMAIL_REMITENTE)}. Puedes reclamar ante la AEPD (aepd.es).</p>"""),
        ("aviso-legal.html", "Aviso legal", f"""<p><b>Titular:</b> {escape(comun.TITULAR)}. Contacto: {escape(comun.EMAIL_REMITENTE)}.</p>
<p>Los datos de licitaciones proceden de fuentes públicas oficiales. Los resúmenes se generan de forma automática y pueden contener errores:
antes de presentar una oferta, consulta siempre el pliego oficial.</p>"""),
    ):
        escribir(ruta, pagina(titulo, f'<div class="wrap" style="padding-top:24px"><h1>{titulo}</h1>'
                                      f'<p class="meta">PLANTILLA: revisa y completa los datos entre corchetes.</p>{texto}</div>'))

    (web / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {comun.URL_WEB}/sitemap.xml\n", encoding="utf-8")
    (web / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"<url><loc>{comun.URL_WEB}/{u}</loc><lastmod>{comun.hoy()}</lastmod></url>\n" for u in urls)
        + "</urlset>\n", encoding="utf-8")
    return len(urls)


def main():
    n = generar()
    print(f"Web generada: {n} páginas en {comun.WEB}")


if __name__ == "__main__":
    main()
