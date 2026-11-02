"""
Agente 1 — BUSCADOR

Busca en Google Maps negocios de un tipo y una ciudad de EE. UU., se queda con
los que tienen reseñas suficientes, mira cuáles de sus últimas reseñas siguen
SIN respuesta del dueño y saca un email de contacto de su web.

Fuentes:
  - Google Places API (oficial)        → negocio, web, nota y sus 5 últimas reseñas.
    Variable: GOOGLE_PLACES_KEY
  - SerpApi (opcional, de pago)        → si el dueño ha respondido o no a cada reseña
    Variable: SERPAPI_KEY              (Google Places no da las respuestas del dueño).
    Sin ella el sistema funciona, pero no sabe qué reseñas están sin contestar y el
    email no puede decir «tienes X sin responder».

Uso:
    python buscador.py --tipo dentist --ciudad "Austin, TX"
    python buscador.py --tipo "auto repair" --ciudad "Tampa, FL" --max 60
"""

import argparse
import html
import os
import re
import sys
import urllib.parse

import comun

MIN_RESENAS = int(os.environ.get("MIN_RESENAS", "20"))
MIN_SIN_RESPONDER = int(os.environ.get("MIN_SIN_RESPONDER", "2"))

CAMPOS = ",".join("places." + c for c in (
    "id", "displayName", "formattedAddress", "websiteUri", "rating", "userRatingCount",
    "reviews", "googleMapsUri", "businessStatus", "primaryTypeDisplayName")) + ",nextPageToken"

# Correos que salen en las webs pero no son del negocio.
EMAIL_BASURA = ("example.", "sentry", "wixpress", "domain.com", "email.com", "yourname",
                "godaddy", "squarespace", "@2x", ".png", ".jpg", ".gif", ".webp", "noreply",
                "no-reply", "privacy@", "abuse@", "webmaster@")
EMAIL_PREFERIDO = ("info@", "contact@", "office@", "hello@", "frontdesk@", "admin@", "team@")


# --------------------------------------------------------------------------
# Google Places
# --------------------------------------------------------------------------

def buscar_places(consulta, maximo):
    clave = os.environ["GOOGLE_PLACES_KEY"]
    sitios, token = [], None
    while len(sitios) < maximo:
        cuerpo = {"textQuery": consulta, "pageSize": 20, "languageCode": "en", "regionCode": "US"}
        if token:
            cuerpo["pageToken"] = token
        r = comun.http_json("https://places.googleapis.com/v1/places:searchText", cuerpo,
                            {"X-Goog-Api-Key": clave, "X-Goog-FieldMask": CAMPOS})
        sitios += r.get("places", [])
        token = r.get("nextPageToken")
        if not token:
            break
    return sitios[:maximo]


def resenas_places(sitio):
    salida = []
    for r in sitio.get("reviews", []):
        salida.append({
            "autor": (r.get("authorAttribution") or {}).get("displayName", ""),
            "nota": r.get("rating"),
            "texto": ((r.get("originalText") or r.get("text") or {}).get("text") or "").strip(),
            "fecha": r.get("publishTime", "")[:10],
            "respondida": None,          # Places no lo dice
        })
    return salida


# --------------------------------------------------------------------------
# SerpApi: reseñas con la respuesta del dueño (si la hay)
# --------------------------------------------------------------------------

def resenas_serpapi(place_id, n=10):
    q = urllib.parse.urlencode({"engine": "google_maps_reviews", "place_id": place_id,
                                "sort_by": "newestFirst", "hl": "en",
                                "api_key": os.environ["SERPAPI_KEY"]})
    r = comun.http_json(f"https://serpapi.com/search.json?{q}", timeout=60)
    salida = []
    for x in r.get("reviews", [])[:n]:
        salida.append({
            "autor": (x.get("user") or {}).get("name", ""),
            "nota": x.get("rating"),
            "texto": (x.get("extracted_snippet") or {}).get("original") or x.get("snippet") or "",
            "fecha": (x.get("iso_date") or "")[:10] or x.get("date", ""),
            "respondida": bool(x.get("response")),
        })
    return salida


# --------------------------------------------------------------------------
# Email de contacto en la web del negocio
# --------------------------------------------------------------------------

def _emails_en(texto):
    texto = html.unescape(texto)
    encontrados = set(comun.EMAIL_RE.findall(texto))
    encontrados |= {m for m in re.findall(r'mailto:([^"\'?>\s]+)', texto)}
    return {e.strip(".").lower() for e in encontrados
            if not any(b in e.lower() for b in EMAIL_BASURA) and len(e) < 80}


def buscar_email(web):
    if not web:
        return None
    partes = urllib.parse.urlparse(web)
    base = f"{partes.scheme or 'https'}://{partes.netloc}"
    dominio = partes.netloc.lower().removeprefix("www.")
    vistos = set()
    for ruta in ("", "/contact", "/contact-us", "/about"):
        try:
            pagina = comun.http(base + ruta, timeout=15, maximo=800_000).decode("utf-8", "replace")
        except Exception:
            continue
        vistos |= _emails_en(pagina)
        if vistos:
            break
    if not vistos:
        return None
    # mejor uno del propio dominio y genérico (info@, contact@…)
    def orden(e):
        return (not e.endswith("@" + dominio) and not e.endswith("." + dominio),
                not e.startswith(EMAIL_PREFERIDO), e)
    return sorted(vistos, key=orden)[0]


# --------------------------------------------------------------------------

def evaluar(sitio, usar_serpapi):
    """Devuelve (prospecto, motivo_descarte)."""
    nombre = (sitio.get("displayName") or {}).get("text", "")
    if sitio.get("businessStatus") not in (None, "OPERATIONAL"):
        return None, "cerrado"
    if (sitio.get("userRatingCount") or 0) < MIN_RESENAS:
        return None, "pocas reseñas"
    if not sitio.get("websiteUri"):
        return None, "sin web"

    resenas = resenas_places(sitio)
    if usar_serpapi:
        try:
            resenas = resenas_serpapi(sitio["id"]) or resenas
        except Exception as e:
            print(f"    SerpApi falló en {nombre}: {e}", file=sys.stderr)
    conocidas = [r for r in resenas if r["respondida"] is not None]
    sin_responder = [r for r in resenas if r["respondida"] is False and r["texto"]]
    if conocidas and len(sin_responder) < MIN_SIN_RESPONDER:
        return None, "ya responde sus reseñas"

    email = buscar_email(sitio["websiteUri"])
    if not email:
        return None, "sin email en la web"
    if comun.esta_suprimido(email):
        return None, "en la lista de supresión"

    return {
        "id": sitio["id"],
        "nombre": nombre,
        "tipo": (sitio.get("primaryTypeDisplayName") or {}).get("text", ""),
        "direccion": sitio.get("formattedAddress", ""),
        "web": sitio["websiteUri"],
        "maps": sitio.get("googleMapsUri", ""),
        "nota": sitio.get("rating"),
        "num_resenas": sitio.get("userRatingCount"),
        "email": email,
        "resenas": resenas,
        "sin_responder_conocido": bool(conocidas),
        "sin_responder": len(sin_responder),
        "encontrado": comun.ahora(),
        "estado": "nuevo",
    }, None


def buscar(tipo, ciudad, maximo=40):
    usar_serpapi = bool(os.environ.get("SERPAPI_KEY"))
    sitios = buscar_places(f"{tipo} in {ciudad}", maximo)
    prospectos = comun.cargar_prospectos()
    nuevos, motivos = 0, {}
    for s in sitios:
        if s["id"] in prospectos:
            motivos["ya visto"] = motivos.get("ya visto", 0) + 1
            continue
        p, motivo = evaluar(s, usar_serpapi)
        if p:
            p["busqueda"] = f"{tipo} | {ciudad}"
            prospectos[p["id"]] = p
            nuevos += 1
        else:
            motivos[motivo] = motivos.get(motivo, 0) + 1
    comun.guardar_prospectos(prospectos)
    return len(sitios), nuevos, motivos, usar_serpapi


def main():
    a = argparse.ArgumentParser(description="Busca negocios con reseñas sin contestar.")
    a.add_argument("--tipo", required=True, help='tipo de negocio en inglés, p. ej. "dentist"')
    a.add_argument("--ciudad", required=True, help='p. ej. "Austin, TX"')
    a.add_argument("--max", type=int, default=40)
    x = a.parse_args()
    total, nuevos, motivos, serp = buscar(x.tipo, x.ciudad, x.max)
    print(f"Revisados {total} negocios: {nuevos} prospectos nuevos.")
    for m, n in sorted(motivos.items(), key=lambda i: -i[1]):
        print(f"  descartados por {m}: {n}")
    if not serp:
        print("  (sin SERPAPI_KEY: no se sabe qué reseñas están sin responder)")


if __name__ == "__main__":
    main()
