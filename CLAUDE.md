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

- [x] Episodio 001 "Why Can't You Remember Being a Baby?" — guion EN escrito.
- [ ] Episodio 001 — audio ElevenLabs pendiente (el usuario elegirá la voz).
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
