"""Orquestador: guion -> imágenes (FLUX) -> voz (ElevenLabs) -> video (ffmpeg) -> YouTube.

Uso:
    python automation/run_pipeline.py            # pipeline completo
    python automation/run_pipeline.py --no-upload  # genera el video sin subirlo (prueba)
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gen_images
import generate_script
import make_video
import sync_channel
import tts
import upload_youtube

CONFIG_PATH = "content/config.json"
OUT_DIR = "output"


def main() -> None:
    subir = "--no-upload" not in sys.argv

    with open(CONFIG_PATH, encoding="utf-8") as f:
        config = json.load(f)

    os.makedirs(OUT_DIR, exist_ok=True)

    if os.environ.get("YT_REFRESH_TOKEN"):
        print("0/5 Leyendo videos ya publicados en el canal...")
        sync_channel.sincronizar()

    print("1/5 Seleccionando guion...")
    video = generate_script.obtener_siguiente(config)
    print(f"   -> {video['titulo']}")

    print("2/5 Generando imágenes del caso...")
    try:
        gen_images.generar(video, config)
    except Exception as e:
        print(f"   Aviso: falló la generación de imágenes ({e}). Se usará el degradado.")

    print("3/5 Generando voz con ElevenLabs...")
    ruta_voz = os.path.join(OUT_DIR, f"{video['id']}_voz.mp3")
    palabras = tts.sintetizar(video["guion"], ruta_voz, config)
    print(f"   -> {len(palabras)} palabras con tiempos")
    ruta_audio = make_video.mezclar_musica(ruta_voz, os.path.join(OUT_DIR, f"{video['id']}.mp3"))

    print("4/5 Montando video con ffmpeg...")
    ruta_ass = os.path.join(OUT_DIR, f"{video['id']}.ass")
    ruta_mp4 = os.path.join(OUT_DIR, f"{video['id']}.mp4")
    make_video.generar_subtitulos_ass(palabras, ruta_ass)
    make_video.montar(ruta_audio, ruta_ass, ruta_mp4, config, video_id=video["id"])

    if not subir:
        print(f"Modo prueba: video guardado en {ruta_mp4}, no se sube a YouTube.")
        return

    print("5/5 Subiendo a YouTube...")
    url = upload_youtube.subir(
        ruta_mp4, video["titulo"], video["descripcion"], video.get("tags", []), config
    )
    generate_script.marcar_publicado(video["id"], url)
    print("Listo. Cola actualizada en content/queue.json")


if __name__ == "__main__":
    main()
