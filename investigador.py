"""
Agente INVESTIGADOR. Busca en la web (con la búsqueda de la IA) qué recursos
para profesores de EE. UU. tienen demanda y poca oferta buena, teniendo en
cuenta la temporada, y deja una lista de ideas en ideas.json.

Necesita ANTHROPIC_API_KEY.  Uso:  python investigador.py --mes diciembre
"""

import argparse
import json
import os

import comun

ESQUEMA = {"type": "object", "additionalProperties": False, "required": ["ideas"], "properties": {"ideas": {
    "type": "array", "items": {"type": "object", "additionalProperties": False,
    "required": ["titulo", "tipo", "grado", "por_que", "estandares", "seguridad"],
    "properties": {
        "titulo": {"type": "string"},
        "tipo": {"type": "string", "enum": ["matematicas", "lectura", "decodables", "otro"]},
        "grado": {"type": "string"},
        "por_que": {"type": "string", "description": "evidencia de demanda, en español"},
        "estandares": {"type": "array", "items": {"type": "string"}},
        "seguridad": {"type": "string", "enum": ["alta", "media", "baja"],
                      "description": "cuánto respaldan las fuentes que se vende"}}}}}}


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--mes", default="el mes que viene")
    a.add_argument("--n", type=int, default=10)
    x = a.parse_args()
    import anthropic
    r = anthropic.Anthropic().messages.create(
        model=os.environ.get("MODELO_IA", "claude-opus-5-5"), max_tokens=16000,
        tools=[{"type": "web_search_20260209", "name": "web_search", "max_uses": 8}],
        output_config={"effort": "high", "format": {"type": "json_schema", "schema": ESQUEMA}},
        messages=[{"role": "user", "content":
            f"Find {x.n} printable PDF resources for US K-5 teachers that are likely to sell on Teachers Pay "
            f"Teachers and Etsy for {x.mes}. Prefer topics with steady demand and room for a clearer, "
            "better-made resource. Base each idea on evidence you found and say how strong it is. "
            "Write 'por_que' in Spanish."}])
    texto = next(b.text for b in reversed(r.content) if b.type == "text")
    ideas = json.loads(texto)["ideas"]
    comun.escribir_json(comun.RAIZ / "ideas.json", ideas)
    for i in ideas:
        print(f"[{i['seguridad']}] {i['titulo']} ({i['grado']}): {i['por_que']}")


if __name__ == "__main__":
    main()
