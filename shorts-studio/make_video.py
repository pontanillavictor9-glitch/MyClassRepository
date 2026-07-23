"""Genera los videos de Shorts del canal sin dependencias externas.

Produce MP4 verticales (1080x1920, 30 fps) de tipografía cinética con
gráficos flat dibujados con código: iconos animados, contador de dinero,
curva animada, barra de progreso y música lo-fi sintetizada con numpy.

Uso:
    python make_video.py 1 [salida.mp4]   # Video 1: Netflix $30.000
    python make_video.py 2 [salida.mp4]   # Video 2: La regla de las 72 horas

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
VERDE = (110, 200, 140)
OSCURO = (24, 26, 33)

# Cada segmento: duración, icono y líneas (texto, tamaño, color, retardo).
# "COUNTER" es la línea especial que cuenta de $0 a $30.000.

VIDEO_01 = [
    (4.0, "tv", [
        ("Tu NETFLIX", 92, BLANCO, 0.0),
        ("no cuesta $15.", 92, BLANCO, 0.2),
        ("", 30, BLANCO, 0),
        ("CUESTA", 96, AMBAR, 1.3),
        ("$30.000", 180, ROJO, 1.6),
    ]),
    (4.0, "monedas", [
        ("$15 al mes", 94, BLANCO, 0.0),
        ("= $180 al año", 94, BLANCO, 0.4),
        ("", 30, BLANCO, 0),
        ("«Poco», piensas.", 70, GRIS, 1.5),
        ("ERROR.", 124, ROJO, 2.3),
    ]),
    (4.5, "etiqueta", [
        ("Cada peso que gastas", 74, BLANCO, 0.0),
        ("tiene un precio", 74, BLANCO, 0.25),
        ("OCULTO:", 118, AMBAR, 1.0),
        ("", 30, BLANCO, 0),
        ("lo que pudo generar", 66, GRIS, 1.9),
        ("INVERTIDO", 96, BLANCO, 2.4),
    ]),
    (5.5, "curva", [
        ("$15 al mes al 10% anual", 68, BLANCO, 0.0),
        ("en 30 años son...", 64, GRIS, 0.8),
        ("COUNTER", 170, ROJO, 1.6),
        ("(promedio histórico de la bolsa)", 40, GRIS, 4.2),
    ]),
    (4.0, "carro", [
        ("Una suscripción", 82, BLANCO, 0.0),
        ("«barata»", 82, GRIS, 0.35),
        ("", 30, BLANCO, 0),
        ("VALE UN CARRO", 106, AMBAR, 1.3),
    ]),
    (5.0, "lista", [
        ("NO canceles Netflix.", 82, BLANCO, 0.0),
        ("Ese no es el punto.", 58, GRIS, 0.9),
        ("", 30, BLANCO, 0),
        ("Elimina la que", 78, BLANCO, 1.9),
        ("NO USASTE", 106, ROJO, 2.4),
        ("este mes", 78, BLANCO, 2.7),
    ]),
    (4.5, "invertir", [
        ("E invierte lo que", 82, BLANCO, 0.0),
        ("te cobraba.", 82, BLANCO, 0.35),
        ("", 30, BLANCO, 0),
        ("Cada mes.", 90, AMBAR, 1.5),
        ("Sin excusas.", 90, ROJO, 2.1),
    ]),
    (5.0, "burbuja", [
        ("¿Cuál suscripción", 80, BLANCO, 0.0),
        ("pagas SIN usar?", 80, BLANCO, 0.35),
        ("", 30, BLANCO, 0),
        ("CONFIÉSALO EN", 88, AMBAR, 1.6),
        ("LOS COMENTARIOS", 88, AMBAR, 1.9),
        ("▼", 84, ROJO, 2.5),
    ]),
]

VIDEO_02 = [
    (4.0, "carrito", [
        ("Tu CEREBRO te", 88, BLANCO, 0.0),
        ("SABOTEA", 128, ROJO, 0.4),
        ("cada vez que compras", 72, BLANCO, 1.0),
        ("", 30, BLANCO, 0),
        ("(y tiene arreglo)", 56, GRIS, 2.2),
    ]),
    (4.5, "chispa", [
        ("Ves algo que te gusta", 70, BLANCO, 0.0),
        ("y BUM:", 82, BLANCO, 0.6),
        ("DOPAMINA", 126, AMBAR, 1.1),
        ("", 30, BLANCO, 0),
        ("Tu cerebro grita:", 62, GRIS, 2.2),
        ("«¡CÓMPRALO YA!»", 94, ROJO, 2.7),
    ]),
    (4.5, "etiqueta", [
        ("Por eso existen las", 72, BLANCO, 0.0),
        ("ofertas «SOLO HOY»", 84, AMBAR, 0.5),
        ("", 30, BLANCO, 0),
        ("Quieren que decidas", 68, BLANCO, 1.6),
        ("SIN PENSAR", 110, ROJO, 2.1),
        ("Pero hay un truco...", 54, GRIS, 3.2),
    ]),
    (3.5, "reloj", [
        ("LA REGLA DE LAS", 82, BLANCO, 0.0),
        ("72 HORAS", 165, AMBAR, 0.5),
    ]),
    (4.5, "calendario", [
        ("¿Quieres comprarlo?", 80, BLANCO, 0.0),
        ("Perfecto.", 68, GRIS, 0.8),
        ("", 30, BLANCO, 0),
        ("ESPERA", 118, ROJO, 1.5),
        ("3 DÍAS", 118, AMBAR, 1.9),
    ]),
    (4.5, "check", [
        ("Si a las 72 horas", 76, BLANCO, 0.0),
        ("lo sigues queriendo:", 74, BLANCO, 0.4),
        ("", 30, BLANCO, 0),
        ("CÓMPRALO", 118, VERDE, 1.4),
        ("Sin culpa.", 68, GRIS, 2.2),
    ]),
    (5.0, "monedas", [
        ("Spoiler:", 80, AMBAR, 0.0),
        ("el 80% de las veces", 74, BLANCO, 0.5),
        ("SE TE OLVIDA", 116, ROJO, 1.4),
        ("", 30, BLANCO, 0),
        ("No era deseo.", 64, GRIS, 2.6),
        ("Era dopamina.", 64, GRIS, 3.1),
    ]),
    (5.0, "burbuja", [
        ("¿De qué compra", 80, BLANCO, 0.0),
        ("te arrepientes?", 80, BLANCO, 0.35),
        ("", 30, BLANCO, 0),
        ("CUÉNTALO EN", 88, AMBAR, 1.5),
        ("LOS COMENTARIOS", 88, AMBAR, 1.8),
        ("▼", 84, ROJO, 2.4),
    ]),
]

VIDEO_03 = [
    (4.0, "banco", [
        ("Ser POBRE", 100, BLANCO, 0.0),
        ("es CARÍSIMO", 110, ROJO, 0.5),
        ("", 30, BLANCO, 0),
        ("Te lo demuestro en 30 seg", 56, GRIS, 1.8),
    ]),
    (4.5, "banco", [
        ("¿Poco saldo en el banco?", 62, BLANCO, 0.0),
        ("COMISIÓN.", 106, ROJO, 0.6),
        ("¿Cajero de otro banco?", 62, BLANCO, 1.5),
        ("COMISIÓN.", 106, ROJO, 2.1),
        ("", 30, BLANCO, 0),
        ("Ser pobre tiene tarifa.", 56, GRIS, 3.2),
    ]),
    (4.5, "etiqueta", [
        ("¿No te alcanza?", 72, BLANCO, 0.0),
        ("Pagas en CUOTAS...", 84, AMBAR, 0.5),
        ("con INTERESES.", 84, ROJO, 1.2),
        ("", 30, BLANCO, 0),
        ("Todo te cuesta MÁS.", 68, BLANCO, 2.2),
        ("Y hay algo peor...", 54, GRIS, 3.3),
    ]),
    (5.0, "bota", [
        ("La teoría de las botas:", 64, BLANCO, 0.0),
        ("", 30, BLANCO, 0),
        ("Botas buenas: $50", 76, BLANCO, 0.8),
        ("duran 10 años", 64, VERDE, 1.3),
        ("Botas baratas: $10", 76, BLANCO, 2.2),
        ("duran 1 año", 64, ROJO, 2.7),
    ]),
    (4.5, "monedas", [
        ("El rico paga $50", 76, BLANCO, 0.0),
        ("UNA vez.", 84, VERDE, 0.6),
        ("", 30, BLANCO, 0),
        ("El pobre paga $10...", 76, BLANCO, 1.5),
        ("DIEZ VECES", 114, ROJO, 2.2),
        ("= $100 por las mismas botas", 54, GRIS, 3.1),
    ]),
    (4.5, "check", [
        ("Y no, no es tu culpa.", 70, BLANCO, 0.0),
        ("El sistema cobra", 70, BLANCO, 0.7),
        ("por NO tener.", 84, AMBAR, 1.2),
        ("", 30, BLANCO, 0),
        ("Pero conocer la trampa", 58, GRIS, 2.3),
        ("es empezar a escapar.", 58, GRIS, 2.8),
    ]),
    (4.5, "invertir", [
        ("Tu primera meta", 72, BLANCO, 0.0),
        ("NO es ser rico.", 72, BLANCO, 0.4),
        ("", 30, BLANCO, 0),
        ("Es un COLCHÓN", 96, AMBAR, 1.3),
        ("que te libre de comisiones,", 54, GRIS, 2.2),
        ("cuotas e intereses.", 54, GRIS, 2.7),
    ]),
    (5.0, "burbuja", [
        ("¿Qué cobro te parece", 76, BLANCO, 0.0),
        ("un ROBO?", 100, ROJO, 0.5),
        ("", 30, BLANCO, 0),
        ("DILO EN", 88, AMBAR, 1.6),
        ("LOS COMENTARIOS", 88, AMBAR, 1.9),
        ("▼", 84, ROJO, 2.5),
    ]),
]

VIDEOS = {
    "1": ("video-01-netflix.mp4", VIDEO_01),
    "2": ("video-02-72horas.mp4", VIDEO_02),
    "3": ("video-03-pobre-caro.mp4", VIDEO_03),
}

_fuentes = {}


def fuente(tam):
    if tam not in _fuentes:
        _fuentes[tam] = ImageFont.truetype(FONT_PATH, tam)
    return _fuentes[tam]


def col(c, a):
    return c + (int(255 * max(0.0, min(1.0, a))),)


def ease_out(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


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


def texto_contador(t_linea):
    p = ease_out(t_linea / 1.8)
    v = int(30000 * p)
    s = f"{v:,}".replace(",", ".")
    return ("+" if p >= 1 else "") + f"${s}"


def texto_centrado(d, texto, f, cx, cy, color):
    ancho = d.textlength(texto, font=f)
    caja = f.getbbox(texto)
    d.text((cx - ancho / 2, cy - (caja[1] + caja[3]) / 2), texto, font=f, fill=color)


def dibujar_icono(d, tipo, cx, cy, s, a, prog):
    """Iconos flat dibujados con primitivas. s = medio-tamaño, a = alfa, prog = animación interna."""
    k = 0.8 + 0.2 * a  # pop de entrada
    s = s * k

    if tipo == "tv":
        d.rounded_rectangle([cx - 1.5 * s, cy - 1.05 * s, cx + 1.5 * s, cy + 0.85 * s],
                            radius=0.22 * s, outline=col(BLANCO, a), width=int(0.11 * s))
        d.polygon([(cx - 0.32 * s, cy - 0.52 * s), (cx - 0.32 * s, cy + 0.32 * s),
                   (cx + 0.52 * s, cy - 0.1 * s)], fill=col(ROJO, a))
        d.line([cx - 0.55 * s, cy + 1.25 * s, cx + 0.55 * s, cy + 1.25 * s],
               fill=col(GRIS, a * 0.8), width=int(0.12 * s))

    elif tipo == "monedas":
        for i in range(3):
            dy = 0.55 * s - i * 0.5 * s
            d.ellipse([cx - 1.05 * s, cy + dy - 0.34 * s, cx + 1.05 * s, cy + dy + 0.34 * s],
                      fill=col((196, 148, 32), a), outline=col(AMBAR, a), width=int(0.06 * s))
        texto_centrado(d, "$", fuente(int(0.62 * s)), cx, cy - 0.48 * s, col(OSCURO, a))

    elif tipo == "etiqueta":
        p = [(-1.35, 0), (-0.45, -0.85), (1.25, -0.85), (1.25, 0.85), (-0.45, 0.85)]
        d.polygon([(cx + x * s, cy + y * s) for x, y in p], fill=col(AMBAR, a))
        d.ellipse([cx - 1.02 * s, cy - 0.14 * s, cx - 0.74 * s, cy + 0.14 * s],
                  fill=col(OSCURO, a))
        texto_centrado(d, "$?", fuente(int(0.75 * s)), cx + 0.35 * s, cy, col(OSCURO, a))

    elif tipo == "curva":
        x0, y0 = cx - 1.6 * s, cy + 1.0 * s
        d.line([x0, y0, cx + 1.7 * s, y0], fill=col(GRIS, a * 0.7), width=6)
        d.line([x0, y0, x0, cy - 1.15 * s], fill=col(GRIS, a * 0.7), width=6)
        n = max(2, int(46 * prog))
        pts = []
        for i in range(n):
            x = (i / 45)
            y = (np.exp(3.1 * x) - 1) / (np.exp(3.1) - 1)
            pts.append((x0 + 3.2 * s * x, y0 - 2.05 * s * y))
        if len(pts) > 1:
            d.polygon(pts + [(pts[-1][0], y0), (x0, y0)], fill=col(ROJO, a * 0.16))
            d.line(pts, fill=col(ROJO, a), width=10, joint="curve")
            fx, fy = pts[-1]
            d.ellipse([fx - 15, fy - 15, fx + 15, fy + 15], fill=col(AMBAR, a))

    elif tipo == "carro":
        d.rounded_rectangle([cx - 1.55 * s, cy - 0.12 * s, cx + 1.55 * s, cy + 0.55 * s],
                            radius=0.2 * s, fill=col(BLANCO, a))
        d.polygon([(cx - 0.75 * s, cy - 0.1 * s), (cx - 0.35 * s, cy - 0.68 * s),
                   (cx + 0.62 * s, cy - 0.68 * s), (cx + 0.95 * s, cy - 0.1 * s)],
                  fill=col(BLANCO, a))
        for wx in (-0.85, 0.85):
            d.ellipse([cx + wx * s - 0.32 * s, cy + 0.3 * s, cx + wx * s + 0.32 * s, cy + 0.94 * s],
                      fill=col(OSCURO, a), outline=col(GRIS, a), width=int(0.07 * s))

    elif tipo == "lista":
        d.rounded_rectangle([cx - 1.3 * s, cy - 1.15 * s, cx + 1.3 * s, cy + 1.15 * s],
                            radius=0.18 * s, fill=col((255, 255, 255), a * 0.09),
                            outline=col(GRIS, a * 0.8), width=5)
        for i, fy in enumerate((-0.62, 0.0, 0.62)):
            yy = cy + fy * s
            ccol = ROJO if i == 1 else VERDE
            d.ellipse([cx - 1.0 * s, yy - 0.13 * s, cx - 0.74 * s, yy + 0.13 * s],
                      fill=col(ccol, a))
            d.line([cx - 0.5 * s, yy, cx + 1.0 * s, yy],
                   fill=col(GRIS if i == 1 else BLANCO, a * 0.75), width=int(0.14 * s))
        d.line([cx - 0.55 * s, cy - 0.16 * s, cx + 1.05 * s, cy + 0.16 * s], fill=col(ROJO, a), width=9)
        d.line([cx - 0.55 * s, cy + 0.16 * s, cx + 1.05 * s, cy - 0.16 * s], fill=col(ROJO, a), width=9)

    elif tipo == "invertir":
        d.ellipse([cx - 1.35 * s, cy - 0.15 * s, cx - 0.25 * s, cy + 0.95 * s],
                  fill=col((196, 148, 32), a), outline=col(AMBAR, a), width=int(0.07 * s))
        texto_centrado(d, "$", fuente(int(0.6 * s)), cx - 0.8 * s, cy + 0.4 * s, col(OSCURO, a))
        d.line([cx - 0.45 * s, cy + 0.45 * s, cx + 1.05 * s, cy - 0.75 * s],
               fill=col(ROJO, a), width=int(0.16 * s))
        d.polygon([(cx + 1.25 * s, cy - 0.92 * s), (cx + 0.62 * s, cy - 0.82 * s),
                   (cx + 1.12 * s, cy - 0.32 * s)], fill=col(ROJO, a))

    elif tipo == "burbuja":
        d.rounded_rectangle([cx - 1.35 * s, cy - 0.95 * s, cx + 1.35 * s, cy + 0.65 * s],
                            radius=0.35 * s, fill=col(BLANCO, a * 0.92))
        d.polygon([(cx - 0.7 * s, cy + 0.6 * s), (cx - 0.25 * s, cy + 0.6 * s),
                   (cx - 0.75 * s, cy + 1.1 * s)], fill=col(BLANCO, a * 0.92))
        for i in (-1, 0, 1):
            d.ellipse([cx + i * 0.42 * s - 0.11 * s, cy - 0.26 * s,
                       cx + i * 0.42 * s + 0.11 * s, cy - 0.04 * s], fill=col(OSCURO, a))

    elif tipo == "carrito":
        d.line([cx - 1.45 * s, cy - 0.85 * s, cx - 0.95 * s, cy - 0.85 * s],
               fill=col(BLANCO, a), width=int(0.12 * s))
        d.polygon([(cx - 0.95 * s, cy - 0.85 * s), (cx + 1.15 * s, cy - 0.85 * s),
                   (cx + 0.85 * s, cy + 0.35 * s), (cx - 0.65 * s, cy + 0.35 * s)],
                  fill=col(BLANCO, a))
        for wx in (-0.4, 0.55):
            d.ellipse([cx + wx * s - 0.17 * s, cy + 0.6 * s, cx + wx * s + 0.17 * s, cy + 0.94 * s],
                      fill=col(BLANCO, a))
        d.ellipse([cx - 0.15 * s, cy - 1.45 * s, cx + 0.45 * s, cy - 0.95 * s],
                  fill=col(ROJO, a))

    elif tipo == "chispa":
        pts = []
        for i in range(16):
            ang = i * np.pi / 8 - np.pi / 2
            r = (1.15 if i % 2 == 0 else 0.45) * s
            pts.append((cx + r * np.cos(ang), cy + r * np.sin(ang)))
        d.polygon(pts, fill=col(AMBAR, a))
        d.ellipse([cx - 0.22 * s, cy - 0.22 * s, cx + 0.22 * s, cy + 0.22 * s],
                  fill=col(BLANCO, a))

    elif tipo == "reloj":
        d.ellipse([cx - 1.1 * s, cy - 1.1 * s, cx + 1.1 * s, cy + 1.1 * s],
                  outline=col(BLANCO, a), width=int(0.12 * s))
        for ang in (0, np.pi / 2, np.pi, 3 * np.pi / 2):
            x1, y1 = cx + 0.88 * s * np.cos(ang), cy + 0.88 * s * np.sin(ang)
            x2, y2 = cx + 1.0 * s * np.cos(ang), cy + 1.0 * s * np.sin(ang)
            d.line([x1, y1, x2, y2], fill=col(GRIS, a), width=int(0.07 * s))
        texto_centrado(d, "72h", fuente(int(0.62 * s)), cx, cy, col(AMBAR, a))

    elif tipo == "calendario":
        d.rounded_rectangle([cx - 1.1 * s, cy - 0.8 * s, cx + 1.1 * s, cy + 1.0 * s],
                            radius=0.15 * s, fill=col(BLANCO, a * 0.94))
        d.rounded_rectangle([cx - 1.1 * s, cy - 0.8 * s, cx + 1.1 * s, cy - 0.32 * s],
                            radius=0.15 * s, fill=col(ROJO, a))
        for wx in (-0.55, 0.55):
            d.line([cx + wx * s, cy - 1.05 * s, cx + wx * s, cy - 0.6 * s],
                   fill=col(GRIS, a), width=int(0.09 * s))
        texto_centrado(d, "3", fuente(int(0.85 * s)), cx, cy + 0.32 * s, col(OSCURO, a))

    elif tipo == "banco":
        d.polygon([(cx - 1.3 * s, cy - 0.4 * s), (cx, cy - 1.1 * s), (cx + 1.3 * s, cy - 0.4 * s)],
                  fill=col(BLANCO, a))
        for wx in (-0.8, -0.15, 0.5):
            d.rectangle([cx + wx * s, cy - 0.25 * s, cx + (wx + 0.32) * s, cy + 0.6 * s],
                        fill=col(BLANCO, a * 0.85))
        d.rectangle([cx - 1.3 * s, cy + 0.72 * s, cx + 1.3 * s, cy + 1.0 * s], fill=col(BLANCO, a))
        texto_centrado(d, "$", fuente(int(0.5 * s)), cx, cy - 0.62 * s, col(ROJO, a))

    elif tipo == "bota":
        d.polygon([(cx - 0.75 * s, cy - 1.05 * s), (cx + 0.05 * s, cy - 1.05 * s),
                   (cx + 0.05 * s, cy + 0.1 * s), (cx + 0.95 * s, cy + 0.4 * s),
                   (cx + 0.95 * s, cy + 0.72 * s), (cx - 0.75 * s, cy + 0.72 * s)],
                  fill=col(BLANCO, a))
        d.rounded_rectangle([cx - 0.82 * s, cy + 0.72 * s, cx + 1.02 * s, cy + 1.0 * s],
                            radius=0.1 * s, fill=col(AMBAR, a))
        d.line([cx - 0.75 * s, cy - 0.45 * s, cx + 0.05 * s, cy - 0.45 * s],
               fill=col(GRIS, a * 0.6), width=int(0.07 * s))

    elif tipo == "check":
        d.ellipse([cx - 1.05 * s, cy - 1.05 * s, cx + 1.05 * s, cy + 1.05 * s],
                  fill=col((66, 148, 96), a))
        d.line([(cx - 0.5 * s, cy + 0.02 * s), (cx - 0.12 * s, cy + 0.42 * s),
                (cx + 0.55 * s, cy - 0.42 * s)], fill=col(BLANCO, a),
               width=int(0.18 * s), joint="curve")


def dibujar_frame(t, bg, segmentos, duracion):
    acc = 0.0
    for i, (dur, icono, lineas) in enumerate(segmentos):
        if t < acc + dur or i == len(segmentos) - 1:
            tl = t - acc
            break
        acc += dur

    # Zoom lento alternando dirección por segmento
    p = min(tl / dur, 1.0)
    z = 1.0 + 0.05 * (p if i % 2 == 0 else 1 - p)
    cw, ch = int(W / z * 1.08), int(H / z * 1.08)
    cx0, cy0 = (bg.width - cw) // 2, (bg.height - ch) // 2
    frame = bg.crop((cx0, cy0, cx0 + cw, cy0 + ch)).resize((W, H), Image.BILINEAR)

    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)

    alto = sum(int(tam * 1.18) + 8 for _, tam, _, _ in lineas)
    y = (H - alto) // 2 + 30

    # Icono animado sobre el bloque de texto
    a_ico = ease_out((tl - 0.05) / 0.45)
    if a_ico > 0:
        if icono == "curva":
            prog = ease_out((tl - 0.9) / 2.6)
            dibujar_icono(d, icono, W / 2, y - 300, 150, a_ico, prog)
        else:
            dibujar_icono(d, icono, W / 2, y - 265, 115, a_ico, 0)

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
                d.text(((W - ancho) / 2, y + dy), texto, font=f, fill=col(color, a))
        y += paso

    # Barra de progreso (truco de retención)
    d.rectangle([0, 1730, W, 1742], fill=(255, 255, 255, 26))
    d.rectangle([0, 1730, int(W * t / duracion), 1742], fill=col(ROJO, 0.9))

    return Image.alpha_composite(frame.convert("RGBA"), capa).convert("RGB")


def musica_lofi(dur):
    """Beat lo-fi sintetizado: batería + bajo + acordes + ruido de vinilo."""
    n = int(SR * dur)
    mezcla = np.zeros(n)

    beat = 60 / 84  # 84 BPM
    bar = beat * 4

    def añadir(sonido, inicio):
        i = int(inicio * SR)
        if i >= n:
            return
        s = sonido[: n - i]
        mezcla[i:i + len(s)] += s

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
        mezcla[i0:i1] += np.sin(2 * np.pi * bajos[idx % 4] * seg_t) * env * 0.14
        pos += bar
        idx += 1

    vinilo = np.convolve(np.random.default_rng(11).standard_normal(n),
                         np.ones(10) / 10, "same") * 0.012
    mezcla += vinilo

    mezcla = np.tanh(mezcla * 1.4) * 0.85
    fi, fo = int(0.3 * SR), int(1.4 * SR)
    mezcla[:fi] *= np.linspace(0, 1, fi)
    mezcla[-fo:] *= np.linspace(1, 0, fo)
    return (mezcla * 32767).astype(np.int16)


def main():
    num = sys.argv[1] if len(sys.argv) > 1 else "1"
    if num not in VIDEOS:
        sys.exit(f"Video desconocido: {num}. Disponibles: {', '.join(VIDEOS)}")
    por_defecto, segmentos = VIDEOS[num]
    salida = sys.argv[2] if len(sys.argv) > 2 else por_defecto
    duracion = sum(d for d, _, _ in segmentos)

    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    print(f"🎵 Sintetizando música lo-fi ({duracion:.1f} s)...")
    audio = musica_lofi(duracion)
    wav_path = tempfile.mktemp(suffix=".wav")
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(audio.tobytes())

    print("🎨 Renderizando frames y codificando...")
    bg = fondo_grande()
    total = int(duracion * FPS)

    proc = subprocess.Popen(
        [ffmpeg, "-y",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-i", wav_path,
         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "160k", "-shortest", salida],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for k in range(total):
        frame = dibujar_frame(k / FPS, bg, segmentos, duracion)
        proc.stdin.write(np.asarray(frame, dtype=np.uint8).tobytes())
        if k % (FPS * 5) == 0:
            print(f"  {k}/{total} frames ({k / FPS:.0f} s)")

    proc.stdin.close()
    proc.wait()
    print(f"✅ Video listo: {salida} ({duracion:.1f} s, {W}x{H}, {FPS} fps)")


if __name__ == "__main__":
    main()
