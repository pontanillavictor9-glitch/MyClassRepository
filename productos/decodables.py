"""
Producto: lecturas descodificables («decodable passages») para 1.º, método
Science of Reading. Un niño que acaba de aprender un patrón (aquí la «e muda»,
CVCe: cake, bike, home, cute) solo debe encontrar palabras que puede leer:
  - sílabas cerradas cortas (cat, ship, jump), ya aprendidas antes,
  - el patrón nuevo (CVCe),
  - y unas pocas palabras de uso frecuente que se enseñan aparte («heart words»).

El programa COMPRUEBA cada palabra de cada cuento con esas reglas. Si una no
encaja, el Revisor lo para.
"""

import re
from html import escape

import comun

COLORES = dict(acento="#6c63ff", titulo="#2b2d63", suave="#e6e4ff")

VOCALES = "aeiou"
# consonantes y grupos que un niño de 1.º ya lee en sílabas cerradas
INICIO = r"(?:sh|ch|th|wh|[bcdfghjklmnpqrstvwxyz]|bl|cl|fl|gl|pl|sl|br|cr|dr|fr|gr|pr|tr|sc|sk|sm|sn|sp|st|sw|tw|spl|spr|str|scr|shr|thr|qu)?"
FINAL_CERRADA = r"(?:ck|ng|nk|sh|ch|tch|th|ff|ll|ss|zz|[bdfgklmnprstvxz]|st|sk|sp|nd|nt|mp|ft|lt|lk|lp|ld|pt|ct|xt)"
CERRADA = re.compile(rf"^{INICIO}[{VOCALES}]{FINAL_CERRADA}(?:s|es)?$")
CVCE = re.compile(rf"^{INICIO}[aeiou][bcdfgklmnprstvz]e(?:s)?$")
# compuestas de dos sílabas cerradas o CVCe (sunset, cupcake, inside…)
def _compuesta(p):
    return any(_simple(p[:i]) and _simple(p[i:]) for i in range(2, len(p) - 1))

HEART = {"a", "the", "to", "is", "was", "said", "of", "i", "he", "she", "we", "me", "be", "my",
         "you", "are", "has", "his", "as", "do", "no", "go", "so", "they", "her", "for", "what",
         "put", "come", "some", "one", "look", "into", "all", "too", "by"}


def _simple(p):
    return bool(CERRADA.match(p) or CVCE.match(p)) or p in {"i", "a"}


def es_descodificable(palabra):
    p = palabra.lower().strip("'")
    if p.endswith("'s"):
        p = p[:-2]
    return p in HEART or _simple(p) or _compuesta(p)


def palabras(texto):
    return re.findall(r"[A-Za-z']+", texto)


def no_descodificables(texto):
    return sorted({w for w in palabras(texto) if not es_descodificable(w)}, key=str.lower)


# Parecen CVCe pero NO tienen vocal larga: no se enseñan como «e muda».
EXCEPCIONES_E = {"come", "some", "have", "give", "live", "love", "done", "gone", "none", "were",
                 "move", "lose", "whose", "dove", "glove", "shove", "above"}


def es_cvce(palabra):
    p = palabra.lower()
    return bool(CVCE.match(p)) and p not in HEART and p not in EXCEPCIONES_E


def palabras_e(texto):
    """Palabras con e muda, con mayúscula si son nombres propios."""
    todas = palabras(texto)
    minusculas = {w for w in todas if w.islower()}
    salida = {}
    for w in todas:
        if es_cvce(w):
            salida[w.lower()] = w.lower() if w.lower() in minusculas else w
    return [salida[k] for k in sorted(salida)]


CSS = """
.cuento p{font-size:20pt;line-height:2.05;margin:0 0 6px}
.palabras{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 10px}
.palabras span{background:var(--suave);border-radius:10px;padding:4px 12px;font-family:Fredoka;font-size:15pt;color:var(--titulo)}
.preg{font-size:16pt;margin:18px 0 6px}.renglon{border-bottom:1.5px solid #94a3b8;height:56px}
.portada{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;height:100%}
.portada h1{font-size:42pt}.grande{font-family:Fredoka;font-weight:600;font-size:88pt;color:var(--acento);line-height:1}
.grande u{text-decoration:none;color:#f4a259}
ul.lista{font-size:12pt;line-height:1.7}
.lee{display:flex;gap:10px;margin-top:6px}.lee span{border:2px solid var(--acento);border-radius:50%;width:34px;height:34px;display:inline-block}
.sol{font-size:11.5pt;margin-bottom:10px}
.hoja{display:flex;flex-direction:column}.hoja>.etiqueta{align-self:flex-start}
.dibujo{flex:1;margin:16px 0 .45in;border:2.5px dashed var(--acento);border-radius:18px;padding:10px 14px;font-size:11pt;color:#64748b}
.preg{margin-top:26px}
"""


def heart_usadas(c):
    t = " ".join(" ".join(cu["texto"]) + " " + cu["titulo"] for cu in c["cuentos"])
    return sorted({w.lower() for w in palabras(t) if w.lower() in HEART})


def html(c):
    hojas, pag = [], 1
    hojas.append(comun.hoja(f"""<div class="portada"><span class="etiqueta">Grade 1 · Science of Reading · Silent e (CVCe)</span>
<div class="grande" style="margin-top:20px">cak<u>e</u> · bik<u>e</u></div>
<h1>Silent e Decodable Passages</h1>
<p class="sub" style="font-size:14pt">{len(c['cuentos'])} decodable stories · Word lists · Comprehension · Word work · Answer key</p>
<p style="font-family:Fredoka;font-size:15pt;color:#64748b;margin-top:30px">{comun.MARCA}</p></div>""", pag)); pag += 1
    hojas.append(comun.hoja(f"""<h1>Teacher Guide</h1><p class="sub">Every word in these stories is checked by our decodability checker.</p>
<h2>What students can read</h2><ul class="lista">
<li><b>Silent e words (CVCe):</b> a_e, i_e, o_e, u_e (cake, bike, home, cute).</li>
<li><b>Closed syllables</b> with short vowels, digraphs (sh, ch, th, ck) and blends (st, fl, gr…).</li>
<li><b>Heart words</b> (taught separately): {", ".join(heart_usadas(c))}.</li></ul>
<h2>Suggested routine (15 minutes)</h2><ul class="lista">
<li>Warm up: read the word list at the top of the page.</li>
<li>Read the story three times (whisper, with a partner, to the teacher). Students color a circle each time.</li>
<li>Answer the questions, then find and highlight every silent e word.</li></ul>
<h2>Standards</h2><p style="font-size:12pt">CCSS RF.1.3c (final -e conventions for long vowel sounds), RF.1.4 (read with accuracy and fluency).</p>""", pag)); pag += 1

    for cu in c["cuentos"]:
        texto = " ".join(cu["texto"])
        cvce = palabras_e(texto)
        lista = "".join(f"<span>{escape(w)}</span>" for w in cvce[:10])
        parrafos = "".join(f"<p>{escape(t)}</p>" for t in cu["texto"])
        hojas.append(comun.hoja(f"""{comun.cabecera_alumno()}<span class="etiqueta">Silent e · {escape(cu['patron'])}</span>
<h1>{escape(cu['titulo'])}</h1><div class="palabras">{lista}</div><div class="cuento">{parrafos}</div>
<div style="font-size:11pt;margin-top:8px">I read it: <div class="lee" style="display:inline-flex"><span></span><span></span><span></span></div></div>
<div class="dibujo">Draw a picture of the story.</div>""", pag)); pag += 1
        preguntas = "".join(f'<div class="preg">{i}. {escape(q["pregunta"])}</div><div class="renglon"></div><div class="renglon"></div>'
                            for i, q in enumerate(cu["preguntas"], 1))
        hojas.append(comun.hoja(f"""{comun.cabecera_alumno()}<h1>{escape(cu['titulo'])}</h1>{preguntas}
<div class="preg" style="margin-top:26px"><b>Word work:</b> Go back to the story. Find and write 4 silent e words.</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:0 30px"><div class="renglon"></div><div class="renglon"></div>
<div class="renglon"></div><div class="renglon"></div></div>""", pag)); pag += 1

    sol = []
    for cu in c["cuentos"]:
        texto = " ".join(cu["texto"])
        cvce = palabras_e(texto)
        r = "<br>".join(f"{i}. <span class='solucion'>{escape(q['respuesta'])}</span>" for i, q in enumerate(cu["preguntas"], 1))
        sol.append(f"<div class='sol'><h2 style='font-size:13pt;margin:0'>{escape(cu['titulo'])}</h2>{r}<br>"
                   f"Silent e words: <span class='solucion'>{escape(', '.join(cvce))}</span></div>")
    hojas.append(comun.hoja(f"<h1>Answer Key</h1>{''.join(sol)}", pag))
    return comun.documento(hojas, extra_css=CSS, **COLORES)
