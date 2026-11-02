"""
Agente CREADOR (con IA) para productos de texto: escribe el contenido en
contenido/<id>.json con el mismo formato que los ejemplos, y el Revisor lo
comprueba después. (Los de matemáticas no necesitan IA: los genera el código.)

Uso:
    python creador.py lectura "Winter animals" --grado 2 --id invierno-g2
    python creador.py decodables "short a and silent a_e" --id a-e-g1

Necesita ANTHROPIC_API_KEY. Después hay que añadir el producto a catalogo.py.
"""

import argparse
import json
import os

import comun

GUIAS = {
    "lectura": ("Write {n} ORIGINAL reading passages for US grade {grado} about: {tema}. Mix fiction and "
                "nonfiction. Every fact must be accurate and well established; if unsure, leave it out. "
                "Use short sentences suitable for the grade. Each passage: 5-8 short paragraphs, "
                "3 multiple-choice questions (4 options), 1 vocabulary-in-context question (4 options) "
                "and 1 written response with a sample answer. Follow exactly this JSON example's shape:\n{ejemplo}"),
    "decodables": ("Write {n} ORIGINAL decodable stories for US grade 1 practicing: {tema}. Use ONLY "
                   "closed-syllable words, the target pattern, and these heart words: {heart}. No other "
                   "words. 4 short paragraphs and 3 simple questions with answers each. Follow exactly "
                   "this JSON example's shape:\n{ejemplo}"),
}


def main():
    a = argparse.ArgumentParser()
    a.add_argument("tipo", choices=list(GUIAS))
    a.add_argument("tema")
    a.add_argument("--grado", default="3")
    a.add_argument("--n", type=int, default=4)
    a.add_argument("--id", required=True)
    x = a.parse_args()
    from productos import decodables
    ejemplo = (comun.CONTENIDO / ("thanksgiving-g3.json" if x.tipo == "lectura" else "silent-e-g1.json")).read_text()
    pedido = GUIAS[x.tipo].format(n=x.n, grado=x.grado, tema=x.tema, ejemplo=ejemplo,
                                 heart=", ".join(sorted(decodables.HEART)))
    import anthropic
    with anthropic.Anthropic().messages.stream(
            model=os.environ.get("MODELO_IA", "claude-opus-5-5"), max_tokens=32000,
            output_config={"effort": "high"},
            system="You write printable classroom resources. Reply with the JSON only, no commentary.",
            messages=[{"role": "user", "content": pedido}]) as s:
        r = s.get_final_message()
    texto = next(b.text for b in r.content if b.type == "text").strip().removeprefix("```json").removesuffix("```")
    datos = json.loads(texto)
    datos["id"] = x.id
    comun.escribir_json(comun.CONTENIDO / f"{x.id}.json", datos)
    print(f"Contenido guardado en contenido/{x.id}.json. Añádelo a catalogo.py y ejecuta: python tienda.py {x.id}")


if __name__ == "__main__":
    main()
