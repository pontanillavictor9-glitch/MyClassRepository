"""Genera las imágenes del caso automáticamente en la nube (Replicate + FLUX),
sustituyendo el paso manual de ComfyUI. Estilo visual fijo de Archivo Rojo."""

import os

import requests

API_URL = "https://api.replicate.com/v1/models/black-forest-labs/flux-schnell/predictions"

ESTILO = (
    "dark moody cinematic true crime documentary style, deep crimson red and black "
    "color palette, heavy shadows, fog, film grain, 35mm photography, dramatic low-key "
    "lighting, mysterious atmosphere, vertical composition, no text, no watermark"
)

PROMPTS_GENERICOS = [
    "an old case file folder on a wooden desk lit by a single lamp, scattered documents and photographs",
    "a dimly lit archive room with rows of filing cabinets disappearing into darkness",
    "a detective's evidence board with strings, maps and blank photographs, night",
    "an empty interrogation room with a metal table under a hanging light",
]


def generar(video: dict, config: dict) -> None:
    """Crea las imágenes del caso en assets/cases/<id>/ si no existen ya.
    Sin REPLICATE_API_TOKEN no hace nada (el video usará el fondo degradado)."""
    token = os.environ.get("REPLICATE_API_TOKEN")
    if not token:
        print("   (sin REPLICATE_API_TOKEN: se usará el fondo degradado)")
        return

    carpeta = os.path.join("assets", "cases", video["id"])
    if os.path.isdir(carpeta) and any(
        f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")) for f in os.listdir(carpeta)
    ):
        print(f"   (ya existen imágenes en {carpeta}, se usan esas)")
        return

    prompts = video.get("prompts_imagenes") or PROMPTS_GENERICOS
    os.makedirs(carpeta, exist_ok=True)

    for i, prompt in enumerate(prompts, start=1):
        resp = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {token}", "Prefer": "wait"},
            json={"input": {
                "prompt": f"{prompt}, {ESTILO}",
                "aspect_ratio": "9:16",
                "output_format": "png",
                "output_quality": 100,
            }},
            timeout=300,
        )
        resp.raise_for_status()
        salida = resp.json()["output"]
        url = salida[0] if isinstance(salida, list) else salida

        img = requests.get(url, timeout=300)
        img.raise_for_status()
        ruta = os.path.join(carpeta, f"{i:02d}.png")
        with open(ruta, "wb") as f:
            f.write(img.content)
        print(f"   -> {ruta}")
