# Higgsfield CLI — instalación y login persistente

Estado a 2026-07-31: login completado como `pontanillavictor9@gmail.com`
(workspace "Private", id `949630f0-298a-45ad-82a0-7d9690a1353d`, plan free).

Este documento explica cómo dejar el CLI de Higgsfield autenticado en
sesiones nuevas de Claude Code web, donde el contenedor es efímero y el
archivo de credenciales se pierde al cerrar la sesión.

## 1. Instalación

```bash
npm i -g @higgsfield/cli
```

Tarda varios minutos. Para no repetirla en cada sesión, añádela al
**setup script del entorno** en la configuración de Claude Code web
(Environment settings), no a un hook de SessionStart (los hooks tienen
timeout corto).

## 2. Login interactivo (solo la primera vez, o si caducan las credenciales)

El flujo OAuth necesita un navegador y un callback local:

1. Ejecutar `higgsfield auth login` en segundo plano dentro de la sesión.
2. El CLI imprime una URL de `https://clerk.higgsfield.ai/oauth/authorize?...`.
   Abrirla en el navegador del usuario e iniciar sesión.
3. El navegador redirige a `http://localhost:8765/callback?code=...&state=...`
   y muestra un error de conexión (normal: el servidor local corre en el
   contenedor, no en la máquina del usuario).
4. Pegar esa URL completa en el chat; Claude la completa dentro del
   contenedor con `curl "<url>"`. Ojo: el parámetro `state` debe coincidir
   exactamente con el de la URL de autorización (al copiar puede truncarse).
5. El CLI escribe `~/.config/higgsfield/credentials.json` y responde
   "Successfully authenticated".
6. Seleccionar workspace: `higgsfield workspace set <workspace_id>`
   (listar con `higgsfield workspace list`). Sin workspace, `generate`
   falla con "No workspace selected".

## 3. Persistencia entre sesiones

El CLI lee las credenciales de `~/.config/higgsfield/credentials.json`
(la ruta puede cambiarse con la variable `HIGGSFIELD_CREDENTIALS_PATH`).
No existe una variable oficial que acepte el contenido directo, así que la
persistencia se hace en dos piezas:

1. **Variable secreta del entorno** — en Environment settings de Claude
   Code web, crear la variable `HIGGSFIELD_CREDENTIALS` (marcada como
   secreto) con el contenido JSON completo de
   `~/.config/higgsfield/credentials.json`. Obtenerlo con:

   ```bash
   cat ~/.config/higgsfield/credentials.json
   ```

   **Nunca** guardar ese JSON en el repositorio: contiene el refresh
   token, que equivale a la contraseña de la cuenta.

2. **Hook de SessionStart** (ya incluido en esta rama) —
   `.claude/settings.json` ejecuta `.claude/hooks/restore-higgsfield-auth.sh`
   al arrancar cada sesión. El script escribe el contenido de
   `$HIGGSFIELD_CREDENTIALS` en `~/.config/higgsfield/credentials.json` y
   restaura la selección de workspace. Si la variable no está definida, no
   hace nada.

Con ambas piezas configuradas, las sesiones nuevas quedan autenticadas sin
repetir el login.

### Caducidad de tokens

- El `access_token` dura ~24 h; el CLI lo renueva solo usando el
  `refresh_token` (scope `offline_access`).
- Si Higgsfield rota el refresh token al renovarlo, la copia estática
  guardada en la variable puede quedar inválida con el tiempo. Síntoma:
  `Session expired` / `Not authenticated`. Solución: repetir el login
  (sección 2) y actualizar el valor de `HIGGSFIELD_CREDENTIALS`.

## 4. Comprobaciones rápidas

```bash
higgsfield account status    # cuenta, plan y créditos
higgsfield workspace list    # workspaces disponibles
higgsfield generate list     # trabajos recientes
```

## 5. Notas del plan free

- Seedance 2.0 requiere plan Pro/Ultimate ("Pro or Ultimate plan required").
- Costes orientativos comprobados: Seedance 2.0 Mini (4 s, 720p) = 10
  créditos; Veo 3.1 Lite = 8 créditos.
- `higgsfield generate cost <modelo> ...` estima el coste sin gastar
  créditos.
- Una vez enviado un job, no hay comando de cancelación en el CLI; los
  créditos se descuentan al enviarlo.
