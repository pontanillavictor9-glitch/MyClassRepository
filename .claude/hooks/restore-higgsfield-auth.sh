#!/usr/bin/env bash
# Restaura la autenticación del CLI de Higgsfield al arrancar la sesión.
# Requiere que el entorno defina la variable secreta HIGGSFIELD_CREDENTIALS
# con el contenido JSON de ~/.config/higgsfield/credentials.json.
# Ver docs/HIGGSFIELD_SETUP.md para el procedimiento completo.
set -u

if [ -z "${HIGGSFIELD_CREDENTIALS:-}" ]; then
  # Sin la variable no hay nada que restaurar; no bloquear la sesión.
  exit 0
fi

CONFIG_DIR="$HOME/.config/higgsfield"
mkdir -p "$CONFIG_DIR"

printf '%s' "$HIGGSFIELD_CREDENTIALS" > "$CONFIG_DIR/credentials.json"
chmod 600 "$CONFIG_DIR/credentials.json"

# Workspace "Private" de pontanillavictor9@gmail.com (el id no es secreto).
if [ ! -f "$CONFIG_DIR/config.json" ]; then
  printf '{"workspace_id":"949630f0-298a-45ad-82a0-7d9690a1353d"}' > "$CONFIG_DIR/config.json"
  chmod 600 "$CONFIG_DIR/config.json"
fi

exit 0
