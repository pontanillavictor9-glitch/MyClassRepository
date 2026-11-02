"""
Producto: «Multiplication Fact Fluency Drills — Grade 3» (CCSS 3.OA.C.7).

Todo lo genera el programa, y las soluciones las CALCULA el programa: no puede
haber una solución mal. Mismo resultado cada vez (semilla fija).

Contenido: portada, guía para el profesor, 9 fichas por tabla (×2 a ×10),
5 repasos mezclados cronometrados, registro de progreso, diploma y soluciones.
"""

import random

import comun

ID = "multiplicacion-g3"
COLORES = dict(acento="#2a9d8f", titulo="#1d3557", suave="#d8f3ee")

CSS = """
.rejilla{display:grid;grid-template-columns:repeat(3,1fr);gap:38px 26px;margin-top:22px;font-size:20pt}
.rejilla.mix{grid-template-columns:repeat(4,1fr);gap:35px 16px;font-size:16.5pt}
.op{white-space:nowrap}.op b{font-weight:400;display:inline-block;border-bottom:1.5px solid #1f2a37;width:.7in;margin-left:4px}
.mix .op b{width:.55in}
.cuadro{border:2px dashed var(--acento);border-radius:14px;padding:8px 14px;font-size:11pt;display:flex;gap:30px;margin:6px 0 4px}
.portada{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;height:100%}
.portada h1{font-size:44pt}.grande{font-family:Fredoka;font-weight:600;font-size:120pt;color:var(--acento);line-height:1}
ul.lista{font-size:12pt;line-height:1.7;text-align:left}
table.reg{border-collapse:collapse;width:100%;font-size:12pt;margin-top:10px}
table.reg td,table.reg th{border:1.5px solid #94a3b8;padding:18px 9px;text-align:center}
.estrella{display:inline-block;width:26px;height:25px;background:var(--acento);clip-path:polygon(50% 0,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%);opacity:.35}
.clave{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.clave .caja{border:1.5px solid #cbd5e1;border-radius:12px;padding:8px 12px}
.clave .lista3{columns:3;font-size:9.5pt;line-height:1.5}
.clave .caja h2{font-size:14pt;margin-bottom:4px}
.diploma{border:10px double var(--acento);border-radius:30px;height:calc(100% - .35in);display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}
.linea{border-bottom:2px solid #1f2a37;width:5in;height:42px;margin:6px auto}
"""


def _tabla(n, rnd):
    unicos = [(n, k) for k in range(0, 11)] + [(k, n) for k in range(0, 11) if k != n]
    extra = [rnd.choice(unicos) for _ in range(30 - len(unicos))]
    ops = unicos + extra
    rnd.shuffle(ops)
    return ops


def _mezcla(rnd, cuantas=40):
    """40 operaciones distintas (sin repetir ninguna dentro de la misma ficha)."""
    todas = [(a, b) for a in range(2, 11) for b in range(0, 11)]
    return rnd.sample(todas, cuantas)


def problemas():
    """Lista de fichas: (titulo, lista de (a, b)). Es lo que comprueba el Revisor."""
    rnd = random.Random(2026)
    fichas = [(f"Facts of {n}", _tabla(n, rnd)) for n in range(2, 11)]
    fichas += [(f"Mixed Review {i}", _mezcla(rnd)) for i in range(1, 6)]
    return fichas


def _operacion(a, b, con_solucion=False):
    sol = f'<span class="solucion">{a * b}</span>' if con_solucion else ""
    return f'<div class="op">{a} × {b} = <b>{sol}</b></div>'


def html():
    fichas = problemas()
    hojas = []
    pag = 1

    hojas.append(comun.hoja(f"""<div class="portada">
<span class="etiqueta">Grade 3 · CCSS 3.OA.C.7</span>
<div class="grande">7×8</div>
<h1>Multiplication<br>Fact Fluency Drills</h1>
<p class="sub" style="font-size:14pt">Facts 0–10 · 9 fact-family pages · 5 timed mixed reviews<br>Progress tracker · Certificate · Full answer keys</p>
<p style="font-family:Fredoka;font-size:15pt;color:#64748b">{comun.MARCA}</p></div>""", pag))
    pag += 1

    hojas.append(comun.hoja(f"""<h1>Teacher Guide</h1><p class="sub">Thank you for choosing this resource!</p>
<h2>What's inside</h2><ul class="lista">
<li><b>9 fact-family pages</b> (×2 to ×10): 30 problems each, every fact of the family, both orders (3 × 4 and 4 × 3).</li>
<li><b>5 mixed reviews</b>: 40 problems each. Use them as 3-minute timed checks or untimed practice.</li>
<li><b>Progress tracker</b>: students record their score and color the facts they have mastered.</li>
<li><b>Certificate</b> to celebrate when a student masters all facts.</li>
<li><b>Answer keys</b> for every page.</li></ul>
<h2>Ideas for using it</h2><ul class="lista">
<li>Morning work or math centers: one fact family per week.</li>
<li>Fluency check: same mixed review on Monday and Friday, compare scores.</li>
<li>Homework: send one page home, check with the answer key.</li>
<li>Print double-sided to save paper; the answer keys are at the end.</li></ul>
<h2>Standard</h2><p style="font-size:12pt">CCSS.MATH.CONTENT.3.OA.C.7: Fluently multiply and divide within 100. By the end of Grade 3,
know from memory all products of two one-digit numbers.</p>""", pag))
    pag += 1

    for titulo, ops in fichas:
        mix = titulo.startswith("Mixed")
        cuadro = ('<div class="cuadro"><span>Time: ________</span><span>Correct: ______ / 40</span></div>' if mix
                  else '<div class="cuadro"><span>Correct: ______ / 30</span><span>Tip: use a fact you know to help!</span></div>')
        hojas.append(comun.hoja(f"""{comun.cabecera_alumno()}<h1>{titulo}</h1>{cuadro}
<div class="rejilla{' mix' if mix else ''}">{''.join(_operacion(a, b) for a, b in ops)}</div>""", pag))
        pag += 1

    filas = "".join(f"<tr><td><b>× {n}</b></td><td></td><td></td><td></td><td><span class=estrella></span></td></tr>" for n in range(2, 11))
    hojas.append(comun.hoja(f"""{comun.cabecera_alumno()}<h1>My Fluency Tracker</h1>
<p class="sub">Write your score each time you practice. Color the star when you get them all right!</p>
<table class="reg"><tr><th>Facts</th><th>Try 1</th><th>Try 2</th><th>Try 3</th><th>Mastered</th></tr>{filas}</table>""", pag))
    pag += 1

    hojas.append(comun.hoja("""<div class="diploma"><span class="etiqueta">Certificate of Achievement</span>
<h1 style="font-size:40pt;margin-top:24px">Multiplication Master</h1><p class="sub">This certificate is proudly presented to</p>
<div class="linea"></div><p class="sub" style="margin-top:14px">for knowing all multiplication facts from 0 to 10!</p>
<div style="display:flex;gap:1.2in;margin-top:40px;font-size:11pt"><div><div class="linea" style="width:2.2in"></div>Teacher</div>
<div><div class="linea" style="width:2.2in"></div>Date</div></div></div>""", pag, borde=False))
    pag += 1

    # Soluciones: 4 fichas por hoja, con el texto «a × b = c» (el Revisor lo relee del PDF).
    for i in range(0, len(fichas), 4):
        cajas = ""
        for titulo, ops in fichas[i:i + 4]:
            lineas = "".join(f"<div>{a} × {b} = <span class=solucion>{a * b}</span></div>" for a, b in ops)
            cajas += f'<div class="caja"><h2>{titulo}</h2><div class="lista3">{lineas}</div></div>'
        hojas.append(comun.hoja(f'<h1>Answer Key</h1><div class="clave">{cajas}</div>', pag))
        pag += 1

    return comun.documento(hojas, extra_css=CSS, **COLORES)


FICHA = {
    "id": ID,
    "titulo": "Multiplication Fact Fluency Drills Grade 3 | Timed Tests Facts 0-10 with Answer Keys",
    "grado": "3",
    "materia": "Math",
    "estandar": "CCSS 3.OA.C.7",
    "precio_sugerido_usd": 4.00,
    "portada": {"grande": "7×8", "linea1": "Multiplication", "linea2": "Fact Fluency Drills",
                "detalle": "Grade 3 · Facts 0–10 · Answer Keys"},
}
