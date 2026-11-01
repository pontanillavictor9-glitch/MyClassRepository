"""
Agente 2 — ANALISTA

Para cada licitación abierta, baja su pliego (PDF) y le pide a la IA un resumen
de un minuto: qué se pide, cuánto se paga, requisitos para presentarse, cómo se
puntúa y a qué tipo de empresa le encaja. El resultado se guarda en
datos/analisis/<clave>.json y no se vuelve a pagar por la misma licitación.

Sin clave de IA (ANTHROPIC_API_KEY) hace un resumen básico con los datos del
anuncio, para que todo lo demás funcione igual.

Uso:
    python analista.py                # analiza las abiertas de los últimos 7 días
    python analista.py --max 20       # como mucho 20 (para controlar el gasto)
    python analista.py --sin-ia       # forzar el resumen básico
"""

import argparse
import base64
import json
import os
import sys
import urllib.request

import comun

# Modelo de IA. Se puede cambiar con la variable MODELO_IA (por ejemplo a
# claude-haiku-5-5, mucho más barato, si la calidad de los resúmenes aguanta).
MODELO = os.environ.get("MODELO_IA", "claude-opus-5-5")
MAX_PDF_BYTES = 20 * 1024 * 1024

ESQUEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["resumen", "que_piden", "requisitos", "criterios", "para_quien",
                 "dificultad", "alertas"],
    "properties": {
        "resumen": {"type": "string", "description": "2-3 frases claras para un autónomo o pyme"},
        "que_piden": {"type": "string"},
        "requisitos": {"type": "array", "items": {"type": "string"},
                       "description": "solvencia económica/técnica, clasificación, certificados"},
        "criterios": {"type": "array", "items": {"type": "string"},
                      "description": "cómo se puntúa: precio, mejoras, memoria técnica…"},
        "para_quien": {"type": "string", "description": "tipo y tamaño de empresa a la que encaja"},
        "dificultad": {"type": "string", "enum": ["baja", "media", "alta"]},
        "alertas": {"type": "array", "items": {"type": "string"},
                    "description": "trampas o plazos a vigilar"},
    },
}

INSTRUCCIONES = """Eres analista de contratación pública en España. Resumes \
licitaciones para autónomos y pequeñas empresas que no tienen tiempo de leerse \
un pliego. Escribe en español, frases cortas, sin jerga innecesaria. Usa solo \
lo que dice el documento y el anuncio; si algo no aparece, dilo («no se indica») \
en vez de suponerlo."""


def resumen_basico(lic):
    """Resumen sin IA, a partir de los datos estructurados del anuncio."""
    return {
        "resumen": f"{lic.get('organo') or 'Un organismo público'} busca empresa para: "
                   f"{lic.get('objeto') or lic.get('titulo')}. "
                   f"Presupuesto: {comun.euros(lic.get('importe_sin_iva'))} sin IVA.",
        "que_piden": lic.get("objeto") or lic.get("titulo") or "",
        "requisitos": ["Consultar el pliego administrativo"],
        "criterios": ["Consultar el pliego"],
        "para_quien": ", ".join(comun.SECTORES.get(c[:2], c[:2]) for c in lic.get("cpv", [])[:3])
                      or "No se indica",
        "dificultad": "media",
        "alertas": [],
        "con_ia": False,
    }


def _bajar_pdf(url):
    req = urllib.request.Request(url, headers={"User-Agent": "alertas-licitaciones/0.1"})
    with urllib.request.urlopen(req, timeout=120) as r:
        datos = r.read(MAX_PDF_BYTES + 1)
    if len(datos) > MAX_PDF_BYTES or not datos.startswith(b"%PDF"):
        return None
    return datos


def _pliegos(lic, maximo=2):
    """Primero el pliego administrativo (requisitos) y luego el técnico."""
    orden = {"Legal": 0, "Technical": 1}
    docs = sorted(lic.get("documentos", []), key=lambda d: orden.get(d["tipo"], 2))
    pdfs = []
    for d in docs:
        if len(pdfs) >= maximo:
            break
        try:
            pdf = _bajar_pdf(d["url"])
        except Exception as e:  # un pliego roto no debe parar el día
            print(f"    no se pudo bajar {d['url']}: {e}", file=sys.stderr)
            continue
        if pdf:
            pdfs.append(pdf)
    return pdfs


def resumen_ia(lic, cliente):
    contenido = []
    for pdf in _pliegos(lic):
        contenido.append({"type": "document", "source": {
            "type": "base64", "media_type": "application/pdf",
            "data": base64.standard_b64encode(pdf).decode()}})
    anuncio = {k: lic.get(k) for k in ("organo", "objeto", "tipo", "importe_sin_iva",
                                         "valor_estimado", "provincia", "fin_plazo", "cpv")}
    contenido.append({"type": "text", "text":
                      "Datos del anuncio:\n" + json.dumps(anuncio, ensure_ascii=False) +
                      ("\n\nResume la licitación usando también los pliegos adjuntos."
                       if len(contenido) else
                       "\n\nNo hay pliego disponible: resume solo con el anuncio.")})

    peticion = dict(
        model=MODELO,
        max_tokens=4000,
        system=INSTRUCCIONES,
        output_config={"effort": "low",
                       "format": {"type": "json_schema", "schema": ESQUEMA}},
        messages=[{"role": "user", "content": contenido}],
    )
    # Si el modelo rechaza una petición, que la repita otro modelo en vez de perderla.
    if MODELO.startswith(("claude-opus-5", "claude-fable-5-1", "claude-sonnet-5-5")):
        r = cliente.beta.messages.create(betas=["server-side-fallback-2026-07-01"],
                                         fallbacks="default", **peticion)
    else:
        r = cliente.messages.create(**peticion)

    if r.stop_reason == "refusal":
        return None
    texto = next((b.text for b in r.content if b.type == "text"), "")
    datos = json.loads(texto)
    datos["con_ia"] = True
    datos["pliegos_leidos"] = sum(1 for c in contenido if c["type"] == "document")
    return datos


def main():
    p = argparse.ArgumentParser(description="Resume las licitaciones abiertas.")
    p.add_argument("--max", type=int, default=50, help="máximo de análisis con IA por pasada")
    p.add_argument("--sin-ia", action="store_true")
    p.add_argument("--dias", type=int, default=7)
    a = p.parse_args()

    cliente = None
    if not a.sin_ia and os.environ.get("ANTHROPIC_API_KEY"):
        try:
            import anthropic
            cliente = anthropic.Anthropic()
        except ImportError:
            print("Falta la librería: pip install anthropic  (sigo sin IA)", file=sys.stderr)
    if cliente is None:
        print("Sin IA: resúmenes básicos con los datos del anuncio.", file=sys.stderr)

    comun.ANALISIS.mkdir(parents=True, exist_ok=True)
    pendientes = [l for l in comun.abiertas(comun.licitaciones_recientes(a.dias))
                  if comun.analisis_de(l) is None
                  or (cliente and not comun.analisis_de(l).get("con_ia"))]
    hechos_ia = 0
    for lic in pendientes:
        datos = None
        if cliente and hechos_ia < a.max:
            try:
                datos = resumen_ia(lic, cliente)
                hechos_ia += 1
            except Exception as e:
                print(f"  IA falló en {lic.get('expediente')}: {e}", file=sys.stderr)
        datos = datos or resumen_basico(lic)
        (comun.ANALISIS / f"{comun.clave(lic)}.json").write_text(
            json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Analizadas {len(pendientes)} licitaciones ({hechos_ia} con IA).")


if __name__ == "__main__":
    main()
