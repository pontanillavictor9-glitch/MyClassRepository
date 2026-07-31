#!/bin/bash
# Prepara Higgsfield en sesiones de Claude Code en la nube.
# Se ejecuta desde el hook SessionStart de .claude/settings.json.

# Solo aplica en sesiones remotas (en tu máquina local no hace nada).
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

# Instala el CLI de Higgsfield si no está presente.
if ! command -v higgsfield >/dev/null 2>&1; then
  npm i -g @higgsfield/cli >/dev/null 2>&1 || true
fi

# Si el entorno define HIGGSFIELD_CREDENTIALS (JSON del archivo de credenciales),
# lo restaura para que no haga falta iniciar sesión en cada sesión nueva.
if [ -n "$HIGGSFIELD_CREDENTIALS" ]; then
  CRED_FILE="$HOME/.higgsfield-credentials.json"
  printf '%s' "$HIGGSFIELD_CREDENTIALS" > "$CRED_FILE"
  chmod 600 "$CRED_FILE"
  if [ -n "$CLAUDE_ENV_FILE" ]; then
    echo "HIGGSFIELD_CREDENTIALS_PATH=$CRED_FILE" >> "$CLAUDE_ENV_FILE"
  fi
fi

exit 0
