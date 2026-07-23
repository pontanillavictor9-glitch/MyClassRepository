"""Genera el video del Short "Netflix te cuesta $30.000" sin dependencias externas.

Produce un MP4 vertical (1080x1920, 30 fps, ~37 s) de tipografía cinética:
texto animado grande sincronizado, contador de dinero, barra de progreso
y música lo-fi sintetizada con numpy. Pensado para publicarse tal cual o
con una voz en off añadida encima (ElevenLabs / CapCut).

Uso:
    python make_video.py [salida.mp4]

Requiere: pillow, numpy, imageio-ffmpeg (pip install pillow numpy imageio-ffmpeg)
"""

import subprocess
import sys
import tempfile
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
SR = 44100
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

BLANCO = (236, 237, 239)
GRIS = (154, 160, 173)
ROJO = (255, 92, 92)
AMBAR = (255, 197, 61)

# Cada segmento: duración y líneas (texto, tamaño, color, retardo de aparición).
# "COUNTER" es la línea especial que cuenta de $0 a $30.000.
SEGMENTOS = [
    (4.0, [
        ("Tu NETFLIX", 92, BLANCO, 0.0),
        ("no cuesta $15.", 92, BLANCO, 0.2),
        ("", 40, BLANCO, 0),
        ("CUESTA", 100, AMBAR, 1.3),
        ("$30.000", 190, ROJO, 1.6),
    ]),
    (4.0, [
        ("$15 al mes", 96, BLANCO, 0.0),
        ("= $180 al año", 96, BLANCO, 0.4),
        ("", 40, BLANCO, 0),
        ("«Poco», piensas.", 72, GRIS, 1.5),
        ("ERROR.", 130, ROJO, 2.3),
    ]),
    (4.5, [
        ("Cada peso que gastas", 76, BLANCO, 0.0),
        ("tiene un precio", 76, BLANCO, 0.25),
        ("OCULTO:", 124, AMBAR, 1.0),
        ("", 40, BLANCO, 0),
        ("lo que pudo generar", 68, GRIS, 1.9),
        ("INVERTIDO", 100, BLANCO, 2.4),
    ]),
    (5.5, [
        ("$15 al mes", 78, BLANCO, 0.0),
        ("al 10% anual", 78, BLANCO, 0.4),
        ("en 30 años son...", 68, GRIS, 1.0),
        ("COUNTER", 180, ROJO, 1.6),
        ("(promedio histórico de la bolsa)", 42, GRIS, 4.2),
    ]),
    (4.0, [
        ("Una suscripción", 84, BLANCO, 0.0),
        ("«barata»", 84, GRIS, 0.35),
        ("", 40, BLANCO, 0),
        ("VALE UN CARRO", 112, AMBAR, 1.3),
    ]),
    (5.0, [
        ("NO canceles Netflix.", 86, BLANCO, 0.0),
        ("Ese no es el punto.", 60, GRIS, 0.9),
        ("", 40, BLANCO, 0),
        ("Elimina la que", 82, BLANCO, 1.9),
        ("NO USASTE", 112, ROJO, 2.4),
        ("este mes", 82, BLANCO, 2.7),
    ]),
    (4.5, [
        ("E invierte lo que", 84, BLANCO, 0.0),
        ("te cobraba.", 84, BLANCO, 0.35),
        ("", 40, BLANCO, 0),
        ("Cada mes.", 92, AMBAR, 1.5),
        ("Sin excusas.", 92, ROJO, 2.1),
    ]),
    (5.0, [
        ("¿Cuál suscripción", 82, BLANCO, 0.0),
        ("pagas SIN usar?", 82, BLANCO, 0.35),
        ("", 40, BLANCO, 0),
        ("CONFIÉSALO EN", 92, AMBAR, 1.6),
        ("LOS COMENTARIOS", 92, AMBAR, 1.9),
        ("▼", 90, ROJO, 2.5),
    ]),
]

DURACION = sum(d for d, _ in SEGMENTOS)

_fuentes = {}


def fuente(tam):
    if tam not in _fuentes:
        _fuentes[tam] = ImageFont.truetype(FONT_PATH, tam)
    return _fuentes[tam]


def fondo_grande():
    """Fondo con degradado vertical y brillos suaves, 8% más grande para el zoom."""
    bw, bh = int(W * 1.08), int(H * 1.08)
    y = np.linspace(0, 1, bh)[:, None, None]
    base = np.array([18, 20, 26]) * (1 - y) + np.array([30, 34, 45]) * y
    img = np.broadcast_to(base, (bh, bw, 3)).astype(np.float64).copy()

    yy, xx = np.mgrid[0:bh, 0:bw]
    glow_r = np.exp(-(((xx - bw * 0.5) ** 2) / (bw * 0.55) ** 2
                      + ((yy - bh * 0.22) ** 2) / (bh * 0.30) ** 2))
    img += glow_r[:, :, None] * np.array([70, 18, 18])
    glow_a = np.exp(-(((xx - bw * 0.15) ** 2) / (bw * 0.45) ** 2
                      + ((yy - bh * 0.85) ** 2) / (bh * 0.28) ** 2))
    img += glow_a[:, :, None] * np.array([28, 22, 6])
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def ease_out(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def texto_contador(t_linea):
    p = ease_out(t_linea / 1.8)
    v = int(30000 * p)
    s = f"{v:,}".replace(",", ".")
    return ("+" if p >= 1 else "") + f"${s}"


def dibujar_frame(t, bg):
    # Segmento activo y tiempo local
    acc = 0.0
    for i, (dur, lineas) in enumerate(SEGMENTOS):
        if t < acc + dur or i == len(SEGMENTOS) - 1:
            tl = t - acc
            break
        acc += dur

    # Zoom lento alternando dirección por segmento
    p = min(tl / dur, 1.0)
    z = 1.0 + 0.05 * (p if i % 2 == 0 else 1 - p)
    cw, ch = int(W / z * 1.08), int(H / z * 1.08)
    cx, cy = (bg.width - cw) // 2, (bg.height - ch) // 2
    frame = bg.crop((cx, cy, cx + cw, cy + ch)).resize((W, H), Image.BILINEAR)

    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)

    # Altura total del bloque para centrarlo verticalmente
    alto = sum(int(tam * 1.18) + 8 for _, tam, _, _ in lineas)
    y = (H - alto) // 2 - 90

    for texto, tam, color, delay in lineas:
        paso = int(tam * 1.18) + 8
        if texto:
            a = ease_out((tl - delay) / 0.35)
            if a > 0:
                if texto == "COUNTER":
                    texto = texto_contador(max(tl - delay, 0.0))
                f = fuente(tam)
                ancho = d.textlength(texto, font=f)
                dy = (1 - a) * 42
                d.text(((W - ancho) / 2, y + dy), texto, font=f,
                       fill=color + (int(255 * a),))
        y += paso

    # Barra de progreso (truco de retención)
    d.rectangle([0, 1730, W, 1742], fill=(255, 255, 255, 26))
    d.rectangle([0, 1730, int(W * t / DURACION), 1742], fill=ROJO + (230,))

    return Image.alpha_composite(frame.convert("RGBA"), capa).convert("RGB")


def musica_lofi(dur):
    """Beat lo-fi sintetizado: batería + bajo + acordes + ruido de vinilo."""
    n = int(SR * dur)
    t = np.arange(n) / SR
    mezcla = np.zeros(n)

    beat = 60 / 84  # 84 BPM
    bar = beat * 4

    def añadir(sonido, inicio):
        i = int(inicio * SR)
        if i >= n:
            return
        s = sonido[: n - i]
        mezcla[i:i + len(s)] += s

    # Percusión
    tt = np.arange(int(0.3 * SR)) / SR
    kick = np.sin(2 * np.pi * (110 * np.exp(-tt * 9) + 42) * tt) * np.exp(-tt * 14) * 0.9
    ruido = np.random.default_rng(7).standard_normal(int(0.22 * SR))
    suave = np.convolve(ruido, np.ones(24) / 24, "same")
    snare = (ruido - suave) * np.exp(-np.arange(len(ruido)) / SR * 26) * 0.30
    hat = (np.random.default_rng(3).standard_normal(int(0.05 * SR))
           * np.exp(-np.arange(int(0.05 * SR)) / SR * 90) * 0.10)

    pos = 0.0
    while pos < dur:
        añadir(kick, pos)
        añadir(kick, pos + 2 * beat)
        añadir(kick, pos + 2.75 * beat)
        añadir(snare, pos + beat)
        añadir(snare, pos + 3 * beat)
        for k in range(8):
            añadir(hat, pos + k * beat / 2)
        pos += bar

    # Armonía: Am7 - Fmaj7 - Cmaj7 - G6 (frecuencias en Hz)
    acordes = [
        [220.00, 261.63, 329.63, 392.00],
        [174.61, 220.00, 261.63, 329.63],
        [196.00, 261.63, 329.63, 392.00],
        [196.00, 246.94, 293.66, 392.00],
    ]
    bajos = [110.00, 87.31, 65.41, 98.00]

    pos, idx = 0.0, 0
    while pos < dur:
        i0 = int(pos * SR)
        i1 = min(int((pos + bar) * SR), n)
        seg_t = np.arange(i1 - i0) / SR
        env = np.minimum(seg_t / 0.5, 1.0) * np.minimum((bar - seg_t) / 0.6, 1.0)
        env = np.clip(env, 0, 1)
        pad = sum(np.sin(2 * np.pi * f * seg_t) + 0.6 * np.sin(2 * np.pi * f * 1.004 * seg_t)
                  for f in acordes[idx % 4])
        mezcla[i0:i1] += pad * env * 0.045
        oct_bajo = np.sin(2 * np.pi * bajos[idx % 4] * seg_t)
        mezcla[i0:i1] += oct_bajo * env * 0.14
        pos += bar
        idx += 1

    # Vinilo
    vinilo = np.convolve(np.random.default_rng(11).standard_normal(n),
                         np.ones(10) / 10, "same") * 0.012
    mezcla += vinilo

    # Master: saturación suave, fundidos
    mezcla = np.tanh(mezcla * 1.4) * 0.85
    fi, fo = int(0.3 * SR), int(1.4 * SR)
    mezcla[:fi] *= np.linspace(0, 1, fi)
    mezcla[-fo:] *= np.linspace(1, 0, fo)
    return (mezcla * 32767).astype(np.int16)


def main():
    salida = sys.argv[1] if len(sys.argv) > 1 else "video-01-netflix.mp4"
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    print(f"🎵 Sintetizando música lo-fi ({DURACION:.1f} s)...")
    audio = musica_lofi(DURACION)
    wav_path = tempfile.mktemp(suffix=".wav")
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(audio.tobytes())

    print("🎨 Renderizando frames y codificando...")
    bg = fondo_grande()
    total = int(DURACION * FPS)

    proc = subprocess.Popen(
        [ffmpeg, "-y",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-i", wav_path,
         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "160k", "-shortest", salida],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for k in range(total):
        frame = dibujar_frame(k / FPS, bg)
        proc.stdin.write(np.asarray(frame, dtype=np.uint8).tobytes())
        if k % (FPS * 5) == 0:
            print(f"  {k}/{total} frames ({k / FPS:.0f} s)")

    proc.stdin.close()
    proc.wait()
    print(f"✅ Video listo: {salida} ({DURACION:.1f} s, {W}x{H}, {FPS} fps)")


if __name__ == "__main__":
    main()
