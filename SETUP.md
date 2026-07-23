# 🔴 Archivo Rojo — Configuración: Shorts automáticos en YouTube

Este repositorio genera y publica un YouTube Short de **Archivo Rojo**
(casos de crímenes sin resolver) **cada día, automáticamente**:

```
Guion (cola o Claude) → Voz (ElevenLabs) → Video con subtítulos (ffmpeg) → YouTube
```

Solo tienes que configurarlo **una vez**. Después, no tocas nada.

---

## Paso 1 — Clave de ElevenLabs (2 minutos)

1. Entra en [elevenlabs.io](https://elevenlabs.io) → tu perfil → **API Keys**.
2. Copia tu clave.
3. (Opcional) Elige una voz en **Voices** y copia su *Voice ID*. Si no, se usa una voz multilingüe por defecto.

## Paso 2 — Credenciales de YouTube (10 minutos, solo una vez)

1. Entra en [Google Cloud Console](https://console.cloud.google.com) y crea un proyecto (ej: `youtube-shorts-bot`).
2. En **APIs y servicios → Biblioteca**, busca **YouTube Data API v3** y actívala.
3. En **APIs y servicios → Pantalla de consentimiento OAuth**: tipo *Externo*, añade tu correo como *usuario de prueba*.
4. En **Credenciales → Crear credenciales → ID de cliente OAuth**: tipo **Aplicación de escritorio**. Copia el *Client ID* y el *Client Secret*.
5. En tu computadora (necesitas Python instalado):

   ```bash
   pip install google-auth-oauthlib
   YT_CLIENT_ID="tu_client_id" YT_CLIENT_SECRET="tu_client_secret" python automation/get_youtube_token.py
   ```

   Se abrirá el navegador: inicia sesión con **la cuenta de tu canal de YouTube** y acepta.
6. Copia el **refresh token** que se imprime en la terminal.

## Paso 3 — Guardar los secretos en GitHub (3 minutos)

En este repositorio: **Settings → Secrets and variables → Actions → New repository secret**.

| Secreto | Valor | ¿Obligatorio? |
|---|---|---|
| `ELEVENLABS_API_KEY` | Tu clave de ElevenLabs | ✅ Sí |
| `ELEVENLABS_VOICE_ID` | ID de la voz que quieras | Opcional |
| `YT_CLIENT_ID` | Client ID de Google Cloud | ✅ Sí |
| `YT_CLIENT_SECRET` | Client Secret de Google Cloud | ✅ Sí |
| `YT_REFRESH_TOKEN` | El token del Paso 2 | ✅ Sí |
| `ANTHROPIC_API_KEY` | Clave de la API de Claude | Opcional* |

\* Sin ella, el sistema publica los 8 casos que ya vienen en `content/queue.json` (D.B. Cooper, el robo Gardner, la mujer de Isdal...) y luego se detiene. Con ella, **genera casos nuevos infinitamente** cuando la cola se vacía, siguiendo el estilo Archivo Rojo (casos reales, sin morbo, con giro final).

## Paso 4 — Probar

1. Ve a **Actions → Publicar Short en YouTube → Run workflow**.
2. Marca la casilla **"Modo prueba"** la primera vez: genera el video y lo deja como *artefacto* descargable, sin subirlo. Descárgalo y revisa que te guste.
3. Cuando estés conforme, vuelve a ejecutarlo **sin** la casilla: se publicará en tu canal.

A partir de ahí se ejecuta solo **todos los días a las 15:00 UTC** (edita el `cron` en `.github/workflows/publish-short.yml` para cambiar la hora).

---

## Personalización

- **Guiones propios**: añade entradas a `content/queue.json` (campos: `id`, `titulo`, `descripcion`, `guion`, `tags`, `publicado: null`). La cola siempre tiene prioridad sobre la generación automática.
- **Temas de la IA**: edita `generacion_automatica.temas` en `content/config.json`.
- **Fondos de video**: sube archivos `.mp4` a `assets/backgrounds/` y se usarán en lugar del degradado animado (se recortan automáticamente a 1080x1920).
- **Colores del degradado**: `video.colores_fondo` en `content/config.json`.
- **Privacidad**: cambia `canal.privacidad` a `"unlisted"` si quieres revisar los videos antes de hacerlos públicos.

## Estructura

```
automation/
  run_pipeline.py      # Orquestador principal
  generate_script.py   # Elige guion de la cola o lo genera con Claude
  tts.py               # Voz + tiempos por palabra (ElevenLabs)
  make_video.py        # Subtítulos .ass + montaje con ffmpeg
  upload_youtube.py    # Subida a YouTube (API v3)
  get_youtube_token.py # Helper de un solo uso para el refresh token
content/
  config.json          # Configuración general
  queue.json           # Cola de guiones (estado de publicación)
.github/workflows/
  publish-short.yml    # Ejecución diaria automática
```

## Límites a tener en cuenta

- **YouTube API**: la cuota gratuita diaria (10.000 unidades) permite ~6 subidas al día. Un video diario va sobrado.
- **ElevenLabs**: cada Short usa ~700–900 caracteres de tu cuota mensual.
- Mientras tu app OAuth esté en modo "prueba" en Google Cloud, el refresh token caduca a los 7 días. Para que dure indefinidamente, publica la app (**Pantalla de consentimiento OAuth → Publicar aplicación**; no requiere verificación para uso propio).
