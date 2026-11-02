"""
Agente REVISOR. Nada sale a la tienda sin pasar por aquí.

Comprueba el PDF FINAL (lo que recibirá el comprador), no solo los datos:
  - todas las páginas en tamaño Letter (EE. UU.) y con las fuentes incrustadas;
  - ninguna página sin el pie de licencia, ni restos de plantilla ({{, None, nan…);
  - matemáticas: relee del PDF cada «a × b = c» de las soluciones y recalcula;
  - lectura: nivel de lectura (Flesch-Kincaid) dentro del curso, 4 opciones por
    pregunta, respuesta válida, y que cada solución aparece en el PDF;
  - descodificables: cada palabra de cada cuento cumple las reglas.

Con ANTHROPIC_API_KEY hace además una lectura con IA buscando errores de
ortografía, datos falsos o algo inadecuado para niños.

Devuelve una lista de fallos (vacía = aprobado) y una lista de avisos.
"""

import re
import unicodedata

import pypdf

import comun

PALABRAS_PROHIBIDAS = ("{{", "}}", "None", "undefined", "NaN", "lorem", "TODO", "[object")


def _texto_paginas(ruta):
    r = pypdf.PdfReader(str(ruta))
    # NFKC deshace las ligaduras tipográficas (ﬁ → fi) que mete el PDF
    return r, [unicodedata.normalize("NFKC", p.extract_text() or "") for p in r.pages]


def comunes(ruta, fallos, avisos):
    r, textos = _texto_paginas(ruta)
    for i, p in enumerate(r.pages, 1):
        w, h = float(p.mediabox.width), float(p.mediabox.height)
        if (round(w), round(h)) != (612, 792):
            fallos.append(f"Página {i}: tamaño {w}x{h}, no es Letter (612x792).")
        fuentes = (p.get("/Resources") or {}).get("/Font") or {}
        for f in fuentes.values():
            f = f.get_object()
            if f.get("/Subtype") == "/Type3":
                continue                      # Type3: los dibujos van dentro del propio PDF
            desc = f.get("/FontDescriptor")
            if f.get("/Subtype") == "/Type0":
                desc = f["/DescendantFonts"][0].get_object().get("/FontDescriptor")
            desc = desc.get_object() if desc else {}
            if not any(k in desc for k in ("/FontFile", "/FontFile2", "/FontFile3")):
                fallos.append(f"Página {i}: la fuente {f.get('/BaseFont')} no va incrustada.")
    for i, t in enumerate(textos, 1):
        if "For use in one classroom" not in t.replace("\n", " "):
            fallos.append(f"Página {i}: falta el pie de licencia.")
        for mala in PALABRAS_PROHIBIDAS:
            if mala in t:
                fallos.append(f"Página {i}: aparece «{mala}» (resto de plantilla).")
    if len(textos) < 5:
        avisos.append(f"Solo {len(textos)} páginas: poco contenido para venderlo.")
    return textos


# --------------------------------------------------------------------------

def matematicas(textos, problemas, fallos):
    clave = " ".join(t for t in textos if "Answer Key" in t)
    encontradas = re.findall(r"(\d+)\s*×\s*(\d+)\s*=\s*(\d+)", clave)
    esperadas = sum(len(ops) for _, ops in problemas)
    if len(encontradas) != esperadas:
        fallos.append(f"Soluciones: hay {len(encontradas)} en el PDF y deberían ser {esperadas}.")
    malas = [f"{a}×{b}={c}" for a, b, c in encontradas if int(a) * int(b) != int(c)]
    if malas:
        fallos.append(f"Soluciones MAL: {malas[:10]}")
    return len(encontradas)


# --------------------------------------------------------------------------
# Nivel de lectura: Flesch-Kincaid (curso escolar de EE. UU.)
# --------------------------------------------------------------------------

def _silabas(palabra):
    p = re.sub(r"[^a-z]", "", palabra.lower())
    if not p:
        return 0
    if len(p) <= 3:
        return 1
    p = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", p)
    p = re.sub(r"^y", "", p)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", p)))


def flesch_kincaid(texto):
    frases = max(1, len(re.findall(r"[.!?]+", texto)))
    palabras = re.findall(r"[A-Za-z']+", texto)
    if not palabras:
        return 0.0
    sil = sum(_silabas(w) for w in palabras)
    return round(0.39 * len(palabras) / frases + 11.8 * sil / len(palabras) - 15.59, 1)


def lectura(textos, contenido, fallos, avisos):
    todo = re.sub(r"\s+", " ", " ".join(textos))
    lo, hi = contenido.get("nivel_fk", [0, 99])
    niveles = {}
    for l in contenido["lecturas"]:
        fk = flesch_kincaid(" ".join(l["texto"]))
        niveles[l["titulo"]] = fk
        if not lo <= fk <= hi:
            fallos.append(f"«{l['titulo']}»: nivel de lectura {fk}, fuera de {lo}-{hi}.")
        for i, q in enumerate(l["preguntas"], 1):
            if q["tipo"] == "escrita":
                if not q.get("ejemplo"):
                    fallos.append(f"«{l['titulo']}» pregunta {i}: falta respuesta de ejemplo.")
                continue
            if len(q.get("opciones", [])) != 4:
                fallos.append(f"«{l['titulo']}» pregunta {i}: no tiene 4 opciones.")
            if not 0 <= q.get("correcta", -1) < len(q.get("opciones", [])):
                fallos.append(f"«{l['titulo']}» pregunta {i}: la respuesta correcta no es válida.")
                continue
            if len(set(q["opciones"])) != len(q["opciones"]):
                fallos.append(f"«{l['titulo']}» pregunta {i}: opciones repetidas.")
            correcta = re.sub(r"\s+", " ", q["opciones"][q["correcta"]])
            if correcta not in todo:
                fallos.append(f"«{l['titulo']}» pregunta {i}: la solución no aparece en el PDF.")
    return niveles


def decodables(contenido, fallos, avisos):
    from productos import decodables as d
    for cu in contenido["cuentos"]:
        malas = d.no_descodificables(" ".join(cu["texto"]) + " " + cu["titulo"])
        if malas:
            fallos.append(f"«{cu['titulo']}»: palabras NO descodificables: {', '.join(malas)}")
        n = len(d.palabras_e(" ".join(cu["texto"])))
        if n < 4:
            avisos.append(f"«{cu['titulo']}»: solo {n} palabras con e muda.")
        if not cu.get("preguntas") or any(not q.get("respuesta") for q in cu["preguntas"]):
            fallos.append(f"«{cu['titulo']}»: faltan preguntas o respuestas.")


# --------------------------------------------------------------------------
# Revisión con IA (opcional): una segunda lectura humana-like del texto final.
# --------------------------------------------------------------------------

ESQUEMA_IA = {
    "type": "object", "additionalProperties": False, "required": ["problemas"],
    "properties": {"problemas": {"type": "array", "items": {
        "type": "object", "additionalProperties": False, "required": ["gravedad", "pagina", "descripcion"],
        "properties": {"gravedad": {"type": "string", "enum": ["grave", "leve"]},
                       "pagina": {"type": "integer"}, "descripcion": {"type": "string"}}}}},
}


def con_ia(textos, fallos, avisos):
    import json
    import os
    if not os.environ.get("ANTHROPIC_API_KEY"):
        avisos.append("Sin ANTHROPIC_API_KEY: no se ha hecho la revisión con IA (ortografía y datos).")
        return
    import anthropic
    paginas = "\n\n".join(f"--- PAGE {i} ---\n{t}" for i, t in enumerate(textos, 1))
    r = anthropic.Anthropic().messages.create(
        model=os.environ.get("MODELO_IA", "claude-opus-5-5"), max_tokens=8000,
        system=("You are a meticulous US elementary school teacher reviewing a printable resource "
                "before it is sold. Report only real problems: spelling or grammar mistakes, factual "
                "errors, wrong answers in the answer key, content above or below the stated grade, "
                "anything inappropriate for children, or confusing instructions. Text was extracted "
                "from a PDF, so ignore spacing and line-break artifacts."),
        output_config={"effort": "high", "format": {"type": "json_schema", "schema": ESQUEMA_IA}},
        messages=[{"role": "user", "content": paginas}])
    if r.stop_reason != "end_turn":
        avisos.append(f"La revisión con IA no terminó ({r.stop_reason}).")
        return
    for p in json.loads(next(b.text for b in r.content if b.type == "text"))["problemas"]:
        (fallos if p["gravedad"] == "grave" else avisos).append(f"IA, página {p['pagina']}: {p['descripcion']}")
