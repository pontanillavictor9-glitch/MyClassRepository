"""Shorts Studio — generador de prompts para crear YouTube Shorts con IA.

Te hace unas pocas preguntas (tema, audiencia, nicho, etc.) y genera un
archivo Markdown con los 12 prompts del playbook (+ el prompt maestro bonus)
ya rellenados, listos para pegar en Claude o ChatGPT.

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
        """Crea la descripción perfecta para un Short sobre {tema}.

Incluye:
- Primera línea con la palabra clave exacta
- 3 líneas de gancho
- 15 hashtags (5 grandes, 5 medianos, 5 de nicho)""",
    ),
    (
        "Paso 8 — Ideas para 30 días",
        "El problema no es hacer 1 Short, es hacer 100.",
        """Dame 30 ideas de Shorts sobre {nicho} para los próximos 30 días.

Cada idea debe incluir:
- Un título
- Un gancho en una línea
- Un ángulo único

No repitas los conceptos.
Mezcla los conceptos educativos / virales / controvertidos.""",
    ),
    (
        "Paso 9 — Reciclar contenido largo",
        "1 vídeo largo = 10 Shorts.",
        """Analiza este guion largo y extrae 10 Shorts independientes.

Para cada uno:
- Un gancho propio
- Un inicio y un final autónomos
- Entre 30 y 60 segundos

Guion: [PEGA AQUÍ TU CONTENIDO LARGO]""",
    ),
    (
        "Paso 10 — Monetizar más allá de AdSense",
        "AdSense es solo el comienzo, no el final.",
        """Soy creador de Shorts en el nicho {nicho} con {suscriptores} suscriptores.
Dame 7 formas de monetizar AHORA MISMO.
Clasifícalas por: ingresos realistas del primer mes + facilidad de implementación.
Sin teoría. Ejemplos concretos.""",
    ),
    (
        "Paso 11 — Analizar la competencia",
        "No reinventes la rueda. Copia lo que ya funciona.",
        """Analiza estos 5 canales de Shorts sobre {nicho}: {canales}.

Dame:
- Los puntos en común en sus hooks
- La estructura de sus títulos
- Lo que hacen diferente aquellos que crecen más rápido
- 3 oportunidades que puedo explotar yo mismo""",
    ),
    (
        "Paso 12 — Calendario de publicación",
        "Publicar cuando quieras = algoritmo en tu contra.",
        """Crea un calendario de publicación de 30 días para un canal de Shorts sobre {nicho}.

Incluye:
- La mejor hora según el huso horario {huso}
- La frecuencia óptima
- Diferentes formatos cada semana""",
    ),
    (
        "BONUS — El prompt maestro",
        "Conecta los 12 anteriores. Pégalo en Claude y tienes un canal.",
        """Actúa como mi estratega de YouTube Shorts.
Con mi nicho {nicho}, crea un plan de 90 días que combine:
guiones, ganchos, títulos y monetización.
Preséntalo en forma de calendario semanal accionable.""",
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
    nicho = preguntar("¿Cuál es tu nicho?", tema)
    suscriptores = preguntar("¿Cuántos suscriptores tienes?", "0")
    canales = preguntar(
        "5 canales de referencia de tu nicho (separados por comas)",
        "[BUSCA 5 CANALES DE TU NICHO]",
    )
    huso = preguntar("¿Cuál es tu huso horario?", "GMT-5 (Perú/Colombia/México)")

    datos = {
        "tema": tema,
        "audiencia": audiencia,
        "edad": edad,
        "intereses": intereses,
        "nicho": nicho,
        "suscriptores": suscriptores,
        "canales": canales,
        "huso": huso,
    }

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
