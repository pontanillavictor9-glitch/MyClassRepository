"""Orquestador: guion -> voz (ElevenLabs) -> video (ffmpeg) -> YouTube.

Uso:
    python automation/run_pipeline.py            # pipeline completo
    python automation/run_pipeline.py --no-upload  # genera el video sin subirlo (prueba)
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import generate_script
import make_video
import tts
import upload_youtube

CONFIG_PATH = "content/config.json"
OUT_DIR = "output"


def main() -> None:
    subir = "--no-upload" not in sys.argv

    with open(CONFIG_PATH, encoding="utf-8") as f:
        config = json.load(f)

    os.makedirs(OUT_DIR, exist_ok=True)

    print("1/4 Seleccionando guion...")
    video = generate_script.obtener_siguiente(config)
    print(f"   -> {video['titulo']}")

    print("2/4 Generando voz con ElevenLabs...")
    ruta_audio = os.path.join(OUT_DIR, f"{video['id']}.mp3")
    palabras = tts.sintetizar(video["guion"], ruta_audio, config)
    print(f"   -> {len(palabras)} palabras con tiempos")

    print("3/4 Montando video con ffmpeg...")
    ruta_ass = os.path.join(OUT_DIR, f"{video['id']}.ass")
    ruta_mp4 = os.path.join(OUT_DIR, f"{video['id']}.mp4")
    make_video.generar_subtitulos_ass(palabras, ruta_ass)
    make_video.montar(ruta_audio, ruta_ass, ruta_mp4, config)

    if not subir:
        print(f"Modo prueba: video guardado en {ruta_mp4}, no se sube a YouTube.")
        return

    print("4/4 Subiendo a YouTube...")
    url = upload_youtube.subir(
        ruta_mp4, video["titulo"], video["descripcion"], video.get("tags", []), config
    )
    generate_script.marcar_publicado(video["id"], url)
    print("Listo. Cola actualizada en content/queue.json")


if __name__ == "__main__":
    main()
