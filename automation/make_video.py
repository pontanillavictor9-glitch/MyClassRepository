"""Monta el video vertical (1080x1920) con ffmpeg: fondo + audio + subtítulos."""

import glob
import os
import random
import subprocess

MAX_PALABRAS_POR_LINEA = 3


def _fmt_ass(segundos: float) -> str:
    h = int(segundos // 3600)
    m = int((segundos % 3600) // 60)
    s = segundos % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def generar_subtitulos_ass(palabras: list[dict], ruta_ass: str) -> None:
    """Agrupa las palabras en frases cortas y crea un archivo .ass centrado."""
    cabecera = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,DejaVu Sans,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,2,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lineas = []
    grupo = []
    for p in palabras:
        grupo.append(p)
        if len(grupo) >= MAX_PALABRAS_POR_LINEA or p["word"].rstrip().endswith((".", ",", "?", "!", ":", "…")):
            lineas.append(grupo)
            grupo = []
    if grupo:
        lineas.append(grupo)

    eventos = []
    for i, grupo in enumerate(lineas):
        inicio = grupo[0]["start"]
        # Cada línea dura hasta que empieza la siguiente, para que no haya huecos.
        fin = lineas[i + 1][0]["start"] if i + 1 < len(lineas) else grupo[-1]["end"] + 0.5
        texto = " ".join(p["word"] for p in grupo).upper()
        eventos.append(
            f"Dialogue: 0,{_fmt_ass(inicio)},{_fmt_ass(fin)},Default,,0,0,0,,{texto}"
        )

    with open(ruta_ass, "w", encoding="utf-8") as f:
        f.write(cabecera + "\n".join(eventos) + "\n")


def _duracion_audio(ruta_audio: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", ruta_audio],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def montar(ruta_audio: str, ruta_ass: str, salida_mp4: str, config: dict) -> None:
    """Crea el MP4 final. Usa un video de assets/backgrounds/ si existe;
    si no, genera un fondo degradado animado con ffmpeg."""
    ancho = config["video"]["ancho"]
    alto = config["video"]["alto"]
    duracion = _duracion_audio(ruta_audio)

    fondos = glob.glob("assets/backgrounds/*.mp4")
    filtro_subs = f"subtitles={ruta_ass}"

    if fondos:
        fondo = random.choice(fondos)
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1", "-i", fondo,
            "-i", ruta_audio,
            "-vf",
            f"scale={ancho}:{alto}:force_original_aspect_ratio=increase,"
            f"crop={ancho}:{alto},{filtro_subs}",
            "-t", f"{duracion:.2f}",
        ]
    else:
        c0, c1 = random.choice(config["video"]["colores_fondo"])
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"gradients=size={ancho}x{alto}:speed=0.03:duration={duracion:.2f}:c0={c0}:c1={c1}",
            "-i", ruta_audio,
            "-vf", filtro_subs,
        ]

    cmd += [
        "-map", "0:v", "-map", "1:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        salida_mp4,
    ]
    subprocess.run(cmd, check=True)
    print(f"Video creado: {salida_mp4} ({os.path.getsize(salida_mp4) / 1e6:.1f} MB, {duracion:.1f}s)")
