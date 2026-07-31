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
- [ ] Episodio 001 — pendiente: el usuario sube el mp3 a TurboScribe, pega
      aquí la transcripción con timestamps, y de ahí salen las descripciones
      de imagen (una por timestamp) para generar con Higgsfield.
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
