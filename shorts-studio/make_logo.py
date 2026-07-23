"""Genera variantes de logo para el canal, con la misma identidad visual de los videos.

Produce PNG de 1024x1024 (dibujados a 2048 y reducidos para suavizar bordes),
pensados para la foto de perfil de YouTube (se recorta en círculo).

Uso:
    python make_logo.py
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont

S = 2048          # tamaño de dibujo (supermuestreo 2x)
OUT = 1024        # tamaño final
C = S // 2        # centro
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

BLANCO = (236, 237, 239)
GRIS = (154, 160, 173)
ROJO = (255, 92, 92)
AMBAR = (255, 197, 61)
ORO = (196, 148, 32)
OSCURO = (24, 26, 33)


def fondo():
    """Fondo circular-friendly: degradado radial oscuro con brillo rojo arriba."""
    y = np.linspace(0, 1, S)[:, None, None]
    base = np.array([20, 22, 28]) * (1 - y) + np.array([32, 36, 48]) * y
    img = np.broadcast_to(base, (S, S, 3)).astype(np.float64).copy()
    yy, xx = np.mgrid[0:S, 0:S]
    glow = np.exp(-(((xx - S * 0.5) ** 2) / (S * 0.55) ** 2
                    + ((yy - S * 0.25) ** 2) / (S * 0.38) ** 2))
    img += glow[:, :, None] * np.array([64, 16, 16])
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def texto_centrado(d, texto, f, cx, cy, color):
    ancho = d.textlength(texto, font=f)
    caja = f.getbbox(texto)
    d.text((cx - ancho / 2, cy - (caja[1] + caja[3]) / 2), texto, font=f, fill=color)


def guardar(img, nombre):
    img.resize((OUT, OUT), Image.LANCZOS).save(nombre)
    print(f"✅ {nombre}")


def variante_a():
    """Moneda dorada con flecha de crecimiento — 'tu dinero sube'."""
    img = fondo()
    d = ImageDraw.Draw(img)
    d.ellipse([100, 100, S - 100, S - 100], outline=AMBAR, width=26)

    d.ellipse([C - 620, C - 130, C + 60, C + 550], fill=ORO, outline=AMBAR, width=42)
    texto_centrado(d, "$", ImageFont.truetype(FONT_PATH, 420), C - 280, C + 210, OSCURO)

    d.line([C - 160, C + 90, C + 470, C - 420], fill=ROJO, width=110)
    d.polygon([(C + 640, C - 560), (C + 300, C - 510), (C + 570, C - 240)], fill=ROJO)
    return img


def variante_b():
    """Monograma $ gigante — minimalista, legible en tamaño pequeño."""
    img = fondo()
    d = ImageDraw.Draw(img)
    d.ellipse([100, 100, S - 100, S - 100], outline=ROJO, width=30)
    d.ellipse([170, 170, S - 170, S - 170], outline=(255, 92, 92, 60), width=6)
    texto_centrado(d, "$", ImageFont.truetype(FONT_PATH, 1250), C, C - 20, AMBAR)
    # barra de progreso característica de los videos
    d.rectangle([C - 420, C + 640, C + 420, C + 690], fill=(255, 255, 255, 30))
    d.rectangle([C - 420, C + 640, C + 180, C + 690], fill=ROJO)
    return img


def variante_c():
    """Botón de play + moneda — 'Shorts de dinero'."""
    img = fondo()
    d = ImageDraw.Draw(img)
    d.ellipse([100, 100, S - 100, S - 100], outline=GRIS, width=18)

    # Play rojo
    d.polygon([(C - 380, C - 480), (C - 380, C + 480), (C + 450, C)], fill=ROJO)

    # Moneda como insignia abajo a la derecha
    d.ellipse([C + 90, C + 130, C + 690, C + 730], fill=ORO, outline=AMBAR, width=40)
    texto_centrado(d, "$", ImageFont.truetype(FONT_PATH, 400), C + 390, C + 430, OSCURO)
    return img


if __name__ == "__main__":
    guardar(variante_a(), "logo-a-moneda-flecha.png")
    guardar(variante_b(), "logo-b-monograma.png")
    guardar(variante_c(), "logo-c-play-moneda.png")
