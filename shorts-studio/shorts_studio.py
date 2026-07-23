"""Shorts Studio — generador de prompts para crear YouTube Shorts con IA.

Te hace unas pocas preguntas (tema, audiencia, edad, intereses) y genera un
archivo Markdown con los 7 prompts del playbook ya rellenados, listos para
pegar en Claude o ChatGPT.

Uso:
    python shorts_studio.py
"""

import re
import unicodedata

PROMPTS = [
    (
        "Paso 1 — Elegir el nicho correcto",
        "El 90 % fracasa por elegir mal el nicho.",
        """Tengo {edad} años y me intereso en {intereses}.
Dame los 5 nichos de Shorts con el CPM más alto.

Incluye:
- La competencia
- Los ingresos reales a 10K suscriptores
- Cuál empezar HOY sin dinero

Clasifícalos por velocidad de monetización.""",
    ),
    (
        "Paso 2 — Escribir el guion",
        "Un Short sin guion es un Short muerto.",
        """Escribe un guion de Short de 45 segundos sobre {tema} para {audiencia}.

Incluye:
- Un gancho en los primeros 3 segundos
- 3 puntos clave con datos
- Un llamado a la acción final que genere comentarios

Tono conversacional, frases cortas.""",
    ),
    (
        "Paso 3 — Generar ganchos",
        "Si pierdes al espectador en 3 segundos, lo pierdes todo.",
        """Dame 20 ganchos de una sola línea para un Short sobre {tema}.
5 de curiosidad. 5 de impacto. 5 de pregunta directa. 5 de promesa fuerte.
Cada gancho debe tener menos de 10 palabras y sonar como lo diría un humano real.""",
    ),
    (
        "Paso 4 — Elegir el título",
        "El título decide si hacen clic... o si te ignoran.",
        """Genera 15 títulos para un Short sobre {tema}.
5 con un número. 5 en forma de pregunta. 5 con una tensión emocional.
Menos de 60 caracteres.
Añade cuál tiene el mayor potencial viral y por qué.""",
    ),
    (
        "Paso 5 — Adaptar para voz de IA",
        "No necesitas tu voz. Ni mostrarte a la cámara.",
        """Adapta este guion para una voz en off generada por IA (ElevenLabs o similar).
Indica las pausas con [...], los acentos con MAYÚSCULAS
y las emociones entre paréntesis.

Guion: [PEGA AQUÍ EL GUION DEL PASO 2]""",
    ),
    (
        "Paso 6 — Optimizar la retención",
        "El algoritmo recompensa a aquellos que se quedan hasta el final.",
        """Reorganiza este guion para una retención máxima en Shorts.

Añade:
- Un bucle al principio y al final
- Un cliffhanger a los 15 segundos
- Un giro a los 30 segundos

Dame la versión optimizada segundo a segundo.

Guion: [PEGA AQUÍ EL GUION DEL PASO 2]""",
    ),
    (
        "Paso 7 — Descripción con SEO",
        "Tu descripción es SEO gratis. La mayoría de la gente lo desperdicia.",
        """Escribe la descripción de YouTube para un Short sobre {tema}
dirigido a {audiencia}.

Incluye:
- Las 2 primeras líneas con las palabras clave principales
- 3 a 5 hashtags relevantes del nicho
- Una pregunta final que invite a comentar

Máximo 150 palabras.""",
    ),
]


def preguntar(mensaje, por_defecto):
    respuesta = input(f"{mensaje} [{por_defecto}]: ").strip()
    return respuesta or por_defecto


def nombre_archivo(tema):
    limpio = unicodedata.normalize("NFKD", tema).encode("ascii", "ignore").decode()
    limpio = re.sub(r"[^a-zA-Z0-9]+", "-", limpio).strip("-").lower()
    return f"mi-short-{limpio or 'sin-tema'}.md"


def main():
    print("🎬 Shorts Studio — generador de prompts\n")

    tema = preguntar("¿Sobre qué tema es tu Short?", "finanzas personales")
    audiencia = preguntar("¿Quién es tu audiencia?", "jóvenes de 18 a 25 años")
    edad = preguntar("¿Cuántos años tienes? (para el paso de nicho)", "25")
    intereses = preguntar("¿Cuáles son tus intereses?", "tecnología, dinero, deporte")

    datos = {"tema": tema, "audiencia": audiencia, "edad": edad, "intereses": intereses}

    lineas = [
        f"# 🎬 Prompts para tu Short: {tema}",
        "",
        f"- **Audiencia:** {audiencia}",
        f"- **Intereses:** {intereses}",
        "",
        "Copia cada prompt (en orden) y pégalo en Claude o ChatGPT.",
        "",
    ]

    for titulo, lema, plantilla in PROMPTS:
        lineas += [
            f"## {titulo}",
            "",
            f"> {lema}",
            "",
            "```",
            plantilla.format(**datos),
            "```",
            "",
        ]

    archivo = nombre_archivo(tema)
    with open(archivo, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

    print(f"\n✅ Listo. Se creó el archivo: {archivo}")
    print("Ábrelo y ve copiando los prompts en orden. ¡A grabar (sin cámara)! 🚀")


if __name__ == "__main__":
    main()
