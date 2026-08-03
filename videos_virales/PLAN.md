# Plan: Canal viral de ASMR imposible (Higgsfield)

## La idea en una frase

Vídeos cortos verticales (9:16, 5-10 segundos) de **cosas imposibles pero increíblemente
satisfactorias**: cortar fruta de cristal, metales que se funden como miel, texturas que
no existen en la realidad. Sin caras, sin idioma, sin voz — audiencia mundial.

## Por qué funciona este nicho

- **Retención altísima**: la gente lo mira en bucle, y la retención es LA métrica que
  los algoritmos de TikTok / Instagram Reels / YouTube Shorts premian.
- **Sin idioma**: un vídeo sirve para todo el planeta.
- **Barato y en serie**: un mismo estilo genera cientos de vídeos; solo cambia el objeto.
- **El sonido es la mitad del truco**: el "crunch" del cristal, el goteo del metal
  fundido. Por eso los prompts llevan el sonido descrito.

## El sonido

- **Opción A (recomendada):** en Higgsfield, elegir un modelo que genere audio nativo
  (p. ej. Veo 3). El prompt ya describe el sonido y sale sincronizado con la imagen.
- **Opción B:** si el clip sale mudo, Claude le añade el sonido ASMR en el montaje
  (bibliotecas de sonido libres + ffmpeg). Guardar el clip igualmente.

## Identidad de la serie (para que el canal se reconozca)

Todos los clips comparten el mismo "look" (ya va incluido en cada prompt):

- Fondo negro mate de estudio, iluminación dramática de un solo foco.
- Macro extremo (la cámara muy cerca del objeto).
- Cámara lenta sutil.
- Sin manos humanas visibles salvo guantes negros cuando haga falta sostener el cuchillo.
- Sin texto en pantalla (en este nicho el texto distrae; el gancho es la textura).

## Calendario de publicación

- **1 vídeo al día, mínimo 30 días seguidos.** La constancia gana a la genialidad.
  Los primeros 10-15 vídeos suelen hacer poco; el algoritmo tarda en encontrar tu audiencia.
- Publicar el MISMO vídeo en TikTok, Instagram Reels y YouTube Shorts (triple alcance,
  mismo esfuerzo). Subirlo nativo a cada app, no compartir enlaces.
- Mejor hora: tarde-noche española (18:00–23:00), pero la constancia importa más que la hora.
- Nombre de canal sugerido: algo corto, pronunciable y sin significado local
  (p. ej. "GlassCut", "MeltLab", "CrystalCrush" — comprobar que esté libre).

## Control de calidad antes de publicar (30 segundos por clip)

1. ¿La física "engaña"? Si el corte parece falso o la textura tiembla → descartar y regenerar.
2. ¿El sonido acompaña? Un ASMR con mal audio muere.
3. ¿El primer segundo engancha? El corte/acción debe empezar YA, sin intro.
4. ¿Bucle limpio? Si el final conecta con el principio, mejor (la gente lo ve 2-3 veces).

## Métricas: qué mirar la primera semana

- **Retención media** (lo más importante): si un formato retiene >80 %, hacer 5 variantes más.
- **Compartidos y guardados**: señal de que el formato es ganador.
- No obsesionarse con seguidores al principio: en Shorts/Reels los vídeos vuelan solos.

## Reparto de trabajo

| Quién | Qué |
|---|---|
| Victor | Pegar prompts en Higgsfield, descargar los clips a la carpeta `clips/` |
| Claude (en el PC) | Revisar clips, recortar a 9:16 si hace falta, añadir/ajustar sonido, dejar los vídeos listos en `listos/`, proponer nuevos prompts según lo que funcione |

## Línea roja

Nada de personas reales reconocibles, marcas, ni contenido que parezca noticia real.
Las plataformas lo detectan y penalizan el canal entero.
