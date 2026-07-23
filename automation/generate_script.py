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

    import sync_channel

    tema = random.choice(config["generacion_automatica"]["temas"])
    # Ni los de la cola ni los ya subidos al canal de YouTube
    usados = [v["titulo"] for v in cola["videos"]] + sync_channel.titulos_guardados()

    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=2000,
        system=(
            "Escribes guiones para 'Archivo Rojo', un canal de YouTube Shorts en español "
            "sobre casos criminales reales SIN RESOLVER (desapariciones, robos, códigos, "
            "identidades desconocidas, muertes misteriosas). Reglas estrictas:\n"
            "- Solo casos reales y bien documentados. Nada inventado; si algo es teoría, dilo.\n"
            "- Tono: narración de misterio, sobria e intrigante. Respetuoso con las víctimas: "
            "sin detalles gráficos ni morbo.\n"
            "- El guion dura 45-60 segundos leído en voz alta (120-150 palabras).\n"
            "- Estructura fija: empieza con 'Archivo Rojo. Caso: [nombre].', desarrolla el "
            "misterio con frases cortas y un giro, y termina con 'Caso abierto. Sígueme para "
            "más casos del Archivo Rojo.'\n"
            "- El título empieza con 'ARCHIVO ROJO 🔴', es intrigante y termina con #Shorts.\n"
            "- El campo 'id' es un slug corto en minúsculas con guiones."
        ),
        messages=[{
            "role": "user",
            "content": (
                f"Genera un guion nuevo de la categoría: {tema}.\n"
                f"NO repitas estos casos ya publicados: {json.dumps(usados, ensure_ascii=False)}"
            ),
        }],
        output_config={"format": {"type": "json_schema", "schema": ESQUEMA_GUION}},
    )
    texto = next(b.text for b in response.content if b.type == "text")
    return json.loads(texto)
