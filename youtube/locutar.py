# -*- coding: utf-8 -*-
"""
LOCUTOR — convierte un guion (.txt) en voz (.mp3). GRATIS e ilimitado.
=====================================================================
Usa las voces neuronales de Microsoft (edge-tts): las mismas que lee Edge
en voz alta. No hay que pagar ElevenLabs para empezar: esto suena bien,
no tiene límite de caracteres y no pide cuenta ni clave.

USO (desde una terminal, dentro de esta carpeta):

    python locutar.py guion.txt
        → crea guion.mp3 al lado del .txt

    python locutar.py guion.txt --voz es-ES-ElviraNeural
    python locutar.py guion.txt --velocidad +8%      (más rápido)
    python locutar.py guion.txt --salida locucion.mp3
    python locutar.py --voces                        (lista de voces)

En Windows, sin terminal: doble clic en locutar.bat (o arrastra tu .txt
encima del .bat).

Requiere una sola instalación (una vez):  python -m pip install edge-tts
"""
import argparse
import asyncio
import re
import sys
from pathlib import Path

# Voces que merecen la pena para narrar. Hay muchas más (edge-tts --list-voices),
# pero con estas se cubre todo: España, Latinoamérica e inglés.
VOCES = [
    ("es-ES-AlvaroNeural",  "España, masculina — la clásica para narrar (recomendada)"),
    ("es-ES-ElviraNeural",  "España, femenina"),
    ("es-MX-JorgeNeural",   "México, masculina — para público latino"),
    ("es-MX-DaliaNeural",   "México, femenina"),
    ("es-AR-TomasNeural",   "Argentina, masculina"),
    ("es-CO-SalomeNeural",  "Colombia, femenina"),
    ("es-US-AlonsoNeural",  "Español de EE.UU., masculina"),
    ("en-US-GuyNeural",     "Inglés EE.UU., masculina — por si haces canal en inglés"),
    ("en-US-JennyNeural",   "Inglés EE.UU., femenina"),
]
VOZ_POR_DEFECTO = "es-ES-AlvaroNeural"

# El mp3 de edge-tts sale a 48 kbit/s ≈ 6.000 bytes por segundo de audio.
BYTES_POR_SEGUNDO = 6000


def listar_voces():
    print("Voces recomendadas (se pasan con --voz NOMBRE):\n")
    for nombre, desc in VOCES:
        marca = "  ← por defecto" if nombre == VOZ_POR_DEFECTO else ""
        print(f"  {nombre:22s} {desc}{marca}")
    print("\nLa lista completa (cientos de voces): edge-tts --list-voices")


async def _locutar(texto, salida, voz, velocidad):
    import edge_tts
    com = edge_tts.Communicate(texto, voz, rate=velocidad)
    await com.save(str(salida))


def main():
    ap = argparse.ArgumentParser(
        description="Convierte un guion .txt en locución .mp3 (gratis, con edge-tts).")
    ap.add_argument("guion", nargs="?", help="fichero .txt con el guion")
    ap.add_argument("--salida", help="nombre del .mp3 (por defecto, el del guion)")
    ap.add_argument("--voz", default=VOZ_POR_DEFECTO,
                    help=f"voz a usar (por defecto {VOZ_POR_DEFECTO}; ver --voces)")
    ap.add_argument("--velocidad", default="+0%",
                    help="ritmo de lectura: +10%% más rápido, -10%% más lento")
    ap.add_argument("--voces", action="store_true", help="lista las voces y sale")
    args = ap.parse_args()

    if args.voces:
        listar_voces()
        return
    if not args.guion:
        ap.error("dime qué guion locutar: python locutar.py guion.txt (o --voces)")

    if not re.fullmatch(r"[+-]\d{1,3}%", args.velocidad):
        sys.exit(f"--velocidad tiene que ser tipo +10% o -5% (me diste: {args.velocidad})")

    ruta = Path(args.guion)
    if not ruta.exists():
        sys.exit(f"No encuentro el guion: {ruta}")
    # utf-8-sig traga el BOM que mete el Bloc de notas de Windows al guardar
    texto = ruta.read_text(encoding="utf-8-sig").strip()
    if not texto:
        sys.exit(f"El guion está vacío: {ruta}")

    try:
        import edge_tts  # noqa: F401 — solo comprobamos que está instalado
    except ImportError:
        sys.exit("Falta el motor de voz. Instálalo UNA vez con:\n"
                 "    python -m pip install edge-tts\n"
                 "y vuelve a ejecutar esto.")

    salida = Path(args.salida) if args.salida else ruta.with_suffix(".mp3")
    palabras = len(texto.split())
    print(f"Locutando {ruta.name}: {palabras} palabras, voz {args.voz}, ritmo {args.velocidad}…")

    try:
        asyncio.run(_locutar(texto, salida, args.voz, args.velocidad))
    except Exception as e:
        sys.exit("No se pudo generar la voz. Suele ser cosa de la conexión a "
                 "internet (esto habla con los servidores de Microsoft). "
                 f"Prueba otra vez en un momento.\nDetalle técnico: {type(e).__name__}: {e}")

    tam = salida.stat().st_size
    if tam == 0:
        sys.exit("El mp3 ha salido vacío — revisa que el guion tenga texto normal.")
    dur = tam / BYTES_POR_SEGUNDO
    print(f"Listo: {salida}  (~{int(dur // 60)} min {int(dur % 60)} s de audio)")


if __name__ == "__main__":
    main()
