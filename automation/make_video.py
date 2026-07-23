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


def mezclar_musica(ruta_voz: str, salida: str) -> str:
    """Mezcla la voz con una pista aleatoria de assets/music/ a volumen bajo.
    Si no hay música, devuelve la voz tal cual."""
    pistas = glob.glob("assets/music/*.mp3")
    if not pistas:
        return ruta_voz
    musica = random.choice(pistas)
    subprocess.run([
        "ffmpeg", "-y",
        "-i", ruta_voz,
        "-stream_loop", "-1", "-i", musica,
        "-filter_complex",
        "[1:a]volume=0.12[m];[0:a][m]amix=inputs=2:duration=first:dropout_transition=3",
        "-c:a", "libmp3lame", "-q:a", "2",
        salida,
    ], check=True, capture_output=True)
    print(f"   -> música de fondo: {os.path.basename(musica)}")
    return salida


def _duracion_audio(ruta_audio: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", ruta_audio],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def montar(ruta_audio: str, ruta_ass: str, salida_mp4: str, config: dict,
           video_id: str | None = None) -> None:
    """Crea el MP4 final. Prioridad del fondo:
    1. Imágenes del caso en assets/cases/<id>/ (p. ej. generadas con ComfyUI),
       animadas con zoom lento estilo documental.
    2. Un video de assets/backgrounds/.
    3. Fondo degradado oscuro generado con ffmpeg."""
    ancho = config["video"]["ancho"]
    alto = config["video"]["alto"]
    duracion = _duracion_audio(ruta_audio)
    filtro_subs = f"subtitles={ruta_ass}"

    imagenes = []
    if video_id:
        for ext in ("png", "jpg", "jpeg", "webp"):
            imagenes += glob.glob(f"assets/cases/{video_id}/*.{ext}")
        imagenes.sort()

    if imagenes:
        _montar_con_imagenes(imagenes, ruta_audio, filtro_subs, salida_mp4,
                             ancho, alto, duracion)
        print(f"Video creado con {len(imagenes)} imágenes del caso: {salida_mp4}")
        return

    fondos = glob.glob("assets/backgrounds/*.mp4")

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


def _montar_con_imagenes(imagenes: list[str], ruta_audio: str, filtro_subs: str,
                         salida_mp4: str, ancho: int, alto: int, duracion: float) -> None:
    """Convierte imágenes fijas en un fondo animado (efecto Ken Burns: zoom
    lento alternando acercamiento y alejamiento) y añade audio y subtítulos."""
    fps = 30
    frames_por_imagen = int(duracion * fps / len(imagenes)) + 1

    entradas = []
    filtros = []
    for i, img in enumerate(imagenes):
        entradas += ["-i", img]
        if i % 2 == 0:
            zoom = "min(1+0.0010*on,1.18)"
        else:
            zoom = "max(1.18-0.0010*on,1.0)"
        filtros.append(
            f"[{i}:v]scale={ancho * 2}:{alto * 2}:force_original_aspect_ratio=increase,"
            f"crop={ancho * 2}:{alto * 2},"
            f"zoompan=z='{zoom}':d={frames_por_imagen}:"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={ancho}x{alto}:fps={fps},"
            f"setsar=1[v{i}]"
        )
    cadena = "".join(f"[v{i}]" for i in range(len(imagenes)))
    filtros.append(f"{cadena}concat=n={len(imagenes)}:v=1:a=0[bg]")
    filtros.append(f"[bg]{filtro_subs}[vout]")

    cmd = [
        "ffmpeg", "-y",
        *entradas,
        "-i", ruta_audio,
        "-filter_complex", ";".join(filtros),
        "-map", "[vout]", "-map", f"{len(imagenes)}:a",
        "-t", f"{duracion:.2f}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-r", str(fps),
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        salida_mp4,
    ]
    subprocess.run(cmd, check=True)
