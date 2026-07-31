# Proyecto: Canal de vídeos explicativos (EN + ES)

## Qué es esto

Dos canales de YouTube con el mismo contenido: explainers animados de ~8 min
estilo monigotes (stick figures), títulos-pregunta de curiosidad
("Why Do Mosquitoes Always Bite YOU?"), temáticas de psicología (efectos con
nombre), biología curiosa e historia. Un canal en inglés y otro en español.
Se empieza por el inglés.

## Reglas de trabajo

- **El usuario lleva el ritmo.** No adelantarse a generar cosas que no ha
  pedido; él va dando cada paso.
- La voz la elige el usuario en ElevenLabs (tiene cuenta de pago y otro
  proyecto donde ya la usa). No elegir voz por él.
- Idioma de trabajo con el usuario: español.
- **Todo lo que se haga se sube a GitHub.** Al terminar cada paso (guion
  nuevo, cambio de estructura, notas), commit + push a `origin` para que el
  trabajo esté igual en local y en GitHub.

## Identidad del canal EN

- **Nombre**: Why Is That Though?
- **Handle**: `@whyisthatthough` (comprobado libre el 31-07-2026).
- Canal reutilizado: ya existía vacío, sin vídeos ni suscriptores.
- Avatar y banner en `Canal - imagenes/canal/` (`avatar.png` 800×800,
  `banner.png` 2560×1440 con el texto en la zona segura de 1235×338).
- El texto del banner se superpone con ffmpeg (fuente Impact, negro con
  borde blanco), no se le pide al modelo de imagen.

## Especificación de cada episodio

- **Longitud**: la narración (solo líneas `NARRATION`) debe sumar
  **9.000–10.000 caracteres**. Equivale a ~1.500–1.700 palabras y ~10 min
  de audio. Comprobarlo antes de generar voz con:
  `node scripts/extract-narration.mjs <script-en.md> --out salida.txt`
- **Ritmo de producción objetivo**: 1 episodio al día.
- **Temáticas**: psicología (efectos con nombre), biología curiosa e
  historia. Título-pregunta de curiosidad en segunda persona.

## Voz del canal EN (fijada)

- **Liam** — `voice_id: TX3LPaxmHKxFdv7VOQHJ` (hombre, americano, joven,
  enérgico). Elegida por el usuario el 31-07-2026.
- Modelo: `eleven_multilingual_v2`.
- Ajustes: stability `0.5`, similarity_boost `0.75`, style `0.0`,
  speaker_boost `true` (ya están en `scripts/tts.mjs`).
- Para el canal ES habrá que elegir una voz nativa distinta: Liam hablaría
  español con acento inglés.

## Imágenes (Higgsfield)

- Cuenta: **plan Plus, 1.200 créditos/mes** (47 €). Contratado el 31-07-2026.
- Modelo por defecto: **`z_image`** — 0,15 créditos/imagen. A 40 imágenes por
  vídeo son 6 créditos (~0,23 €), unos 180 créditos al mes. Sobra margen.
- `gpt_image_2` (el que pide el prompt original) cuesta **7 créditos/imagen**:
  280 por vídeo. Inviable para el ritmo diario, no usarlo por defecto.
- `nano_banana_2_lite` (1 crédito): **descartado**. En la comparativa salió
  con línea fina, colores apagados y solo 1376×768. Cuesta 6× más que
  z_image y se ve peor.
- **Reparto recomendado**: `z_image` para el grueso del vídeo y
  `gpt_image_2` para la portada y las 2-3 imágenes clave (es el único que
  compone bien escenas con varias cosas pasando a la vez, y da 2688×1520).
  Sale a ~27 créditos/vídeo → ~800 al mes con 30 vídeos.
- **Regla de estilo aprendida en las pruebas**: color plano en la ropa y los
  objetos (camisetas, cunas, sábanas, muebles), pero **las personas siempre
  monigote blanco de línea negra** — cabeza redonda, ojos de punto,
  extremidades de línea. Si se pide "bebé con color" sin más, el modelo
  deriva a ilustración infantil bonita y se sale del estilo del canal.
- **El texto dentro de la imagen sí sale bien** si la escena se describe con
  detalle: los tres modelos escribieron "HIPPOCAMPUS" correctamente. El
  "HIPOCAMPS" de la primera prueba vino de un prompt demasiado vago.
  Aun así, para el texto de la portada es más seguro superponerlo con
  ffmpeg que pedírselo al modelo.
- Aspect ratio siempre `16:9`.

### Portadas (miniaturas) — FÓRMULA FIJA

Esta fórmula sale de comparar nuestra primera portada (mala) con las de los
dos canales de referencia (`prueba2.png`, `prueba3.png`). **Aplicarla a
todos los episodios.** Lo que la hace funcionar es que a 200 píxeles solo se
lee una cara con expresión; un objeto detallado no se lee.

1. **Un monigote grande y de frente**, con la cabeza ocupando alrededor de un
   tercio del alto de la imagen, mirando al espectador con una expresión
   clara (agobio, susto, duda). Nunca de espaldas, nunca pequeño.
2. **El objeto que cuenta la historia, diminuto y simple** — un chupete en el
   suelo, no una cuna entera. El objeto contextualiza; la cara vende.
3. **Fondo en dos bandas planas**: cielo de color pálido arriba (crema,
   amarillo claro, azul) y una franja de suelo abajo (verde, marrón). Nada
   de un color plano vacío.
4. **Texto de borde a borde**, en el tercio superior, fuente Impact, 2-4
   palabras. Negro con borde blanco sobre fondo claro; amarillo con borde
   negro sobre fondo oscuro.
5. **El texto NO repite el título.** Lo complementa: título "Why Can't You
   Remember Being a Baby?" + portada "WHO WERE YOU?".
6. Dejar el tercio superior del dibujo **vacío** al generarlo, para que el
   texto no tape nada.

- Generar el dibujo con `gpt_image_2` y **superponer el texto con ffmpeg**,
  nunca pedírselo al modelo.
- YouTube: 1280×720, máximo 2 MB.
- Duración de los vídeos de referencia: 3:58 a 12:58. La nuestra ~10 min.
- Comandos: `higgsfield generate cost <modelo> --prompt "..."` para estimar y
  `higgsfield generate create <modelo> --aspect_ratio 16:9 --prompt "..." --wait`
  para generar. Requiere workspace fijado:
  `higgsfield workspace set 949630f0-298a-45ad-82a0-7d9690a1353d`.

## Scripts de utilidad

- `scripts/list-voices.mjs` — lista las voces de la cuenta con sus IDs.
- `scripts/extract-narration.mjs` — saca del guion solo lo que se locuta,
  y da el recuento de caracteres/palabras/duración estimada.
- `scripts/tts.mjs` — genera el mp3. Todos leen la key del `.env`.

## Estructura

```
Canal - imagenes/
└── episodio-XXX-titulo/
    ├── script-en.md   ← guion; las líneas NARRATION van a ElevenLabs tal
    │                    cual, las líneas VISUAL son dirección de animación
    └── audio-en.mp3   ← voz generada con ElevenLabs (el usuario la usa
                         para montar el vídeo)
```

Flujo por episodio: guion → ElevenLabs (párrafo a párrafo, modelo
multilingüe para reutilizar la misma voz en ES) → audio en la carpeta del
episodio → el usuario monta el vídeo.

## Estado (actualizar al avanzar)

- [x] Voz del canal EN elegida: Liam.
- [x] Episodio 001 "Why Can't You Remember Being a Baby?" — guion EN reescrito
      en narración pura (10.098 caracteres) y audio generado
      (`audio-en.mp3`, 10:37, un único mp3 continuo).
- [x] Pruebas de estilo de imagen hechas (`pruebas-imagen/`): 6 en blanco y
      negro y 4 con color. La buena de referencia es `C1-color-bebe-y-adulto`.
- [x] **Episodio 001 publicado**: `6GhGOCW_1NQ`, 39 escenas, portada y
      subtítulos puestos, programado para el 31-07-2026 a las 18:00 (España).
- [x] TurboScribe eliminado del flujo: `scripts/tts-timestamps.mjs` devuelve
      audio y marcas de tiempo en la misma llamada a ElevenLabs.
- [x] Subida a YouTube automatizada (`scripts/subir-youtube.mjs`). La
      programación con `publishAt` **sí funciona** aunque el proyecto de
      Google no esté auditado.
- Requisitos que costaron un rato y conviene recordar: la cuenta del canal
  (`zhaaall1234@gmail.com`) debe estar en *Usuarios de prueba* del proyecto
  de Google Cloud, y el canal debe estar **verificado por teléfono** o
  YouTube rechaza las miniaturas personalizadas.
- Rama de trabajo: `claude/higgsfield-cli-auth-6u1tz7`.

## Notas técnicas

- ElevenLabs: la API key del usuario debe estar disponible como variable de
  entorno `ELEVENLABS_API_KEY` (pedírsela si no está). No guardar claves ni
  tokens en el repositorio.
- En el entorno remoto de Claude Code web, `api.elevenlabs.io` está
  bloqueado por la política de red; en la máquina local del usuario no hay
  ese bloqueo.
- Higgsfield CLI: instalación y login persistente documentados en
  `docs/HIGGSFIELD_SETUP.md` (cuenta free, quedan 2 créditos — no lanzar
  generaciones sin confirmar coste con `higgsfield generate cost`).
