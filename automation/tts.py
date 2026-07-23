"""Genera la voz con ElevenLabs y devuelve el audio + tiempos por palabra."""

import base64
import os

import requests

API_BASE = "https://api.elevenlabs.io/v1"
# Voz por defecto: "Antoni" (multilingüe). Puedes cambiarla con ELEVENLABS_VOICE_ID.
DEFAULT_VOICE_ID = "ErXwobaYiN019PkySvjV"


def sintetizar(texto: str, salida_mp3: str, config: dict) -> list[dict]:
    """Convierte texto a voz. Devuelve una lista de palabras con tiempos:
    [{"word": str, "start": float, "end": float}, ...]
    """
    api_key = os.environ["ELEVENLABS_API_KEY"]
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID", DEFAULT_VOICE_ID)

    resp = requests.post(
        f"{API_BASE}/text-to-speech/{voice_id}/with-timestamps",
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        json={
            "text": texto,
            "model_id": config["elevenlabs"]["model_id"],
            "voice_settings": config["elevenlabs"]["voice_settings"],
        },
        timeout=300,
    )
    resp.raise_for_status()
    data = resp.json()

    with open(salida_mp3, "wb") as f:
        f.write(base64.b64decode(data["audio_base64"]))

    return _palabras_desde_alineacion(data["alignment"])


def _palabras_desde_alineacion(alignment: dict) -> list[dict]:
    chars = alignment["characters"]
    starts = alignment["character_start_times_seconds"]
    ends = alignment["character_end_times_seconds"]

    palabras = []
    actual = ""
    inicio = None
    fin = 0.0
    for ch, s, e in zip(chars, starts, ends):
        if ch.isspace():
            if actual:
                palabras.append({"word": actual, "start": inicio, "end": fin})
                actual = ""
                inicio = None
        else:
            if inicio is None:
                inicio = s
            actual += ch
            fin = e
    if actual:
        palabras.append({"word": actual, "start": inicio, "end": fin})
    return palabras
