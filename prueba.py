"""
Prueba de punta a punta SIN internet ni cuentas: sustituye Google, SerpApi, las
webs y la IA por respuestas falsas (negocios inventados) y comprueba que cada
agente hace lo que debe. Uso:  python prueba.py
"""

import json
import os
import tempfile
import types
from pathlib import Path

os.environ["DATOS_DIR"] = tempfile.mkdtemp(prefix="resenas_prueba_")
os.environ["GOOGLE_PLACES_KEY"] = os.environ["SERPAPI_KEY"] = "falsa"
os.environ["DIRECCION_POSTAL"] = "Calle Falsa 123, 28000 Madrid, Spain"

import comun, buscador, redactor, cartero, atencion  # noqa: E402

def sitio(i, nombre, resenas, web=True, n=80):
    return {"id": f"P{i}", "displayName": {"text": nombre}, "formattedAddress": "1 Main St, Austin, TX",
            "websiteUri": f"https://negocio{i}.example-falso.com" if web else None, "rating": 4.4,
            "userRatingCount": n, "businessStatus": "OPERATIONAL", "googleMapsUri": "https://maps",
            "primaryTypeDisplayName": {"text": "Dentist"},
            "reviews": [{"authorAttribution": {"displayName": f"Autor {k}"}, "rating": 5,
                         "text": {"text": f"Great visit number {k}"}, "publishTime": "2026-10-2%dT00:00:00Z" % k}
                        for k in range(resenas)]}

SITIOS = [sitio(1, "Smile Dental (falso)", 5), sitio(2, "Ya Responde Dental (falso)", 5),
          sitio(3, "Sin Web Dental (falso)", 5, web=False), sitio(4, "Poquitas (falso)", 5, n=3),
          sitio(5, "Sin Email Dental (falso)", 5)]
RESPONDIDAS = {"P1": [False, False, True], "P2": [True, True, True], "P5": [False, False, False]}

def http_falso(url, datos=None, cabeceras=None, timeout=30, maximo=0):
    if "serpapi" in url:
        pid = url.split("place_id=")[1].split("&")[0]
        return json.dumps({"reviews": [{"user": {"name": f"Autor {k}"}, "rating": 4 if k else 2,
                           "snippet": "Long wait but nice staff" if not k else f"Good {k}",
                           "iso_date": "2026-10-20", **({"response": {"snippet": "Thanks"}} if r else {})}
                           for k, r in enumerate(RESPONDIDAS.get(pid, []))]}).encode()
    if "places.googleapis" in url:
        return json.dumps({"places": SITIOS}).encode()
    if "negocio1." in url:
        return b'<a href="mailto:info@negocio1.example-falso.com">Mail</a> <img src="logo@2x.png">'
    if "negocio2." in url:
        return b'contact@negocio2.example-falso.com'
    return b"<html>sin email</html>"

comun.http = http_falso
comun.http_json = lambda *a, **k: json.loads(http_falso(*a, **k))

class Bloque:
    type = "text"
    def __init__(self, t): self.text = t

def ia_falsa(json_salida):
    crear = lambda **kw: types.SimpleNamespace(stop_reason="end_turn", content=[Bloque(json.dumps(json_salida))])
    m = types.SimpleNamespace(create=crear)
    return types.SimpleNamespace(messages=m, beta=types.SimpleNamespace(messages=m))

def comprobar(cond, texto):
    print(("  OK   " if cond else "  FALLO ") + texto)
    if not cond:
        raise SystemExit(1)

print("1. Buscador")
total, nuevos, motivos, _ = buscador.buscar("dentist", "Austin, TX")
comprobar(nuevos == 1, f"1 prospecto válido de {total} (descartes: {motivos})")
p = comun.cargar_prospectos()["P1"]
comprobar(p["email"] == "info@negocio1.example-falso.com", "email bueno, sin coger 'logo@2x.png'")
comprobar(p["sin_responder"] == 2 and p["sin_responder_conocido"], "sabe que hay 2 sin responder")

print("2. Redactor")
borrador = {"respuestas": [{"autor": "Autor 0", "respuesta": "Thank you, we're sorry about the wait."},
                           {"autor": "Autor 1", "respuesta": "Thanks so much!"}],
            "asunto": "2 unanswered reviews at Smile Dental", "cuerpo": "Hi there,\n\n{{RESPUESTAS}}\n\nWorth a try?",
            "seguimiento": "Just checking in."}
pr = comun.cargar_prospectos()
pr["P1"]["borrador"] = redactor.redactar(pr["P1"], ia_falsa(borrador))
pr["P1"]["estado"] = "listo"
comun.guardar_prospectos(pr)
comprobar(pr["P1"]["borrador"]["asunto"].startswith("2 unanswered"), "borrador guardado")

print("3. Cartero (modo revisión)")
hechos = cartero.repartir(de_verdad=False)
comprobar(hechos == [("Smile Dental (falso)", "primero")], "prepara el primer email")
eml = next((comun.BUZON_SALIDA).rglob("*.eml")).read_text()
comprobar("Calle Falsa 123" in eml and "no thanks" in eml and "List-Unsubscribe" in eml,
          "lleva dirección postal, baja y cabecera List-Unsubscribe")
comprobar("Thanks so much!" in eml and "{{RESPUESTAS}}" not in eml, "las respuestas van dentro")
comprobar(comun.cargar_prospectos()["P1"]["estado"] == "listo", "en modo revisión no lo marca como enviado")

print("4. Seguimiento a los 4 días")
pr = comun.cargar_prospectos()
pr["P1"].update(estado="enviado", enviado="2026-01-01T10:00:00", message_id="<x@y>")
comun.guardar_prospectos(pr)
cola = cartero.pendientes(comun.cargar_prospectos())
comprobar([(c[0]["id"], c[1]) for c in cola] == [("P1", "seguimiento")], "toca el seguimiento")

print("5. Atención")
interesado = b"From: Ana <info@negocio1.example-falso.com>\nSubject: Re: hi\n\nSounds good, how do we start?\n\nOn Mon, X wrote:\n> old"
autom = b"From: info@negocio2.example-falso.com\nSubject: Out of Office\n\nI am away."
baja = b"From: otro@negocio9.example-falso.com\nSubject: Re: hi\n\nPlease remove me. Not interested."
para_ti = atencion.procesar([interesado, autom, baja])
comprobar(len(para_ti) == 1 and para_ti[0]["negocio"] == "Smile Dental (falso)", "solo te avisa del interesado")
comprobar(comun.cargar_prospectos()["P1"]["estado"] == "respondio", "para el seguimiento del que contestó")
comprobar(comun.esta_suprimido("otro@negocio9.example-falso.com"), "el que pide baja va a la supresión")
comprobar(cartero.pendientes(comun.cargar_prospectos()) == [], "ya no hay nada que mandar")
aviso = atencion.avisar(para_ti)
comprobar(aviso and "how do we start" in Path(aviso).read_text(), "te deja el aviso con lo que dijo")

print("\nTodo bien. Datos de la prueba en", os.environ["DATOS_DIR"])
