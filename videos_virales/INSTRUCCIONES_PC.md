# Qué tienes que hacer en tu PC, paso a paso

Este proyecto vive en el repositorio **MyClassRepository** (aparte del baloncesto).
Objetivo: **Shorts de ASMR imposible listos para subir a YouTube**.

## Paso 0 — Traer estos archivos a tu PC (2 minutos)

1. Abre **GitHub Desktop**.
2. Si aún no tienes **MyClassRepository** en el PC: File → Clone repository →
   elige `pontanillavictor9-glitch/MyClassRepository` → Clone.
3. Arriba, en "Current branch", elige la rama
   **`claude/sedaance-video-montaje-ntltx2`**.
4. Dale a **"Pull origin"** (o "Fetch origin" y luego "Pull").
5. Ya tienes la carpeta `videos_virales` con el plan, los prompts y esto.

## Paso 1 — Instalar Claude Code en el PC (una sola vez, 5 minutos)

1. Abre Chrome y ve a **https://claude.com/claude-code**.
2. Descarga la **aplicación de escritorio para Windows** y ábrela cuando termine
   (instalación normal: Siguiente → Siguiente → Finalizar).
3. Al abrirla, **inicia sesión con tu cuenta de Claude** (la misma que usas para
   hablar conmigo). No hace falta configurar nada más.

## Paso 2 — Preparar las carpetas (1 minuto)

Dentro de `MyClassRepository\videos_virales`, crea dos carpetas vacías
(clic derecho → Nuevo → Carpeta):

- `clips`   ← aquí guardarás lo que descargues de Higgsfield
- `listos`  ← aquí dejará Claude los Shorts terminados

## Paso 3 — Generar los clips en Higgsfield (esto es lo tuyo)

1. Abre **Higgsfield** en Chrome con tu cuenta.
2. Abre el archivo `PROMPTS.md` (doble clic; se abre con el Bloc de notas si hace falta).
3. Copia el primer prompt en inglés, pégalo en Higgsfield.
   - Formato **vertical 9:16**, duración 5-10 segundos.
   - Si puedes elegir modelo, usa uno **con audio** (por ejemplo Veo 3):
     el sonido ASMR saldrá ya puesto. Si sale mudo, no pasa nada —
     Claude le pondrá el audio después.
4. Cuando el clip esté listo, **descárgalo** y guárdalo en la carpeta `clips`
   con el número del prompt: `clip_A1.mp4`, `clip_A2.mp4`, etc.
5. Si un clip sale raro (corte falso, texturas que tiemblan), no lo guardes:
   regenera. Mejor 5 clips buenos que 20 regulares.
6. Con **5-10 clips ya se puede empezar**. No hace falta hacerlos todos hoy.

## Paso 4 — Lanzar a Claude en tu PC y dejarlo trabajando

1. Abre la aplicación de **Claude Code**.
2. Cuando pregunte por la carpeta de trabajo, elige
   **`MyClassRepository\videos_virales`**.
3. Copia y pega este mensaje tal cual:

```
Lee PLAN.md y PROMPTS.md de esta carpeta. En la carpeta clips/ tienes los vídeos
que he generado con Higgsfield. Tu trabajo es dejarme Shorts de YouTube
terminados:
1) Revisa cada clip y descarta los que tengan fallos visuales evidentes.
2) Deja todos en vertical 9:16, buena calidad, y menos de 60 segundos.
3) Si algún clip no tiene sonido, móntale un audio ASMR que encaje (crujidos
   de cristal, goteos, etc.). Instala ffmpeg tú mismo si hace falta, tienes
   mi permiso.
4) Recorta cada uno para que la acción empiece en el primer segundo, sin intro.
5) Si varios clips cortos combinan bien, haz también alguna versión uniendo
   3-4 en un solo Short.
6) Deja los vídeos terminados en la carpeta listos/, numerados, y un archivo
   PUBLICAR.md con el orden de subida y, para cada Short, el título y la
   descripción con hashtags para YouTube Shorts.
Trabaja tú solo hasta acabar. Yo no estaré delante.
```

4. Y ya está: te puedes ir. Cuando vuelvas, en la carpeta `listos` tendrás los
   Shorts preparados y `PUBLICAR.md` con títulos y descripciones para copiar y pegar.

## Paso 5 — Publicar en YouTube Shorts (lo tuyo otra vez, 5 minutos al día)

1. Pásate los vídeos de `listos` al móvil (por WhatsApp a ti mismo, por ejemplo,
   o con el cable).
2. En la app de YouTube: botón **+** → **Crear un Short** → sube el vídeo →
   pega el título y la descripción que diga `PUBLICAR.md`.
3. **Uno al día, todos los días.** La constancia es el 80 % del éxito.
   (El mismo vídeo también lo puedes subir a TikTok e Instagram Reels gratis —
   mismo esfuerzo, triple alcance.)

## Dudas rápidas

- **¿Puedo hacerlo en varios días?** Sí. Genera clips cuando quieras, guárdalos en
  `clips`, y vuelve a lanzar el mismo mensaje del Paso 4: Claude solo procesará
  los nuevos.
- **¿Y si Claude me pregunta permisos al trabajar?** Dale a permitir para acciones
  dentro de la carpeta del proyecto. Es normal la primera vez.
- **¿Esto toca algo del baloncesto / Más Allá del Acta?** No. Está en otro
  repositorio y no se mezcla con nada de la web.
