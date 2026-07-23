"""Elige el próximo guion: primero de la cola (content/queue.json);
si la cola está vacía y hay ANTHROPIC_API_KEY, genera uno nuevo con Claude."""

import datetime
import json
import os
import random

QUEUE_PATH = "content/queue.json"

ESQUEMA_GUION = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "titulo": {"type": "string"},
        "descripcion": {"type": "string"},
        "guion": {"type": "string"},
        "tags": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["id", "titulo", "descripcion", "guion", "tags"],
    "additionalProperties": False,
}


def obtener_siguiente(config: dict) -> dict:
    with open(QUEUE_PATH, encoding="utf-8") as f:
        cola = json.load(f)

    pendientes = [v for v in cola["videos"] if not v.get("publicado")]
    if pendientes:
        return pendientes[0]

    if os.environ.get("ANTHROPIC_API_KEY"):
        video = _generar_con_claude(config, cola)
        cola["videos"].append({**video, "publicado": None})
        _guardar(cola)
        return video

    raise SystemExit(
        "La cola está vacía y no hay ANTHROPIC_API_KEY configurada. "
        "Añade guiones a content/queue.json o configura la clave para generación automática."
    )


def marcar_publicado(video_id: str, url: str) -> None:
    with open(QUEUE_PATH, encoding="utf-8") as f:
        cola = json.load(f)
    for v in cola["videos"]:
        if v["id"] == video_id:
            v["publicado"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            v["url"] = url
    _guardar(cola)


def _guardar(cola: dict) -> None:
    with open(QUEUE_PATH, "w", encoding="utf-8") as f:
        json.dump(cola, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _generar_con_claude(config: dict, cola: dict) -> dict:
    import anthropic

    tema = random.choice(config["generacion_automatica"]["temas"])
    usados = [v["titulo"] for v in cola["videos"]]

    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=2000,
        system=(
            "Escribes guiones para YouTube Shorts en español. Reglas: el guion debe durar "
            "40-55 segundos leído en voz alta (110-140 palabras), empezar con un gancho "
            "sorprendente en la primera frase, usar frases cortas, terminar pidiendo seguir "
            "el canal, y ser 100% factual. El título debe ser llamativo, incluir un emoji "
            "y terminar con #Shorts. El campo 'id' debe ser un slug corto en minúsculas con guiones."
        ),
        messages=[{
            "role": "user",
            "content": (
                f"Genera un guion nuevo sobre: {tema}.\n"
                f"NO repitas estos temas ya usados: {json.dumps(usados, ensure_ascii=False)}"
            ),
        }],
        output_config={"format": {"type": "json_schema", "schema": ESQUEMA_GUION}},
    )
    texto = next(b.text for b in response.content if b.type == "text")
    return json.loads(texto)
