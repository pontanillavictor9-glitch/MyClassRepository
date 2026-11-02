"""
Producto de comprensión lectora a partir de un contenido en JSON
(contenido/<id>.json): lecturas con sus preguntas y las respuestas.

Para cada lectura: una hoja con el texto (párrafos numerados) y otra con las
preguntas (3 de opción múltiple, 1 de vocabulario y 1 escrita). Al final, las
soluciones. El Revisor comprueba el nivel de lectura y que cada pregunta tiene
su respuesta.
"""

from html import escape

import comun

COLORES = dict(acento="#e07a2f", titulo="#5b2a12", suave="#fbe3cf")

CSS = """
.texto p{font-size:14pt;line-height:1.85;margin:0 0 10px;position:relative;padding-left:.32in}
.texto p .n{position:absolute;left:0;top:2px;font-size:9pt;color:var(--acento);font-weight:600}
.preg{margin:0 0 30px;font-size:13.5pt;break-inside:avoid}
.preg .q{font-weight:600;margin-bottom:6px}
.opc{display:grid;grid-template-columns:1fr 1fr;gap:10px 18px;padding-left:10px}
.opc{counter-reset:o}.opc div{counter-increment:o}
.opc div:before{content:counter(o,upper-alpha) ")";font-weight:600;color:#475569;margin-right:7px}
.renglon{border-bottom:1.5px solid #94a3b8;height:38px}
.portada{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;height:100%}
.portada h1{font-size:42pt}
.indice{font-size:13pt;line-height:2;margin-top:10px}
ul.lista{font-size:12pt;line-height:1.7}
.sol{font-size:11pt;line-height:1.55;margin-bottom:12px}
.sol h2{font-size:14pt;margin:0 0 4px}
.hoja-sol{columns:2;column-gap:28px}
.tarro{width:2.3in;height:2.9in;border:4px solid var(--acento);border-radius:30px 30px 40px 40px;margin:16px auto 0;position:relative}
.tarro:before{content:"";position:absolute;top:-22px;left:.35in;right:.35in;height:18px;background:var(--acento);border-radius:6px}
"""

LETRAS = "ABCD"


def _cubierta(c):
    lista = "".join(f"<div>{escape(l['titulo'])} <span class='etiqueta'>{l['tipo']}</span></div>" for l in c["lecturas"])
    return f"""<div class="portada"><span class="etiqueta">Grade {c['grado']} · Reading Comprehension</span>
<h1 style="margin-top:22px">{escape(c['titulo_producto'])}</h1>
<p class="sub" style="font-size:14pt">{len(c['lecturas'])} passages · Comprehension questions · Vocabulary · Written response · Answer keys</p>
<div class="indice">{lista}</div>
<p style="font-family:Fredoka;font-size:15pt;color:#64748b;margin-top:30px">{comun.MARCA}</p></div>"""


def _guia(c):
    return f"""<h1>Teacher Guide</h1><p class="sub">Thank you for choosing this resource!</p>
<h2>What's inside</h2><ul class="lista">
<li><b>{len(c['lecturas'])} original passages</b> (fiction and nonfiction) written for Grade {c['grado']}.</li>
<li>Each passage has <b>numbered paragraphs</b>, so students can cite where they found an answer.</li>
<li><b>5 questions per passage</b>: 3 multiple choice, 1 vocabulary in context, 1 written response.</li>
<li><b>Answer keys</b> with sample written responses.</li>
<li>A bonus <b>Thankful Jar</b> writing page.</li></ul>
<h2>Ideas for using it</h2><ul class="lista">
<li>Whole-class close reading the week before Thanksgiving.</li>
<li>Small groups or literacy centers.</li>
<li>Early finishers, homework, or a sub plan: just print and go.</li></ul>
<h2>Standards</h2><p style="font-size:12pt">CCSS RL.3.1 / RI.3.1 (ask and answer questions referring to the text),
RL.3.3 (describe characters), RI.3.4 / L.3.4 (word meaning in context).</p>"""


def _lectura(l):
    parrafos = "".join(f'<p><span class="n">{i}</span>{escape(t)}</p>' for i, t in enumerate(l["texto"], 1))
    return f"""{comun.cabecera_alumno()}<span class="etiqueta">{l['tipo']}</span>
<h1>{escape(l['titulo'])}</h1><div class="texto" style="margin-top:12px">{parrafos}</div>"""


def _preguntas(l):
    trozos = []
    for i, q in enumerate(l["preguntas"], 1):
        if q["tipo"] == "escrita":
            renglones = "".join('<div class="renglon"></div>' for _ in range(5))
            trozos.append(f'<div class="preg"><div class="q">{i}. {escape(q["pregunta"])}</div>{renglones}</div>')
        else:
            opc = "".join(f"<div>{escape(o)}</div>" for o in q["opciones"])
            trozos.append(f'<div class="preg"><div class="q">{i}. {escape(q["pregunta"])}</div><div class="opc">{opc}</div></div>')
    return f"""{comun.cabecera_alumno()}<h1>{escape(l['titulo'])}</h1>
<p class="sub">Read the passage again. Then answer the questions.</p>{''.join(trozos)}"""


def _soluciones(c):
    bloques = []
    for l in c["lecturas"]:
        filas = []
        for i, q in enumerate(l["preguntas"], 1):
            if q["tipo"] == "escrita":
                filas.append(f"{i}. <i>Sample answer:</i> <span class='solucion'>{escape(q['ejemplo'])}</span>")
            else:
                k = q["correcta"]
                filas.append(f"{i}. <span class='solucion'>{LETRAS[k]}) {escape(q['opciones'][k])}</span>")
        bloques.append(f'<div class="sol"><h2>{escape(l["titulo"])}</h2>{"<br>".join(filas)}</div>')
    return bloques


def html(c):
    hojas, pag = [], 1
    hojas.append(comun.hoja(_cubierta(c), pag)); pag += 1
    hojas.append(comun.hoja(_guia(c), pag)); pag += 1
    for l in c["lecturas"]:
        hojas.append(comun.hoja(_lectura(l), pag)); pag += 1
        hojas.append(comun.hoja(_preguntas(l), pag)); pag += 1
    hojas.append(comun.hoja(f"""{comun.cabecera_alumno()}<h1>My Thankful Jar</h1>
<p class="sub">Write or draw five things you are thankful for inside the jar.</p><div class="tarro"></div>
<p style="font-size:12.5pt;margin-top:26px">Which one are you the MOST thankful for? Why?</p>
{''.join('<div class="renglon"></div>' for _ in range(4))}""", pag)); pag += 1
    # Las soluciones, 4 lecturas por hoja (en orden, no en columnas que corten la lectura)
    bloques = _soluciones(c)
    for i in range(0, len(bloques), 4):
        hojas.append(comun.hoja(f"<h1>Answer Key</h1>{''.join(bloques[i:i + 4])}", pag)); pag += 1
    return comun.documento(hojas, extra_css=CSS, **COLORES)

